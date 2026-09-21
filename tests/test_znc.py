import unittest
from ircsh.backends import ZncBackend
from ircsh.runtime import RuntimeState
from ircsh.services import ServiceState

class FakeRuntime:
    def __init__(self):self.current=RuntimeState.INACTIVE;self.calls=[]
    def state(self,unit):self.calls.append(("state",unit));return self.current
    def start(self,unit):self.calls.append(("start",unit));self.current=RuntimeState.ACTIVE
    def stop(self,unit):self.calls.append(("stop",unit));self.current=RuntimeState.INACTIVE
    def restart(self,unit):self.calls.append(("restart",unit));self.current=RuntimeState.ACTIVE

class ZncTests(unittest.TestCase):
    def test_status_mapping(self):
        self.assertEqual(ServiceState.STOPPED,ZncBackend("znc1",FakeRuntime()).status().state)
    def test_lifecycle_uses_fixed_unit(self):
        r=FakeRuntime();b=ZncBackend("znc1",r)
        self.assertEqual(ServiceState.RUNNING,b.start().state)
        self.assertIn(("start","znc.service"),r.calls)
        self.assertEqual(ServiceState.STOPPED,b.stop().state)
        self.assertEqual(ServiceState.RUNNING,b.restart().state)
    def test_arbitrary_unit_rejected(self):
        with self.assertRaises(ValueError):ZncBackend("znc1",FakeRuntime(),"user-controlled.service")

if __name__=="__main__":unittest.main()
