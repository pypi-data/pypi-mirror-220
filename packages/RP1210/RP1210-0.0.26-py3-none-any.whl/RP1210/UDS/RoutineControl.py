from . import UDSMessage
from .. import sanitize_msg_param


class RoutineControlRequest(UDSMessage):
    """
    Routine Control (Request)
    - `sid` = 0x31
    - `subfn` = routineControlType
    - 'did` = routineIdentifier (2 bytes)
    - `data` = routineControlOptionRecord
    """

    _sid = 0x31
    _isResponse = False

    # sub-function IDs, for convenience:
    startRoutine = 0x01
    stopRoutine = 0x02
    requestRoutineResults = 0x03

    def __init__(self, subfn: int = startRoutine, did: int = 0, data: bytes = b''):
        super().__init__()
        self._hasSubfn = True
        self._hasDID = True
        self._hasData = True
        self._dataSize = len(data)
        self._dataSizeCanChange = True

        self.subfn = subfn
        self.did = did
        self.data = data

class RoutineControlResponse(UDSMessage):
    """
    Routine Control (Response)
    - `sid` = 0x71
    - `subfn` = routineControlType
    - 'did` = routineIdentifier (2 bytes)
    - `data` = routineInfo (1 byte) + routineStatusRecord (n bytes)
    """

    _sid = 0x71
    _isResponse = True

    # sub-function IDs, for convenience:
    startRoutine = 0x01
    stopRoutine = 0x02
    requestRoutineResults = 0x03

    def __init__(self, subfn: int = startRoutine, did: int = 0, data: bytes = b''):
        super().__init__()
        self._hasSubfn = True
        self._hasDID = True
        self._hasData = True
        self._dataSize = len(data)
        self._dataSizeCanChange = True

        self.subfn = subfn
        self.did = did
        self.data = data
