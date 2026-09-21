import subprocess,unittest
from ircsh.client_sessions import ClientSession
from ircsh.sessions import SessionState
from ircsh.tmux_runtime import TmuxSessionRuntime

class Runner:
    def __init__(self):self.calls=[];self.exists=False
    def __call__(self,args,**kwargs):
        self.calls.append((args,kwargs))
        if args[1]=="has-session":return subprocess.CompletedProcess(args,0 if self.exists else 1,"","")
        if args[1]=="new-session":self.exists=True;return subprocess.CompletedProcess(args,0,"","")
        if args[1]=="list-clients":return subprocess.CompletedProcess(args,0,"","")
        return subprocess.CompletedProcess(args,0,"","")

class ClientSessionTests(unittest.TestCase):
    def test_fixed_programs(self):
        self.assertEqual(("weechat",),ClientSession("weechat",object()).argv)
        self.assertEqual(("irssi",),ClientSession("irssi",object()).argv)
        self.assertEqual(("BitchX",),ClientSession("bitchx",object()).argv)
        with self.assertRaises(ValueError):ClientSession("bash",object())

    def test_tmux_start_uses_fixed_argv(self):
        r=Runner();s=ClientSession("weechat",TmuxSessionRuntime(r))
        self.assertEqual(SessionState.DETACHED,s.start().state)
        self.assertIn(["tmux","new-session","-d","-s","ircsh-session-weechat","--","weechat"],[x[0] for x in r.calls])
        for _,kwargs in r.calls:self.assertNotIn("shell",kwargs)

    def test_existing_session_not_replaced(self):
        r=Runner();r.exists=True
        with self.assertRaises(RuntimeError):ClientSession("irssi",TmuxSessionRuntime(r)).start()
        self.assertFalse(any(c[0][1]=="new-session" for c in r.calls))

if __name__=="__main__":unittest.main()
