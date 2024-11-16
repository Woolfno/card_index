from enum import Enum
from litestar.connection import ASGIConnection
from litestar.handlers.base import BaseRouteHandler
from litestar.exceptions import NotAuthorizedException


class UserRole(str, Enum):
    GUEST = "guest"
    AUTHENTICATED = "authenticated"

def guest_user_guard(connection: ASGIConnection, _:BaseRouteHandler)->None:
    if not connection.user.is_guest:
        raise NotAuthorizedException
    
def authenticated_user_guard(connection:ASGIConnection, _:BaseRouteHandler) ->None:
    if not connection.user.is_authenticated:
        raise NotAuthorizedException
                