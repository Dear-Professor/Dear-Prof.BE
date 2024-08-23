import imaplib
import email
from email.header import decode_header
from dotenv import load_dotenv
import os
from datetime import datetime


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def post_emails(receiver, subject, body):
    
    # .env 파일 로드
    load_dotenv()

    # Naver 메일 서버 정보
    SMTP_SERVER = "smtp.naver.com"
    SMTP_PORT = 587

    # 이메일 계정 정보
    EMAIL_ACCOUNT = os.getenv('EMAIL_ACCOUNT')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

    # 이메일 메시지 생성
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ACCOUNT
    msg['To'] = receiver
    msg['Subject'] = subject

    # 본문 첨부
    msg.attach(MIMEText(body, 'plain'))

    try:
        # SMTP 서버 연결
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # TLS 모드로 전환
        server.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)

        # 이메일 전송
        server.sendmail(EMAIL_ACCOUNT, receiver, msg.as_string())
        print(f"Email sent to {receiver} successfully.")

    except Exception as e:
        print(f"Failed to send email: {e}")

    finally:
        # 서버 연결 종료
        server.quit()




def fetch_emails(sender, since_date):

    # MIME 디코딩 함수
    def decode_mime_words(s):
        decoded_string = ''
        for word, charset in decode_header(s):
            if isinstance(word, bytes):
                decoded_string += word.decode(charset or 'utf-8')
            else:
                decoded_string += word
        return decoded_string


    # Naver 메일 서버 정보
    IMAP_SERVER = "imap.naver.com"
    IMAP_PORT = 993

    # .env 파일 활성화
    load_dotenv()
    EMAIL_ACCOUNT = os.getenv('EMAIL_ACCOUNT')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

    # IMAP 서버에 연결
    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)

    # 이메일 계정으로 로그인
    try:
        mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
    except imaplib.IMAP4.error as e:
        print("Login failed:", e)
        return

    # 받은 편지함 선택
    mail.select("inbox")

    # DateTimeField 형식의 날짜를 IMAP 날짜 형식으로 변환
    since_str = since_date.strftime('%d-%b-%Y')

    # 발신자와 날짜 기준으로 검색 (FROM과 SINCE 필터 사용)
    status, messages = mail.search(None, f'(FROM "{sender}" SINCE {since_str})')

    # 이메일 ID 목록을 가져옵니다.
    email_ids = messages[0].split()

    if not email_ids:
        print("No emails found.")
        return None

    # 가장 최신의 이메일 ID 가져오기
    latest_email_id = email_ids[-1]

    # 최신 이메일의 데이터 가져오기
    status, msg_data = mail.fetch(latest_email_id, "(RFC822)")

    mail = {'subject':None, 'from':None, 'body':None}

    for response_part in msg_data:
        if isinstance(response_part, tuple):
            msg = email.message_from_bytes(response_part[1])

            # 이메일 제목 디코딩
            subject = decode_mime_words(msg["Subject"])

            # 발신자 정보 디코딩
            from_ = decode_mime_words(msg.get("From"))

            # print("Latest Email from:", sender)
            mail["subject"] = subject
            mail["from"] = from_
            # print("Subject:", subject)
            # print("From:", from_)
           
            
            # 이메일 본문 가져오기
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))

                    if content_type == "text/plain" and "attachment" not in content_disposition:
                        body += part.get_payload(decode=True).decode("utf-8")
            else:
                body = msg.get_payload(decode=True).decode("utf-8")
            
            # 본문 내용 출력 (여러 줄이 하나의 문자열로 결합되어 출력됩니다)
            # print("Body:", body.strip())
            mail["body"] = body.strip()

    # 연결 종료
    mail.close()
    mail.logout()

    return mail

# example_date = datetime(2023, 8, 22)  # 원하는 날짜로 변경
# sender = "hybyun0207@gmail.com"
# fetch_emails(sender, example_date)


receiver = "hybyun0207@gmail.com"
subject = "시험 메일"
body = "시험 메일입니다!!!"
# post_emails(receiver, subject, body)