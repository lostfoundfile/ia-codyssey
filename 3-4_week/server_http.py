from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime

PORT = 8080


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 접속 로그 출력
        client_ip = self.client_address[0]
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f'[{now}] 접속한 클라이언트 IP: {client_ip}')

        # index.html 읽기
        try:
            with open('index.html', 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            content = '<h1>index.html 파일을 찾을 수 없습니다.</h1>'

        # 응답 헤더 전송
        self.send_response(200)  # 성공 코드
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

        # 응답 본문 전송
        self.wfile.write(content.encode('utf-8'))


def run():
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f'HTTP 서버가 {PORT} 포트에서 실행 중입니다...')
    httpd.serve_forever()


if __name__ == '__main__':
    run()