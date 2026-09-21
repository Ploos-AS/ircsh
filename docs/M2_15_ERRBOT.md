# M2.15 — Errbot IRC backend

Errbot is supported as a multi-instance `ServiceKind.BOT` backend for IRC deployments.

Validated instance names map to deterministic targets such as `ircsh-errbot-helper.service`. Existing `bot list|status|start|stop|restart` commands and `bots.read` / `bots.manage` capabilities apply.

ircsh controls only lifecycle state. It does not expose arbitrary Errbot backend selection, plugin commands, executable paths, service-unit names, or shell execution through the restricted shell. Production instances should use an explicit IRC configuration and isolated per-instance state.

## Qualification

```sh
python -m unittest discover -s tests -v
```
