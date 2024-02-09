import smtplib
from dataclasses import dataclass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import boto3

ssm = boto3.client('ssm')
login = ssm.get_parameter(Name='/taxreturns/email/login', WithDecryption=True)
password = ssm.get_parameter(Name='/taxreturns/email/user-password', WithDecryption=True)


@dataclass
class EmailConfig:
    user_password: str = password['Parameter']['Value']
    from_email: str = 'dev@pontte.com.br'
    from_name: str = "Pontte"
    to_email: str = 'lucas@pontte.com.br'
    smtp_server: str = 'email-smtp.us-east-1.amazonaws.com'
    smtp_port: int = 587
    login_email: str = login['Parameter']['Value']
    subject: str = 'Imposto de Renda Exercício 2022 - Demonstrativo de Valores Pagos'

    def send_email(self, html: str) -> None:
        print("usguriii", password, user_password)

        msg = MIMEMultipart()
        msg['From'] = f"{self.from_name} <{self.from_email}>"
        msg['To'] = self.from_email
        msg['Subject'] = self.subject
        msg.attach(MIMEText(html, 'html'))
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.login_email or self.from_email, self.user_password)
            server.sendmail(self.from_email, self.from_email, msg.as_string())

    def send_emails(self, html: str, emails) -> None:
        print("self.to_email", self.to_email)
        msg = MIMEMultipart()
        msg['From'] = f"{self.from_name} <{self.from_email}>"
        msg['Subject'] = self.subject
        msg.attach(MIMEText(html, 'html'))
        msg['To'] = self.to_email
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.login_email, self.user_password)
            for email in emails:
                print(email)
            server.sendmail(self.to_email, email, msg.as_string())
            server.sendmail(self.from_email, self.from_email, msg.as_string())
