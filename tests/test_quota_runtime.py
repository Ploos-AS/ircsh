import unittest
from ircsh.isolation import ResourceLimits
from ircsh.quotas import QuotaEnforcer,QuotaExceeded,QuotaUsage
from ircsh.quota_runtime import QuotaRuntime
from ircsh.runtime import RuntimeState

class Runtime:
    def __init__(self,state=RuntimeState.INACTIVE):self.current=state;self.calls=[]
    def state(self,u):return self.current
    def start(self,u):self.calls.append(("start",u));self.current=RuntimeState.ACTIVE
    def stop(self,u):self.calls.append(("stop",u));self.current=RuntimeState.INACTIVE
    def restart(self,u):self.calls.append(("restart",u))
class Meter:
    def __init__(self,usage):self.usage=usage;self.reads=0
    def read(self):self.reads+=1;return self.usage

class QuotaRuntimeTests(unittest.TestCase):
    def q(self,r,m):return QuotaRuntime(r,m,QuotaEnforcer(ResourceLimits(services=2,connections=2,disk_mb=100)))
    def test_start_checks_quota_before_runtime(self):
        r=Runtime();m=Meter(QuotaUsage(10,1,1));self.q(r,m).start("ircsh-x.service")
        self.assertEqual(1,m.reads);self.assertEqual([("start","ircsh-x.service")],r.calls)
    def test_start_denied_at_service_limit(self):
        r=Runtime();m=Meter(QuotaUsage(10,1,2))
        with self.assertRaises(QuotaExceeded):self.q(r,m).start("ircsh-x.service")
        self.assertEqual([],r.calls)
    def test_active_start_is_idempotent_without_consuming_slot(self):
        r=Runtime(RuntimeState.ACTIVE);m=Meter(QuotaUsage(100,2,2));self.q(r,m).start("ircsh-x.service")
        self.assertEqual(0,m.reads);self.assertEqual([],r.calls)
    def test_stop_remains_available_when_over_quota(self):
        r=Runtime(RuntimeState.ACTIVE);m=Meter(QuotaUsage(101,3,3));self.q(r,m).stop("ircsh-x.service")
        self.assertEqual([("stop","ircsh-x.service")],r.calls)
    def test_restart_denied_if_account_over_quota(self):
        r=Runtime(RuntimeState.ACTIVE);m=Meter(QuotaUsage(101,0,1))
        with self.assertRaises(QuotaExceeded):self.q(r,m).restart("ircsh-x.service")
        self.assertEqual([],r.calls)

if __name__=="__main__":unittest.main()
