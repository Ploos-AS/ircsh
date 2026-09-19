# Threat model

## Security objective

An IRC shell account must not become a general operating-system shell merely because a user can supply arbitrary terminal input.

## Initial threats

### Command injection
User input must not be concatenated into shell command strings. M0 uses an explicit exact-match built-in registry and contains no subprocess execution.

### Escape to a general shell
Unknown commands are rejected. There is no fallback command interpreter.

### Path traversal
Future file operations must resolve paths inside explicit account roots and reject traversal and symlink escapes.

### Service abuse
Future service lifecycle operations require per-account capability and ownership checks.

### Resource exhaustion
Future runtime milestones must enforce quotas for processes, memory, CPU, disk, connections, and service counts.

### SSH feature bypass
Production deployment must explicitly consider port forwarding, agent forwarding, X11 forwarding, environment variables, PTY allocation, subsystem requests, command arguments, and file-transfer mechanisms. Setting a login shell alone is not sufficient isolation.

### Privilege escalation
ircsh should run unprivileged. Any privileged helper must be minimal and accept structured validated requests rather than shell commands.

## M0 security invariant

For every input line, M0 either executes one known in-process built-in, exits, or returns an error. It does not ask the operating system to interpret the input.
