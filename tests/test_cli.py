import unittest
from ircsh.cli import execute

class CommandTests(unittest.TestCase):
    def test_help(self):
        output, should_exit = execute("help")
        self.assertIn("Available commands", output)
        self.assertFalse(should_exit)

    def test_exit(self):
        output, should_exit = execute("exit")
        self.assertEqual("", output)
        self.assertTrue(should_exit)

    def test_unknown_command_is_rejected(self):
        output, should_exit = execute("echo should-not-run")
        self.assertEqual("ircsh: unknown command: echo should-not-run", output)
        self.assertFalse(should_exit)

    def test_shell_metacharacters_are_not_interpreted(self):
        output, _ = execute("status; id")
        self.assertEqual("ircsh: unknown command: status; id", output)

if __name__ == "__main__":
    unittest.main()
