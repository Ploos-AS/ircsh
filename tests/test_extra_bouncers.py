import unittest
from ircsh.backends import MuhBackend,BipBackend,PounceBackend
from ircsh.runtime import RuntimeState
from ircsh.services import ServiceState

class FakeRuntime:
    def __init__(self):self.current=RuntimeState.INACTIVE;self.calls=[]
    def state(self,u):self.calls.append(("state",u));return self.current
    def start(self,u):self.calls.append(("start",u));self.current=RuntimeState.ACTIVE
    def stop(self,u):self.calls.append(("stop",u));self.current=RuntimeState.INACTIVE
    def restart(self,u):self.calls.append(("restart",u));self.current=RuntimeState.ACTIVE

class ExtraBouncerTests(unittest.TestCase):
    def test_fixed_runtime_targets(self):
        for cls,name,unit in ((MuhBackend,"muh1","ircsh-muh.service"),(BipBackend,"bip1","ircsh-bip.service"),(PounceBackend,"pounce1","ircsh-pounce.service")):
            r=FakeRuntime();b=cls(name,r)
            self.assertEqual(ServiceState.RUNNING,b.start().state)
            self.assertIn(("start",unit),r.calls)
    def test_arbitrary_units_rejected(self):
        for cls in (MuhBackend,BipBackend,PounceBackend):
            with self.assertRaises(ValueError):cls("test",FakeRuntime(),"evil.service")
    def test_lifecycle(self):
        for cls in (MuhBackend,BipBackend,PounceBackend):
            r=FakeRuntime();b=cls("test",r);b.start()
            self.assertEqual(ServiceState.STOPPED,b.stop().state)
            self.assertEqual(ServiceState.RUNNING,b.restart().state)

if __name__=="__main__":unittest.main()
