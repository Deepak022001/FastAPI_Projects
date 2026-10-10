from typing import Any, cast

from fastapi import FastAPI

from data import pincode_db
from exceptions import (
    Invalid_Pincode_Error,
    Invalid_Pincode_Handler,
    Pincode_not_found_Error,
    Pincode_Not_Found_Handler,
)
from models import BulkRequest, BulkResponse, LocationResponse

app = FastAPI(
    title="Pincode lookup API",
    description="Auto fill city and state from Indian Pincode during checkout",
)

# Register your custom exception handlers
app.add_exception_handler(
    Pincode_not_found_Error,
    cast(Any, Pincode_Not_Found_Handler),
)

app.add_exception_handler(
    Invalid_Pincode_Error,
    cast(Any, Invalid_Pincode_Handler),
)


@app.get("/")
def root():
    return {"messaage": "Pincode lookup api"}


@app.get("/pincode/{code}", response_model=LocationResponse)
def get_pincode(code: str):
    if len(code) != 6 or not code.isdigit():
        raise Invalid_Pincode_Error(code, "Must be  exactly 6 digit")
    if code not in pincode_db:
        raise Pincode_not_found_Error(code)
    return pincode_db[code]


@app.post("/pincode/bulk", response_model=BulkResponse)
def bulk_lookup(request: BulkRequest):
    results = []
    missing = []

    for code in request.pincodes:
        if code in pincode_db:
            results.append(pincode_db[code])
        else:
            missing.append(code)

    return BulkResponse(
        found=len(results), not_found=len(missing), results=results, missing=missing
    )
