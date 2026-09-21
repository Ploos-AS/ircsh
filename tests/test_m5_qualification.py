import base64,unittest
from types import SimpleNamespace
from ircsh.ssh_policy import DEFAULT_SSH_POLICY,authorized_key_options,shell_entry
from ircsh.sshd_config import render_match_group
from ircsh.provisioning import AccountProvisioning
from ircsh.ssh_deploy import DeploymentPlan,SshdValidator
class M5Qualification(unittest.TestCase):
 def test_restricted_account_policy_is_consistent(self):
  self.assertEqual("/usr/bin/ircsh",shell_entry())
  fragment=render_match_group("ircsh")
  for directive in ("AllowTcpForwarding no","AllowAgentForwarding no","X11Forwarding no","PermitUserEnvironment no","PermitTTY yes"):
   self.assertIn(directive,fragment)
  opts=authorized_key_options("alice")
  self.assertIn("restrict",opts);self.assertIn("no-port-forwarding",opts)
 def test_key_to_account_path_is_fixed_and_restricted(self):
  p=AccountProvisioning("alice")
  key="ssh-ed25519 "+base64.b64encode(b"qualification-key").decode()
  line=p.key_line(key)
  self.assertEqual("/home/alice/.ssh/authorized_keys",p.authorized_keys)
  self.assertEqual(0o600,p.modes()[p.authorized_keys])
  self.assertTrue(line.startswith("no-agent-forwarding,no-port-forwarding,no-X11-forwarding,restrict "))
 def test_deployment_must_validate_before_reload(self):
  calls=[]
  def run(argv,**kw):calls.append(argv);return SimpleNamespace(returncode=0)
  self.assertTrue(SshdValidator(run).validate().valid)
  self.assertEqual([["sshd","-t","-f","/etc/ssh/sshd_config"]],calls)
  self.assertEqual(("systemctl","reload","sshd"),DeploymentPlan().reload_argv())
 def test_invalid_validation_blocks_deployment(self):
  self.assertFalse(SshdValidator(lambda *a,**k:SimpleNamespace(returncode=255)).validate().valid)
if __name__=="__main__":unittest.main()
