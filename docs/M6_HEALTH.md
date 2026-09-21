# M6.8 administrative health

`HealthProvider` exposes a small machine-readable administrative snapshot: total, enabled and disabled managed accounts, plus missing accounts and accounts whose host state requires reconciliation.

`ok=true` only when no managed account has detected drift and no enabled account is missing. The JSON representation contains counts only; it intentionally avoids usernames, SSH keys, paths and other account-specific data so it is suitable for monitoring integration.

This is an in-process provider, not a network listener. A future metrics/export layer may expose it through a separately authenticated local service.
