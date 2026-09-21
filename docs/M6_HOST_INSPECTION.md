# M6.6 trusted host account inspection

`HostInspector` reads the local Unix account database through Python's `pwd` and `grp` interfaces. It returns the actual UID, GID, primary group, home directory and login shell for a validated username, or `None` when the account does not exist.

Malformed host records and missing primary groups fail closed. The inspector performs no shell execution and accepts no arbitrary lookup expression.

This removes the need for user-supplied host-state assumptions in the next reconciliation integration: the administrator CLI can derive existence and detect drift from trusted local account state.
