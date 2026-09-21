# M4 isolation model

M4 separates **policy** from **runtime execution**.

`ResourceLimits` defines bounded CPU, memory, process, disk, connection and service-count limits. `IsolationPolicy` defines secure isolation switches.

The policy deliberately cannot contain an executable, command, systemd unit, filesystem path, container image, namespace name, environment variable or runtime option. Those mappings belong to trusted runtime adapters.

Default policy: CPU 25%, memory 256 MiB, processes 64, disk 1024 MiB, connections 32, services 4. Private temporary storage, home protection, no-new-privileges, private devices and namespace restrictions are enabled.

M4 runtime adapters must fail closed when a requested policy cannot be enforced.
