from typing import Any, Optional

from django.contrib.auth.backends import RemoteUserBackend
from django.contrib.auth.models import AbstractBaseUser
from django.http import HttpRequest


class CognitoUserBackend(RemoteUserBackend):
    """
    This backend is to be used in conjunction with the ``RemoteUserMiddleware``
    found in the middleware module of this package, and is used when the server
    is handling authentication outside of Django.

    By default, the ``authenticate`` method creates ``User`` objects for
    usernames that don't already exist in the database.  Subclasses can disable
    this behavior by setting the ``create_unknown_user`` attribute to
    ``False``.

    Override configure_user for post login customization

    """

    # Change this to False if you do not want to create a remote user.
    create_unknown_user = True

    cognito_jwt: dict

    def authenticate(  # type: ignore[override]
        self, request: HttpRequest, cognito_jwt: dict[str, Any], **kwargs: Any
    ) -> Optional[AbstractBaseUser]:
        self.cognito_jwt = cognito_jwt
        remote_user = cognito_jwt["email"]
        return super().authenticate(request, remote_user=remote_user, **kwargs)

    def configure_user(  # type: ignore[override]
        self, request: HttpRequest, user: AbstractBaseUser, **kwargs: Any
    ) -> AbstractBaseUser:
        """
        Configure a user after creation and return the updated user.

        By default, return the user unmodified.
        """
        return user
