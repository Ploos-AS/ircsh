# M4.8 audit logging

Security-relevant runtime decisions emit structured JSON through the dedicated `ircsh.audit` logger. Events record action, trusted target, result and a bounded reason token.

Quota-aware start/restart records allowed, denied and runtime-failed outcomes. Stop records allowed or failed outcomes and remains available to reduce resource use.

Audit fields reject newline/NUL injection and are length bounded. Exception messages are not logged; only exception type names are used, avoiding accidental leakage of secrets or command output. Production deployments can route the logger to journald/syslog with normal host policy.
