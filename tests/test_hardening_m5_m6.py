import unittest
from ircsh.admin_model import AccountPlan
from ircsh.isolation import ResourceLimits
from ircsh.ssh_policy import authorized_key_options
from ircsh.sshd_config import render_match_group
class HardeningTests(unittest.TestCase):
 def test_plan_rejects_unknown_capability(self):
  with self.assertRaises(ValueError):AccountPlan("bad",frozenset({"root.shell"}),ResourceLimits())
 def test_key_policy_disables_user_rc(self):self.assertIn("no-user-rc",authorized_key_options("alice").split(","))
 def test_sshd_policy_disables_user_rc(self):self.assertIn("PermitUserRC no",render_match_group())
if __name__=="__main__":unittest.main()
