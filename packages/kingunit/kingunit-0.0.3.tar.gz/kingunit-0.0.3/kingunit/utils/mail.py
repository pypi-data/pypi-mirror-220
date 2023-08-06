# 调用SMTP进行邮件发送
from email.mime.multipart import MIMEMultipart
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from kingunit.config import config
import datetime


def send_mail(receivers, subject, content) -> bool:
    """
    :param receivers: 收件人列表
    :param subject: 邮件主题
    :param content: 邮件内容
    :return: True or False
    """
    mail_config = config["mail"]

    message = MIMEText(content, "plain", "utf-8")
    message["From"] = Header(mail_config["sender"])
    message["To"] = Header(mail_config["recevier"], "utf-8")

    message["Subject"] = Header(subject, "utf-8")

    try:
        smtpObj = smtplib.SMTP_SSL(mail_config["host"], 465)
        resp = smtpObj.login(mail_config["user"], mail_config["pass"])
        resp = smtpObj.sendmail(mail_config["sender"], receivers, message.as_string())
        print("邮件发送成功")
        return True
    except smtplib.SMTPException:
        print("Error: 发送失败")
        return False


def send_email_with_zip(receivers, subject, content, zip_file_path):
    """
    :param receivers: 收件人列表
    :param subject: 邮件主题
    :param content: 邮件内容
    :param zip_file_path: 压缩包路径
    :return: True or False
    """
    mail_config = config["mail"]

    message = MIMEMultipart()
    message["From"] = Header(mail_config["sender"])
    message["To"] = Header(mail_config["recevier"], "utf-8")

    message["Subject"] = Header(subject, "utf-8")
    message.attach(MIMEText(content, "plain", "utf-8"))

    # 构造附件
    att = MIMEText(open(zip_file_path, "rb").read(), "base64", "utf-8")
    att["Content-Type"] = "application/octet-stream"
    att["Content-Disposition"] = "attachment; filename=" + zip_file_path.split("/")[-1]
    message.attach(att)

    try:
        smtpObj = smtplib.SMTP_SSL(mail_config["host"], 465)
        resp = smtpObj.login(mail_config["user"], mail_config["pass"])
        resp = smtpObj.sendmail(mail_config["sender"], receivers, message.as_string())
        print(f"邮件发送成功，接收者：{receivers}")
        return True
    except smtplib.SMTPException:
        print("Error: 发送失败")
        return False


def test_send_mail():
    send_mail(
        ["zjy2414@outlook.com"],
        "KingUnit测试报告(" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ")",
        "请查收附件。",
    )
