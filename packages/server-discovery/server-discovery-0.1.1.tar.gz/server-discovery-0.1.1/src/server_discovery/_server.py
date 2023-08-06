import socket, uuid
from typing import Optional, Callable, Any

from ._info_model import LocalInfo
from ._broadcast import broadcast as _broadcast





def listenloop(port: int, callback: Callable[[], Any]):
	"""Starts a loop and runs the callback function everytime the scan port is pinged"""
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	sock.bind(("0.0.0.0", port))
	while True:
		sock.recvfrom(1024)[0]
		callback()





def broadcast(local_info: LocalInfo, response_port: int):
	"""Broadcast the server info on the local network.
     Calls out on all available interfaces, so works when using multiple (virtual) networks 
     (like when in a Docker container)."""
	info = local_info.model_dump_json()
	_broadcast(info, response_port)
	



def main(scan_port: int, response_port: int, 
	 device_name: Optional[str] = None, service_version: Optional[str] = None):
	"""
	Start loop of listening for server searches and responding.

	scan_port and response_port can be any arbitrary ports, 
	as long as the same ones are set on client devices.

	device_name and service_version are optional extra info you can pass to the client.
	"""
	local_info = LocalInfo(
		device_id=uuid.getnode(), 
	    device_name=device_name,
	    service_version=service_version
	)
	respond = lambda: broadcast(local_info, response_port)
	listenloop(scan_port, callback=respond)

