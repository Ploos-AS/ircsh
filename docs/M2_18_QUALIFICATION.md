# M2.18 — M2 integrated qualification

M2 now covers a backend-neutral, multi-instance service model across three service kinds.

- Bouncers: soju, ZNC, psyBNC, muh, BIP, pounce
- Bots: Eggdrop, Limnoria, Sopel, Errbot, EnergyMech, Psotnic
- Clients: WeeChat, Irssi, BitchX

The integrated qualification verifies the complete default backend matrix and, critically, that default accounts remain read-only. Management capabilities are known capabilities but are never granted merely because a backend was added.

During M2.18 source cleanup, literal escaped newline artifacts in the default service registry were repaired.

Run:

```sh
python -m unittest discover -s tests -v
```

CI executes the suite on Python 3.11, 3.12 and 3.13. A green CI run is required before marking M2 PASS.
