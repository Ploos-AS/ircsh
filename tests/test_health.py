import tempfile,unittest
from pathlib import Path
from ircsh.account_store import AccountStore,ManagedAccount
from ircsh.host_inspector import HostAccount
from ircsh.health import HealthProvider
class Inspector:
 def __init__(self,items):self.items=items
 def inspect(self,u):return self.items.get(u)
class HealthTests(unittest.TestCase):
 def test_healthy(self):
  with tempfile.TemporaryDirectory() as d:
   s=AccountStore(Path(d)/"a.json");s.put(ManagedAccount("alice","irc-basic"))
   h=HostAccount("alice",1001,1001,"ircsh","/home/alice","/usr/bin/ircsh",False)
   x=HealthProvider(s,Inspector({"alice":h})).read();self.assertTrue(x.ok);self.assertEqual(0,x.drifted)
 def test_missing_enabled_is_unhealthy(self):
  with tempfile.TemporaryDirectory() as d:
   s=AccountStore(Path(d)/"a.json");s.put(ManagedAccount("alice","irc-basic"))
   x=HealthProvider(s,Inspector({})).read();self.assertFalse(x.ok);self.assertEqual(1,x.missing);self.assertEqual(1,x.drifted)
 def test_disabled_unlocked_is_drift(self):
  with tempfile.TemporaryDirectory() as d:
   s=AccountStore(Path(d)/"a.json");s.put(ManagedAccount("alice","irc-basic",False))
   h=HostAccount("alice",1001,1001,"ircsh","/home/alice","/usr/sbin/nologin",False)
   x=HealthProvider(s,Inspector({"alice":h})).read();self.assertFalse(x.ok);self.assertEqual(1,x.drifted)
 def test_disabled_locked_nologin_is_healthy(self):
  with tempfile.TemporaryDirectory() as d:
   s=AccountStore(Path(d)/"a.json");s.put(ManagedAccount("alice","irc-basic",False))
   h=HostAccount("alice",1001,1001,"ircsh","/home/alice","/usr/sbin/nologin",True)
   x=HealthProvider(s,Inspector({"alice":h})).read();self.assertTrue(x.ok);self.assertEqual(0,x.drifted)
 def test_json_is_machine_readable(self):
  with tempfile.TemporaryDirectory() as d:
   s=AccountStore(Path(d)/"a.json");self.assertIn('"ok":true',HealthProvider(s,Inspector({})).read().json())
if __name__=="__main__":unittest.main()
