import socket
import threading

clients = []
nicknames = []

def broadcast(message, sender_socket=None):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                remove_client(client)

def handle_client(client):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == '/종료':
                index = clients.index(client)
                nickname = nicknames[index]
                leave_message = f'{nickname}님이 퇴장하셨습니다.'
                print(leave_message)
                broadcast(leave_message, client)
                client.close()
                remove_client(client)
                break
            elif message.startswith('/귓속말'):
                parts = message.split(' ', 2)
                if len(parts) < 3:
                    client.send('귓속말 형식: /귓속말 닉네임 메시지'.encode('utf-8'))
                    continue
                to_nickname = parts[1]
                private_message = parts[2]
                send_private_message(client, to_nickname, private_message)
            else:
                index = clients.index(client)
                nickname = nicknames[index]
                full_message = f'{nickname}> {message}'
                print(full_message)
                broadcast(full_message, client)
        except:
            remove_client(client)
            break

def send_private_message(sender, to_nickname, message):
    if to_nickname in nicknames:
        index = nicknames.index(to_nickname)
        recipient = clients[index]
        sender_index = clients.index(sender)
        sender_nickname = nicknames[sender_index]
        try:
            recipient.send(f'[귓속말] {sender_nickname}> {message}'.encode('utf-8'))
        except:
            remove_client(recipient)
    else:
        sender.send(f'사용자 {to_nickname}를 찾을 수 없습니다.'.encode('utf-8'))

def remove_client(client):
    if client in clients:
        index = clients.index(client)
        nickname = nicknames[index]
        clients.remove(client)
        nicknames.remove(nickname)

def receive():
    while True:
        client, address = server.accept()
        print(f'연결됨: {str(address)}')

        client.send('닉네임을 입력하세요: '.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        print(f'닉네임: {nickname}')
        welcome_message = f'{nickname}님이 입장하셨습니다.'
        broadcast(welcome_message)
        client.send('서버에 접속되었습니다! 채팅을 시작하세요.'.encode('utf-8'))

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()


if __name__ == '__main__':
    host = '127.0.0.1'
    port = 55555

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()

    print(f'서버가 {host}:{port} 에서 실행 중입니다...')
    receive()
