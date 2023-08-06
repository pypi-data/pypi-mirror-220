import socket

from ._info_model import LocalInfo, ServerInfo
from ._broadcast import broadcast as _broadcast


def broadcast(port):
	_broadcast("hello", port)



def listen_back(port: int, timeout=1):
	"""
	Listens for responses from servers until the selected timeout ends. 
    Returns data and source addresses as a generator, 
	so data can be processed without waiting for the timeout.
	"""

	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	sock.settimeout(timeout)
	sock.bind(("0.0.0.0", port))

	while True:
		try:
			data, address = sock.recvfrom(1024)
			yield data, address[0]
		except TimeoutError as e:
			break




def process_response(data, source_address: str):
	info = LocalInfo.model_validate_json(data)
	return ServerInfo(ip_address=source_address, **info.model_dump())



def main(scan_port: int, response_port: int, timeout=1):
	"""
	Search for servers on the local network and give their details as ServerInfo.
	Keeps returning found servers as a generator, 
	so they can be shown and used without waiting for timeout.

	scan_port and response_port can be any arbitrary ports, 
	as long as the same ones are set on client devices.
	"""
	already_found: list[ServerInfo] = []
	broadcast(scan_port)
	for response in listen_back(response_port, timeout):
		try:
			server = process_response(*response)
			if server not in already_found:
				already_found.append(server)
				yield server
		except:
			pass
