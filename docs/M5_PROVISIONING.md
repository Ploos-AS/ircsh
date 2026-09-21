# M5.3 account and SSH-key provisioning

`AccountProvisioning` describes the trusted IRC-only account layout without executing privileged host commands.

For account `alice` the fixed model is:

- group: `ircsh`
- home: `/home/alice`
- login shell: `/usr/bin/ircsh`
- SSH directory: `/home/alice/.ssh`, mode 0700
- authorized keys: `/home/alice/.ssh/authorized_keys`, mode 0600
- home mode: 0700

Provisioned keys are restricted with the M5.1 authorized-key policy. Only Ed25519 and FIDO2/security-key Ed25519 public keys are accepted by this provisioning layer. Embedded newline, NUL and malformed base64 data are rejected, preventing an uploaded key from injecting an additional authorized_keys entry or option line.

The provisioning object produces data and paths only. Creation of Unix users/groups, ownership changes and file installation are privileged administrator/package operations and must not be exposed to an ircsh account.
