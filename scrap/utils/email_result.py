import smtplib
from email.mime.text import MIMEText
from configurations.secrets import EmailSecrets

smtp_server = "smtp.gmail.com"
smtp_port = 587


def email_result(emessages):
    # 이메일 내용 설정
    subject = "스크래핑 결과"
    # 메일 구성
    msg = MIMEText(emessages)
    msg["Subject"] = subject
    msg["From"] = EmailSecrets.sender_email
    msg["To"] = EmailSecrets.receiver_email

    # 이메일 전송
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(msg["From"], EmailSecrets.password)
            server.sendmail(msg["From"], msg["To"], msg.as_string())
        print("이메일이 성공적으로 전송되었습니다.")
    except Exception as e:
        print(f"이메일 전송 중 오류 발생: {e}")
