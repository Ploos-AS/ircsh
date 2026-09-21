"""Fail-closed SSH deployment validation and recovery planning."""
from __future__ import annotations
from dataclasses import dataclass
from collections.abc import Callable,Sequence
@dataclass(frozen=True,slots=True)
class ValidationResult:
    valid:bool
    detail:str=""
class SshdValidator:
    def __init__(self,runner:Callable[...,object]):self._runner=runner
    def validate(self,config:str="/etc/ssh/sshd_config")->ValidationResult:
        if config!="/etc/ssh/sshd_config":raise ValueError("unsupported sshd config path")
        try:r=self._runner(["sshd","-t","-f",config],capture_output=True,text=True,check=False)
        except Exception as exc:return ValidationResult(False,type(exc).__name__)
        rc=getattr(r,"returncode",None)
        if type(rc) is not int:return ValidationResult(False,"invalid validator result")
        if rc!=0:return ValidationResult(False,"sshd configuration rejected")
        return ValidationResult(True)
@dataclass(frozen=True,slots=True)
class DeploymentPlan:
    fragment:str="/etc/ssh/sshd_config.d/60-ircsh.conf"
    backup:str="/etc/ssh/sshd_config.d/60-ircsh.conf.previous"
    def __post_init__(self):
        if self.fragment!="/etc/ssh/sshd_config.d/60-ircsh.conf":raise ValueError("unsupported fragment path")
        if self.backup!="/etc/ssh/sshd_config.d/60-ircsh.conf.previous":raise ValueError("unsupported backup path")
    def validation_argv(self)->Sequence[str]:return ("sshd","-t","-f","/etc/ssh/sshd_config")
    def reload_argv(self)->Sequence[str]:return ("systemctl","reload","sshd")
    def recovery_validation_argv(self)->Sequence[str]:return self.validation_argv()
