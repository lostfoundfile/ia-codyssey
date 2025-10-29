import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import csv

def read_csv(file_name):
    """CSV 파일을 읽어서 이름과 이메일 리스트를 반환하는 함수"""
    targets = []
    try:
        with open(file_name, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # 헤더 건너뛰기
            for row in reader:
                name, email = row
                targets.append((name, email))
    except FileNotFoundError:
        print(f'파일 {file_name}을 찾을 수 없습니다.')
    return targets

def create_html_message():
    """HTML 형식의 이메일 메시지를 생성하는 함수"""
    html_content = '''
    <html>
        <body>
            <h1>생존 확인</h1>
            <p>안녕하세요!</p>
            <p>저는 한송희 박사입니다. 화성에서 보내는 생존 메시지입니다. 우리는 잘 지내고 있으며, 여러분의 응원에 감사드립니다!</p>
        </body>
    </html>
    '''
    return html_content

def send_email(from_email, from_password, to_email, subject, html_content):
    """이메일을 보내는 함수"""
    try:
        # SMTP 서버 연결 (네이버 이메일의 경우)
        server = smtplib.SMTP('smtp.naver.com', 587)
        server.starttls()
        server.login(from_email, from_password)

        # 이메일 메시지 생성
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(html_content, 'html'))

        # 이메일 전송
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        print(f'이메일 전송 완료: {to_email}')
    except Exception as e:
        print(f'이메일 전송 실패: {e}')

def send_bulk_emails(csv_file, from_email, from_password, subject):
    """CSV 파일에 있는 모든 이메일로 메일을 보내는 함수"""
    targets = read_csv(csv_file)
    html_content = create_html_message()

    # 한 명씩 이메일 보내기
    for name, email in targets:
        send_email(from_email, from_password, email, subject, html_content)

# 메일 전송을 위한 사용자 정보 입력
from_email = 'your_email@naver.com'  # 발신 이메일
from_password = 'your_password'  # 발신 이메일 비밀번호 (혹은 앱 비밀번호)
subject = '생존 확인 메시지'

# 메일 전송
send_bulk_emails('mail_target_list.csv', from_email, from_password, subject)