"""Validated provisioning plan for IRC-only SSH accounts."""
from __future__ import annotations
from dataclasses import dataclass
from .ssh_policy import authorized_key_options,shell_entry
@dataclass(frozen=True,slots=True)
class AccountProvisioning:
    username:str
    group:str="ircsh"
    home_root:str="/home"
    def __post_init__(self):
        # Reuse strict account validation without executing anything.
        authorized_key_options(self.username)
        if self.group!="ircsh":raise ValueError("unsupported IRC shell group")
        if self.home_root!="/home":raise ValueError("unsupported home root")
    @property
    def home(self)->str:return f"{self.home_root}/{self.username}"
    @property
    def shell(self)->str:return shell_entry()
    @property
    def ssh_dir(self)->str:return f"{self.home}/.ssh"
    @property
    def authorized_keys(self)->str:return f"{self.ssh_dir}/authorized_keys"
    def key_line(self,public_key:str)->str:
        key=public_key.strip()
        if "\n" in key or "\r" in key or "\0" in key:raise ValueError("invalid public key")
        parts=key.split()
        if len(parts)<2 or parts[0] not in {"ssh-ed25519","sk-ssh-ed25519@openssh.com"}:raise ValueError("unsupported public key type")
        import base64,binascii
        try:base64.b64decode(parts[1],validate=True)
        except (binascii.Error,ValueError) as exc:raise ValueError("invalid public key encoding") from exc
        return f"{authorized_key_options(self.username)} {key}\n"
    def modes(self)->dict[str,int]:
        return {self.home:0o700,self.ssh_dir:0o700,self.authorized_keys:0o600}
