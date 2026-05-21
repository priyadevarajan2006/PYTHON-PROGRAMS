import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_ip = input("Enter server system IP address: ")
port = 5000

client.connect((server_ip, port))

print("Connected to server")

while True:
    message = input("You: ")
    client.send(message.encode())

    if message.lower() == "bye":
        break

    reply = client.recv(1024).decode()

    if reply.lower() == "bye":
        print("Server ended the chat")
        break

    print("Server:", reply)

client.close()
