# M5.1 SSH deployment model

IRC-only accounts use `/usr/bin/ircsh` as their login shell. The executable path is pinned by policy; account configuration cannot select Bash, a command, or another executable.

Secure SSH defaults disable TCP forwarding, agent forwarding, X11 forwarding and user-controlled SSH environment injection. PTY remains enabled because the restricted interactive shell and persistent IRC-client sessions require a terminal.

Provisioned public keys should carry restrictive authorized_keys options generated from trusted account provisioning. The account name is validated and never becomes a command.

The host administrator must add `/usr/bin/ircsh` to `/etc/shells` only after installing the packaged executable at that exact path. Advanced/developer Unix-shell tiers are separate account policies and must not weaken IRC-only accounts.
