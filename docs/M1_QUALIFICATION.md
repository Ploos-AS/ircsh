# M1 qualification

Status: **IMPLEMENTED — CI qualification required**

M1 adds validated system/user configuration, an account identity model, explicit read-only capabilities, and read-only provider abstractions.

## Security properties

- configuration has a closed schema
- unknown capabilities are rejected
- M1 capabilities are read-only
- no service mutation API exists
- no subprocess or shell execution is introduced
- commands require their declared capability

## Required checks

```sh
python -m unittest discover -s tests -v
ircsh --command account
ircsh --command capabilities
ircsh --command status
```

The existing M0 arbitrary-command rejection test remains mandatory.

M1 can be marked PASS after CI succeeds on `main`.
