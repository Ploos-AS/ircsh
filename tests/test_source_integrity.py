import ast,tomllib,unittest
from pathlib import Path
class SourceIntegrityTests(unittest.TestCase):
 def test_cli_parses(self):ast.parse(Path("src/ircsh/cli.py").read_text())
 def test_admin_cli_parses(self):ast.parse(Path("src/ircsh/admin_cli.py").read_text())
 def test_pyproject_parses(self):
  with Path("pyproject.toml").open("rb") as f:data=tomllib.load(f)
  self.assertEqual("ircsh.cli:main",data["project"]["scripts"]["ircsh"])
  self.assertEqual("ircsh.admin_cli:main",data["project"]["scripts"]["ircsh-admin"])
if __name__=="__main__":unittest.main()
