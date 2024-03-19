from werkzeug.exceptions import HTTPException

def handle_generic_try_catch(err):
    if isinstance(err, DoLandBaseException):
        raise err
    raise DoLandInternalErrorException()



# DoLandErrCode used for custom error handling
#  - sometimes HttpCode is not enough, and message parsing can be pain.
class DoLandBaseException(HTTPException):
    code = None
    DoLandErrCode = None
    def __init__(self, error_message = "Base Exception"):
        super().__init__(description=error_message)

class DoLandNotFoundException(DoLandBaseException):
    code = 404
    DoLandErrCode = -1
    def __init__(self, error_message = "The requested object was not found"):
        super().__init__(error_message)

class DoLandInternalErrorException(DoLandBaseException):
    code = 500
    DoLandErrCode = -2

    def __init__(self, error_message = "Unkown internal server error occured"):
        super().__init__(error_message)


class DoLandBadReqException(DoLandBaseException):
    code = 400
    DoLandErrCode = -3
    def __init__(self, error_message = "The request was found to be bad"):
        super().__init__(error_message)

class MatterAPIException(DoLandBaseException):
    code = 500
    DoLandErrCode = -4

    def __init__(self, error_message = "Unkown Matter API exception"):
        super().__init__(error_message)