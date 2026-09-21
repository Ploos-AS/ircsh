import unittest
from unittest.mock import patch
from types import SimpleNamespace
from ircsh.host_inspector import HostInspector
class HostInspectorTests(unittest.TestCase):
 @patch("ircsh.host_inspector.grp.getgrgid",return_value=SimpleNamespace(gr_name="ircsh"))
 @patch("ircsh.host_inspector.pwd.getpwnam",return_value=SimpleNamespace(pw_uid=1001,pw_gid=1001,pw_dir="/home/alice",pw_shell="/usr/bin/ircsh"))
 def test_inspects_account(self,p,g):
  a=HostInspector().inspect("alice");self.assertEqual("ircsh",a.group);self.assertEqual("/usr/bin/ircsh",a.shell)
 @patch("ircsh.host_inspector.pwd.getpwnam",side_effect=KeyError)
 def test_missing_is_none(self,p):self.assertIsNone(HostInspector().inspect("alice"))
 def test_invalid_name_rejected(self):
  with self.assertRaises(ValueError):HostInspector().inspect("../root")
 @patch("ircsh.host_inspector.grp.getgrgid",side_effect=KeyError)
 @patch("ircsh.host_inspector.pwd.getpwnam",return_value=SimpleNamespace(pw_uid=1001,pw_gid=1001,pw_dir="/home/alice",pw_shell="/usr/bin/ircsh"))
 def test_missing_group_fails_closed(self,p,g):
  with self.assertRaises(RuntimeError):HostInspector().inspect("alice")
if __name__=="__main__":unittest.main()
