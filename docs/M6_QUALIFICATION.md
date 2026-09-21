# M6 integrated qualification

M6 qualification covers the trusted administrative chain:

1. validated account plan and persistent desired-state store;
2. trusted Unix host inspection;
3. dry-run-by-default drift reconciliation;
4. explicit apply through an injected privileged runner;
5. structured audit event on mutation;
6. aggregate health and Prometheus output;
7. fail-closed behavior for unknown plans/accounts.

## PASS criteria

M6 is PASS only when the repository CI runs the complete test suite successfully on every supported Python version. A committed qualification test is not itself a PASS.

No network listener is introduced by M6.
