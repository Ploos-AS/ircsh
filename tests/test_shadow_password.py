import tempfile,unittest
from pathlib import Path
from ircsh.host_inspector import _shadow_password

class ShadowPasswordTests(unittest.TestCase):
 def shadow(self,text):
  tmp=tempfile.TemporaryDirectory();path=Path(tmp.name)/"shadow";path.write_text(text,encoding="utf-8");return tmp,path
 def test_reads_exact_account_password_field(self):
  t,p=self.shadow("root:!:1:2:3:4:5:6:7\nalice:!$6$locked:1:2:3:4:5:6:7\n")
  try:self.assertEqual("!$6$locked",_shadow_password("alice",p))
  finally:t.cleanup()
 def test_missing_account_fails_closed(self):
  t,p=self.shadow("root:!:1:2:3:4:5:6:7\n")
  try:
   with self.assertRaises(RuntimeError):_shadow_password("alice",p)
  finally:t.cleanup()
 def test_duplicate_account_fails_closed(self):
  t,p=self.shadow("alice:!:1:2:3:4:5:6:7\nalice:*:1:2:3:4:5:6:7\n")
  try:
   with self.assertRaises(RuntimeError):_shadow_password("alice",p)
  finally:t.cleanup()
 def test_matching_malformed_record_fails_closed(self):
  t,p=self.shadow("alice\n")
  try:
   with self.assertRaises(RuntimeError):_shadow_password("alice",p)
  finally:t.cleanup()
 def test_unreadable_or_missing_database_fails_closed(self):
  with tempfile.TemporaryDirectory() as d:
   with self.assertRaises(RuntimeError):_shadow_password("alice",Path(d)/"missing")
if __name__=="__main__":unittest.main()
