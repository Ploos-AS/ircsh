import tempfile,unittest
from pathlib import Path
from ircsh.account_store import AccountStore
from ircsh.admin_cli import execute
class Sink:
 def __init__(self):self.events=[]
 def emit(self,e):self.events.append(e)
class Inspector:
 def inspect(self,username):return None
class AdminReconcileTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.store=AccountStore(Path(self.tmp.name)/"a.json");execute(["account","create","alice"],self.store)
 def tearDown(self):self.tmp.cleanup()
 def test_dry_run_is_default_and_executes_nothing(self):
  calls=[];out=execute(["account","reconcile","alice"],self.store,lambda *a,**k:calls.append(a),inspector=Inspector())
  self.assertTrue(out.startswith("DRY-RUN"));self.assertEqual([],calls);self.assertIn("useradd",out)
 def test_apply_requires_explicit_runner_and_audits(self):
  with self.assertRaises(RuntimeError):execute(["account","reconcile","alice","--apply"],self.store,inspector=Inspector())
  calls=[];sink=Sink();out=execute(["account","reconcile","alice","--apply"],self.store,lambda argv,**kw:calls.append((argv,kw)),sink,Inspector())
  self.assertTrue(out.startswith("APPLIED"));self.assertEqual("useradd",calls[0][0][0]);self.assertTrue(calls[0][1]["check"]);self.assertEqual("allowed",sink.events[-1].result)
 def test_failure_is_audited_and_stops(self):
  sink=Sink()
  def fail(*a,**k):raise OSError()
  with self.assertRaises(RuntimeError):execute(["account","reconcile","alice","--apply"],self.store,fail,sink,Inspector())
  self.assertEqual("failed",sink.events[-1].result)
if __name__=="__main__":unittest.main()
