# M2.9 — Bot commands

The restricted shell now exposes bot operations through explicit parsing:

- `bot list`
- `bot status <name>`
- `bot start <name>`
- `bot stop <name>`
- `bot restart <name>`

Read operations require `bots.read`. Lifecycle operations require `bots.manage`.

Commands resolve an exact BOT instance from the service registry. There is no shell fallback. Runtime mutation still fails closed when the configured backend/runtime does not authorize it.

## Qualification

```sh
python -m unittest discover -s tests -v
```

Tests cover read and management capabilities, missing bots, fail-closed mutation and shell-like input.
