"""Read-only, allowlisted service log access."""
from __future__ import annotations
import subprocess
from collections.abc import Callable

UNITS={
 "soju":"soju.service","znc":"znc.service","psybnc":"ircsh-psybnc.service",
 "muh":"ircsh-muh.service","bip":"ircsh-bip.service","pounce":"ircsh-pounce.service",
 "eggdrop":"ircsh-eggdrop.service","limnoria":"ircsh-limnoria.service",
 "sopel":"ircsh-sopel.service","errbot":"ircsh-errbot.service",
 "energymech":"ircsh-energymech.service","psotnic":"ircsh-psotnic.service",
 "weechat":"ircsh-weechat-main.service","irssi":"ircsh-irssi-main.service",
 "bitchx":"ircsh-bitchx-main.service",
}
MAX_LINES=200

class JournalLogProvider:
    def __init__(self,runner:Callable[...,subprocess.CompletedProcess[str]]|None=None):
        self._run=runner or subprocess.run
    def read(self,service:str,lines:int=50)->str:
        unit=UNITS.get(service)
        if unit is None:raise ValueError("unsupported log service")
        if type(lines) is not int or lines<1 or lines>MAX_LINES:raise ValueError("log line limit must be 1..200")
        result=self._run(["journalctl","--no-pager","--output=short","-n",str(lines),"-u",unit],
                         capture_output=True,text=True,check=False)
        if result.returncode!=0:raise RuntimeError("log backend unavailable")
        return result.stdout.rstrip()
