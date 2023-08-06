from iqrfpy.exceptions import RequestParameterInvalidValueError
import iqrfpy.utils.dpa as dpa_constants

__all__ = [
    'IoTriplet'
]


class IoTriplet:

    __slots__ = '_port', '_mask', '_value'

    def __init__(self, port: int, mask: int, value: int):
        self._validate(port=port, mask=mask, value=value)
        self._port = port
        self._mask = mask
        self._value = value

    def _validate(self, port: int, mask: int, value: int):
        self._validate_port(port=port)
        self._validate_mask(mask=mask)
        self._validate_value(value=value)

    @staticmethod
    def _validate_port(port: int):
        if not (dpa_constants.BYTE_MIN <= port <= dpa_constants.BYTE_MAX):
            raise RequestParameterInvalidValueError('Port should be between 0 and 255.')

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, val: int):
        self._validate_port(port=val)
        self._value = val

    @staticmethod
    def _validate_mask(mask: int):
        if not (dpa_constants.BYTE_MIN <= mask <= dpa_constants.BYTE_MAX):
            raise RequestParameterInvalidValueError('Mask should be between 0 and 255.')

    @property
    def mask(self):
        return self._mask

    @mask.setter
    def mask(self, val: int):
        self._validate_mask(mask=val)
        self._mask = val

    @staticmethod
    def _validate_value(value: int):
        if not (dpa_constants.BYTE_MIN <= value <= dpa_constants.BYTE_MAX):
            raise RequestParameterInvalidValueError('Value should be between 0 and 255.')

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val: int):
        self._validate_value(value=val)
        self._value = val
