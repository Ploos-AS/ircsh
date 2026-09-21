import tempfile,unittest
from pathlib import Path
from ircsh.quota_meter import QuotaMeter
from ircsh.runtime import RuntimeState

class Runtime:
    def __init__(self,states):self.states=states
    def state(self,u):return self.states[u]

class QuotaMeterTests(unittest.TestCase):
    def test_measures_disk_and_active_services(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/"a").write_bytes(b"x"*1048577)
            m=QuotaMeter(root,("ircsh-a.service","ircsh-b.service"),Runtime({"ircsh-a.service":RuntimeState.ACTIVE,"ircsh-b.service":RuntimeState.INACTIVE}))
            u=m.read();self.assertEqual(2,u.disk_mb);self.assertEqual(1,u.services);self.assertEqual(0,u.connections)
    def test_requires_absolute_root(self):
        with self.assertRaises(ValueError):QuotaMeter(Path("relative"),(),Runtime({}))
    def test_rejects_path_like_units(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):QuotaMeter(Path(d),("../x.service",),Runtime({}))
    def test_missing_file_during_walk_is_tolerated(self):
        with tempfile.TemporaryDirectory() as d:self.assertEqual(0,QuotaMeter(Path(d),(),Runtime({})).disk_mb())

if __name__=="__main__":unittest.main()
