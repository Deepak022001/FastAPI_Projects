from fastapi import Request
from fastapi.responses import JSONResponse


class Pincode_not_found_Error(Exception):
    def __init__(self, pincode: str):
        self.pincode = pincode


class Invalid_Pincode_Error(Exception):
    def __init__(
        self, reason: str = "Invalid pincode", pincode: str = "Invalid format"
    ):
        self.reason = reason
        self.pincode = pincode


async def Pincode_Not_Found_Handler(request: Request, exc: Pincode_not_found_Error):
    return JSONResponse(
        status_code=404,
        content={
            "error": "Pincode not found",
            "message": f"No location for pincode:{exc.pincode}",
            "pincode": exc.pincode,
        },
    )


async def Invalid_Pincode_Handler(request: Request, exc: Invalid_Pincode_Error):
    return JSONResponse(
        status_code=404,
        content={
            "error": "Pincode not found",
            "message": f"Pincode '{exc.pincode}' is invalid '{exc.reason}'",
            "pincode": exc.pincode,
        },
    )
