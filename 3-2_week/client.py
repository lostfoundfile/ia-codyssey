import socket
import threading

def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message:
                print(message)
        except:
            print('서버와의 연결이 종료되었습니다.')
            client.close()
            break

def send_messages():
    while True:
        message = input()
        client.send(message.encode('utf-8'))
        if message == '/종료':
            break

if __name__ == '__main__':
    host = '127.0.0.1'
    port = 55555

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    receive_thread = threading.Thread(target=receive_messages)
    receive_thread.start()

    send_thread = threading.Thread(target=send_messages)
    send_thread.start()
