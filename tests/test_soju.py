import unittest
from ircsh.backends import SojuBackend
from ircsh.runtime import RuntimeState
from ircsh.services import ServiceState

class FakeRuntime:
    def __init__(self):self.current=RuntimeState.INACTIVE;self.calls=[]
    def state(self,unit):self.calls.append(("state",unit));return self.current
    def start(self,unit):self.calls.append(("start",unit));self.current=RuntimeState.ACTIVE
    def stop(self,unit):self.calls.append(("stop",unit));self.current=RuntimeState.INACTIVE
    def restart(self,unit):self.calls.append(("restart",unit));self.current=RuntimeState.ACTIVE

class SojuTests(unittest.TestCase):
    def test_status_mapping(self):
        r=FakeRuntime();b=SojuBackend("main",r)
        self.assertEqual(ServiceState.STOPPED,b.status().state)
    def test_start_uses_fixed_unit(self):
        r=FakeRuntime();b=SojuBackend("main",r)
        self.assertEqual(ServiceState.RUNNING,b.start().state)
        self.assertIn(("start","soju.service"),r.calls)
    def test_arbitrary_unit_rejected(self):
        with self.assertRaises(ValueError):SojuBackend("main",FakeRuntime(),"../../bin/sh")
    def test_restart(self):
        r=FakeRuntime();b=SojuBackend("main",r)
        self.assertEqual(ServiceState.RUNNING,b.restart().state)

if __name__=="__main__":unittest.main()
