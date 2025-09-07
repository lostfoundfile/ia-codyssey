import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(message)
        except:
            print('서버와의 연결이 종료되었습니다.')
            client_socket.close()
            break

def send_messages(client_socket):
    while True:
        message = input()
        client_socket.send(message.encode('utf-8'))
        if message == '/종료':
            break

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    port = 999

    try:
        client_socket.connect((host, port))
        print(client_socket.recv(1024).decode('utf-8'))  # 닉네임 요청
        nickname = input('닉네임 입력: ')
        client_socket.send(nickname.encode('utf-8'))

        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        send_thread = threading.Thread(target=send_messages, args=(client_socket,))
        receive_thread.start()
        send_thread.start()

    except ConnectionRefusedError:
        print('서버에 연결할 수 없습니다. 서버가 실행 중인지 확인하세요.')

if __name__ == '__main__':
    start_client()