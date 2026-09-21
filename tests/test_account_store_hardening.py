import os,tempfile,unittest
from pathlib import Path
from ircsh.account_store import AccountStore,ManagedAccount
class AccountStoreHardeningTests(unittest.TestCase):
 def test_store_symlink_rejected(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);target=root/"real";target.write_text("{}");link=root/"accounts.json";link.symlink_to(target)
   with self.assertRaises(RuntimeError):AccountStore(link).read()
 def test_lock_symlink_rejected(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);path=root/"accounts.json";(root/"target").write_text("")
   (root/"accounts.json.lock").symlink_to(root/"target")
   with self.assertRaises(RuntimeError):AccountStore(path).read()
 def test_modes_and_roundtrip(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d)/"db";path=root/"accounts.json";store=AccountStore(path);store.put(ManagedAccount("alice","irc-basic"))
   self.assertEqual(0o700,os.stat(root).st_mode&0o777);self.assertEqual(0o600,os.stat(path).st_mode&0o777);self.assertIn("alice",store.read())
if __name__=="__main__":unittest.main()
