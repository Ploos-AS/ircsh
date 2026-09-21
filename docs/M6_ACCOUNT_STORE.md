# M6.2 persistent account registry

`AccountStore` is the administrator-owned source of truth mapping Unix account names to trusted ircsh plans and enabled/disabled state.

The production default is `/var/lib/ircsh/accounts.json`. Writes are deterministic and atomic (temporary file, fsync, mode 0600, replace); the containing directory is mode 0700. The on-disk schema is closed: unexpected fields, malformed JSON, invalid usernames and unknown plans fail closed.

Disabling an account preserves its plan but changes its administrative state to disabled. This registry does not itself execute `useradd`, alter passwords, or kill sessions; privileged host reconciliation is a separate step.

Account sessions must never be permitted to write this store.
