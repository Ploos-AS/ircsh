# M2.3 — ZNC adapter

M2.3 adds ZNC as the second concrete bouncer adapter.

Like the soju adapter, ZNC uses the narrow runtime interface and does not invoke a shell or construct commands from user input. The adapter is restricted to the fixed `znc.service` runtime unit.

This gives soju and ZNC the same lifecycle contract while keeping their implementation details outside the shell parser.

## Qualification

```sh
python -m unittest discover -s tests -v
```

Tests cover state mapping, start/stop/restart through the controlled runtime, and rejection of arbitrary runtime unit names.
