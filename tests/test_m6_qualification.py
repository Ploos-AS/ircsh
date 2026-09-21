import tempfile,unittest,json
from pathlib import Path
from ircsh.account_store import AccountStore,ManagedAccount
from ircsh.admin_cli import execute
from ircsh.host_inspector import HostAccount
class Inspector:
 def __init__(self,host=None):self.host=host
 def inspect(self,u):return self.host
class Audit:
 def __init__(self):self.events=[]
 def emit(self,e):self.events.append(e)
class M6Qualification(unittest.TestCase):
 def setUp(self):self.tmp=tempfile.TemporaryDirectory();self.store=AccountStore(Path(self.tmp.name)/"accounts.json")
 def tearDown(self):self.tmp.cleanup()
 def test_end_to_end_desired_state_dry_run_apply_audit_health(self):
  execute(["account","create","alice","--plan","irc-basic"],self.store)
  self.assertEqual("irc-basic",self.store.read()["alice"].plan)
  dry=execute(["account","reconcile","alice"],self.store,inspector=Inspector())
  self.assertTrue(dry.startswith("DRY-RUN"));self.assertIn("useradd",dry)
  calls=[];audit=Audit()
  out=execute(["account","reconcile","alice","--apply"],self.store,runner=lambda argv,**kw:calls.append((argv,kw)),audit=audit,inspector=Inspector())
  self.assertTrue(out.startswith("APPLIED"));self.assertEqual("useradd",calls[0][0][0]);self.assertEqual("allowed",audit.events[-1].result)
  host=HostAccount("alice",1001,1001,"ircsh","/home/alice","/usr/bin/ircsh",False)
  health=json.loads(execute(["health","--json"],self.store,inspector=Inspector(host)))
  self.assertTrue(health["ok"]);self.assertEqual(0,health["drifted"])
  metrics=execute(["health","--prometheus"],self.store,inspector=Inspector(host))
  self.assertIn("ircsh_health_ok 1",metrics)
 def test_unknown_plan_and_unknown_account_fail_closed(self):
  with self.assertRaises(ValueError):execute(["account","create","alice","--plan","root"],self.store)
  with self.assertRaises(KeyError):execute(["account","reconcile","alice"],self.store,inspector=Inspector())
 def test_drift_is_reported_without_mutation(self):
  execute(["account","create","alice"],self.store)
  host=HostAccount("alice",1001,1001,"users","/home/alice","/bin/bash",False)
  calls=[]
  dry=execute(["account","reconcile","alice"],self.store,runner=lambda *x:calls.append(x),inspector=Inspector(host))
  self.assertIn("usermod",dry);self.assertEqual([],calls)
  health=json.loads(execute(["health","--json"],self.store,inspector=Inspector(host)))
  self.assertFalse(health["ok"]);self.assertEqual(1,health["drifted"])
if __name__=="__main__":unittest.main()
