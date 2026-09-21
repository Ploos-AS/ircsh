# M6.5 explicit reconciliation

`ircsh-admin account reconcile USER` is dry-run by default. It prints the deterministic privileged argv plan but executes nothing.

Execution requires the explicit `--apply` flag **and** an injected privileged runner. The normal library path therefore cannot accidentally elevate itself. Each completed reconciliation is audited as `account_reconcile`; execution failure is audited and aborts immediately.

`--exists` represents host-state discovery supplied by the privileged administration layer. Future host integration should replace this explicit input with a trusted account inspector rather than parsing user-controlled data.
