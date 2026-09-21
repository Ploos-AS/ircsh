# M3.10 integrated qualification

M3 qualifies persistent IRC-client sessions, controlled configuration and
read-only observability as one restricted-shell security boundary.

## Required properties

- Session targets are deterministic and validated.
- Only fixed IRC client programs can be started.
- No account-controlled executable, shell command, tmux subcommand or option.
- Session management requires explicit capabilities and fails closed.
- Service configuration is restricted to typed allowlisted keys and services.
- Configuration writes are atomic and private.
- Logs are read-only, map services to fixed journal units, and are bounded to
  200 lines per request.
- Arbitrary service names, paths, commands, units and injection payloads are
  rejected.
- The complete unit suite runs on Python 3.11, 3.12 and 3.13.

## Qualification

Run:

    python -m unittest discover -s tests -v

CI additionally smoke-tests the installed CLI and verifies that arbitrary OS
commands remain rejected.

**Result: pending CI.**
