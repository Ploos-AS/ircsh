# ircsh roadmap

## M0 — Foundation — PASS

- Define scope and security boundary.
- Establish repository structure and license.
- Provide a runnable interactive prototype.
- Implement an explicit built-in command registry.
- Reject arbitrary operating-system commands.
- Add architecture, threat-model, qualification documentation, and CI.

## M1 — Account and configuration model — PASS

- System and per-user configuration.
- Account identity and capability model.
- Read-only status and quota providers.
- Structured output/error model.
- Configuration validation.

## M2 — Service abstraction — PASS

- Backend-neutral, typed, multi-instance service API.
- Read/status and capability-gated lifecycle operations.
- Bouncers: soju, ZNC, psyBNC, muh, BIP, pounce.
- Bots: Eggdrop, Limnoria, Sopel, Errbot, EnergyMech, Psotnic.
- Persistent clients: WeeChat, Irssi, BitchX.
- Deterministic runtime targets; no account-selected units or commands.
- Separate read/manage capabilities with read-only defaults.
- Fail-closed mutation when no writable runtime is configured.
- Integrated qualification on Python 3.11, 3.12 and 3.13.

## M3 — Sessions, configuration and observability — PASS

- Persistent terminal-session integration for IRC clients.
- Controlled service configuration editing with schema/policy validation.
- Read-only service log access with policy enforcement.
- Session attach/detach/status abstraction without generic shell escape.
- Qualification for session/config/log security boundaries.

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

## M7 — Network identity and vhosts

- Managed VHOST/vanity-host pool; users never select arbitrary bind addresses.
- First-class IPv4 and IPv6 support, including administratively delegated IPv6 pools/prefixes.
- Per-account VHOST assignment, revocation and default selection.
- Separate server/service bind identity from IRC-network cloaks/vanity hosts.
- Validate address ownership, local availability and DNS policy before assignment.
- Capability-gated user commands for list/show/request/set-default.
- Administrative assign/revoke/pool management with audit logging.
- Apply approved identities to supported bouncers, bots and persistent IRC clients without shell escape.
- VHOST-aware quotas, reconciliation, health checks and qualification tests.
- Keep the model suitable for later shells.no plan/tier and custom-host integration.

## Later

- Additional IRC bouncers, bots and clients.
- Optional web administration.
- Multi-host scheduling.
- Backup/restore tooling.
- Packaging for common Linux distributions.
