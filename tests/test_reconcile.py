import unittest
from ircsh.account_store import ManagedAccount
from ircsh.host_inspector import HostAccount
from ircsh.reconcile import AccountReconciler
def host(shell="/usr/bin/ircsh",locked=False,group="ircsh",home="/home/alice"):
 return HostAccount("alice",1001,1001,group,home,shell,locked)
class ReconcileTests(unittest.TestCase):
 def test_create_enabled_account(self):
  a=AccountReconciler().plan(ManagedAccount("alice","irc-basic"),None)
  self.assertEqual("useradd",a[0].argv[0])
 def test_existing_enabled_account_is_compliant(self):
  self.assertEqual((),AccountReconciler().plan(ManagedAccount("alice","irc-advanced"),host()))
 def test_disabled_account_is_locked_and_nologin(self):
  a=AccountReconciler().plan(ManagedAccount("alice","irc-basic",False),host())
  self.assertEqual(("usermod","--lock","--shell","/usr/sbin/nologin","--","alice"),a[0].argv)
 def test_nologin_but_unlocked_is_not_compliant(self):
  a=AccountReconciler().plan(ManagedAccount("alice","irc-basic",False),host("/usr/sbin/nologin",False))
  self.assertEqual(("usermod","--lock","--","alice"),a[0].argv)
 def test_locked_but_login_shell_is_not_compliant(self):
  a=AccountReconciler().plan(ManagedAccount("alice","irc-basic",False),host("/usr/bin/ircsh",True))
  self.assertEqual(("usermod","--shell","/usr/sbin/nologin","--","alice"),a[0].argv)
 def test_disabled_compliant(self):
  self.assertEqual((),AccountReconciler().plan(ManagedAccount("alice","irc-basic",False),host("/usr/sbin/nologin",True)))
 def test_disabled_missing_account_is_not_created(self):
  self.assertEqual((),AccountReconciler().plan(ManagedAccount("alice","irc-basic",False),None))
if __name__=="__main__":unittest.main()
