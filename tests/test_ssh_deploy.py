import unittest
from types import SimpleNamespace
from ircsh.ssh_deploy import *
class DeployTests(unittest.TestCase):
 def test_validator_exact_argv(self):
  calls=[]
  def run(argv,**kw):calls.append((argv,kw));return SimpleNamespace(returncode=0)
  self.assertTrue(SshdValidator(run).validate().valid)
  self.assertEqual(["sshd","-t","-f","/etc/ssh/sshd_config"],calls[0][0])
  self.assertNotIn("shell",calls[0][1])
 def test_validation_failure_is_closed(self):
  self.assertFalse(SshdValidator(lambda *a,**k:SimpleNamespace(returncode=1)).validate().valid)
  self.assertFalse(SshdValidator(lambda *a,**k:(_ for _ in ()).throw(OSError())).validate().valid)
 def test_paths_and_actions_are_pinned(self):
  p=DeploymentPlan()
  self.assertEqual(("systemctl","reload","sshd"),p.reload_argv())
  with self.assertRaises(ValueError):DeploymentPlan(fragment="/tmp/x")
if __name__=="__main__":unittest.main()
