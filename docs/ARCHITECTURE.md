# Architecture

ircsh is a restricted login environment for IRC-oriented shell accounts. It presents IRC-specific commands while keeping operating-system execution behind explicit, policy-checked interfaces.

## M0 boundary

```text
SSH / terminal
      |
      v
+-------------+
|    ircsh    |
| parser      |
| built-ins   |
+-------------+
      |
      +--> static status/service placeholders
```

There is no subprocess launcher, shell expansion, container API, systemd integration, IRC protocol client, or privileged helper in M0.

## Principles

1. No fallback to a general-purpose shell.
2. Commands are explicit capabilities, not executable names.
3. User-controlled strings must never become shell command lines.
4. Privilege belongs outside the interactive parser.
5. Backends expose narrow typed operations.
6. Policy checks happen before runtime operations.
7. Runtime implementations are replaceable.
8. Read-only introspection is introduced before mutation.

A mature ircsh may be registered as a Unix login shell and used through SSH. Doing so is not an M0 deployment recommendation; SSH policy and backend isolation must first be qualified.
