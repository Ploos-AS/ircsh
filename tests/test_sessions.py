import unittest
from ircsh.sessions import PersistentSession,ReadOnlySessionRuntime,SessionState

class FakeSessionRuntime:
    def __init__(self):self.current=SessionState.DETACHED;self.targets=[]
    def state(self,target):self.targets.append(target);return self.current
    def attach(self,target):self.targets.append(target);self.current=SessionState.ATTACHED
    def detach(self,target):self.targets.append(target);self.current=SessionState.DETACHED

class SessionTests(unittest.TestCase):
    def test_deterministic_target(self):
        s=PersistentSession("weechat")
        self.assertEqual("ircsh-session-weechat",s.target)

    def test_unsafe_names_rejected(self):
        for name in ("x;id","../x","x y","x/../../bin/sh"):
            with self.subTest(name=name),self.assertRaises(ValueError):PersistentSession(name)

    def test_attach_detach_status(self):
        r=FakeSessionRuntime();s=PersistentSession("irssi",r)
        self.assertEqual(SessionState.DETACHED,s.status().state)
        self.assertEqual(SessionState.ATTACHED,s.attach().state)
        self.assertEqual(SessionState.DETACHED,s.detach().state)
        self.assertTrue(all(x=="ircsh-session-irssi" for x in r.targets))

    def test_default_runtime_fails_closed(self):
        s=PersistentSession("weechat",ReadOnlySessionRuntime())
        self.assertEqual(SessionState.MISSING,s.status().state)
        with self.assertRaises(PermissionError):s.attach()
        with self.assertRaises(PermissionError):s.detach()

if __name__=="__main__":unittest.main()
