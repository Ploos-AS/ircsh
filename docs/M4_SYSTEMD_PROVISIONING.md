# M4.3 systemd policy provisioning

The drop-in provisioner materializes the trusted M4 isolation policy as a deterministic systemd user-unit drop-in named `50-ircsh-isolation.conf`.

Only units accepted by the narrow systemd runtime can be provisioned. Output is generated entirely from typed policy; accounts cannot inject directives, paths, commands, executables or arbitrary units.

Writes are atomic. Drop-in directories are mode 0700 and generated files mode 0600. Applying daemon-reload/restart remains a separate privileged or administrative deployment step.
