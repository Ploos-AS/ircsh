# M5 qualification

M5 qualifies the restricted SSH deployment boundary for IRC-only accounts.

Integrated tests verify:

- the login shell is pinned to `/usr/bin/ircsh`;
- SSH forwarding and user environment features are disabled by default;
- PTY remains available for the restricted interactive shell;
- account/key paths and permissions are deterministic;
- uploaded public keys receive restrictive authorized_keys options;
- sshd validation uses a fixed argv and configuration path;
- a failed `sshd -t` result is represented as failure before any reload action;
- the documented reload action is fixed and separate from validation.

The test suite does not modify the host SSH daemon or require root. Live installation remains an administrator operation and must follow the M5 operational recovery procedure.

## CI result

Pending GitHub Actions.
