from pydantic import BaseModel, field_validator


class PincodeRequest(BaseModel):
    pincode: str

    @field_validator("pincode")
    @classmethod
    def validate_pincode(cls, values):
        if len(values) != 6 or not values.isdigit():
            raise ValueError("Pincode not found error")
        return values


class LocationResponse(BaseModel):
    pincode: str
    city: str
    state: str
    district: str


class BulkRequest(BaseModel):
    pincodes: list[str]

    @field_validator("pincodes")
    @classmethod
    def validate_pincode(cls, values):
        if len(values) == 0:
            raise ValueError("At least one pincode is required")
        if len(values) > 20:
            raise ValueError("Only passing of 20 data is allowed")
        for code in values:
            if len(code) != 6 or not code.isdigit():
                raise ValueError(
                    "please send correct pincode with 6 digit or pincode shoould be no only"
                )
            return values


class BulkResponse(BaseModel):
    status: str = "success"
    found: int
    not_found: int
    results: list[LocationResponse]
    missing: list[str]
