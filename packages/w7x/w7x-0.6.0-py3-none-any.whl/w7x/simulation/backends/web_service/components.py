"""
Web service backend of the components code
"""
import typing
import logging
import re
import os
import numpy as np

import osa
import rna
import tfields
import w7x
from w7x.simulation.components import ComponentsBackend
from w7x.simulation.backends.web_service.base import (
    get_server,
    OsaType,
    to_osa_type,
    to_tfields_type,
)


LOGGER = logging.getLogger(__name__)
WS_SERVER = w7x.config.components.web_service.server
WS_DB = w7x.config.components.web_service.database
WS_DB_DUPLICATE = w7x.config.components.web_service.database_duplicate


class Base(OsaType):
    """
    Base class for components db web service types
    """

    ws_server = WS_DB


class Polygon(Base):
    """
    element.vertices gives you the three points numbers to a triangle.
    This is normally refered to as face
    """

    prop_defaults = {"vertices": None}


class MeshedModel(Base):
    """
    Args:
        multiple ways:
            vertices (list)
            faces (list)

            - or -

            group from ObjFile

            - or -

            tfields.Mesh3D object
    Attributes:
        nodes (Points3D): = vertices (coordinates) of the points.
        elements (list[Polygon]): = faces (always three indices of points for a
            triangle). Starting at 1 here
    Examples:
        use with Mesh3D as inp
        >>> import tfields
        >>> from w7x.simulation.backends.web_service.components import MeshedModel
        >>> m = tfields.Mesh3D([[1,2,3], [3,3,3], [0,0,0], [5,6,7]],
        ...                    faces=[[0, 1, 2], [1, 2, 3]])
        >>> mm = MeshedModel(m)

        Get the osa type, in this case for field line server
        >>> fls = mm.as_input()

        return Mesh3D works
        >>> bool((m == mm.as_mesh3d()).all())
        True

        create with meshed Model from fls works
        >>> m2 = MeshedModel(fls).as_mesh3d()
        >>> assert tfields.Points3D(m2).equal(
        ...     [[ 1.,  2.,  3.],
        ...      [ 3.,  3.,  3.],
        ...      [ 0.,  0.,  0.],
        ...      [ 5.,  6.,  7.]])
        >>> assert tfields.Tensors(m2.faces).equal([[0, 1, 2], [1, 2, 3]])

    """

    prop_defaults = {
        "nodes": None,
        "elements": None,
        "nodesIds": None,
        "elementsIds": None,
    }

    def __init__(self, *args, **kwargs):
        args = list(args)
        if len(args) > 1:
            logging.error(" Implementation did not work.")
            raise NotImplementedError(
                " Implementation with args %s not yet implemented!" % args
            )
        if len(args) == 1 and issubclass(args[0].__class__, tfields.Mesh3D):
            mesh = args.pop(0)
            nodes = to_osa_type(mesh, ws_server=WS_DB)
            faces = mesh.faces + 1
            kwargs["nodes"] = kwargs.pop("nodes", nodes)
            kwargs["elements"] = kwargs.pop(
                "elements", [Polygon(vertices=face) for face in faces]
            )
        super().__init__(*args, **kwargs)

    @classmethod
    def from_mm_id(cls, mm_id):
        """
        Factory method to create from meshed model id
        """
        comp_db_server = get_server(WS_DB)
        # caching mechanism
        with rna.log.timeit(
            "[w7x cache] - Calling getComponentData(" "{mm_id})".format(**locals())
        ):
            component_data = comp_db_server.service.getComponentData(mm_id)
            obj = cls(component_data[0])
        return obj

    @classmethod
    def from_component(cls, component):
        """
        Factory method to create from component
        """
        return cls.from_mm_id(component.id)

    @classmethod
    def mesh3d(cls, mm_id):
        """
        Equivalent to MeshedModel(mm_id).as_mesh3d() but much faster cache
        as compared to cached MeshedModel. tfields loading is fast.

        Returns:
            tfields.Mesh3D
        """
        # caching mechanism
        mm_id_cache_path = os.path.join(
            w7x.config.general.cache,
            "components/mesh_mm_id_" + str(mm_id) + ".npz",
        )
        if os.path.exists(str(mm_id_cache_path)):
            with rna.log.timeit(
                "[w7x cache] - Loading Mesh3D for mm_id" " {mm_id}".format(**locals())
            ):
                obj = tfields.Mesh3D.load(mm_id_cache_path)
        else:
            with rna.log.timeit(
                "[w7x cache] - Calling MeshedModel({mm_id})"
                ".as_mesh3d()".format(**locals())
            ):
                instance = cls.from_mm_id(mm_id)
                obj = instance.as_mesh3d()
                obj.save(mm_id_cache_path)
        return obj

    def as_mesh3d(self):
        """
        Returns:
            tfields.Mesh3D
        """
        # pylint:disable=no-member
        faces = np.array([pol.vertices for pol in self.elements])
        faces -= 1
        # pylint:disable=no-member
        return tfields.Mesh3D(to_tfields_type(self.nodes), faces=faces)


def get_user(server: osa.Client):
    """
    Get the server.types.User with the local user and password set.
    """
    user_alias = w7x.config.components.web_service.user.alias
    user_password = w7x.config.components.web_service.user.password
    assert user_alias, (
        "Provide the option 'alias' under the '[components.web_service.user']"
        " group in your '~/.w7x/config.cfg' file. For an example look in this"
        " project's 'examples/.w7x/config.cfg'."
    )
    assert user_password, (
        "Provide the option 'password' under the '[components.web_service.user']"
        " group in your '~/.w7x/config.cfg' file. For an example look in this"
        " project's 'examples/.w7x/config.cfg'. Make it private"
        " ('$ chmod 700 ~/.w7x/config.cfg') to not expose your password!!!"
    )
    user = server.types.User()
    user.name = user_alias
    user.password = user_password
    return user


DE_NAME_FLAG = "de-mesh-id: "


class ComponentsWebServiceBackend(ComponentsBackend):
    """
    Backend implementation

    This backend is special in that it is the main intefrace to the database.
    All other backends are only accessing a copy of the database.
    """

    @staticmethod
    @w7x.node
    def _get_mesh(mm_id):
        return MeshedModel.mesh3d(mm_id)

    @staticmethod
    @w7x.node
    def _filter_infos(*ids, **filters):
        """
        Args:
            mm_id (int): meshed model id if not given, filters are used
            **filters: filters to search the database
        """
        component_infos = []
        comp_db_server = get_server(w7x.config.components.web_service.database)
        if ids:
            # TODO(dboe-1): forward when run_service is good again
            regex = re.compile(
                (
                    r"SOAP Fault ([-a-zA-Z0-9()@:%_\+.~#?&\/\/=]*): getComponentInfo "
                    r"<senv:Server> Entry ([-+]?\d+) does not exist in category components "
                )
            )
            try:
                component_infos_from_ids = comp_db_server.service.getComponentInfo(
                    list(ids)
                )
            except RuntimeError as err:
                if regex.match(str(err)):
                    component_infos_from_ids = []
                else:
                    raise err
            component_infos.extend(component_infos_from_ids)
        if filters:
            info_mask = comp_db_server.types.ComponentInfoMask()
            info_mask.__dict__.update(filters)
            component_infos_from_filter = comp_db_server.service.findComponentInfo(
                info_mask
            )
            component_infos.extend(component_infos_from_filter)
        return component_infos

    @w7x.node
    def _filter(self, *ids: int, **filters) -> typing.List[int]:
        """
        Returns:
            Meshed model ids

        Args:
            **filters: filters to search the database
        """
        valid_ids = [id_ for id_ in ids if self._filter_infos(id_)]

        if filters:
            comp_db_server = get_server(w7x.config.components.web_service.database)
            info_mask = comp_db_server.types.ComponentInfoMask()
            info_mask.__dict__.update(filters)
            valid_ids_from_filter = comp_db_server.service.findComponentId(info_mask)
            if valid_ids_from_filter:
                valid_ids.extend(
                    [
                        id_
                        for id_ in valid_ids_from_filter
                        if valid_ids_from_filter not in valid_ids
                    ]
                )
        return valid_ids

    @w7x.node
    def _get_id(self, **filters) -> int:
        """
        Returns:
            meshed model id, None if no id found

        Raises:
            ValueError: if more than one meshed model is found

        Args:
            **filters: filters to search the database
        """
        ids = self._filter(**filters)
        n_comp = len(ids)
        assert (
            n_comp <= 1
        ), f"More than one {n_comp} component found with filters {filters}"
        if not ids:
            return None

        return ids[0]

    @w7x.node
    def exists(self, id_: typing.Optional[int] = None, **filters) -> bool:
        """
        Args:
            id_: meshed model id
            **filters: filters to search the database
        """

        if id_ is not None and filters:
            raise ValueError("You can't use both id_ and filters")
        if id_ is None and not filters:
            raise ValueError("You must use either id_ or filters")

        if id_ is not None:
            ids = self._filter(id_)
        else:
            ids = self._filter(**filters)
        return bool(ids)

    @staticmethod
    @w7x.node
    # pylint:disable=too-many-locals
    def _mesh_slice(component, phi) -> tfields.TensorMaps:
        mesh_server = get_server(WS_SERVER)

        mesh_set = mesh_server.types.SurfaceMeshSet()
        wrap = mesh_server.types.SurfaceMeshWrap()
        reference = mesh_server.types.DataReference()
        reference.dataId = "10"
        wrap.reference = reference
        mesh_set.meshes = [
            wrap,
        ]

        # append mm_id_wrap
        mm_id_wrap = mesh_server.types.SurfaceMeshWrap()
        mm_id_reference = mesh_server.types.DataReference()
        mm_id_reference.dataId = str(component.id)
        mm_id_wrap.reference = mm_id_reference
        mesh_set.meshes.append(mm_id_wrap)

        # ask web service for result and process it to right format
        # careful: Returns None if there is no component.
        res = mesh_server.service.intersectMeshPhiPlane(phi, mesh_set)

        # pylint:disable=too-many-nested-blocks
        if isinstance(res, list):
            vertex_index_offset = 0
            vertex_list = []
            nodes = []
            edges = []
            if res[0] is None:
                return tfields.TensorMaps([])
            if str(type(res[0])) == "<class 'osa.xmltypes.PolygonPlaneIntersection'>":
                # Result is from MeshPhiIntersection
                for intersection in res:
                    # res.surfs has entries for every phi
                    vertex_points = to_tfields_type(intersection.vertices)
                    vertex_points.transform(tfields.bases.CYLINDER)
                    # phi is correct with rounding precision before.
                    # This way it is perfectly correct
                    vertex_points[:, 1].fill(phi)
                    while True:
                        # This while is only active if duplicates are found to be mappable to len
                        # 1 or 2
                        if len(vertex_points) == 1:
                            nodes.append(
                                np.arange(len(vertex_points)) + vertex_index_offset
                            )
                        elif len(vertex_points) == 2:
                            edges.append(
                                np.arange(len(vertex_points)) + vertex_index_offset
                            )
                        else:
                            duplicates = tfields.lib.util.duplicates(
                                vertex_points, axis=0
                            )
                            if len(set(duplicates)) <= 2:
                                vertex_points = vertex_points[list(set(duplicates))]
                                continue
                            raise ValueError("More than two edges given")
                        break

                    vertex_list.append(vertex_points)
                    vertex_index_offset += len(vertex_points)

                slices = tfields.TensorMaps(tfields.Tensors.merged(*vertex_list))
                slices.maps[1] = tfields.Tensors(nodes, dim=1)
                slices.maps[2] = tfields.Tensors(edges, dim=2)
                return slices
            LOGGER.error("Can not handle result list content.")
        elif res is None:
            LOGGER.debug(
                "Result was None. Probably there was no"
                "intersection of the mesh with this plane."
            )
        else:
            LOGGER.error("Result is not of the right type")
        return None

    @staticmethod
    @w7x.node
    def upload_component(
        component: w7x.model.Component, **kwargs
    ) -> w7x.model.Component:
        assert isinstance(component.mesh, tfields.Mesh3D)
        assert component.machine
        assert component.variant
        assert component.location
        assert component.info

        quality = kwargs.pop("quality", 80)
        method = kwargs.pop("method", "ad-hoc")
        accuracy = kwargs.pop("accuracy", 0.0)

        cmpdb = get_server(WS_DB)
        cmpdb2 = get_server(WS_DB_DUPLICATE)

        usr1 = get_user(cmpdb)
        usr2 = get_user(cmpdb2)

        cmpinfo = {
            "name": component.name,
            "machine": component.machine,
            "state": component.variant,
            "quality": quality,
            "location": component.location,
            "author": usr1.name,
            "method": method,
            "id": "",
            "accuracy": accuracy,
            "comment": component.info,
        }

        mmod = MeshedModel(component.mesh).as_input()

        data = cmpdb2.types.MeshUnion()
        smesh = cmpdb2.types.SurfaceMesh()
        smesh.polygonIds = np.arange(1, len(mmod.elements) + 1)
        smesh.numVertices = []
        smesh.polygons = []

        for j in range(len(mmod.elements)):
            smesh.numVertices.append(3)
            smesh.polygons.extend(mmod.elements[j].vertices)

        data.surfaceMesh = smesh

        info1 = cmpdb.types.ComponentStorageInfo()
        info2 = cmpdb2.types.ComponentInfo()
        info1.__dict__.update(cmpinfo)
        info2.__dict__.update(cmpinfo)

        smesh.nodes = cmpdb2.types.Points3D()
        smesh.nodes.x1 = mmod.nodes.x1
        smesh.nodes.x2 = mmod.nodes.x2
        smesh.nodes.x3 = mmod.nodes.x3
        smesh.nodeIds = np.arange(1, len(mmod.nodes.x1) + 1).tolist()

        id1 = cmpdb.service.addComponent(info1, mmod, usr1)
        LOGGER.info(f"Created new component with id {id1} in components database")
        id2 = cmpdb2.service.addComponent(info2, data, usr2)
        LOGGER.info(
            f"Created new component with id {id2} in duplicate components database"
        )

        component.id = id1
        return component

    @staticmethod
    @w7x.node
    def delete_component(
        component: typing.Union[w7x.model.Component, int], **kwargs
    ) -> None:
        """
        Delete a component from the database.

        Args:
            component: The component to delete (or the corresponding componentsDB id).
        """
        if isinstance(component, w7x.model.Component):
            id_ = component.id
        else:
            assert isinstance(component, int)
            id_ = component
        cmpdb = get_server(WS_DB)
        cmpdb2 = get_server(WS_DB_DUPLICATE)

        usr1 = get_user(cmpdb)
        usr2 = get_user(cmpdb2)

        cmpdb.service.delComponent(id_, usr1)
        cmpdb2.service.delComponent(id_, usr2)
