# ircsh

A purpose-built restricted login shell for IRC hosting accounts.

ircsh provides a small, capability-controlled interface for managing IRC bouncers, bots and persistent IRC clients without exposing a general Unix shell. It is intended for SSH-based IRC shell services and multi-user IRC hosting.

> **Status:** active development. M0 and M1 foundations are implemented; the M2 service/backend layer is implemented and undergoing integrated qualification.

## Service support

| Type | Backends |
| --- | --- |
| Bouncers | soju, ZNC, psyBNC, muh, BIP, pounce |
| Bots | Eggdrop, Limnoria, Sopel, Errbot, EnergyMech, Psotnic |
| Persistent clients | WeeChat, Irssi, BitchX |

Backends use explicit service kinds and validated instance names. Runtime targets are deterministic; account input is never converted into arbitrary operating-system commands.

## Commands

Core commands:

```text
help
account
capabilities
status
services
quota
version
exit
quit
```

Service commands:

```text
bouncer list
bouncer status <name>
bouncer start|stop|restart <name>

bot list
bot status <name>
bot start|stop|restart <name>

client list
client status <name>
client start|stop|restart <name>
```

Lifecycle operations require explicit management capabilities. Default accounts are read-only.

## Security model

ircsh is deliberately **not** a replacement for Bash, Zsh or Fish. There is no fallback to an operating-system shell for unknown commands.

The design follows these rules:

- explicit command and capability allowlists;
- no generic shell-command execution;
- validated service identities and deterministic runtime targets;
- separate read and management capabilities;
- fail-closed lifecycle operations when no mutation runtime is configured;
- stronger isolation guidance for legacy software such as psyBNC, muh, EnergyMech and Psotnic;
- runtime isolation and quotas are planned as a dedicated milestone.

See [architecture](docs/ARCHITECTURE.md) and [threat model](docs/THREAT_MODEL.md).

## Installation for development

Requires Python 3.11 or newer.

```sh
git clone https://github.com/Ploos-AS/ircsh.git
cd ircsh
python -m venv .venv
. .venv/bin/activate
python -m pip install -e .
ircsh
```

Run one built-in command:

```sh
ircsh --command status
```

## Tests

```sh
python -m unittest discover -s tests -v
```

CI tests supported Python versions and verifies that arbitrary commands are rejected. See [M2 integrated qualification](docs/M2_18_QUALIFICATION.md).

## Configuration

Configuration is loaded from:

```text
/etc/ircsh/config.toml
~/.ircsh/config.toml
```

Example:

```toml
[account]
name = "alice"
capabilities = [
  "status.read",
  "quota.read",
  "services.read",
  "bots.read",
  "bouncers.read",
  "clients.read",
]
```

Management capabilities such as `bots.manage`, `bouncers.manage` and `clients.manage` must be granted explicitly.

See [examples/config.toml](examples/config.toml).

## Roadmap

- **M0:** restricted-shell foundation
- **M1:** account/configuration and capabilities
- **M2:** service abstraction, bouncers, bots and persistent clients
- **M3:** persistent terminal integration and controlled service configuration
- **M4:** runtime isolation, quotas and audit logging
- **M5:** SSH deployment and hardening
- **M6:** administration and provisioning

See [ROADMAP.md](ROADMAP.md) for details.

## License

Software in this repository is licensed under the [MIT License](LICENSE).

Copyright © 2026 Ploos AS.
