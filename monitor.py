import smtplib
from email.mime.text import MIMEText
import time
import psutil
import subprocess

SMTP_SERVER = 'smtp.example.com'  # SMTP服务器地址
SMTP_PORT = 587  # SMTP服务器端口
SMTP_USER = 'your-email@example.com'  # 发件人邮箱
SMTP_PASSWORD = 'your-password'  # 发件人邮箱密码

EMAIL_FROM = 'your-email@example.com'  # 发件人邮箱
EMAIL_TO = 'recipient-email@example.com'  # 收件人邮箱
EMAIL_SUBJECT = 'Port 22 Alert'  # 邮件主题

CHECK_PORT = 22  # 需要检查的端口
CHECK_INTERVAL = 60  # 检查间隔，单位：秒

# Command to start the service
base_service_command = ['sudo', '-E', 'python3', 'pshitt.py', '-p', '22', '-o']

def send_email():
    msg = MIMEText('Port 22 is no longer listening. Restarting service.')
    msg['Subject'] = EMAIL_SUBJECT
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(SMTP_USER, SMTP_PASSWORD)
    server.send_message(msg)
    server.quit()

def send_restart_email():
    msg = MIMEText('Service restarted.')
    msg['Subject'] = EMAIL_SUBJECT
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(SMTP_USER, SMTP_PASSWORD)
    server.send_message(msg)
    server.quit()

def is_port_listening(port):
    for conn in psutil.net_connections():
        if conn.status == psutil.CONN_LISTEN and conn.laddr.port == port:
            return True
    return False

def restart_service(restart_count):
    log_file = 'logs' + str(restart_count) + '.txt'
    service_command = base_service_command + [log_file]
    subprocess.run(service_command)
    send_restart_email()

def main():
    restart_count = 1
    while True:
        if not is_port_listening(CHECK_PORT):
            send_email()
            print('Email sent')
            restart_count += 1
            restart_service(restart_count)
            print('Service restarted')
        time.sleep(CHECK_INTERVAL)

if __name__ == '__main__':
    main()
