# M2.8 — Bot abstraction and Eggdrop

M2.8 establishes the first concrete BOT backend using Eggdrop.

Bots use the same ServiceId and lifecycle contract as bouncers, but are classified as `ServiceKind.BOT`. Multiple bot instances are supported. Each validated instance name maps deterministically to a dedicated runtime target:

`ircsh-eggdrop-<instance>.service`

For example, `trivia` and `guard` become separate runtime targets. ServiceId validation occurs before the unit name is created, preventing path or shell syntax from entering the runtime identifier.

No arbitrary executable, command, unit template, or shell string is accepted.

Future quota policy can therefore count BOT instances independently from BOUNCER and CLIENT instances.

## Qualification

```sh
python -m unittest discover -s tests -v
```

Tests cover BOT classification, deterministic units, multiple instances, unsafe-name rejection and lifecycle behavior.
