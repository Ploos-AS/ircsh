import subprocess,unittest
from ircsh.logs import JournalLogProvider

class Runner:
    def __init__(self,rc=0):self.calls=[];self.rc=rc
    def __call__(self,args,**kwargs):
        self.calls.append((args,kwargs));return subprocess.CompletedProcess(args,self.rc,"one\ntwo\n","err")

class LogTests(unittest.TestCase):
    def test_fixed_unit_and_bounded_lines(self):
        r=Runner();p=JournalLogProvider(r)
        self.assertEqual("one\ntwo",p.read("soju",25))
        self.assertEqual(["journalctl","--no-pager","--output=short","-n","25","-u","soju.service"],r.calls[0][0])
        self.assertNotIn("shell",r.calls[0][1])
    def test_rejects_service_and_line_injection(self):
        p=JournalLogProvider(Runner())
        for service in ("../x","soju;id","ssh"):
            with self.subTest(service=service),self.assertRaises(ValueError):p.read(service)
        for lines in (0,201,-1,"50"):
            with self.subTest(lines=lines),self.assertRaises(ValueError):p.read("soju",lines)
    def test_backend_failure_is_closed(self):
        with self.assertRaises(RuntimeError):JournalLogProvider(Runner(1)).read("weechat")

if __name__=="__main__":unittest.main()
