import socket

SIZE = 2000
PORT = 9100

sock = socket.socket()
sock.connect(('localhost', PORT))
result = sock.recv(SIZE)
print(result.decode("utf-8"))

