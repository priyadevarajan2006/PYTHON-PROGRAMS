from scapy.all import IP,TCP
packet=IP(dst="172.16.18.1")/TCP(dport=80)
print(f"packet structure:{packet.summary()}")
