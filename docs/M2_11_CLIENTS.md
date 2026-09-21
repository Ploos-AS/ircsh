# M2.11 — Persistent IRC clients

ircsh now treats persistent WeeChat and Irssi sessions as `ServiceKind.CLIENT`.

Commands are `client list`, `client status <name>`, and capability-gated `client start|stop|restart <name>`. Read access requires `clients.read`; lifecycle operations require `clients.manage`.

The backend identifier is restricted to `weechat` or `irssi`. Validated instance names produce deterministic dedicated runtime targets such as `ircsh-weechat-main.service`. No executable path or shell command is accepted.

## Qualification

```sh
python -m unittest discover -s tests -v
```
