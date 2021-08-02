import socket

SIZE = 2000
PORT = 9100

sock = socket.socket()
sock.connect(('localhost', PORT))
result = sock.recv(SIZE)
print(result.decode("utf-8"))

while True:
    sock.send(input("Enter: ").encode('utf-8'))
    result = sock.recv(SIZE)
    print(result.decode("utf-8"))
    result1 = sock.recv(SIZE)
    print(result1.decode("utf-8"))

    if result1 in ('exit', '\nCongratulations!'):
        sock.close()
        break
