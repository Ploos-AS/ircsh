# ircsh roadmap

## M0 — Foundation

- Define scope and security boundary.
- Establish repository structure and license.
- Provide a runnable interactive prototype.
- Implement an explicit built-in command registry.
- Reject arbitrary operating-system commands.
- Add architecture, threat-model, qualification documentation, and CI.

## M1 — Account and configuration model

- System and per-user configuration.
- Account identity and capability model.
- Read-only status and quota providers.
- Structured output/error model.
- Configuration validation.

## M2 — Service abstraction

- Backend-neutral service API.
- Lifecycle/status operations.
- soju and ZNC adapters.
- Log access with policy enforcement.
- Explicit per-account service permissions.

## M3 — IRC clients and bots

- Irssi and WeeChat session launching.
- Eggdrop/bot lifecycle abstraction.
- Persistent terminal-session integration.
- Controlled configuration editing.

## M4 — Isolation and quotas

- Runtime backend for rootless containers and/or systemd user services.
- CPU, memory, process, disk, connection, and service limits.
- Namespace/filesystem isolation.
- Audit logging.

## M5 — SSH deployment

- Supported login-shell installation.
- SSH key/account provisioning guidance.
- Restricted forwarding/PTY/environment policy.
- Operational hardening and recovery documentation.

## M6 — Administration

- Administrative CLI/API.
- Account plans/capabilities.
- Provisioning/deprovisioning.
- Metrics and health integration.

## Later

- Additional IRC bouncers and bots.
- Optional web administration.
- Multi-host scheduling.
- Backup/restore tooling.
- Packaging for common Linux distributions.
