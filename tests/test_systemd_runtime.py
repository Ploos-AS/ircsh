import subprocess,unittest
from ircsh.runtime import RuntimeState
from ircsh.systemd_runtime import SystemdUserRuntime
class Runner:
    def __init__(self,rc=0,out="active\n"):self.calls=[];self.rc=rc;self.out=out
    def __call__(self,args,**kwargs):self.calls.append((args,kwargs));return subprocess.CompletedProcess(args,self.rc,self.out,"")
class SystemdRuntimeTests(unittest.TestCase):
    def test_state_and_fixed_argv(self):
        r=Runner();x=SystemdUserRuntime(runner=r);self.assertEqual(RuntimeState.ACTIVE,x.state("ircsh-weechat.service"));self.assertNotIn("shell",r.calls[0][1])
    def test_mutations_are_narrow(self):
        r=Runner();x=SystemdUserRuntime(runner=r);x.start("soju.service");x.stop("znc.service");x.restart("ircsh-eggdrop.service");self.assertEqual(["start","stop","restart"],[c[0][2] for c in r.calls])
    def test_rejects_arbitrary_units(self):
        x=SystemdUserRuntime(runner=Runner())
        for unit in ("ssh.service","../x.service","ircsh-x;id.service","x"):
            with self.subTest(unit=unit),self.assertRaises(ValueError):x.state(unit)
    def test_policy_properties(self):
        p=SystemdUserRuntime(runner=Runner()).unit_properties();self.assertIn("CPUQuota=25%",p);self.assertIn("MemoryMax=256M",p);self.assertIn("TasksMax=64",p);self.assertIn("NoNewPrivileges=yes",p)
if __name__=="__main__":unittest.main()
