"""
Web service backend of the components code
"""
import typing
import numpy as np

import tfields
import w7x
from w7x.simulation.coils import CoilsBackend
from w7x.simulation.backends.web_service.base import get_server


WS_DB = w7x.config.coils.web_service.database


class CoilsWebServiceBackend(CoilsBackend):
    """
    Backend implementation
    """

    @staticmethod
    @w7x.node
    # pylint:disable=too-many-locals
    def _get_filaments(
        *coil_ids: typing.Union[int, w7x.model.Coil]
    ) -> typing.List[tfields.Points3D]:
        """
        Get the filaments belonging to the coils of the given coil_ids
        """
        coils_db_client = get_server(WS_DB)

        # One request is nothing in time as compared to the communication time with the ws!
        coil_data = coils_db_client.service.getCoilData(list(coil_ids))

        filaments = []
        for coil_info in coil_data:
            filament = tfields.Points3D(
                np.transpose(
                    [
                        coil_info.vertices.x1,
                        coil_info.vertices.x2,
                        coil_info.vertices.x3,
                    ]
                )
            )
            filaments.append(filament)
        return filaments
