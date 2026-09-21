import unittest
from ircsh.account_store import ManagedAccount
from ircsh.reconcile import *
class ReconcileTests(unittest.TestCase):
 def test_create_enabled_account(self):
  a=AccountReconciler().plan(ManagedAccount("alice","irc-basic"),False)
  self.assertEqual(("useradd","--create-home","--home-dir","/home/alice","--gid","ircsh","--shell","/usr/bin/ircsh","--","alice"),a[0].argv)
 def test_existing_enabled_account_is_normalized(self):
  a=AccountReconciler().plan(ManagedAccount("alice","irc-advanced"),True)
  self.assertEqual(("usermod","--gid","ircsh","--shell","/usr/bin/ircsh","--","alice"),a[0].argv)
 def test_disabled_account_is_locked(self):
  a=AccountReconciler().plan(ManagedAccount("alice","irc-basic",False),True)
  self.assertEqual(("usermod","--lock","--shell","/usr/sbin/nologin","--","alice"),a[0].argv)
 def test_disabled_missing_account_is_not_created(self):
  self.assertEqual((),AccountReconciler().plan(ManagedAccount("alice","irc-basic",False),False))
if __name__=="__main__":unittest.main()
