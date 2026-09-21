import tempfile,unittest
from pathlib import Path
from ircsh.connection_meter import ProcConnectionMeter,ConnectionMeasurementError
from ircsh.quota_meter import QuotaMeter,QuotaMeasurementError
class Runtime:pass
class HardeningTests(unittest.TestCase):
 def test_proc_malformed_row_fails_closed(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);(p/"net").mkdir();(p/"net"/"tcp").write_text("header\nbad\n");(p/"net"/"tcp6").write_text("header\n")
   with self.assertRaises(ConnectionMeasurementError):ProcConnectionMeter(1000,p).count()
 def test_proc_counts_active_states(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);(p/"net").mkdir();row="0: A B 02 C D E 1000\n"
   (p/"net"/"tcp").write_text("header\n"+row);(p/"net"/"tcp6").write_text("header\n")
   self.assertEqual(1,ProcConnectionMeter(1000,p).count())
 def test_disk_uses_lstat_not_symlink_target(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d)/"root";root.mkdir();outside=Path(d)/"large";outside.write_bytes(b"x"*2000000);(root/"link").symlink_to(outside)
   self.assertEqual(1,QuotaMeter(root,(),Runtime()).disk_mb())
 def test_walk_error_fails_closed(self):
  def walker(root,onerror=None,followlinks=False):
   if onerror:onerror(OSError("denied"))
   return iter(())
  with self.assertRaises(QuotaMeasurementError):QuotaMeter(Path("/tmp/x"),(),Runtime(),walker=walker).disk_mb()
if __name__=="__main__":unittest.main()
