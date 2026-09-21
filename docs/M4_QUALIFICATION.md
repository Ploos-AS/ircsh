# M4.9 integrated qualification

M4 qualification covers the complete security path:

1. typed isolation/resource policy;
2. deterministic systemd drop-in generation;
3. narrow systemd user runtime;
4. trusted disk/service/connection measurement;
5. fail-closed quota admission;
6. quota-aware runtime mutation;
7. structured security audit events.

The integrated tests verify that policy output cannot inject execution/environment directives, quota denial happens before runtime mutation, denial is audited, and an allowed service start reaches systemd only through fixed argv.

CI result: pending GitHub Actions.
