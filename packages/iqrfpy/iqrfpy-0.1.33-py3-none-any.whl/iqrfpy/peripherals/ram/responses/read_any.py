from __future__ import annotations
from typing import List, Optional
from iqrfpy.iresponse import IResponseGetterMixin
from iqrfpy.enums.commands import RAMResponseCommands
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.utils.common import Common
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.utils.dpa import ResponseCodes, ResponsePacketMembers
from iqrfpy.utils.validators import DpaValidator

__all__ = ['ReadAnyResponse']


class ReadAnyResponse(IResponseGetterMixin):

    __slots__ = '_data'

    def __init__(self, nadr: int, hwpid: int = dpa_constants.HWPID_MAX, rcode: int = 0, dpa_value: int = 0,
                 msgid: Optional[str] = None, pdata: Optional[List[int]] = None, result: Optional[dict] = None):
        super().__init__(
            nadr=nadr,
            pnum=EmbedPeripherals.RAM,
            pcmd=RAMResponseCommands.READ_ANY,
            m_type=None,
            hwpid=hwpid,
            rcode=rcode,
            dpa_value=dpa_value,
            msgid=msgid,
            pdata=pdata,
            result=result
        )
        if rcode == ResponseCodes.OK:
            self._data = result['pData']

    @property
    def data(self) -> List[int]:
        return self._data

    @staticmethod
    def from_dpa(dpa: bytes) -> ReadAnyResponse:
        DpaValidator.base_response_length(dpa=dpa)
        nadr = dpa[ResponsePacketMembers.NADR]
        hwpid = Common.hwpid_from_dpa(dpa[ResponsePacketMembers.HWPID_HI], dpa[ResponsePacketMembers.HWPID_LO])
        rcode = dpa[ResponsePacketMembers.RCODE]
        dpa_value = dpa[ResponsePacketMembers.DPA_VALUE]
        pdata = None
        result = None
        if rcode == ResponseCodes.OK:
            pdata = Common.pdata_from_dpa(dpa=dpa)
            result = {'pData': list(dpa[8:])}
        return ReadAnyResponse(nadr=nadr, hwpid=hwpid, rcode=rcode, dpa_value=dpa_value, pdata=pdata, result=result)

    @staticmethod
    def from_json(json: dict) -> ReadAnyResponse:
        raise NotImplementedError('ReadAny JSON API request not implemented.')
