import logging

from drf_spectacular.extensions import OpenApiAuthenticationExtension
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from accounts.auth import verify_supabase_jwt
from accounts.services import get_or_create_user_from_claims

logger = logging.getLogger(__name__)

_GENERIC_MESSAGE = "Authentication failed."


class SupabaseJWTAuthentication(BaseAuthentication):
 """Authenticate requests carrying a Supabase access token as `Authorization: Bearer <jwt>`."""

 def authenticate(self, request):
  header = request.headers.get("Authorization")
  if header is None:
   # No credentials offered: anonymous, left for the permission classes to decide.
   return None

  # A header that is present but malformed is an error, never anonymous.
  parts = header.split()
  if len(parts) != 2:
   logger.warning("Malformed Authorization header: expected 'Bearer <token>'")
   raise AuthenticationFailed(_GENERIC_MESSAGE)

  scheme, token = parts
  if scheme.lower() != "bearer":
   logger.warning("Authorization header uses an unsupported scheme")
   raise AuthenticationFailed(_GENERIC_MESSAGE)

  # AuthenticationFailed from either call propagates unchanged.
  claims = verify_supabase_jwt(token)
  user = get_or_create_user_from_claims(claims)

  if not user.is_active:
   logger.warning("Authentication rejected: user id=%s is inactive", user.pk)
   raise AuthenticationFailed(_GENERIC_MESSAGE)

  return (user, None)

 def authenticate_header(self, request):
  # Makes DRF answer failures with 401 + WWW-Authenticate instead of 403.
  return "Bearer"


class SupabaseJWTAuthenticationScheme(OpenApiAuthenticationExtension):
 # Lives beside the class it documents: drf-spectacular only registers an extension
 # when its module is imported, and this module is always imported once the
 # authenticator is configured in DEFAULT_AUTHENTICATION_CLASSES.
 target_class = "accounts.authentication.SupabaseJWTAuthentication"
 name = "SupabaseJWTAuth"

 def get_security_definition(self, auto_schema):
  return {
   "type": "http",
   "scheme": "bearer",
   "bearerFormat": "JWT",
  }
