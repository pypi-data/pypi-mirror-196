# django-cognito-saml

Library to implement django authentication using cognito (via pyjwt).

Assumptions made:

- Using `authorization code` flow. Implicit grant is insecure as the access token is transferred over in the request parameters without encryption.

## Settings

| Setting                   | Description                                                                                                                  |
| ------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| **COGNITO_ENDPOINT**      | Either the hosted domain or custom domain for your cognito app                                                               |
| **COGNITO_CLIENT_ID**     | CLIENT_ID of your application in your user pool                                                                              |
| **COGNITO_CLIENT_SECRET** | CLIENT_SECRET of your application in your user pool                                                                          |
| **COGNITO_JWKS_URI**      | The JWKS URI of your user pool. Used to verify the JWT.                                                                      |
| **COGNITO_REDIRECT_URI**  | **OPTIONAL** It is possible to share one cognito app with multiple websites via a proxy.                                     |
| **COGNITO_RESPONSE_HOOK** | **OPTIONAL** Post authentication hook to modify the response (perhaps to add headers). Specify it as a django import_string. |

## Installation

1. Add the above settings to your settings.

```settings.py
COGNITO_ENDPOINT = "..."
COGNITO_CLIENT_ID = "..."
COGNITO_CLIENT_SECRET = "..."
COGNITO_JWKS_URI = "..."
COGNITO_REDIRECT_URI = "..."
COGNITO_RESPONSE_HOOK = ""
```

2. Define your authentication backend. Subclass off `django_cognito_saml.backends.CognitoUserBackend`.
   A custom backend is where you add users to groups and / or do something custom.
   Set `create_unknown_user = False` if we want only pre-created users to be used.

```python
class CustomCognitoBackend(CognitoUserBackend):
    # Change this to False if you do not want to create a remote user.
    create_unknown_user = True

    def authenticate(  # type: ignore[override]
        self, request: HttpRequest, cognito_jwt: dict[str, Any], **kwargs: Any
    ) -> Optional[AbstractBaseUser]:
        remote_user = cognito_jwt["email"]
        user = super().authenticate(request, remote_user=remote_user, **kwargs)

        # Lets add the user to the group

        groups = cognito_jwt["custom:groups"]

        add_user_to_groups(user, group)
        return user

    def configure_user(  # type: ignore[override]
        self, request: HttpRequest, user: AbstractBaseUser
    ) -> AbstractBaseUser:
        """
        Configure a user after creation and return the updated user.
        By default, return the user unmodified.
        """
        return user


```

3. Add `CustomCognitoBackend` to your authentication backends.
   Alternatively; If you wish to modify the authentication logic (ie: Adding permissions)<>

```python
AUTHENTICATION_BACKENDS = (
    ...
    "apps.backends.CustomCognitoBackend",
    ...
)
```

4. Add the cognito saml urls to your `urls.py`

```python
urls = [
    ...
    path("/", include("django_cognito_saml.urls")),
]
```
