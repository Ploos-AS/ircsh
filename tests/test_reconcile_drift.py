import unittest
from ircsh.account_store import ManagedAccount
from ircsh.host_inspector import HostAccount
from ircsh.reconcile import AccountReconciler
class DriftTests(unittest.TestCase):
 def test_compliant(self):
  h=HostAccount("alice",1001,1001,"ircsh","/home/alice","/usr/bin/ircsh");self.assertEqual((),AccountReconciler().plan(ManagedAccount("alice","irc-basic"),h))
 def test_drift(self):
  h=HostAccount("alice",1001,1001,"users","/srv/alice","/bin/bash")
  self.assertEqual(("usermod","--gid","ircsh","--home","/home/alice","--move-home","--shell","/usr/bin/ircsh","--","alice"),AccountReconciler().plan(ManagedAccount("alice","irc-basic"),h)[0].argv)
 def test_missing(self):self.assertEqual("useradd",AccountReconciler().plan(ManagedAccount("alice","irc-basic"),None)[0].argv[0])
 def test_disabled_idempotent(self):
  h=HostAccount("alice",1001,1001,"ircsh","/home/alice","/usr/sbin/nologin");self.assertEqual((),AccountReconciler().plan(ManagedAccount("alice","irc-basic",False),h))
if __name__=="__main__":unittest.main()
