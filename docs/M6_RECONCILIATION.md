# M6.3 privileged account reconciliation

`AccountReconciler` converts a validated managed-account record into a deterministic argv plan for the privileged host layer.

Enabled missing accounts are created with a fixed home, `ircsh` primary group and `/usr/bin/ircsh` login shell. Existing enabled accounts are normalized to the same group/shell boundary. Disabled existing accounts are locked and moved to `/usr/sbin/nologin`; disabled missing accounts are not created.

The reconciler only returns argv tuples. It never invokes a shell or executes privileged commands itself. A later administrator/service layer must execute approved actions, verify results, provision SSH keys and record audit events.

The `--` separator is used before the validated username so account data cannot be interpreted as an option.
