import unittest
from ircsh.isolation import ResourceLimits
from ircsh.quotas import QuotaEnforcer,QuotaExceeded,QuotaUsage

class QuotaTests(unittest.TestCase):
    def setUp(self):self.q=QuotaEnforcer(ResourceLimits(disk_mb=100,connections=2,services=2))
    def test_usage_within_limits(self):self.q.check(QuotaUsage(100,2,2))
    def test_existing_overage_fails_closed(self):
        for u in (QuotaUsage(101,0,0),QuotaUsage(0,3,0),QuotaUsage(0,0,3)):
            with self.assertRaises(QuotaExceeded):self.q.check(u)
    def test_service_and_connection_admission(self):
        self.q.allow_service_start(QuotaUsage(0,0,1));self.q.allow_connection(QuotaUsage(0,1,0))
        with self.assertRaises(QuotaExceeded):self.q.allow_service_start(QuotaUsage(0,0,2))
        with self.assertRaises(QuotaExceeded):self.q.allow_connection(QuotaUsage(0,2,0))
    def test_disk_growth(self):
        self.q.allow_disk_growth(QuotaUsage(90,0,0),10)
        with self.assertRaises(QuotaExceeded):self.q.allow_disk_growth(QuotaUsage(90,0,0),11)
        with self.assertRaises(ValueError):self.q.allow_disk_growth(QuotaUsage(),-1)
    def test_usage_rejects_invalid_values(self):
        with self.assertRaises(ValueError):QuotaUsage(disk_mb=-1)
        with self.assertRaises(ValueError):QuotaUsage(connections=True)

if __name__=="__main__":unittest.main()
