import socket
srv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
srv.bind(("", 5005))
while True:
    data, addr = srv.recvfrom(2048)
    print("Message: ", data)