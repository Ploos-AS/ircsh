import unittest
from ircsh.backends import EggdropBackend
from ircsh.runtime import RuntimeState
from ircsh.services import ServiceKind,ServiceState

class FakeRuntime:
    def __init__(self):self.current=RuntimeState.INACTIVE;self.calls=[]
    def state(self,u):self.calls.append(("state",u));return self.current
    def start(self,u):self.calls.append(("start",u));self.current=RuntimeState.ACTIVE
    def stop(self,u):self.calls.append(("stop",u));self.current=RuntimeState.INACTIVE
    def restart(self,u):self.calls.append(("restart",u));self.current=RuntimeState.ACTIVE

class EggdropTests(unittest.TestCase):
    def test_is_bot(self):
        self.assertEqual(ServiceKind.BOT,EggdropBackend("trivia",FakeRuntime()).service_id.kind)
    def test_instance_has_deterministic_unit(self):
        r=FakeRuntime();b=EggdropBackend("trivia",r);b.start()
        self.assertIn(("start","ircsh-eggdrop-trivia.service"),r.calls)
    def test_multiple_instances_are_separate(self):
        self.assertNotEqual(EggdropBackend("trivia",FakeRuntime()).unit,EggdropBackend("guard",FakeRuntime()).unit)
    def test_unsafe_instance_rejected_before_unit_creation(self):
        with self.assertRaises(ValueError):EggdropBackend("../../evil",FakeRuntime())
    def test_lifecycle(self):
        r=FakeRuntime();b=EggdropBackend("guard",r)
        self.assertEqual(ServiceState.RUNNING,b.start().state)
        self.assertEqual(ServiceState.STOPPED,b.stop().state)
        self.assertEqual(ServiceState.RUNNING,b.restart().state)

if __name__=="__main__":unittest.main()
