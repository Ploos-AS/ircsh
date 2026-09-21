import tempfile,unittest
from pathlib import Path
from ircsh.service_config import ServiceConfigStore

class ServiceConfigTests(unittest.TestCase):
    def test_allowlisted_typed_write(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)/"cfg";s=ServiceConfigStore(root)
            s.set("weechat","nick","tester")
            s.set("weechat","autoconnect",True)
            self.assertEqual("autoconnect=true\nnick=tester\n",(root/"weechat.conf").read_text())
            self.assertEqual(0o600,(root/"weechat.conf").stat().st_mode & 0o777)

    def test_rejects_unknown_service_key_and_type(self):
        with tempfile.TemporaryDirectory() as d:
            s=ServiceConfigStore(Path(d))
            for args in (("bash","nick","x"),("weechat","command","id"),("weechat","autoconnect","yes")):
                with self.subTest(args=args),self.assertRaises(ValueError):s.set(*args)

    def test_rejects_path_and_line_injection(self):
        with tempfile.TemporaryDirectory() as d:
            s=ServiceConfigStore(Path(d))
            with self.assertRaises(ValueError):s.set("../x","nick","x")
            with self.assertRaises(ValueError):s.set("weechat","nick","ok\ncommand=id")
            self.assertEqual([],list(Path(d).iterdir()))

if __name__=="__main__":unittest.main()
