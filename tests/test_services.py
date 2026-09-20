import unittest
from ircsh.services import MutationDisabled,PlaceholderBackend,ServiceRegistry,ServiceState

class ServiceTests(unittest.TestCase):
    def test_registry_has_soju_and_znc(self):
        r=ServiceRegistry()
        self.assertIsNotNone(r.get("soju")); self.assertIsNotNone(r.get("znc"))
    def test_status_is_typed(self):
        info=ServiceRegistry().get("soju").status()
        self.assertEqual(ServiceState.UNAVAILABLE,info.state)
        self.assertEqual("soju",info.backend)
    def test_mutation_is_fail_closed(self):
        with self.assertRaises(MutationDisabled):
            PlaceholderBackend("soju","soju").restart()
    def test_unknown_service_is_not_resolved(self):
        self.assertIsNone(ServiceRegistry().get("../../bin/sh"))

if __name__=="__main__": unittest.main()
