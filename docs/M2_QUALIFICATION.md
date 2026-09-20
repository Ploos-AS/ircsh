# M2 qualification

Status: **IMPLEMENTED — CI qualification required**

M2 introduces the backend-neutral service API and registry. Soju and ZNC have explicit adapter slots; other M0 services remain placeholders.

## Security boundary

The M2 foundation deliberately fails closed for lifecycle mutation. A backend can expose typed status, but `start`, `stop`, and `restart` raise `MutationDisabled` until a controlled runtime implementation and policy checks are wired in.

Service lookup is exact registry lookup. User input is never interpreted as a path, executable, unit name, or shell command.

## Required checks

```sh
python -m unittest discover -s tests -v
ircsh --command services
ircsh --command 'services; id'
```

The second command must be rejected as an unknown command and execute nothing externally.

M2 can be marked PASS after CI succeeds on `main`.
