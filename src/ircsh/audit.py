"""Structured security audit events for ircsh."""
from __future__ import annotations
import json,logging,re
from dataclasses import asdict,dataclass
_NAME=re.compile(r"^[A-Za-z0-9_-]{1,64}$")
@dataclass(frozen=True,slots=True)
class AuditEvent:
    action:str;target:str;result:str;reason:str=""
    def __post_init__(self):
        if not _NAME.fullmatch(self.action):raise ValueError("invalid audit action")
        if not _NAME.fullmatch(self.result):raise ValueError("invalid audit result")
        if len(self.target)>128 or any(c in self.target for c in "\r\n\0"):raise ValueError("invalid audit target")
        if len(self.reason)>256 or any(c in self.reason for c in "\r\n\0"):raise ValueError("invalid audit reason")
class AuditLogger:
    def __init__(self,logger=None):self.logger=logger or logging.getLogger("ircsh.audit")
    def emit(self,event:AuditEvent)->None:self.logger.info(json.dumps(asdict(event),sort_keys=True,separators=(",",":")))
