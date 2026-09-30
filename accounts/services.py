import logging

from django.db import IntegrityError, transaction
from rest_framework.exceptions import AuthenticationFailed

from accounts.models import User
from profiles.models import UserProfile, UserSchedule

logger = logging.getLogger(__name__)


def _clean(value, max_length):
 # user_metadata is client-controlled: coerce to a trimmed, length-capped string.
 if not isinstance(value, str):
  return ""
 return value.strip()[:max_length]


def _resolve_names(meta):
 # Tier 1: our own signup form. Tier 2: Google's split name fields. Each wins only
 # if both halves are present.
 first = _clean(meta.get("firstName"), 150)
 last = _clean(meta.get("lastName"), 150)
 if first and last:
  return first, last

 given = _clean(meta.get("given_name"), 150)
 family = _clean(meta.get("family_name"), 150)
 if given and family:
  return given, family

 # Tier 3: a single display name goes entirely into first_name.
 full = _clean(meta.get("full_name") or meta.get("name"), 150)
 if full:
  return full, ""

 # No complete name anywhere: keep whatever partial value exists (e.g. a form
 # signup with no last name) rather than discarding it.
 for partial_first, partial_last in ((first, last), (given, family)):
  if partial_first or partial_last:
   return partial_first, partial_last

 return "", ""


def get_or_create_user_from_claims(claims: dict) -> User:
 """Resolve the local User for verified Supabase claims, creating it on first sight."""
 auth_id = claims["sub"]  # guaranteed present by verify_supabase_jwt

 user = User.objects.filter(auth_id=auth_id).first()
 if user is not None:
  return user

 email = claims.get("email")
 if not email:
  logger.warning("Cannot create user for auth_id=%s: no email claim", auth_id)
  raise AuthenticationFailed("Authentication failed.")

 meta = claims.get("user_metadata")
 if not isinstance(meta, dict):
  meta = {}

 first_name, last_name = _resolve_names(meta)
 brand_name = _clean(meta.get("brandName"), 100)

 try:
  with transaction.atomic():
   user = User.objects.create_user(
    email=email,
    auth_id=auth_id,
    first_name=first_name,
    last_name=last_name,
   )
   UserSchedule.objects.create(user=user)
   UserProfile.objects.create(user=user, brand_name=brand_name or None)
 except IntegrityError:
  # Either a concurrent first request created this user (auth_id unique), or
  # the email already belongs to a different auth_id (email unique).
  user = User.objects.filter(auth_id=auth_id).first()
  if user is None:
   logger.error("Cannot create user for auth_id=%s: email already in use", auth_id)
   raise AuthenticationFailed("Authentication failed.")

 return user
