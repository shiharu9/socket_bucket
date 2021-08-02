import socket


def run() -> None:
    """Function start a server_side socket, accept client socket requests and sends back a response."""

    SIZE = 2000
    PORT = 9100

    sock = socket.socket()
    sock.bind(('', PORT))
    while True:
        sock.listen(1)
        conn, addr = sock.accept()
        print(f'Connect {addr}')
        # server_working = True


run()
