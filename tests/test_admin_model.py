import unittest
from ircsh.admin_model import *
class AdminModelTests(unittest.TestCase):
 def test_basic_is_read_only(self):
  p=get_plan("irc-basic")
  self.assertIn("bouncers.read",p.capabilities);self.assertNotIn("bouncers.manage",p.capabilities)
  self.assertEqual(2,p.limits.services)
 def test_advanced_has_controlled_management(self):
  p=get_plan("irc-advanced")
  self.assertIn("sessions.manage",p.capabilities);self.assertIn("config.manage",p.capabilities)
  self.assertEqual(8,p.limits.services)
 def test_unknown_plan_fails_closed(self):
  for name in ("developer","../root",""):
   with self.assertRaises(ValueError):get_plan(name)
if __name__=="__main__":unittest.main()
