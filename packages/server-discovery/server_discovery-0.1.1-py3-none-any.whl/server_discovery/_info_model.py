import pydantic
from typing import Optional


class LocalInfo(pydantic.BaseModel):
    device_id: int
    device_name: Optional[str] = None
    service_version: Optional[str] = None

    
        

class ServerInfo(LocalInfo):
    ip_address: str

    def __eq__(self, other):
        if isinstance(other, ServerInfo):
            return (self.device_id == other.device_id)
        elif isinstance(other, int):
            return (self.device_id == other)
        else:
            return False
