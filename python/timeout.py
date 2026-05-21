import socket
s = socket.socket()
s.settimeout(1)
# connect_ex returns 0 if the port is open
status = s.connect_ex(("127.0.0.1", 80))
print("[+] Port 80 is OPEN" if status == 0 else "[-] Port 80 is CLOSED")

