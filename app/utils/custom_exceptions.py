from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

# from app.exceptions import WarehouseNotFoundError, ProductAlreadyExistsError


async def global_exception_handler(request: Request, exc: Exception):

    if isinstance(exc, ItemNotFound):
        return JSONResponse(status_code=404, content={"message": exc.message})

    if isinstance(exc, InvalidToken):
        return JSONResponse(status_code=403, content={"message": exc.message})

    if isinstance(exc, InactiveUser):
        return JSONResponse(status_code=403, content={"message": exc.message})

    if isinstance(exc, TokenExpired):
        return JSONResponse(status_code=403, content={"message": exc.message})

    if isinstance(exc, ServerError):
        return JSONResponse(status_code=505, content={"message": exc.message})

    if isinstance(exc, AuthError):
        return JSONResponse(
            status_code=exc.code,
            content={"message": exc.message},
            headers=exc.headers,
        )

    else:
        return JSONResponse(status_code=500, content={"detail": "Server has error"})


class ItemNotFound(Exception):
    def __init__(self, item_id: int, item: str):
        self.item_id = item_id
        self.message = f"{item.upper()} with id {item_id} not found."
        super().__init__(self.message)


class AlreadyExists(Exception):
    def __init__(self, item_param: int, item: str):
        self.item_id = item_param
        self.message = f"{item.upper()} with id {item_param} already exists."
        super().__init__(self.message)


class TokenExpired(Exception):
    def __init__(self):
        self.message = "Token has expired"
        super().__init__(self.message)


class ServerError(Exception):
    def __init__(self):
        self.message = "Something went wrong, please try again"
        super().__init__(self.message)


class InvalidToken(Exception):
    def __init__(self):
        self.message = "Invalid signature, Wrong secret key or algorithm"
        super().__init__(self.message)


class InactiveUser(Exception):
    def __init__(self):
        self.message = "Current user is Inactive"
        super().__init__(self.message)


class AuthError(Exception):
    def __init__(self):
        self.code = 401
        self.message = "Incorrect username or password"
        self.headers = {"WWW-Authenticate": "Bearer"}
        super().__init__(self.message, self.code, self.headers)
