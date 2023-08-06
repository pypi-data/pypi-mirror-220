import socket, netifaces


def _get_interfaces():
	"""Get local IP (v4) addresses of all network interfaces"""
	ips = []
	for interface in netifaces.interfaces():
		for address in netifaces.ifaddresses(interface).values():
			ip = address[0]['addr']
			if '.' in ip:  # IPv4
				ips.append(ip)
	return ips


def broadcast(message: str, receiving_port: int):
	"""Broadcast a UDP message on the local network.
     Calls out on all available interfaces, so works when using multiple (virtual) networks 
     (like when in a Docker container)."""
	info_encoded = message.encode()
	for interface in _get_interfaces():
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
		sock.bind((interface, 0))
		sock.sendto(info_encoded, ("255.255.255.255", receiving_port))
		sock.close()