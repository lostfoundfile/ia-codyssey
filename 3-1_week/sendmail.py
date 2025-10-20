#!usrbinenv python3
# -- coding utf-8 --


sendmail.py
-----------
Gmail SMTP 서버를 이용하여 메일을 전송하는 프로그램.
Python 표준 라이브러리만 사용하며, 예외 처리를 포함한다.


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


def send_email(sender, password, receiver, subject, body, attachment_path=None)
    Gmail SMTP 서버를 이용하여 메일을 보내는 함수

    smtp_server = 'smtp.gmail.com'
    smtp_port = 587  # TLS를 사용하는 SMTP 기본 포트

    try
        # 메일 본문 작성
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = receiver
        msg['Subject'] = subject

        # 텍스트 본문 추가
        msg.attach(MIMEText(body, 'plain'))

        # 첨부 파일 추가 (보너스 과제)
        if attachment_path
            try
                with open(attachment_path, 'rb') as f
                    part = MIMEApplication(f.read(), Name=attachment_path)
                part['Content-Disposition'] = f'attachment; filename={attachment_path}'
                msg.attach(part)
            except FileNotFoundError
                print(f'첨부 파일을 찾을 수 없습니다 {attachment_path}')
                return

        # SMTP 서버 연결 및 로그인
        with smtplib.SMTP(smtp_server, smtp_port) as server
            server.starttls()  # TLS 보안 연결 시작
            server.login(sender, password)
            server.send_message(msg)
            print('메일이 성공적으로 전송되었습니다.')

    except smtplib.SMTPAuthenticationError
        print('로그인 인증에 실패했습니다. 이메일 주소나 비밀번호를 확인하세요.')
    except smtplib.SMTPConnectError
        print('SMTP 서버에 연결할 수 없습니다.')
    except smtplib.SMTPException as e
        print(f'SMTP 오류가 발생했습니다 {e}')
    except Exception as e
        print(f'예기치 못한 오류가 발생했습니다 {e}')


def main()
    프로그램 실행 진입점
    sender = input('보내는 Gmail 주소 ')
    password = input('앱 비밀번호 ')
    receiver = input('받는 이메일 주소 ')
    subject = input('메일 제목 ')
    body = input('메일 내용 ')

    attach_choice = input('첨부 파일을 추가하시겠습니까 (yn) ')
    attachment_path = None
    if attach_choice.lower() == 'y'
        attachment_path = input('첨부 파일 경로를 입력하세요 ')

    send_email(sender, password, receiver, subject, body, attachment_path)


if __name__ == '__main__'
    main()