# M2.17 — Psotnic bot backend

Psotnic is supported as a legacy multi-instance `ServiceKind.BOT` backend.

Validated instance names map to deterministic targets such as `ircsh-psotnic-guard.service`. The generic `bot list|status|start|stop|restart` interface and `bots.read` / `bots.manage` capabilities apply.

## Legacy hardening

Production instances must run under an unprivileged identity with dedicated per-instance configuration/state. Account input cannot select executable paths, service units, command lines, modules, scripts or shell commands. Filesystem/device access and Linux capabilities should be minimized; process, memory, file and connection limits should be applied. Bot linking, listeners, DCC/file-transfer and other optional network surfaces should remain disabled unless explicitly enabled by policy.

ircsh controls lifecycle only and does not expose Psotnic's internal command interface as operating-system commands.

## Qualification

```sh
python -m unittest discover -s tests -v
```
