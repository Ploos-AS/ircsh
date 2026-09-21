# M6.1 administrative account plans

M6 starts with trusted, named account plans. A plan is an administrator-selected bundle of capabilities and resource limits; an IRC account cannot define or extend its own plan.

Initial plans:

- `irc-basic`: read-only status/quota/service access plus bouncer visibility, maximum 2 services.
- `irc-advanced`: controlled bouncer/bot/client/session/config management and log access, with larger memory, disk, connection and service limits.

Unknown plan names fail closed. The earlier Developer tier is intentionally not part of this restricted-shell plan registry because a normal Unix shell has a different security boundary and should be provisioned separately.

This milestone defines the administrative data model only. Persistent account storage, privileged provisioning and administrative CLI/API actions follow in later M6 increments.
