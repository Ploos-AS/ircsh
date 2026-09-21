import base64,unittest
from ircsh.provisioning import AccountProvisioning
KEY="ssh-ed25519 "+base64.b64encode(b"test-key-material").decode()
class ProvisioningTests(unittest.TestCase):
 def test_fixed_identity_paths_and_modes(self):
  p=AccountProvisioning("alice")
  self.assertEqual("/home/alice",p.home);self.assertEqual("/usr/bin/ircsh",p.shell)
  self.assertEqual(0o700,p.modes()[p.ssh_dir]);self.assertEqual(0o600,p.modes()[p.authorized_keys])
 def test_restricted_ed25519_key_line(self):
  line=AccountProvisioning("alice").key_line(KEY)
  self.assertTrue(line.startswith("no-agent-forwarding,no-port-forwarding,no-X11-forwarding,restrict "))
  self.assertIn(KEY,line)
 def test_rejects_legacy_or_injected_keys(self):
  p=AccountProvisioning("alice")
  with self.assertRaises(ValueError):p.key_line("ssh-rsa AAAA")
  with self.assertRaises(ValueError):p.key_line(KEY+"\ncommand=\"/bin/sh\"")
 def test_fixed_group_and_home_root(self):
  with self.assertRaises(ValueError):AccountProvisioning("alice",group="sudo")
  with self.assertRaises(ValueError):AccountProvisioning("alice",home_root="/tmp")
if __name__=="__main__":unittest.main()
