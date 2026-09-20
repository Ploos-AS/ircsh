import unittest
from ircsh.services import MutationDisabled,PlaceholderBackend,ServiceKind,ServiceRegistry,ServiceState

class ServiceTests(unittest.TestCase):
    def test_registry_has_bouncer_backends(self):
        r=ServiceRegistry()
        self.assertEqual("soju",r.get("main",ServiceKind.BOUNCER).backend)
        self.assertEqual("znc",r.get("znc1",ServiceKind.BOUNCER).backend)
        self.assertEqual("psybnc",r.get("legacy",ServiceKind.BOUNCER).backend)
    def test_bot_and_client_taxonomy(self):
        r=ServiceRegistry()
        self.assertEqual("eggdrop",r.get("eggdrop1",ServiceKind.BOT).backend)
        self.assertEqual("weechat",r.get("weechat",ServiceKind.CLIENT).backend)
    def test_status_is_typed(self):
        info=ServiceRegistry().get("main").status()
        self.assertEqual(ServiceState.UNAVAILABLE,info.state)
        self.assertEqual(ServiceKind.BOUNCER,info.kind)
    def test_multi_instance(self):
        r=ServiceRegistry((PlaceholderBackend(ServiceKind.BOT,"bot1","eggdrop"),PlaceholderBackend(ServiceKind.BOT,"bot2","eggdrop")))
        self.assertEqual(2,len(r.statuses(ServiceKind.BOT)))
    def test_mutation_is_fail_closed(self):
        with self.assertRaises(MutationDisabled):PlaceholderBackend(ServiceKind.BOUNCER,"main","soju").restart()
    def test_unsafe_instance_name_rejected(self):
        with self.assertRaises(ValueError):PlaceholderBackend(ServiceKind.BOT,"../../bin/sh","eggdrop")

if __name__=="__main__":unittest.main()
