"""
Additional w7x specific methods for tfields objects
"""
import logging
import numpy as np
import tfields
import tfields.lib.io


LOGGER = logging.getLogger(__name__)


def to_segment_one(tensors, mirror_z=True):
    """
    Map the points to the first module of w7x and mirror to positive z
    if mirror_zOption is True. The mirror option is interesting for the
    divertor for example.
    Examples:
        >>> import tfields
        >>> import w7x
        >>> import numpy as np
        >>> pStart = tfields.Points3D([[6, np.pi, 1],
        ...                            [6, np.pi / 5 * 3, -1]],
        ...                           coord_sys='cylinder')
        >>> w7x.lib.tfields.to_segment_one(pStart)
        >>> pStart
        Points3D([[ 6.        , -0.62831853,  1.        ],
                  [ 6.        ,  0.62831853,  1.        ]])

    """
    with tensors.tmp_transform(tfields.bases.CYLINDER):
        offset_segment_0 = -2 * np.pi / 10
        tensors.to_segment(0, 5, 1, offset=offset_segment_0)
        if mirror_z:
            condition = tensors[:, 2] < 0
            tensors.mirror([1, 2], condition=condition)


def where_phi_between(tensors, phi_min, phi_max):
    """
    Args:
        phi_min (float): minimum phi in radian
        phi_max (float): maximum phi in radian

    Returns:
        output of np.where with condition
    """
    with tensors.tmp_transform(tfields.bases.CYLINDER):
        phi = tensors[:, 1]
    if phi_min < phi_max:
        return np.where((phi_min <= phi) & (phi <= phi_max))
    if phi_min > phi_max:
        return np.where(np.logical_not((phi_max < phi) & (phi < phi_min)))
    return np.where(phi == phi_min)


def phi_between(tensors, phi_min, phi_max):
    """
    Args:
        phi_min (float): minimum phi in radian
        phi_max (float): maximum phi in radian
    Returns:
        bool: if phi of all points is in between the given values
    """
    return len(tensors.where_phi_between(phi_min, phi_max)[0]) == len(tensors)


def _load_dat(cls, path, **kwargs):
    """
    Load Tensors file from .dat format
    """
    kwargs.setdefault("coord_sys", tfields.bases.PHYSICAL_CYLINDER)
    # pylint:disable=protected-access
    obj = cls._load_txt(path, **kwargs)
    # The dat format saves in Bphi, Br, Bz format!
    obj[:, [0, 1]] = obj[:, [1, 0]]
    return obj


def _save_dat(self, path, **kwargs):
    """
    kwargs passed to np.savetxt
    """
    kwargs.setdefault("fmt", "%.8f")
    with self.tmp_transform(tfields.bases.PHYSICAL_CYLINDER):
        # The dat format saves in Bphi, Br, Bz format!
        array = self[:, [1, 0, 2]]
    # pylint:disable=protected-access
    array._save_txt(path, **kwargs)


def _load_datc(cls, path, **kwargs):
    """
    Load Tensors file from .datc format ("dat complete")
    Examples:
        >>> import tfields
        >>> from tempfile import NamedTemporaryFile
        >>> out_file = NamedTemporaryFile(suffix=".datc")
        >>> tg = tfields.TensorGrid.empty((0, 0, 1), (0, 0, 1), (0, 2, 3))
        >>> tg.fields.append(
        ...     tfields.Tensors([[0, 1, 2], [3, 4, 5], [6, 7, 8]],
        ...                     coord_sys=tfields.bases.PHYSICAL_CYLINDER)
        ... )
        >>> tg.save(out_file.name)
        >>> _ = out_file.seek(0)  # this is only necessary in the test
        >>> tg_load = tfields.TensorGrid.load(out_file.name)
        >>> tg.equal(tg_load)
        True
    """
    # pylint:disable=protected-access
    field = tfields.Tensors._load_dat(path, set_header=True, **kwargs)
    name, header = field.name
    field.name = name
    for line in header:
        key, rest = line.split(": ")
        # pylint:disable=unused-variable
        tpe, val = rest.split(" = ")

        if key in ("base_vectors", "iter_order", "num"):
            kwargs[key] = tfields.lib.io.str_to_numpy(val)
        if key == "base_vectors_coord_sys":
            kwargs["coord_sys"] = str(val)

    obj = cls(np.empty(shape=(len(field), 0)), **kwargs)
    obj.fields.append(field)
    return obj


def _save_datc(self, path, **kwargs):
    """
    kwargs passed to np.savetxt
    """
    field_index = kwargs.pop("field_index", 0)
    field = self.fields[field_index]

    # save the mgrid properties with the Tensor
    # pylint:disable=protected-access
    field._save_dat(
        path,
        header={
            "base_vectors": tfields.lib.io.numpy_to_str(self.base_vectors),
            "base_vectors_coord_sys": self.base_vectors.coord_sys,
            "num": tfields.lib.io.numpy_to_str(self.num),
            "iter_order": tfields.lib.io.numpy_to_str(self.iter_order),
        },
        **kwargs
    )


def _load_kisslinger(cls, path, rescale_poloidal_resolution=1, **kwargs):
    """
    Load Tensors file from .kisslinger format ("grids along poloidal positions")

    The format has the following structure:
        name
                n_phi           n_rz           n_fold_periodicity  reference_r   reference_z
        phi_deg_0
          r_cm_00    z_cm_00
          r_cm_01    z_cm_01
          ...        ...
        phi_deg_1
          r_cm_10    z_cm_10
          r_cm_11    z_cm_11
          ...        ...
        ...
    """
    name = np.loadtxt(path, skiprows=0, max_rows=1, dtype=str)
    header = np.loadtxt(path, skiprows=1, max_rows=1)
    n_phi = int(header[0])
    n_rz = int(header[1])
    n_fold = int(header[2])
    reference_r = int(header[3])
    reference_z = int(header[4])
    LOGGER.debug("File: %s", path.split("/")[-1])
    LOGGER.debug(
        "Kisslinger mesh with %d Phi values with %d R,Z values per phi.", n_phi, n_rz
    )
    LOGGER.debug("%d-fold periodicity", n_fold)
    LOGGER.debug("Reference point: %f [cm] %f [cm] (R,Z)", reference_r, reference_z)

    R = np.zeros((n_phi, n_rz))
    Z = np.zeros(np.shape(R))
    P = np.ones(np.shape(R))
    for i in range(n_phi):
        P[i, :] = np.multiply(
            P[i, :], np.loadtxt(path, skiprows=2 + (n_rz + 1) * i, max_rows=1)
        )
        tmp = np.loadtxt(
            path, skiprows=3 + (n_rz + 1) * i, max_rows=n_rz, usecols=(0, 1)
        )
        R[i, :] = tmp[:, 0]
        Z[i, :] = tmp[:, 1]

    if rescale_poloidal_resolution != 1:
        # Refine poloidal resolution by fac
        Rnew, Znew, Pnew = [], [], []
        for i in range(n_rz - 1):
            R0, Z0, R1, Z1 = R[:, i], Z[:, i], R[:, i + 1], Z[:, i + 1]
            P0 = P[:, i]
            dR = (R1 - R0) / rescale_poloidal_resolution
            dZ = (Z1 - Z0) / rescale_poloidal_resolution
            for j in range(rescale_poloidal_resolution):
                Rnew.append(R0 + dR * j)
                Znew.append(Z0 + dZ * j)
                Pnew.append(P0)
            # Add last point of last intervall (not in refinement)
            Rnew.append(R1)
            Znew.append(Z1)
            Pnew.append(P0)

        R, Z, P = np.array(Rnew).T, np.array(Znew).T, np.array(Pnew).T
        n_rz = R.shape[1]

    # build the grid as requested
    obj = cls.plane(
        (0, 0, 1),  # build a dummy plane in phi-z first. later rearrange
        P[:, 0] * np.pi / 180,  # convert to radians
        (1, 2, complex(n_rz)),
        coord_sys=tfields.bases.CYLINDER,
    )
    # rearrange dummy plane vertices and convert cm to m
    for p in range(n_phi):
        obj[p * n_rz : (p + 1) * n_rz, 0] = R[p] / 100
        obj[p * n_rz : (p + 1) * n_rz, 2] = Z[p] / 100
    obj.name = name

    return obj


# pylint:disable=protected-access
tfields.Tensors._load_dat = classmethod(_load_dat)
# pylint:disable=protected-access
tfields.Tensors._save_dat = _save_dat


# pylint:disable=protected-access
tfields.TensorGrid._load_datc = classmethod(_load_datc)
# pylint:disable=protected-access
tfields.TensorGrid._save_datc = _save_datc


# pylint:disable=protected-access
tfields.Mesh3D._load_kisslinger = classmethod(_load_kisslinger)
