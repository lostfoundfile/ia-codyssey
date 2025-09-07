import socket
import threading

clients = []
nicknames = []

def broadcast(message, exclude_socket=None):
    for client in clients:
        if client != exclude_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                remove_client(client)

def handle_client(client):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if not message:
                break

            if message.startswith('/종료'):
                index = clients.index(client)
                nickname = nicknames[index]
                leave_message = f'{nickname}님이 퇴장하셨습니다.'
                broadcast(leave_message)
                client.close()
                remove_client(client)
                break

            elif message.startswith('/귓속말'):
                parts = message.split(' ', 2)
                if len(parts) < 3:
                    client.send('형식: /귓속말 닉네임 메시지'.encode('utf-8'))
                    continue
                to_nick = parts[1]
                msg = parts[2]
                send_private_message(client, to_nick, msg)
            else:
                index = clients.index(client)
                nickname = nicknames[index]
                full_message = f'{nickname}> {message}'
                broadcast(full_message, client)
        except:
            remove_client(client)
            break

def send_private_message(sender, target_nickname, message):
    if target_nickname in nicknames:
        sender_nick = nicknames[clients.index(sender)]
        target_index = nicknames.index(target_nickname)
        target_client = clients[target_index]
        private_msg = f'[귓속말] {sender_nick}> {message}'
        target_client.send(private_msg.encode('utf-8'))
    else:
        sender.send(f'{target_nickname}님을 찾을 수 없습니다.'.encode('utf-8'))

def remove_client(client):
    if client in clients:
        index = clients.index(client)
        nickname = nicknames[index]
        clients.remove(client)
        nicknames.remove(nickname)

def accept_connections(server_socket):
    while True:
        client, _ = server_socket.accept()
        client.send('닉네임을 입력하세요: '.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')

        clients.append(client)
        nicknames.append(nickname)

        welcome = f'{nickname}님이 입장하셨습니다.'
        broadcast(welcome)
        client.send('서버에 연결되었습니다. 채팅을 시작하세요.'.encode('utf-8'))

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('소캣 생성완료')

    host = socket.gethostname()
    host_ip = socket.gethostbyname(host)
    port = 999

    print(f'호스트 이름: {host}')
    print(f'호스트 IP: {host_ip}')

    server_socket.bind((host_ip, port))
    server_socket.listen(3)
    print(f'서버가 {port}번 포트에서 실행 중입니다...')

    accept_connections(server_socket)

if __name__ == '__main__':
    start_server()