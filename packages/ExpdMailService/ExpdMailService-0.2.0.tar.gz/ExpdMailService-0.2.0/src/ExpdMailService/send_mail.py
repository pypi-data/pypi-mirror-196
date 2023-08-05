# -*- encoding=utf-8 -*-
from os import path, sys
import pathlib
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import smtplib
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.header import Header
from email.header import make_header
from loguru import logger
import uuid
import pandas as pd


class SendingMail:
    """
    SendingMail类：发送邮件

    参数:
    - mail_server (str): 发邮件服务器
    - sender (str): 发件人邮件地址
    - to (str): 接收邮件地址，使用逗号分隔多个邮箱, 例如："123@abc.com,456@abc.com"
    - cc (str): 抄送邮件地址，使用逗号分隔多个邮箱, 例如："123@abc.com,456@abc.com"
    - subject (str): 邮件主题
    - attachment (list of str): 附件的完整路径列表（若无附件则默认为[]）
    - body(str): 邮件文字类内容
    - table(pandas dataframe): 表格
    - branchcode (str): 邮件签名
    
    使用:
    SendingMail(sender="999@123.com", to="123@abc.com,456@abc.com", cc="789@abc.com", subject="Test mail", attachment=['C:/xxx/file.txt'], body="Test body", table=[], branchcode='SHA')

    """
    def __init__(self, mail_server, sender, to, subject, cc='', attachment=None, body='', table=None, branchcode=None):
        self.currentpath = pathlib.Path(__file__).parent.absolute()
        self.sender = sender
        self.to = [t.strip() for t in to.split(",")]
        self.cc = [c.strip() for c in cc.split(",")]
        self.subject = subject
        self.body = body
        self.table = table or pd.DataFrame([]) 
        self.attachment = attachment or []
        self.receiver = self.to + self.cc  
        self.branchcode = branchcode
        self.mail_server = mail_server
        self.try_send()

    def generateTableBody(self):
        unique = path.join(r"c:\temp", f"{uuid.uuid4().hex[:10]}.html")  
        htmltp = path.join(self.currentpath, "template.html")
        styles = path.join(self.currentpath, "style.css")
        with open(htmltp, encoding='utf-8') as html5, open(styles, encoding='utf-8') as style, open(unique, 'w', encoding='utf-8') as h:
            html5 = html5.read()
            style = style.read()
            h.write(html5.format(table=self.table.to_html(index=True, header=False), texts=self.body, style=style, branch=self.branchcode))
        with open(unique, 'r', encoding='utf-8') as h:    
            return h.read() 
    
    def try_send(self):
        msg = MIMEMultipart()
        # ----------------------邮件主体-------------------------
        msgtext = MIMEText(self.generateTableBody(), 'html', 'utf-8')
        msg['Subject'] = Header(self.subject)
        msg['From'] = self.sender
        msg['To'] = ", ".join(self.to)
        msg['Cc'] = ", ".join(self.cc)
        msg.attach(msgtext)
        # ----------------------邮件附件-------------------------
        for f in self.attachment:
            if path.exists(f):
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(open(f, 'rb').read())
                encoders.encode_base64(part)
                file_path, file_name = path.split(f)
                part.add_header('Content-Disposition', f"attachment; filename={make_header([(file_name, 'UTF-8')]).encode('UTF-8')}")
                msg.attach(part)
        # ------------------------------------------------------
        server = smtplib.SMTP(self.mail_server, 465)
        server.starttls()
        server.set_debuglevel(1)
        server.sendmail(from_addr=self.sender, to_addrs=self.receiver, msg=msg.as_string())
        server.quit()
        logger.debug("Mail sent successfully.")



if __name__ == '__main__':
    pass
