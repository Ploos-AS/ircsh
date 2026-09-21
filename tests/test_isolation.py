import unittest
from ircsh.isolation import DEFAULT_POLICY,IsolationPolicy,ResourceLimits

class IsolationPolicyTests(unittest.TestCase):
    def test_secure_defaults(self):
        p=DEFAULT_POLICY
        self.assertTrue(p.private_tmp and p.protect_home and p.no_new_privileges)
        self.assertTrue(p.private_devices and p.restrict_namespaces)
        self.assertEqual(25,p.limits.cpu_percent);self.assertEqual(256,p.limits.memory_mb)
    def test_limit_boundaries(self):
        ResourceLimits(cpu_percent=100,memory_mb=4096,processes=512,disk_mb=102400,connections=256,services=32)
        for kwargs in ({"cpu_percent":0},{"memory_mb":0},{"processes":513},{"disk_mb":63},{"connections":257},{"services":0}):
            with self.subTest(kwargs=kwargs),self.assertRaises(ValueError):ResourceLimits(**kwargs)
    def test_rejects_bool_as_integer_and_non_bool_policy(self):
        with self.assertRaises(ValueError):ResourceLimits(cpu_percent=True)
        with self.assertRaises(ValueError):IsolationPolicy(private_tmp=1)

if __name__=="__main__":unittest.main()
