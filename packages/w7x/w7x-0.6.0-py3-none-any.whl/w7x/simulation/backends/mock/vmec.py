import os
import logging
import shutil

import numpy as np
import netCDF4
import omegaconf

import rna.config
from w7x.simulation.vmec import VmecInput, VmecBackend, Wout, Status
import w7x.config


omegaconf.OmegaConf.set_struct(w7x.config, False)
w7x.config.vmec.mock = omegaconf.OmegaConf.create()

LOGGER = logging.getLogger(__name__)


class VmecMockupBackend(VmecBackend):
    """
    Mockup backend for VMEC.

    Examples:
        >>> import w7x
        >>> import tempfile
        >>> dtemp = tempfile.mkdtemp()
        >>> w7x.config.vmec.local.folder = dtemp
        >>> state = w7x.State(
        ...     w7x.config.CoilSets.Ideal(),
        ...     w7x.config.Plasma.Vacuum(),
        ...     w7x.config.Equilibria.InitialGuess())
        >>> vmec = w7x.simulation.vmec.Vmec(strategy="mock")
        >>> state = vmec.free_boundary(state)

        >>> state.equilibrium.beta is not None
        True

        >>> import shutil
        >>> shutil.rmtree(dtemp)
    """

    @property
    def folder(self):
        return rna.config.fallback(w7x.config.vmec, "mock", "folder")

    def _compute(self, state, **kwargs) -> Wout:
        """
        Compute the equilibrium field with VMEC.
        """

        dry_run = kwargs.pop("dry_run")

        vmec_input = VmecInput.from_state(state, **kwargs)
        vmec_id = vmec_input.vmec_id

        LOGGER.info(f"Executing {vmec_input.vmec_id} run on {self.__class__.__name__}.")

        job_dir_path = os.path.join(self.folder, vmec_id)
        if not os.path.isdir(job_dir_path):
            os.makedirs(job_dir_path)

        if dry_run:
            return Wout(file_id=vmec_id, status=Status.NOT_STARTED)

        #  Mimic VMEC execution
        if vmec_input.num_iter <= 4000:
            return Wout(file_id=vmec_id, status=Status.INCREASE_NITER)
        elif abs(vmec_input.phi_edge) >= 3.0:
            return Wout(file_id=vmec_id, status=Status.BOUNDARY)
        elif vmec_input.force_tolerance_levels[-1] <= 1e-16:
            return Wout(file_id=vmec_id, status=Status.TIMEOUT)

        #  Work on copy of mock wout file
        #  TODO-1(@amerlo): is there a better solution?
        src_wout_file_path = os.path.join(
            w7x.config.package.resources,
            "vmec",
            "wout_w7x.0972_0926_0880_0852_+0000_+0000.01.00jh.nc",
        )
        wout_file_path = os.path.join(job_dir_path, f"wout_{vmec_id}.nc")
        shutil.copyfile(src_wout_file_path, wout_file_path)

        #  Use simple scaling from EJM+252 configuration plus noise
        #  Noise level has been set to 0.8 not to make beta search task
        #  too difficult in tests.
        data = netCDF4.Dataset(wout_file_path, "r+")
        beta = (
            0.03
            * vmec_input.pressure_profile(0.0)
            / 2e5
            * (13067 / vmec_input.coil_currents[0]) ** 2
        )
        beta *= 1 + np.random.uniform(low=-1.0, high=1.0) / 8e1
        data["betatotal"][:] = beta
        #  Hack to fix magnetic field on axis
        #  TODO-2(@amerlo): is there a better way to do it?
        b_axis = 2.52 * vmec_input.coil_currents[0] / 13067
        b_lcfs = 2.23 * vmec_input.coil_currents[0] / 13067
        bmnc = np.interp(
            np.linspace(0, 1, num=data["bmnc"].shape[0]),
            [0.0, 1.0],
            [b_axis, b_lcfs],
        )
        data["bmnc"][:, :] = 0.0
        data["bmnc"][:, 0] = bmnc

        return Wout(
            file_id=vmec_id, status=Status.SUCCESS, data=data, path=wout_file_path
        )
