from __future__ import annotations
from typing import List, Optional, Union
from iqrfpy.enums.commands import IORequestCommands
from iqrfpy.enums.message_types import IOMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.exceptions import RequestParameterInvalidValueError
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.irequest import IRequest
from iqrfpy.peripherals.io.requests.io_triplet import IoTriplet

__all__ = [
    'SetRequest',
    'IoTriplet',
]


class SetRequest(IRequest):

    __slots__ = '_triplets'

    def __init__(self, nadr: int, triplets: List[IoTriplet], hwpid: int = dpa_constants.HWPID_MAX,
                 dpa_rsp_time: Optional[float] = None, dev_process_time: Optional[float] = None,
                 msgid: Optional[str] = None):
        self._validate_triplets(triplets=triplets)
        super().__init__(
            nadr=nadr,
            pnum=EmbedPeripherals.IO,
            pcmd=IORequestCommands.SET,
            m_type=IOMessages.SET,
            hwpid=hwpid,
            dpa_rsp_time=dpa_rsp_time,
            dev_process_time=dev_process_time,
            msgid=msgid
        )
        self._triplets = triplets

    @staticmethod
    def _validate_triplets(triplets: List[IoTriplet]):
        if len(triplets) > 18:
            raise RequestParameterInvalidValueError('Request can carry at most 18 triplets.')

    @property
    def triplets(self):
        return self._triplets

    @triplets.setter
    def triplets(self, val: List[IoTriplet]):
        self._validate_triplets(triplets=val)
        self._triplets = val

    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        pdata = []
        for triplet in self._triplets:
            pdata.extend([triplet.port, triplet.mask, triplet.value])
        self._pdata = pdata
        return super().to_dpa(mutable=mutable)

    def to_json(self) -> dict:
        ports = [{'port': triplet.port, 'mask': triplet.mask, 'value': triplet.value} for triplet in self._triplets]
        self._params = {'ports': ports}
        return super().to_json()
