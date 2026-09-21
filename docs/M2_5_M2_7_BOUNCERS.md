# M2.5–M2.7 — Additional bouncers

ircsh now models three additional bouncer backends:

- M2.5: muh (legacy)
- M2.6: BIP
- M2.7: pounce

Each adapter uses the same narrow runtime contract as soju, ZNC and psyBNC. Runtime targets are fixed to `ircsh-muh.service`, `ircsh-bip.service`, and `ircsh-pounce.service`. Account-controlled unit names, executable paths and shell command construction are forbidden.

muh is treated as a legacy service and should receive isolation comparable to psyBNC. BIP and pounce are also kept behind dedicated runtime targets so the shell-facing policy remains independent of process supervision.

## Qualification

```sh
python -m unittest discover -s tests -v
```

The tests verify fixed targets, lifecycle behavior and rejection of arbitrary runtime units.
