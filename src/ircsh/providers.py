"""Read-only status/quota providers and concrete service provider wiring."""
from __future__ import annotations
from dataclasses import dataclass
from .services import ServiceInfo,ServiceKind,ServiceRegistry
from .backends import SojuBackend,ZncBackend,PsybncBackend,MuhBackend,BipBackend,PounceBackend,EggdropBackend,LimnoriaBackend,SopelBackend,ErrbotBackend,EnergyMechBackend,PsotnicBackend,PersistentClientBackend

@dataclass(frozen=True,slots=True)
class Status:
    session:str="active"
    runtime:str="not configured"

class StatusProvider:
    def read(self)->Status:return Status()

class QuotaProvider:
    def read(self)->str:return "Quota backend: not configured (M1)"

def production_registry(runtime)->ServiceRegistry:
    """Build the fixed production service map around a trusted runtime."""
    backends=(
        SojuBackend("main",runtime),
        ZncBackend("znc1",runtime),
        PsybncBackend("legacy",runtime),
        MuhBackend("muh1",runtime),
        BipBackend("bip1",runtime),
        PounceBackend("pounce1",runtime),
        EggdropBackend("eggdrop1",runtime),
        LimnoriaBackend("limnoria1",runtime),
        SopelBackend("sopel1",runtime),
        ErrbotBackend("errbot1",runtime),
        EnergyMechBackend("energymech1",runtime),
        PsotnicBackend("psotnic1",runtime),
        PersistentClientBackend("weechat",runtime,"weechat"),
        PersistentClientBackend("irssi",runtime,"irssi"),
        PersistentClientBackend("bitchx",runtime,"bitchx"),
    )
    return ServiceRegistry(backends)

class ServiceProvider:
    def __init__(self,registry:ServiceRegistry|None=None):
        self.registry=registry or ServiceRegistry()
    def read(self)->tuple[ServiceInfo,...]:return self.registry.statuses()
    def bots(self)->tuple[ServiceInfo,...]:return self.registry.statuses(ServiceKind.BOT)
    def bot(self,name:str):return self.registry.get(name,ServiceKind.BOT)
    def bouncers(self)->tuple[ServiceInfo,...]:return self.registry.statuses(ServiceKind.BOUNCER)
    def bouncer(self,name:str):return self.registry.get(name,ServiceKind.BOUNCER)
    def clients(self)->tuple[ServiceInfo,...]:return self.registry.statuses(ServiceKind.CLIENT)
    def client(self,name:str):return self.registry.get(name,ServiceKind.CLIENT)
