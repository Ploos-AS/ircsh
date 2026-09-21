# M4.5 trusted quota measurement

`QuotaMeter` measures disk usage below a fixed absolute account root and counts active services through the trusted runtime interface. The resulting `QuotaUsage` can be passed to `QuotaEnforcer`.

Disk usage is rounded up to MiB. Files that disappear during traversal are tolerated; measurement failures otherwise fail closed.

Service targets are supplied by trusted provisioning code, not by the IRC account. Connection measurement remains zero until M4 adds a dedicated trusted network/accounting backend; it is not inferred from account input.
