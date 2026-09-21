import unittest
from ircsh.providers import production_registry
from ircsh.runtime import ReadOnlyRuntime
from ircsh.services import ServiceKind
class WiringTests(unittest.TestCase):
 def test_all_expected_services_are_concrete(self):
  r=production_registry(ReadOnlyRuntime())
  self.assertEqual(6,len(r.statuses(ServiceKind.BOUNCER)))
  self.assertEqual(6,len(r.statuses(ServiceKind.BOT)))
  self.assertEqual(3,len(r.statuses(ServiceKind.CLIENT)))
 def test_runtime_is_shared_by_backends(self):
  rt=ReadOnlyRuntime();r=production_registry(rt)
  self.assertIs(rt,r.get("main",ServiceKind.BOUNCER).runtime)
  self.assertIs(rt,r.get("eggdrop1",ServiceKind.BOT).runtime)
  self.assertIs(rt,r.get("weechat",ServiceKind.CLIENT).runtime)
if __name__=="__main__":unittest.main()
