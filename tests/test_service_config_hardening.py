import os,tempfile,unittest
from pathlib import Path
from ircsh.service_config import ServiceConfigStore
class ConfigHardeningTests(unittest.TestCase):
 def test_unknown_existing_key_fails_closed(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);(p/"weechat.conf").write_text("evil=value\n")
   with self.assertRaises(RuntimeError):ServiceConfigStore(p).read("weechat")
   with self.assertRaises(RuntimeError):ServiceConfigStore(p).set("weechat","nick","alice")
 def test_malformed_bool_fails_closed(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);(p/"weechat.conf").write_text("autoconnect=yes\n")
   with self.assertRaises(RuntimeError):ServiceConfigStore(p).read("weechat")
 def test_root_mode_is_repaired(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/"cfg";p.mkdir(mode=0o755);ServiceConfigStore(p).set("weechat","nick","alice")
   self.assertEqual(0o700,os.stat(p).st_mode&0o777)
 def test_symlink_file_rejected(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/"cfg";p.mkdir();outside=Path(d)/"outside";outside.write_text("nick=alice\n");(p/"weechat.conf").symlink_to(outside)
   with self.assertRaises(RuntimeError):ServiceConfigStore(p).read("weechat")
if __name__=="__main__":unittest.main()
