import unittest
from types import SimpleNamespace
from unittest.mock import patch
from ircsh.tmux_runtime import TmuxSessionRuntime
from ircsh.cli import context
class Runner:
 def __init__(self):self.calls=[]
 def __call__(self,args,**kw):
  self.calls.append((args,kw));return SimpleNamespace(returncode=1,stdout="",stderr="")
class TmuxHardeningTests(unittest.TestCase):
 def test_start_uses_fixed_tmux_command(self):
  r=Runner();TmuxSessionRuntime(r).start("ircsh-session-weechat",("weechat",))
  self.assertEqual(["tmux","new-session","-d","-s","ircsh-session-weechat","--","weechat"],r.calls[-1][0])
 def test_program_arguments_not_accepted(self):
  with self.assertRaises(ValueError):TmuxSessionRuntime(Runner()).start("ircsh-session-weechat",("weechat","/bin/sh"))
 @patch("ircsh.cli.load_config")
 def test_production_context_wires_tmux_sessions(self,lc):
  lc.return_value=SimpleNamespace()
  c=context();self.assertEqual({"weechat","irssi","bitchx"},{x.name for x in c.sessions._sessions});self.assertEqual({"weechat","irssi","bitchx"},set(c.sessions._clients))
if __name__=="__main__":unittest.main()
