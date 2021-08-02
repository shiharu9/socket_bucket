import socket


def filling(command_fill: str, bucket_3: int, bucket_5: int, conn: socket) -> tuple:
    """Function what perform pour in/out from buckets

    :param command_fill: commands pour in/out from buckets
    :param bucket_5: current bucket volume
    :param bucket_3: current bucket volume
    :param conn: socket client
    :return: value empty or full buckets
    """
    pour = 'You poured water into a {}l. bucket.'
    pour_out = 'You poured water out of a {}l. bucket.'
    if command_fill == '+5':
        bucket_5 = 5
        conn.sendall(pour.format(5).encode('utf-8'))
    elif command_fill == '+3':
        bucket_3 = 3
        conn.sendall(pour.format(3).encode('utf-8'))

    elif command_fill == '-5':
        bucket_5 = 0
        conn.sendall(pour_out.format(5).encode('utf-8'))
    elif command_fill == '-3':
        bucket_3 = 0
        conn.sendall(pour_out.format(3).encode('utf-8'))
    return bucket_5, bucket_3


def transfer(command_transfer: str, bucket_3: int, bucket_5: int, conn: socket) -> tuple:
    """Function pouring from one bucket to another

    :param command_transfer: commands transfusion from one bucket to another
    :param bucket_3: current bucket volume
    :param bucket_5: current bucket volume
    :param conn: socket client
    :return: volume
    """
    common_volume = bucket_5 + bucket_3
    text = 'You poured from a {}l. bucket into a {}l. bucket.'
    if command_transfer == '3+5':
        if common_volume > 2:
            bucket_3 = 3
            bucket_5 = common_volume - 3
        else:
            bucket_3 += common_volume
            bucket_5 = 0
    else:
        if common_volume > 5:
            bucket_5 = 5
            bucket_3 = common_volume - 5
        else:
            bucket_5 += bucket_3
            bucket_3 = 0
    conn.sendall((text.format(command_transfer[-1:], command_transfer[:1])).encode('utf-8'))

    return bucket_5, bucket_3


def remind_command() -> str:
    """Function display rule

    :return: rule
    """

    text_commands = '''
    Welcome to the world pf Steve Jobs mysteries!
    There are two buckets. First 5 liters, second
          3 liters and unlimited water.
         Commands are available to you:
        1. pour water into a 5l. bucket: +5
        2. pour water into a 3l. bucket: +3
        3. pour water out of a 5l. bucket: -5
        4. pour water out of a 5l. bucket: -3
        5. pour from a 5l. bucket into a 3l.: 3+5
        6. pour from a 3l. bucket into a 5l.: 5+3
        7. remind commands: help
        8. go out: exit
    You need to use commands to get 4 liters in a
                    5l. bucket.
    '''
    return text_commands


def run() -> None:
    """Function start a server_side socket, accept client socket requests and sends back a response."""

    SIZE = 1024
    PORT = 9100

    sock = socket.socket()
    sock.bind(('', PORT))
    while True:
        sock.listen(1)
        conn, addr = sock.accept()
        print(f'Connect {addr}')
        # server_working = True

        conn.sendall(remind_command().encode('utf-8'))
        bucket_3 = 0
        bucket_5 = 0

        while bucket_5 != 4:
            conn.sendall(f'\nBucket 5l: {bucket_5}l Bucket 3l: {bucket_3}l\n'.encode('utf-8'))
            command = conn.recv(SIZE).decode('utf-8')

            if command in ('+5', '+3', '-5', '-3'):
                bucket_5, bucket_3 = filling(command, bucket_3, bucket_5, conn)
            elif command in ('3+5', "5+3"):
                bucket_5, bucket_3 = transfer(command, bucket_3, bucket_5, conn)
            elif command == 'help':
                conn.sendall(remind_command().encode('utf-8'))
            elif command == 'exit':
                conn.sendall('exit'.encode('utf-8'))
                conn.close()
                break
            else:
                conn.sendall('You entered the wrong command!'.encode('utf-8'))
        if bucket_5 == 4:
            conn.sendall('\nCongratulations!'.encode('utf-8'))
            conn.close()
            break


run()