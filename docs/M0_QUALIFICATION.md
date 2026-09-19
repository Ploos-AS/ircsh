# M0 qualification

Status: **FOUNDATION IMPLEMENTED — CI qualification required**

M0 qualifies the repository foundation and minimal command parser. It does not qualify ircsh as a production login shell.

## Required checks

```sh
python -m unittest discover -s tests -v
python -m ircsh --command version
python -m ircsh --command status
python -m ircsh --command services
python -m ircsh --command 'echo SHOULD_NOT_RUN'
```

The final command must report an unknown command, exit 2, and execute nothing externally.

M0 can be marked PASS after the workflow succeeds on `main`.
