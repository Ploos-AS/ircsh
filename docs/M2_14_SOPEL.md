# M2.14 — Sopel bot backend

Sopel is supported as a multi-instance `ServiceKind.BOT` backend.

Validated names produce deterministic runtime targets such as `ircsh-sopel-helper.service`. Sopel uses the existing `bot list|status|start|stop|restart` command family and `bots.read` / `bots.manage` capabilities.

Account input cannot select an executable path, service unit, Python command, plugin command, or shell command. Production instances should run unprivileged with per-instance configuration/data directories.

## Qualification

```sh
python -m unittest discover -s tests -v
```
