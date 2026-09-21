# M2.2 — soju adapter

M2.2 adds the first concrete bouncer adapter.

The adapter does not invoke subprocesses and never builds shell command strings. It receives a narrow runtime object and is restricted to the fixed `soju.service` unit. This keeps process supervision separate from command parsing and account policy.

The default runtime remains read-only. Production systemd/container integration is intentionally deferred until its authorization and isolation boundary is qualified.

## Qualification

```sh
python -m unittest discover -s tests -v
```

Tests verify state mapping, lifecycle calls through the runtime interface, the fixed unit boundary, and restart behavior.
