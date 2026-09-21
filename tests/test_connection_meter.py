import tempfile,unittest
from pathlib import Path
from ircsh.connection_meter import ProcConnectionMeter

HEADER="sl local_address rem_address st tx_queue rx_queue tr tm->when retrnsmt uid timeout inode\n"
def row(state,uid):return f"0: 00000000:1A0B 00000000:0000 {state} 0 0 0 {uid} 0 0\n"

class ConnectionMeterTests(unittest.TestCase):
    def test_counts_established_for_uid_ipv4_and_ipv6(self):
        with tempfile.TemporaryDirectory() as d:
            n=Path(d)/"net";n.mkdir()
            (n/"tcp").write_text(HEADER+row("01",1000)+row("0A",1000)+row("01",1001))
            (n/"tcp6").write_text(HEADER+row("01",1000))
            self.assertEqual(2,ProcConnectionMeter(1000,Path(d)).count())
    def test_validates_uid_and_proc_root(self):
        with self.assertRaises(ValueError):ProcConnectionMeter(True)
        with self.assertRaises(ValueError):ProcConnectionMeter(-1)
        with self.assertRaises(ValueError):ProcConnectionMeter(1,Path("proc"))
if __name__=="__main__":unittest.main()
