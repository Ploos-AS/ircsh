# M2.16 — EnergyMech bot backend

EnergyMech is supported as a legacy multi-instance `ServiceKind.BOT` backend.

Validated instance names map only to deterministic runtime targets such as `ircsh-energymech-guard.service`. Existing `bot list|status|start|stop|restart` commands and `bots.read` / `bots.manage` capabilities apply.

## Mandatory legacy hardening

A production EnergyMech runtime should be treated as untrusted legacy application code:

- dedicated unprivileged identity and per-instance state directory;
- no arbitrary executable, unit or command supplied by the account;
- shell-command functionality disabled in the EnergyMech build/configuration;
- private temporary storage and restricted filesystem/device access;
- no Linux capabilities unless explicitly justified;
- process, memory, file and connection limits;
- explicit outbound IRC/network policy;
- DCC, bot linking, telnet/listener and file-transfer features disabled unless the hosting plan explicitly enables them;
- separate secrets/configuration from account-writable plugin/script data.

ircsh itself exposes lifecycle control only and never translates account strings into shell commands.

## Qualification

```sh
python -m unittest discover -s tests -v
```
