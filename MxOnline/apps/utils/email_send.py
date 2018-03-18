# _*_ coding:utf-8 _*_
__author__ = 'edison'
__date__ = '17-12-21 上午12:15'
from users.models import EmailVerifyRecord
from random import Random
from django.core.mail import send_mail
from MxOnline.settings import EMAIL_FROM



def random_str(randomlenth=8):
    str=''
    chars='AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length=len(chars)-1
    random=Random()
    for i in  range(randomlenth):
        str+=chars[random.randint(0,length)]
    return str

def send_register_email(email,send_type):
    email_record = EmailVerifyRecord()
    if send_type=="update_email":
        code=random_str(4)
    else:
        code=random_str(16)
    email_record.code=code
    email_record.email=email
    email_record.send_type=send_type
    email_record.save()

    email_title=""
    email_body=""

    if send_type == "register":
        email_title = "lianjie"
        email_body = "lianjie：http://127.0.0.1:8000/active/{0}".format(code)

        send_status = send_mail(email_title,email_body,EMAIL_FROM,[email])
        if send_status:
            pass
    elif send_type=="forget":
        email_title = u"慕学在线网密码重置"
        email_body = u"请点击下面的链接重置密码：http://127.0.0.1:8000/reset/{0}".format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass

    else:
        send_type=="update_email"
        email_title = u"慕学在线网邮箱修改验证码"
        email_body = u"你的邮箱验证码为：{0}".format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass


