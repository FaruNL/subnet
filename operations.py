import socket
import struct

def ip_to_int(ip_address: str) -> int:
    return struct.unpack("!I", socket.inet_aton(ip_address))[0]

def int_to_ip(int: int) -> str:
    return socket.inet_ntoa(struct.pack("!I", int))

def suma(ip_address: str, num: int) -> str:  
    int_value = ip_to_int(ip_address)
    return int_to_ip(int_value + num)

def suma_salto(ip_address: str, num: int, pos: int) -> str:
    if pos == 0:
        num *= (256 * 256 * 256)
    elif pos == 1:
        num *= (256 * 256)
    elif pos == 2:
        num *= 256
    
    int_value = ip_to_int(ip_address)
    return int_to_ip(int_value + num)

def resta(ip_address: str, num: int) -> str:  
    int_value = ip_to_int(ip_address)
    return int_to_ip(int_value - num)
