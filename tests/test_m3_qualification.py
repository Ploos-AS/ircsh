import subprocess,tempfile,unittest
from pathlib import Path
from ircsh.client_sessions import ClientSession
from ircsh.logs import JournalLogProvider
from ircsh.service_config import ServiceConfigStore
from ircsh.tmux_runtime import TmuxSessionRuntime

class Runner:
    def __init__(self):self.calls=[]
    def __call__(self,args,**kwargs):
        self.calls.append((args,kwargs))
        if args[0]=="tmux" and args[1]=="has-session":return subprocess.CompletedProcess(args,1,"","")
        return subprocess.CompletedProcess(args,0,"","")

class M3QualificationTests(unittest.TestCase):
    def test_session_start_boundary_has_no_shell_escape(self):
        r=Runner();ClientSession("weechat",TmuxSessionRuntime(r)).start()
        for args,kwargs in r.calls:
            self.assertNotIn("shell",kwargs)
            self.assertNotIn("bash",args)
            self.assertNotIn("sh",args)
    def test_only_known_client_programs(self):
        with self.assertRaises(ValueError):ClientSession("bash",TmuxSessionRuntime(Runner()))
    def test_config_boundary_rejects_command_and_path_input(self):
        with tempfile.TemporaryDirectory() as d:
            s=ServiceConfigStore(Path(d))
            with self.assertRaises(ValueError):s.set("weechat","command","id")
            with self.assertRaises(ValueError):s.set("../weechat","nick","x")
    def test_log_boundary_is_read_only_and_bounded(self):
        r=Runner();p=JournalLogProvider(r);p.read("soju",200)
        self.assertEqual("journalctl",r.calls[-1][0][0])
        self.assertIn("200",r.calls[-1][0])
        with self.assertRaises(ValueError):p.read("soju",201)
        with self.assertRaises(ValueError):p.read("ssh",50)

if __name__=="__main__":unittest.main()
