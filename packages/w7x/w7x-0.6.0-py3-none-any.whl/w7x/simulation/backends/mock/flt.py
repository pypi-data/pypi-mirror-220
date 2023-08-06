import typing
import random
import numpy as np
import tfields
import w7x.simulation.flt


class FieldLineTracerMockupBackend(w7x.simulation.flt.FieldLineTracerBackend):
    """
    Backend base class to be subclassed for implementations of the Field Line Tracer Code
    """

    @staticmethod
    def _find_lcfs(state, **kwargs) -> tfields.Points3D:
        """
        Calculate the position of the last closed flux surface.
        """
        # TODO-2: make state dependent
        return tfields.Points3D([[5.7, 0, 0]])

    @staticmethod
    def _magnetic_characteristics(state, **kwargs) -> tfields.Points3D:
        """
        Calculate the position of the last closed flux surface.
        """
        points = kwargs["points"]

        if state.coil_set == w7x.config.CoilSets.Ideal():
            if points.equal(tfields.Points3D([[6.2, 0.0, 0.0]])):

                class MockupMagneticCharacteristics:
                    def __init__(self):
                        self.iota = 0.98
                        self.reff = 0.55
                        self.phi0 = 0.0

                return [MockupMagneticCharacteristics()]
        raise NotImplementedError(state.coil_set)

    @staticmethod
    def _trace_surface(state, **kwargs):
        """
        Trace a surface given a single point on that surface.

        Args:
            start_point: point to trace
            n_points: number of points required on that surface
            **kwargs: used for specific implementation of the backend
        """
        start_point = kwargs.pop("start_point")
        n_points = kwargs.pop("n_points")
        assert len(start_point) == 1
        return tfields.Points3D([start_point[0]] * n_points)

    @staticmethod
    def _trace_poincare(state, **kwargs) -> typing.List[tfields.Points3D]:
        phi_list_rad = kwargs.pop("phi")
        seeds = kwargs.pop("seeds")
        n_points = kwargs.pop("n_points")

        seeds = seeds.copy()
        seeds.transform("cylinder")

        res = []
        for seed in seeds:
            seed_tmp = []
            for phi in phi_list_rad:
                tmp = []
                s = seed.copy()
                for i in range(n_points):
                    s = s.copy()
                    s[2] += 1 / n_points
                    tmp.append(s)
                tmp = tfields.Points3D(tmp, coord_sys="cylinder")
                tmp[:, 1] = phi
                seed_tmp.append(tmp)
            res.append(tfields.Points3D.merged(*seed_tmp))
        return res

    @staticmethod
    def _trace_connection_length(
        state, **kwargs
    ) -> typing.Tuple[tfields.Points3D, typing.List[tfields.Mesh3D]]:
        """
        Run the tracing calculation with diffusion perpendicular to the field
        """
        start_points = kwargs.pop("start_points")
        inverse_field = kwargs.pop("inverse_field")

        terminating_points = start_points.copy() + random.random()
        if inverse_field:
            terminating_points *= -1
        component_ids = [
            random.randint(0, len(state.assembly.get_components(flat=True)))
            for iter in range(len(start_points))
        ]

        component_id_set = set(component_ids)

        pwi = w7x.model.Pwi(origin_points=start_points)

        for i, component_id in enumerate(component_id_set):
            component_index = component_id
            origin_point_indices = [
                i for i, c_id in enumerate(component_ids) if c_id == component_id
            ]
            hit_points = terminating_points[origin_point_indices]

            if component_index is not None:
                connection_lengths = tfields.Tensors(
                    [400 for _ in hit_points], dtype=int
                )
                hit_points_faces = tfields.Tensors(
                    [random.randint(0, 100) for _ in hit_points], dtype=int
                )
                n_hits = {f: hit_points_faces.count(f) for f in set(hit_points_faces)}
                areas = {f: 0.01 * f for f in n_hits.keys()}
            else:
                connection_lengths = tfields.Tensors([np.inf] * len(hit_points))
                hit_points_faces = None
                n_hits = None
                areas = None

            pci = w7x.model.PlasmaComponentInteraction(
                component_index=component_index,
                inverse_field=inverse_field,
                origin_point_indices=origin_point_indices,
                hit_points=hit_points,
                hit_points_faces=hit_points_faces,
                connection_lengths=connection_lengths,
                n_hits=n_hits,
                areas=areas,
            )
            pwi.add(pci)
        return pwi

    @staticmethod
    def _trace_diffusion(
        state, **kwargs
    ) -> typing.Tuple[tfields.Points3D, typing.List[tfields.Mesh3D]]:
        """
        Run the tracing calculation with diffusion perpendicular to the field
        """
        start_points = kwargs.pop("start_points")
        inverse_field = kwargs.pop("inverse_field")

        terminating_points = start_points.copy() + random.random()
        if inverse_field:
            terminating_points *= -1
        component_ids = [
            random.randint(0, len(state.assembly.get_components(flat=True)))
            for iter in range(len(start_points))
        ]

        component_id_set = set(component_ids)

        pwi = w7x.model.Pwi(origin_points=start_points)

        for i, component_id in enumerate(component_id_set):
            component_index = component_id
            origin_point_indices = [
                i for i, c_id in enumerate(component_ids) if c_id == component_id
            ]
            hit_points = terminating_points[origin_point_indices]

            if component_index is not None:
                connection_lengths = tfields.Tensors(
                    [100 * random.random() for _ in hit_points], dtype=int
                )
                hit_points_faces = tfields.Tensors(
                    [random.randint(0, 100) for _ in hit_points], dtype=int
                )
                n_hits = {
                    f: list(hit_points_faces).count(f) for f in set(hit_points_faces)
                }
                areas = {f: 0.01 * f for f in n_hits.keys()}
            else:
                connection_lengths = tfields.Tensors([np.inf] * len(hit_points))
                hit_points_faces = None
                n_hits = None
                areas = None

            pci = w7x.model.PlasmaComponentInteraction(
                component_index=component_index,
                inverse_field=inverse_field,
                origin_point_indices=origin_point_indices,
                hit_points=hit_points,
                hit_points_faces=hit_points_faces,
                connection_lengths=connection_lengths,
                n_hits=n_hits,
                areas=areas,
            )
            pwi.add(pci)
        return pwi
