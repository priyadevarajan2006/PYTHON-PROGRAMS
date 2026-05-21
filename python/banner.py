import socket
s=socket.socket()
s.connect(("127.0.0.1",80))
s.send(b"HEAD /http /1.0\r\n\r\n")
banner=s.recv(1024).decode()
print("response")
print(banner)
s.close
