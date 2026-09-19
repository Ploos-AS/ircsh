import unittest
from ircsh.cli import Context,execute
from ircsh.config import Config
from ircsh.model import Account
from ircsh.providers import QuotaProvider,ServiceProvider,StatusProvider

def ctx(caps=frozenset({"status.read","quota.read","services.read"})):
    return Context(Config(Account("test",caps)),StatusProvider(),QuotaProvider(),ServiceProvider())

class CommandTests(unittest.TestCase):
    def test_help(self):
        output,should_exit=execute("help",ctx())
        self.assertIn("Available commands",output); self.assertFalse(should_exit)
    def test_exit(self):
        output,should_exit=execute("exit",ctx())
        self.assertEqual("",output); self.assertTrue(should_exit)
    def test_unknown_command_is_rejected(self):
        output,should_exit=execute("echo should-not-run",ctx())
        self.assertEqual("ircsh: unknown command: echo should-not-run",output); self.assertFalse(should_exit)
    def test_shell_metacharacters_are_not_interpreted(self):
        output,_=execute("status; id",ctx())
        self.assertEqual("ircsh: unknown command: status; id",output)
    def test_capability_is_enforced(self):
        output,_=execute("services",ctx(frozenset()))
        self.assertEqual("ircsh: permission denied: services.read",output)
    def test_account_command(self):
        output,_=execute("account",ctx())
        self.assertEqual("Account: test",output)

if __name__=="__main__": unittest.main()
