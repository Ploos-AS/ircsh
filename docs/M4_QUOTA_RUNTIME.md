# M4.7 quota-aware runtime

`QuotaRuntime` decorates the trusted runtime boundary. Before starting a stopped service it obtains fresh trusted usage from `QuotaMeter` and applies `QuotaEnforcer.allow_service_start`.

Starting an already-active unit is idempotent and does not consume another service slot. Restart requires an active service and current usage within quota. Stop is deliberately always permitted so an over-quota account can reduce resource use.

Measurement or enforcement failure prevents start/restart before the underlying runtime is mutated.
