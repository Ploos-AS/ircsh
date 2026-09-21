# M2.4 — psyBNC adapter

psyBNC is supported as a legacy bouncer backend, but ircsh treats it more conservatively than modern backends.

The adapter is pinned to a dedicated `ircsh-psybnc.service` runtime target. User-controlled unit names are forbidden. No shell commands are constructed and no executable path is accepted from an ircsh account.

## Isolation requirements for production runtime

The production unit/container MUST run as an unprivileged identity with a private writable data directory. It SHOULD use filesystem protection, private temporary storage, restricted devices, a minimal capability set, resource limits, and an explicit network policy appropriate for IRC connections.

The shell-facing adapter does not weaken these requirements: it can request lifecycle operations only against the pre-authorized runtime target.

Actual host runtime wiring remains deferred until the runtime authorization/isolation milestone.

## Qualification

```sh
python -m unittest discover -s tests -v
```

Qualification includes lifecycle behavior and rejection of arbitrary unit selection.
