import subprocess,unittest
from ircsh.cli import Context,execute
from ircsh.config import Config
from ircsh.logs import JournalLogProvider
from ircsh.model import Account
from ircsh.providers import QuotaProvider,ServiceProvider,StatusProvider

class Runner:
    def __init__(self):self.calls=[]
    def __call__(self,args,**kwargs):
        self.calls.append(args);return subprocess.CompletedProcess(args,0,"line1\nline2\n","")

def ctx(caps):
    r=Runner()
    return Context(Config(Account("test",frozenset(caps))),StatusProvider(),QuotaProvider(),ServiceProvider(),None,None,JournalLogProvider(r)),r

class LogCliTests(unittest.TestCase):
    def test_requires_capability(self):
        c,_=ctx(set())
        self.assertEqual("ircsh: permission denied: logs.read",execute("logs soju",c)[0])
    def test_default_and_explicit_limit(self):
        c,r=ctx({"logs.read"})
        self.assertEqual("line1\nline2",execute("logs soju",c)[0])
        self.assertIn("50",r.calls[-1])
        self.assertEqual("line1\nline2",execute("logs znc 20",c)[0])
        self.assertIn("20",r.calls[-1])
    def test_rejects_bad_service_limit_and_extra_args(self):
        c,_=ctx({"logs.read"})
        self.assertIn("unsupported log service",execute("logs soju;id",c)[0])
        self.assertIn("log operation denied",execute("logs soju 999",c)[0])
        self.assertIn("log operation denied",execute("logs soju nope",c)[0])
        self.assertEqual("ircsh: invalid logs command: logs soju 20 extra",execute("logs soju 20 extra",c)[0])

if __name__=="__main__":unittest.main()
