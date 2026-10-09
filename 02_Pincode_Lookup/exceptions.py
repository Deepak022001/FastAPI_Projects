from fastapi.responses import JSONResponse
from fastapi import Request

class PincodeNotFounError(Exception):
    def __init__(self,pincode:str):
        self.pincode=pincode

class InvalidPinCodeError(Exception):
    def __init__(self,pincode:str="Invalid format",reason:str="Invalid format"):
        self.pincode=pincode
        self.reason=reason

async def pincode_not_found_handler(request:Request,exc:PincodeNotFounError):
    return JSONResponse(
        status_code=404,
        content={
            "error":"pincode not found",
            "message":f"No location for pincode :{exc.pincode}",
            "pincode":exc.pincode
        }
    )

async def invalid_pincode(request:Request,exc:InvalidPinCodeError):
    return JSONResponse(
        status_code=404,
        content={
            "error":"pincode not found",
            "message":f"Pincode '{exc.pincode}'is invalid :{exc.reason}",
            "pincode":exc.pincode
        }
    )