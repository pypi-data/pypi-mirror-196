from __future__ import annotations

# Kept here for backwards compatibility
from typing import Any, Optional, Protocol, TypeVar, cast

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.http import HttpRequest, HttpResponse
from django.utils.module_loading import import_string

R_ = TypeVar("R_", bound=HttpResponse)


class ResponseHookProtocol(Protocol):
    def __call__(
        self,
        request: HttpRequest,
        response: R_,
        user: AbstractBaseUser,
        cognito_jwt: dict[str, Any],
    ) -> R_:
        ...


class Settings:
    """
    Shadow Django's settings with a little logic
    """

    @property
    def COGNITO_ENDPOINT(self) -> str:
        return cast(str, getattr(settings, "COGNITO_ENDPOINT"))

    @property
    def COGNITO_AUTH_ENDPOINT(self) -> str:
        return f"{self.COGNITO_ENDPOINT}/oauth2/authorize"

    @property
    def COGNITO_TOKEN_ENDPOINT(self) -> str:
        return f"{self.COGNITO_ENDPOINT}/oauth2/token"

    @property
    def COGNITO_CLIENT_ID(self) -> str:
        return cast(str, getattr(settings, "COGNITO_CLIENT_ID"))

    @property
    def COGNITO_CLIENT_SECRET(self) -> str:
        return cast(str, getattr(settings, "COGNITO_CLIENT_SECRET"))

    @property
    def COGNITO_REDIRECT_URI(self) -> Optional[str]:
        return cast(str, getattr(settings, "COGNITO_REDIRECT_URI", ""))

    @property
    def COGNITO_JWKS_URI(self) -> str:
        return cast(str, getattr(settings, "COGNITO_JWKS_URI", ""))

    @property
    def response_hook(self) -> ResponseHookProtocol:
        fn = getattr(settings, "COGNITO_RESPONSE_HOOK", "")
        return import_string(fn) if fn else default_response_hook


def default_response_hook(
    request: HttpRequest,
    response: HttpResponse,
    user: AbstractBaseUser,
    cognito_jwt: dict[str, Any],
) -> HttpResponse:
    return response


conf = Settings()
