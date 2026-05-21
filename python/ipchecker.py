import socket
try:
    
   tar_url="christy.com"
   tar_ip=socket.gethostbyname(tar_url)
   print(f"the ip address of {tar_url} is {tar_ip}")
except socket.gaierror:
    print("invalid website")
