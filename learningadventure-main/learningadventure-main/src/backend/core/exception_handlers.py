from core.exceptions import (
    ObjectNotFoundError,
    InvalidSessionError,
    PermissionDeniedError,
    ValidationError,
    DatabaseError,
    SessionExpiredError,
    UnauthorizedError,
    JSONParsingError
)
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
async def object_not_found_handler(
    request:Request,
    exc:ObjectNotFoundError,
):
    return JSONResponse(
        status_code = 404,
        content={
            "detail": exc.message
        },
    )
async def invalid_session_handler(
    request:Request,
    exc:InvalidSessionError,
):
    return JSONResponse(
        status_code = 401,
        content={
            "detail":"Invalid session"
        },
    )
async def permission_denied_handler(
    request:Request,
    exc:PermissionDeniedError,
):
    return JSONResponse(
        status_code = 403,
        content={
            "detail":exc.message
        },
    )
async def validation_error_handler(
    request:Request,
    exc:ValidationError,
):
    return JSONResponse(
        status_code = 422,
        content={
            "detail":exc.message
        },
    )
async def database_error_handler(
    request:Request,
    exc:DatabaseError,
):
    return JSONResponse(
        status_code = 500,
        content={
            "detail":exc.message
        },
    )
async def session_expired_handler(
    request:Request,    
    exc:SessionExpiredError,
):
    return JSONResponse(
        status_code = 401,
        content={
            "detail":exc.message
        },
    )
async def unauthorized_handler(
    request:Request,
    exc:UnauthorizedError,
):
    return JSONResponse(
        status_code = 401,
        content={
            "detail":exc.message
        },
    )
async def json_parsing_error_handler(
    request:Request,
    exc:JSONParsingError,
):
    return JSONResponse(
        status_code = 400,
        content={
            "detail":exc.message
        },
    )

def register_exception_handler(app:FastAPI):
    app.add_exception_handler(
        ObjectNotFoundError,
        object_not_found_handler
    )
    app.add_exception_handler(
        InvalidSessionError,
        invalid_session_handler
    )
    app.add_exception_handler(
        PermissionDeniedError,
        permission_denied_handler
    )
    app.add_exception_handler(
        ValidationError,
        validation_error_handler
    )
    app.add_exception_handler(
        DatabaseError,
        database_error_handler
    )
    app.add_exception_handler(
        SessionExpiredError,
        session_expired_handler
    )
    app.add_exception_handler(
        UnauthorizedError,
        unauthorized_handler
    )
    app.add_exception_handler(
        JSONParsingError,
        json_parsing_error_handler
    )
    

# usage: raise ObjectNotFoundError("Profile")