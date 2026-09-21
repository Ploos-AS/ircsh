import unittest
from ircsh.sshd_config import render_match_group
from ircsh.ssh_policy import SshPolicy
class SshdConfigTests(unittest.TestCase):
 def test_secure_group_fragment(self):
  s=render_match_group()
  self.assertEqual("""Match Group ircsh
    AllowTcpForwarding no
    AllowAgentForwarding no
    X11Forwarding no
    PermitTTY yes
    PermitUserEnvironment no
""",s)
 def test_group_injection_rejected(self):
  for g in ("ircsh users","../ircsh","ircsh\nForceCommand /bin/sh",""):
   with self.assertRaises(ValueError):render_match_group(g)
 def test_explicit_policy_is_rendered(self):
  s=render_match_group("ircsh",SshPolicy(permit_tty=False))
  self.assertIn("PermitTTY no",s)
if __name__=="__main__":unittest.main()
