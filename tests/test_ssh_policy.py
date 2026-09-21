import unittest
from ircsh.ssh_policy import *
class SshPolicyTests(unittest.TestCase):
 def test_secure_defaults(self):
  p=DEFAULT_SSH_POLICY
  self.assertFalse(p.allow_tcp_forwarding);self.assertFalse(p.allow_agent_forwarding)
  self.assertFalse(p.allow_x11_forwarding);self.assertFalse(p.permit_user_environment);self.assertTrue(p.permit_tty)
 def test_shell_is_pinned(self):
  self.assertEqual("/usr/bin/ircsh",shell_entry())
  with self.assertRaises(ValueError):shell_entry("/bin/bash")
 def test_key_options_restrict_forwarding(self):
  o=authorized_key_options("alice")
  self.assertIn("restrict",o);self.assertIn("no-port-forwarding",o);self.assertIn("no-agent-forwarding",o)
 def test_account_validation(self):
  with self.assertRaises(ValueError):authorized_key_options("../root")
if __name__=="__main__":unittest.main()
