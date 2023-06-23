from authlib.integrations.flask_oauth2 import ResourceProtector
from .validator import Auth0JWTBearerTokenValidator


require_auth = ResourceProtector()

validator = Auth0JWTBearerTokenValidator(
    "YOUR_DOMAIN",
    "YOUR_API_IDENTIFIER"
)

require_auth.register_token_validator(validator)
