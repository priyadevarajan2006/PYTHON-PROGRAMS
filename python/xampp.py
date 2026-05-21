
import socket
 
s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
 
s.connect((" fe80::1acb:16cf:1bfe:1c28%19", 80))
 
print("Connected to local IPv6 Apache server")

