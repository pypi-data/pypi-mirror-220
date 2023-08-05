from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

from starlette.requests import HTTPConnection

from esmerald.enums import ScopeType
from esmerald.parsers import ArbitraryBaseModel
from esmerald.protocols.middleware import MiddlewareProtocol

if TYPE_CHECKING:
    from starlette.types import ASGIApp, Receive, Scope, Send


class AuthResult(ArbitraryBaseModel):
    user: Any


class BaseAuthMiddleware(ABC, MiddlewareProtocol):
    scopes = {ScopeType.HTTP, ScopeType.WEBSOCKET}

    def __init__(self, app: "ASGIApp"):
        super().__init__(app)
        self.app = app

    async def __call__(self, scope: "Scope", receive: "Receive", send: "Send") -> None:
        auth_result = await self.authenticate(HTTPConnection(scope))
        scope["user"] = auth_result.user
        await self.app(scope, receive, send)

    @abstractmethod
    async def authenticate(self, request: HTTPConnection) -> AuthResult:  # pragma: no cover
        """
        The abstract method that needs to be implemented for any authentication middleware.
        """
        raise NotImplementedError("authenticate must be implemented.")
