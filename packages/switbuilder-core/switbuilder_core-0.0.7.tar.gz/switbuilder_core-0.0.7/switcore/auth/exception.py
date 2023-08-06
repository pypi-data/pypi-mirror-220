from fastapi import HTTPException

from switcore.action.schemas import SwitRequest


class SwitUserNotFoundException(HTTPException):
    def __init__(self, detail: str, swit_request):
        super().__init__(status_code=403, detail=detail)
        self.swit_request: SwitRequest = swit_request


class SwitNeedScopeException(HTTPException):
    def __init__(self, detail: str, swit_request):
        super().__init__(status_code=403, detail=detail)
        self.swit_request: SwitRequest = swit_request
