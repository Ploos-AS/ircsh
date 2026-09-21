import unittest
from ircsh.backends import PsybncBackend
from ircsh.runtime import RuntimeState
from ircsh.services import ServiceState

class FakeRuntime:
    def __init__(self):self.current=RuntimeState.INACTIVE;self.calls=[]
    def state(self,unit):self.calls.append(("state",unit));return self.current
    def start(self,unit):self.calls.append(("start",unit));self.current=RuntimeState.ACTIVE
    def stop(self,unit):self.calls.append(("stop",unit));self.current=RuntimeState.INACTIVE
    def restart(self,unit):self.calls.append(("restart",unit));self.current=RuntimeState.ACTIVE

class PsybncTests(unittest.TestCase):
    def test_dedicated_isolated_unit(self):
        r=FakeRuntime();b=PsybncBackend("legacy",r)
        self.assertEqual(ServiceState.RUNNING,b.start().state)
        self.assertIn(("start","ircsh-psybnc.service"),r.calls)
    def test_lifecycle(self):
        r=FakeRuntime();b=PsybncBackend("legacy",r)
        b.start();self.assertEqual(ServiceState.STOPPED,b.stop().state)
        self.assertEqual(ServiceState.RUNNING,b.restart().state)
    def test_arbitrary_unit_rejected(self):
        with self.assertRaises(ValueError):PsybncBackend("legacy",FakeRuntime(),"psybnc@evil.service")

if __name__=="__main__":unittest.main()
