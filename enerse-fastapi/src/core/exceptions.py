from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from typing import List


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors: List[dict] = []
    for err in exc.errors():
        errors.append({
            "field": ".".join(str(loc) for loc in err["loc"] if loc != "body"),
            "message": err["msg"].capitalize()
        })

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({
            "message": "Validation failed",
            "errors": errors,
            "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY
        }),
    )
