import socket
import os
s=socket.socket()
s.settimeout(5)
status=s.connect_ex(("127.0.0.1",80))
if status==0:
    print("port 80 is open")
else:
    print(f"port 80 is closed")
    print(f"error code:{status}")
print(f"reason:{os.strerror(status)}")
