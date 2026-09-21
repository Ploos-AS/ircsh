import logging,tempfile,unittest
from pathlib import Path
from ircsh.audit import AuditLogger
from ircsh.isolation import DEFAULT_POLICY
from ircsh.quota_runtime import QuotaRuntime
from ircsh.quotas import QuotaEnforcer,QuotaExceeded,QuotaUsage
from ircsh.runtime import RuntimeState
from ircsh.systemd_provision import SystemdDropInProvisioner
from ircsh.systemd_runtime import SystemdUserRuntime

class FakeSystemd:
    def __init__(self):self.calls=[]
    def __call__(self,args,**kwargs):
        import subprocess
        self.calls.append(args)
        if args[2]=="is-active":return subprocess.CompletedProcess(args,3,"inactive\n","")
        return subprocess.CompletedProcess(args,0,"","")
class Meter:
    def __init__(self,u):self.u=u
    def read(self):return self.u
class Audit:
    def __init__(self):self.events=[]
    def emit(self,e):self.events.append(e)

class M4Qualification(unittest.TestCase):
    def test_policy_materializes_without_account_controlled_directives(self):
        with tempfile.TemporaryDirectory() as d:
            p=SystemdDropInProvisioner(Path(d))
            text=p.render("ircsh-weechat.service")
            self.assertIn("NoNewPrivileges=yes",text);self.assertIn("MemoryMax=256M",text)
            self.assertNotIn("ExecStart",text);self.assertNotIn("Environment",text)
            with self.assertRaises(ValueError):p.render("../escape.service")
    def test_quota_denial_precedes_systemd_mutation_and_is_audited(self):
        runner=FakeSystemd();base=SystemdUserRuntime(runner=runner);audit=Audit()
        rt=QuotaRuntime(base,Meter(QuotaUsage(1024,32,4)),QuotaEnforcer(DEFAULT_POLICY.limits),audit)
        with self.assertRaises(QuotaExceeded):rt.start("ircsh-weechat.service")
        self.assertEqual(["systemctl","--user","is-active","ircsh-weechat.service"],runner.calls[0])
        self.assertEqual(1,len(runner.calls));self.assertEqual("denied",audit.events[0].result)
    def test_allowed_start_uses_fixed_systemctl_argv(self):
        runner=FakeSystemd();audit=Audit()
        rt=QuotaRuntime(SystemdUserRuntime(runner=runner),Meter(QuotaUsage(1,1,1)),QuotaEnforcer(DEFAULT_POLICY.limits),audit)
        rt.start("ircsh-weechat.service")
        self.assertEqual(["systemctl","--user","start","ircsh-weechat.service"],runner.calls[-1])
        self.assertEqual("allowed",audit.events[-1].result)
if __name__=="__main__":unittest.main()
