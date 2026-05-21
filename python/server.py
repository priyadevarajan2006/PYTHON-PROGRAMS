import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = "0.0.0.0"
port = 5000

server.bind((host, port))
server.listen(1)

print("Waiting for connection...")
conn, addr = server.accept()

print("Connected with:", addr)

while True:
    message = conn.recv(1024).decode()

    if message.lower() == "bye":
        print("Client ended the chat")
        break

    print("Client:", message)

    reply = input("You: ")
    conn.send(reply.encode())

    if reply.lower() == "bye":
        break

conn.close()
server.close()

