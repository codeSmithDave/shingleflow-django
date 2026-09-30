import logging

import jwt
from django.conf import settings
from jwt import PyJWKClient
from jwt.exceptions import (
 DecodeError,
 ExpiredSignatureError,
 ImmatureSignatureError,
 InvalidAlgorithmError,
 InvalidAudienceError,
 InvalidIssuerError,
 InvalidSignatureError,
 MissingRequiredClaimError,
 PyJWKClientConnectionError,
 PyJWKClientError,
 PyJWTError,
)
from rest_framework.exceptions import AuthenticationFailed

logger = logging.getLogger(__name__)

# Instantiated once at import; PyJWKClient doesn't fetch until the first lookup.
# lifespan=3600 caches the JWK set for an hour, cache_keys=True caches per-kid lookups.
# timeout=5 keeps a slow/unreachable Supabase from hanging a worker for the 30s default.
_jwks_client = PyJWKClient(
 settings.SUPABASE_JWKS_URL,
 cache_keys=True,
 lifespan=3600,
 timeout=5,
)

# Asymmetric algorithms only, so a token can never be verified with a shared secret.
_ALGORITHMS = ["ES256", "RS256"]
_AUDIENCE = "authenticated"
_ISSUER = f"{settings.SUPABASE_URL.rstrip('/')}/auth/v1"
_LEEWAY_SECONDS = 10

# Every failure returns this same message to the client; the specific reason is
# only logged, so a forged token gets no signal about which check it failed.
_GENERIC_MESSAGE = "Authentication failed."


def _fail(reason: str, level: int = logging.WARNING) -> AuthenticationFailed:
 logger.log(level, "JWT verification failed: %s", reason)
 return AuthenticationFailed(_GENERIC_MESSAGE)


def verify_supabase_jwt(token: str) -> dict:
 """Verify a Supabase access token and return its decoded claims.

 Checks signature (against the project's JWKS), exp, aud, iss, and requires sub.
 Raises AuthenticationFailed with a generic message on any failure; the specific
 reason is logged server-side.
 """
 try:
  signing_key = _jwks_client.get_signing_key_from_jwt(token)
 except PyJWKClientConnectionError as e:
  # Checked before PyJWKClientError, which is its parent class.
  # An ops problem rather than a bad token, so logged at error level.
  raise _fail(f"could not fetch signing keys from the JWKS endpoint ({e})", logging.ERROR)
 except PyJWKClientError:
  raise _fail("no signing key matches the token's key id")
 except DecodeError:
  raise _fail("malformed token")
 except PyJWTError:
  raise _fail("token could not be inspected")

 try:
  return jwt.decode(
   token,
   signing_key.key,
   algorithms=_ALGORITHMS,
   audience=_AUDIENCE,
   issuer=_ISSUER,
   leeway=_LEEWAY_SECONDS,
   options={"require": ["exp", "aud", "iss", "sub"]},
  )
 except ExpiredSignatureError:
  raise _fail("token has expired")
 except ImmatureSignatureError:
  raise _fail("token is not yet valid")
 except InvalidAudienceError:
  raise _fail("token audience is invalid")
 except InvalidIssuerError:
  raise _fail("token issuer is invalid")
 except InvalidSignatureError:
  raise _fail("token signature is invalid")
 except InvalidAlgorithmError:
  raise _fail("token signing algorithm is not allowed")
 except MissingRequiredClaimError as e:
  raise _fail(f"token is missing required claim: {e.claim}")
 except DecodeError:
  raise _fail("malformed token")
 except PyJWTError:
  raise _fail("token is invalid")
