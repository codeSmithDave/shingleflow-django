# shingle-flow

A backend service for roofing contractors to manage clients, projects, and scheduled work; built with Django and Django REST Framework.

## What it does

Contractors track their clients, the jobs (projects) tied to each client, and the individual scheduled work days for each project. The API enforces strict row-level data isolation: every user only ever sees and modifies their own data, regardless of how deep the relationship chain runs (a work day, for example, is scoped through its project and that project's client back to the requesting user).

## Design decisions worth noting

- **Per-app versioned API structure.** Each Django app owns its own `api/v1/` package (serializers, views, urls), rather than a single monolithic `api` app. It allows versioning one app independently of others as the API evolves.
- **No hard deletes.** All foreign keys use `PROTECT`; user deactivation is handled via a soft-delete flag rather than removing rows, preserving referential integrity and historical data.
- **PATCH-only partial updates.** `PUT` is intentionally excluded from every endpoint - partial payloads against `PUT` risk silently nulling out fields the client didn't intend to touch; `PATCH` covers every legitimate update case without that risk.
- **Row-level security via `get_queryset()`.** Every ownership check happens at the queryset level, not just at the permission layer, so a user can never retrieve, update, or reference a resource outside their own account, even across multi-hop relationships.
- **Server-derived ownership on writes.** Foreign keys tied to ownership (e.g. which client a project belongs to) are never trusted from client-submitted payloads. They're marked read-only on the serializer and resolved server-side against the authenticated user before saving.

## Stack

Django, Django REST Framework, PostgreSQL ( SQLite being used during the initial setup , before being replaces with PostgreSQL ).