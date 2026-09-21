# M2.13 — Limnoria bot backend

Limnoria is supported as a multi-instance `ServiceKind.BOT` backend.

Validated instance names map to deterministic runtime targets such as `ircsh-limnoria-helper.service`. The generic `bot list|status|start|stop|restart` commands and `bots.read` / `bots.manage` capabilities apply.

ircsh does not accept arbitrary executable paths, service unit names, or shell command construction from account input. Production instances should use dedicated configuration/data directories and unprivileged runtime identities.

## Qualification

```sh
python -m unittest discover -s tests -v
```
