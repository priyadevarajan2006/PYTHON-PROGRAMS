import socket
s=socket.socket()
s.settimeout(5)
status=s.connect_ex(("127.0.0.1",80))
if status==0:
    print("port 80 is open")
else:
    print("port 80 is closed")
    print(f"error code:{status}")
    if status==10061:
         print("reason:connection refused")
    elif status==10035:
         print("operation would block")
    else:
         print("unknown")
         
