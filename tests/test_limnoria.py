import unittest
from ircsh.backends import LimnoriaBackend
from ircsh.runtime import RuntimeState
from ircsh.services import ServiceKind,ServiceState

class FakeRuntime:
    def __init__(self):self.current=RuntimeState.INACTIVE
    def state(self,u):return self.current
    def start(self,u):self.current=RuntimeState.ACTIVE
    def stop(self,u):self.current=RuntimeState.INACTIVE
    def restart(self,u):self.current=RuntimeState.ACTIVE

class LimnoriaTests(unittest.TestCase):
    def test_identity_and_unit(self):
        b=LimnoriaBackend("helper",FakeRuntime())
        self.assertEqual(ServiceKind.BOT,b.service_id.kind)
        self.assertEqual("limnoria",b.backend)
        self.assertEqual("ircsh-limnoria-helper.service",b.unit)
    def test_lifecycle(self):
        b=LimnoriaBackend("helper",FakeRuntime())
        self.assertEqual(ServiceState.RUNNING,b.start().state)
        self.assertEqual(ServiceState.STOPPED,b.stop().state)
        self.assertEqual(ServiceState.RUNNING,b.restart().state)
    def test_unsafe_name_rejected(self):
        with self.assertRaises(ValueError):LimnoriaBackend("../../evil",FakeRuntime())

if __name__=="__main__":unittest.main()
