import json,logging,unittest
from ircsh.audit import AuditEvent,AuditLogger
class Handler(logging.Handler):
    def __init__(self):super().__init__();self.messages=[]
    def emit(self,r):self.messages.append(r.getMessage())
class AuditTests(unittest.TestCase):
    def test_structured_event(self):
        l=logging.getLogger("test.audit");l.setLevel(logging.INFO);l.propagate=False;h=Handler();l.handlers=[h]
        AuditLogger(l).emit(AuditEvent("service_start","ircsh-x.service","denied","QuotaExceeded"))
        self.assertEqual({"action":"service_start","reason":"QuotaExceeded","result":"denied","target":"ircsh-x.service"},json.loads(h.messages[0]))
    def test_rejects_log_injection(self):
        with self.assertRaises(ValueError):AuditEvent("service_start","x\nforged","denied")
        with self.assertRaises(ValueError):AuditEvent("bad action","x","allowed")
if __name__=="__main__":unittest.main()
