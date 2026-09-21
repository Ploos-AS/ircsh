# M5.2 sshd server policy

IRC-only accounts should belong to a dedicated Unix group, normally `ircsh`. `render_match_group()` creates a deterministic `sshd_config` Match Group fragment from the trusted SSH policy.

Default fragment:

    Match Group ircsh
        AllowTcpForwarding no
        AllowAgentForwarding no
        X11Forwarding no
        PermitTTY yes
        PermitUserEnvironment no

The group identifier is strictly validated and cannot inject additional sshd directives. PTY is intentionally enabled for the restricted interactive shell.

Deployment should install the fragment under the distribution's sshd include directory, validate the complete configuration with `sshd -t`, and only then reload sshd. Installation/reload remains an administrator operation; ircsh never edits the live SSH daemon configuration from an account session.

The login-shell restriction remains separate: IRC-only accounts must use the pinned `/usr/bin/ircsh` shell from M5.1.
