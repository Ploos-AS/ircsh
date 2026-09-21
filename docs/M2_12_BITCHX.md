# M2.12 — BitchX persistent client

BitchX is supported as a persistent `ServiceKind.CLIENT` backend alongside WeeChat and Irssi.

A validated instance name maps to a deterministic runtime target such as `ircsh-bitchx-main.service`. ircsh does not accept a user-selected executable path or arbitrary service unit.

Because BitchX is a legacy client, production deployment should use an unprivileged identity, a dedicated configuration/data directory, filesystem and device restrictions, resource limits, and only the network access required for IRC.

The existing `client list|status|start|stop|restart` command family and `clients.read` / `clients.manage` capabilities apply without special shell logic.

## Qualification

```sh
python -m unittest discover -s tests -v
```
