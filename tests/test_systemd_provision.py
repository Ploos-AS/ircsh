import tempfile,unittest
from pathlib import Path
from ircsh.systemd_provision import SystemdDropInProvisioner

class SystemdProvisionTests(unittest.TestCase):
    def test_deterministic_render(self):
        with tempfile.TemporaryDirectory() as d:
            p=SystemdDropInProvisioner(Path(d));text=p.render("ircsh-weechat.service")
            self.assertTrue(text.startswith("[Service]\n"))
            self.assertIn("CPUQuota=25%",text);self.assertIn("MemoryMax=256M",text)
            self.assertIn("NoNewPrivileges=yes",text)
    def test_atomic_private_write(self):
        with tempfile.TemporaryDirectory() as d:
            p=SystemdDropInProvisioner(Path(d));path=p.write("ircsh-weechat.service")
            self.assertEqual(0o600,path.stat().st_mode & 0o777)
            self.assertEqual(0o700,path.parent.stat().st_mode & 0o777)
            self.assertEqual(p.render("ircsh-weechat.service"),path.read_text())
    def test_rejects_arbitrary_units_and_paths(self):
        with tempfile.TemporaryDirectory() as d:
            p=SystemdDropInProvisioner(Path(d))
            for unit in ("ssh.service","../x.service","ircsh-x;id.service"):
                with self.subTest(unit=unit),self.assertRaises(ValueError):p.write(unit)

if __name__=="__main__":unittest.main()
