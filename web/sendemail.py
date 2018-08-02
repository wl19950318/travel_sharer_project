#coding:utf-8
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

my_sender='2392315223@qq.com'    # 发件人邮箱账号
my_pass = 'vuhzsrhrfbiadijc'              # 发件人邮箱密码(当时申请smtp给的口令)
my_user='2147353584@qq.com'      # 收件人邮箱账号


def mail(user_email, url):
    ret=True
    try:
        msg=MIMEText('This is a verification email, please click: <br>'+
                     '<a href="'+url+'">Please click verification</a><br>'+url
                     ,'html','utf-8')
        msg['From']=formataddr(["service",my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To']=formataddr(["dear",user_email])              # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject']="Account verification"                # 邮件的主题，也可以说是标题

        server=smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是465
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender,[user_email,],msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()# 关闭连接
    except Exception:# 如果 try 中的语句没有执行，则会执行下面的 ret=False
        ret=False
    return ret

if __name__ =='__main__':
    ret=mail('2147353584@qq.com', 'http://www.baidu.com')
    if ret:
        print("send ok!")
    else:
        print("send error!")