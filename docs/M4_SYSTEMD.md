# M4.2 systemd user runtime

SystemdUserRuntime is a narrow adapter for pre-provisioned systemd user units. It accepts only soju.service, znc.service and validated ircsh-*.service targets. Lifecycle operations are fixed to is-active, start, stop and restart; no shell is used.

The M4 policy translates to fixed CPUQuota, MemoryMax, TasksMax, PrivateTmp, ProtectHome, NoNewPrivileges, PrivateDevices and RestrictNamespaces properties.

IRC accounts cannot create units, select executables, add systemd options or weaken policy. Applying unit/drop-in policy remains an administrative provisioning operation.
