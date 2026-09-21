# M2.10 — Bouncer commands

ircsh exposes explicit bouncer commands: `bouncer list`, `bouncer status <name>`, and capability-gated `start`, `stop`, and `restart`.

Read access requires `bouncers.read`; lifecycle operations require `bouncers.manage`. Resolution is restricted to ServiceKind.BOUNCER, so bot/client instances cannot be targeted through this command family. There is no shell fallback.

The command model applies uniformly to soju, ZNC, psyBNC, muh, BIP and pounce instances registered for the account.

## Qualification

```sh
python -m unittest discover -s tests -v
```
