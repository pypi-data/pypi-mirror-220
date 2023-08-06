# flake8: noqa:E402
"""
Neural network approximation for VMEC.
This model is only valid in the domain of W7-X.
"""
import pytest

torch = pytest.importorskip("torch")
import json
import logging
from copy import deepcopy

import numpy as np
from netCDF4 import Dataset

from vmecnn.models import MHDNet
from vmecnn.physics.equilibrium import Equilibrium, _to_vmec

import w7x
from w7x.simulation.vmec import VmecInput, VmecBackend, Wout, Status

LOGGER = logging.getLogger(__name__)


def _normalize(data: dict, metadata: dict) -> dict:
    """Normalize model input data with normalization parameters."""
    return {
        k: (v - metadata["mean"][k][0]) / metadata["std"][k][0]
        if k in metadata["mean"]
        else v
        for k, v in data.items()
    }


#  TODO-1(@amerlo): move this to vmecnn project
def _equi_to_wout(equi: Equilibrium, vmec_id: str, mgrid_file: str) -> Wout:
    """Create VMEC wout file from Equilibrium object."""

    wout = Dataset(
        f"wout_{vmec_id}.nc",
        mode="w",
        diskless=True,
        format="NETCDF4_CLASSIC",
    )

    out_dtype = np.float64 if equi.rmnc.dtype == torch.float64 else np.float32
    mn_num = equi.xm.shape[0]

    #  TODO-1(@amerlo): add all relevant outputs

    dimensions = [("dim_00200", 200), ("mn_mode", mn_num), ("radius", equi.ns)]
    for dim in dimensions:
        wout.createDimension(*dim)

    variables = [
        ("nfp", np.int32, (), equi.num_field_period),
        ("ns", np.int32, (), equi.ns),
        ("xm", np.float64, ("mn_mode",), equi.xm),
        ("xn", np.float64, ("mn_mode",), equi.xn),
        ("phi", out_dtype, ("radius",), equi.normalized_flux * equi.phiedge),
        ("rmnc", out_dtype, ("radius", "mn_mode"), _to_vmec(equi.rmnc)),
        ("lmns", out_dtype, ("radius", "mn_mode"), _to_vmec(equi.lmns)),
        ("zmns", out_dtype, ("radius", "mn_mode"), _to_vmec(equi.zmns)),
        ("iotaf", out_dtype, ("radius",), equi.iota),
        ("presf", out_dtype, ("radius",), equi.pressure),
        ("vp", out_dtype, ("radius",), equi.vp),
        ("volume_p", out_dtype, (), equi.volume),
        ("betatotal", out_dtype, (), equi.beta),
        ("Rmajor_p", out_dtype, (), equi.rmajor),
        ("Aminor_p", out_dtype, (), equi.aminor),
        # TODO
        # ("bmnc", out_dtype, ("radius", "mn_mode"), _to_vmec(equi.bmnc)),
    ]

    for name, dtype, size, value in variables:
        var = wout.createVariable(name, dtype, size)
        var[:] = value

    #  Create special variables
    mgrid = wout.createVariable("mgrid_file", np.dtype("S1"), ("dim_00200",))
    mgrid_file += "".join([" "] * (200 - len(mgrid_file)))
    for i, v in enumerate(mgrid_file):
        mgrid[i] = v

    #  TODO: which other status are allowed here?
    status = Status.SUCCESS
    return Wout(file_id=vmec_id, data=wout, status=status)


def _to_model_input(vmec_input: VmecInput, ns_profiles: int, dtype) -> dict:
    ns = vmec_input.num_grid_points_radial[-1]

    coil_current_ratios = (
        torch.tensor(vmec_input.coil_currents, dtype=dtype)
        / vmec_input.coil_currents[0]
    )

    #  TODO-1(@amerlo): add assert for input parameters that are not supported (e.g. fixed boundary)
    #  TODO-0(@amerlo): add assert for input parameters outside training boundaries (data domain check)
    assert (
        coil_current_ratios[7:] == 0
    ).all(), "VMECNN only supports I1...5 and IA...B coils"

    phiedge = vmec_input.phi_edge
    p0 = vmec_input.pressure_profile(0.0) * vmec_input.pressure_scale
    curtor = vmec_input.total_toroidal_current

    #  Normalized flux for profiles generation
    s = torch.linspace(0, 1, ns_profiles, dtype=dtype)

    pressure = torch.from_numpy(vmec_input.pressure_profile(s))
    p0_profile = vmec_input.pressure_profile(0.0)
    if p0_profile != 0.0:
        pressure /= p0_profile

    toroidal_current = torch.from_numpy(vmec_input.toroidal_current_profile(s))
    curtor_profile = vmec_input.toroidal_current_profile(1.0)
    if curtor_profile != 0.0:
        toroidal_current /= curtor_profile

    return {
        "npc": coil_current_ratios[1:5].expand(ns, 4),
        "pc": coil_current_ratios[5:7].expand(ns, 2),
        "phiedge": phiedge * torch.ones(ns, 1, dtype=dtype),
        "p0": p0 * torch.ones(ns, 1, dtype=dtype),
        "curtor": curtor * torch.zeros(ns, 1, dtype=dtype),
        "pressure": pressure.view(1, -1).expand(ns, ns_profiles),
        "toroidal_current": toroidal_current.view(1, -1).expand(ns, ns_profiles),
        "normalized_flux": torch.linspace(0, 1, ns, dtype=dtype).view(ns, 1),
    }


class VmecNNBackend(VmecBackend):
    """
    A concrete VMEC implementation approximated by a NN model.

    Examples:
        >>> import w7x
        >>> from w7x.simulation.vmec import Vmec
        >>> state = w7x.State(
        ...     w7x.config.CoilSets.Ideal(), w7x.config.Plasma.Vacuum(),
        ...     w7x.config.Equilibria.InitialGuess())
        >>> vmec = Vmec()
        >>> vmec.backend = "nn"

        >>> wout = vmec.backend._compute(state, free_boundary=True, dry_run=False)
        >>> wout.data["betatotal"][:].data < 1e-10
        True

    """

    def __init__(self):
        checkpoint = w7x.config.vmec.nn.checkpoint
        metadata_path = w7x.config.vmec.nn.metadata

        LOGGER.info("Loading model metadata from %s" % metadata_path)
        with open(metadata_path, "r") as f:
            data = f.read()
        self.metadata = json.loads(data)

        LOGGER.info("Loading model checkpoint from %s" % checkpoint)
        # TODO-2(@amerlo): eventualy add options to pass arguments here
        # The options here are the same that could be added to the Model.__init__
        self.model = MHDNet.load_from_checkpoint(
            checkpoint,
            enable_grad_on_predict=False,
            to_double=True,
        )
        self.model.setup()
        self.model.eval()

    def _compute(self, state, **kwargs):
        """
        Compute an equilibrium with VMECNN.
        """

        vmec_input = VmecInput.from_state(state, **kwargs)

        if not vmec_input.free_boundary:
            raise RuntimeError("VMECNN does only support free boundary equilibria")

        config = _to_model_input(
            vmec_input=vmec_input,
            ns_profiles=self.metadata["ns"],
            dtype=self.model.dtype,
        )

        #  Scaling factors for an equivalent free-boundary problem with coilCurrents[0] == I1
        #  phiedge' = phiedge * scale_factor
        #  Itor' = Itor' * scale_factor
        #  pressure' = pressure * scale_factor**2
        scaled_config = deepcopy(config)
        scale_factor = w7x.config.vmec.nn.training_I1 / vmec_input.coil_currents[0]
        scaled_config["phiedge"] *= scale_factor
        scaled_config["p0"] *= scale_factor**2
        scaled_config["curtor"] *= scale_factor

        normalized_config = _normalize(scaled_config, self.metadata)

        dry_run = kwargs.pop("dry_run")
        if dry_run:
            return Wout(file_id=vmec_input.vmec_id, status=Status.NOT_STARTED)

        LOGGER.info("Run inference model ...")
        with torch.no_grad():
            equi = Equilibrium.from_model(
                {**config, **self.model.forward(normalized_config)}
            )

        return _equi_to_wout(
            equi,
            vmec_id=vmec_input.vmec_id,
            mgrid_file=w7x.config.vmec.nn.training_mgrid_file,
        )
