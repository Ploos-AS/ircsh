"""Trusted connection accounting from Linux /proc."""
from __future__ import annotations
from pathlib import Path

class ConnectionMeasurementError(RuntimeError):pass

_ACTIVE_TCP_STATES=frozenset({"01","02","03","04","05","08","09","0B"})

class ProcConnectionMeter:
    """Count active TCP sockets owned by a trusted account UID."""
    def __init__(self,uid:int,proc:Path=Path("/proc")):
        if type(uid) is not int or uid<0:raise ValueError("uid must be a non-negative integer")
        if not proc.is_absolute():raise ValueError("proc root must be absolute")
        self.uid=uid;self.proc=proc
    def _table(self,path:Path)->int:
        try:lines=path.read_text(encoding="ascii").splitlines()[1:]
        except (OSError,UnicodeError) as exc:raise ConnectionMeasurementError("connection table unavailable") from exc
        count=0
        for line in lines:
            fields=line.split()
            if len(fields)<8:raise ConnectionMeasurementError("malformed connection table")
            try:state=fields[3];uid=int(fields[7])
            except (ValueError,IndexError) as exc:raise ConnectionMeasurementError("malformed connection table") from exc
            if state in _ACTIVE_TCP_STATES and uid==self.uid:count+=1
        return count
    def count(self)->int:
        return self._table(self.proc/"net"/"tcp")+self._table(self.proc/"net"/"tcp6")
