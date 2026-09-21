import unittest
from ircsh.backends import PersistentClientBackend
from ircsh.runtime import RuntimeState
from ircsh.services import ServiceKind,ServiceState

class FakeRuntime:
    def __init__(self):self.current=RuntimeState.INACTIVE;self.calls=[]
    def state(self,u):self.calls.append(("state",u));return self.current
    def start(self,u):self.calls.append(("start",u));self.current=RuntimeState.ACTIVE
    def stop(self,u):self.calls.append(("stop",u));self.current=RuntimeState.INACTIVE
    def restart(self,u):self.calls.append(("restart",u));self.current=RuntimeState.ACTIVE

class BitchXTests(unittest.TestCase):
    def test_client_classification_and_unit(self):
        b=PersistentClientBackend("main",FakeRuntime(),"bitchx")
        self.assertEqual(ServiceKind.CLIENT,b.service_id.kind)
        self.assertEqual("ircsh-bitchx-main.service",b.unit)
    def test_lifecycle(self):
        r=FakeRuntime();b=PersistentClientBackend("main",r,"bitchx")
        self.assertEqual(ServiceState.RUNNING,b.start().state)
        self.assertEqual(ServiceState.STOPPED,b.stop().state)
        self.assertEqual(ServiceState.RUNNING,b.restart().state)
    def test_unsafe_instance_rejected(self):
        with self.assertRaises(ValueError):PersistentClientBackend("../../sh",FakeRuntime(),"bitchx")

if __name__=="__main__":unittest.main()
