# M5.4 SSH operational hardening and recovery

SSH policy deployment is transactional and fail-closed.

1. Keep an existing privileged console/session open.
2. Render the trusted ircsh Match Group fragment.
3. Preserve the previous `60-ircsh.conf` as `60-ircsh.conf.previous`.
4. Install the candidate as `/etc/ssh/sshd_config.d/60-ircsh.conf`.
5. Run exactly `sshd -t -f /etc/ssh/sshd_config`.
6. If validation fails, restore the previous fragment and do **not** reload sshd.
7. If validation succeeds, reload (not restart) sshd with `systemctl reload sshd`.
8. Open a second connection and verify an IRC-only test account before closing the recovery session.

Recovery uses console/out-of-band access or the deliberately retained privileged session. Restore the previous fragment, validate the complete configuration again, and only reload after validation succeeds.

The library exposes only pinned validation/reload plans. It does not run the privileged installation or reload from an ircsh account. Validation errors fail closed and do not expose sshd stderr to the restricted account.
