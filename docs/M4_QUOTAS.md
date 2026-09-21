# M4.4 disk, connection and service quotas

M4 separates quota measurement from quota admission. `QuotaUsage` is a typed snapshot supplied by a trusted measurement backend; account input cannot claim its own usage.

`QuotaEnforcer` fails closed when current usage is already above a limit and provides admission checks for starting another service, opening another connection, or growing disk usage.

Default limits come from `ResourceLimits`. This layer does not pretend that application checks alone enforce filesystem or network quotas: later runtime adapters must provide trusted usage measurement and OS-level enforcement where available.
