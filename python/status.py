import socket
s=socket.socket()
s.settimeout(1)
status=s.connect_ex(("127.0.0.1",80))
if status==0:
    print("port 80 is open")
else:
    print(f"port 80 is closed| error code:{status}")
    
