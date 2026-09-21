import subprocess,unittest
from ircsh.sessions import SessionState
from ircsh.tmux_runtime import TmuxSessionRuntime

class Runner:
    def __init__(self,has=0,clients=""):self.calls=[];self.has=has;self.clients=clients
    def __call__(self,args,**kwargs):
        self.calls.append((args,kwargs))
        if args[1]=="has-session":return subprocess.CompletedProcess(args,self.has,"","")
        if args[1]=="list-clients":return subprocess.CompletedProcess(args,0,self.clients,"")
        return subprocess.CompletedProcess(args,0,"","")

class TmuxRuntimeTests(unittest.TestCase):
    def test_state(self):
        self.assertEqual(SessionState.MISSING,TmuxSessionRuntime(Runner(has=1)).state("ircsh-session-weechat"))
        self.assertEqual(SessionState.DETACHED,TmuxSessionRuntime(Runner()).state("ircsh-session-weechat"))
        self.assertEqual(SessionState.ATTACHED,TmuxSessionRuntime(Runner(clients="tty\n")).state("ircsh-session-weechat"))

    def test_fixed_attach_and_detach_commands(self):
        r=Runner();x=TmuxSessionRuntime(r)
        x.attach("ircsh-session-irssi");x.detach("ircsh-session-irssi")
        commands=[c[0] for c in r.calls]
        self.assertIn(["tmux","attach-session","-t","ircsh-session-irssi"],commands)
        self.assertIn(["tmux","detach-client","-s","ircsh-session-irssi"],commands)

    def test_rejects_arbitrary_targets(self):
        for target in ("x","ircsh-session-x;id","ircsh-session-../x","ircsh-session-x y"):
            with self.subTest(target=target),self.assertRaises(ValueError):
                TmuxSessionRuntime(Runner()).state(target)

    def test_no_shell_execution(self):
        r=Runner();TmuxSessionRuntime(r).state("ircsh-session-weechat")
        self.assertTrue(r.calls)
        for _,kwargs in r.calls:self.assertNotIn("shell",kwargs)

if __name__=="__main__":unittest.main()
