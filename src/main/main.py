#coding=utf8
'''
Created on 2016年12月19日

@author: ZWJ
'''

import smtplib,os
from email.mime.text import MIMEText#发送html,plain
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart#发送附件
from tool import *
#smtplib.SMTP([host[, port[, local_hostname[, timeout]]]])

mailto_list=['email1xx@.com','email2xx@.com']
mail_host="smtp.sina.com"  #设置新浪服务器
sender="xxxxxx"
#账户密码
mail_user,mail_pass='',''

def send_mail_plain(mailto,sub,content):  
    '''
        文本邮件发送的实现，关键是要将MIMEText中_subtype设置为plain。首先导入smtplib和mimetext。创建smtplib.smtp实例，connect邮件smtp服务器，login后发送
        多个接收人，msg['To'] 是字符串，多个地址用逗号分开； sendmail()函数的mailTo形参是列表类型，而且两个地址要一致
    '''
    msg = MIMEText(content,_subtype='plain',_charset='utf-8')  
    msg['Subject'] = sub  #主题
    msg['From'] = "xxxxxx"+"<"+sender+">"
    msg['To'] = ','.join(mailto)
    try:  
        server = smtplib.SMTP()  
#       server.set_debuglevel(True)#调试信息
        server.connect(mail_host)  
        server.login(mail_user,mail_pass)  
        server.sendmail(msg['From'], mailto, msg.as_string())  
        server.close()  
        return True  
    except Exception, e:  
        print str(e)  
        return False  


def send_mail_html(mailto,sub,content):  
    '''
        普通文本邮件发送的实现，关键是要将MIMEText中_subtype设置为html。首先导入smtplib和mimetext。创建smtplib.smtp实例，connect邮件smtp服务器，login后发送
    '''
    msg = MIMEText(content,_subtype='html',_charset='utf-8')  
    msg['Subject'] = sub  #主题
    msg['From'] = "xxx"+"<"+sender+">"    #发件人
    msg['To'] = ','.join(mailto)
    try:  
        server = smtplib.SMTP()  
#       server.set_debuglevel(True)
        server.connect(mail_host)  
        server.login(mail_user,mail_pass)  
        server.sendmail(msg['From'], mailto, msg.as_string())  
        server.close()  
        return True  
    except Exception, e:  
        print str(e)  
        return False  

def send_mail_fujian(mailto,sub,attachment_path_list):
    '''
    mailto:收件箱，列表
    sub:主题
    attachment_path_list:附件的地址,列表
    '''
    #创建带附件消息对象
    msg = MIMEMultipart()
    text=MIMEText(u'这里是正文...','plain','utf-8')
    msg.attach(text)
    for attach_p in attachment_path_list:
        attach_name=os.path.basename(attach_p)
        #构造附件
        attachment = MIMEText(open(attach_p,'rb').read(), 'base64', 'utf-8')
        attachment["Content-Type"] = 'application/octet-stream'
        #下面的filename相当于重命名，即邮件中显示什么名字,注意接收方扩展名(建议原名)
        attachment["Content-Disposition"] = 'attachment; filename="%s"'%attach_name
        print attachment['Content-Disposition']
        msg.attach(attachment)

    #加邮件头
    msg['To'] = ','.join(mailto)
    msg['From'] = "liubi"+"<"+sender+">"
    msg['Subject'] = sub
    #发送邮件
    try:
        server = smtplib.SMTP()
        server.connect(mail_host)
        server.login(mail_user,mail_pass)#XXX为用户名，XXXXX为密码
        server.sendmail(msg['from'],mailto,msg.as_string())
        server.quit()
        print '发送成功'
        return True
    except Exception, e:  
        print str(e) 
        return False
    
def  send_mail_image(mailto,sub,pic_path_l):
    '''
    mailto:收件箱，列表
    sub:主题
    pic_path_l:图片
    '''
    imgnum = len(pic_path_l)
    msg = MIMEMultipart()
    content='''
    <p>Python 发送图片测试...</p>
    <p><a href="http://www.runoob.com">菜鸟教程链接</a></p>
    <p>图片演示：</p>
    '''
    for index in range(imgnum):
        content = content+'<p><img src="cid:image%s"></p>'%index
    textmsg = MIMEText(content,'html','utf-8')
    msg.attach(textmsg)
    
    #deal图片
    for index,image_p in enumerate(pic_path_l,0):
        with open(image_p,'rb') as f:
            imgmsg = MIMEImage(f.read())
            # 定义图片 ID，在 HTML 文本中引用
            imgmsg.add_header('Content-ID', '<image%s>'%index)
            msg.attach(imgmsg)
    
    msg['Subject'] = u'发送图片测试'
    msg['To'] = ','.join(mailto)
    msg['From'] ="<"+sender+">"
    
    try:
        server = smtplib.SMTP()
        server.connect(mail_host)
        server.login(mail_user,mail_pass)
        server.sendmail(msg['from'],mailto,msg.as_string())
        server.quit()
        print '发送成功'
        return True
    except Exception, e:  
        print str(e) 
        return False
         
       
def main():
    global mail_user,mail_pass
    mail_user,mail_pass=user_pwd()
    #send_mail_plain(mailto_list,"just test plain","HI ALL,\nBye.")#返回False,True
    #send_mail_html(mailto_list,"just test html","<a href='www.baidu.com'>百度一下</a>")#返回False,True
    #send_mail_fujian(mailto_list,u'附件测试',['d:\\3.rar','d:\\5.txt'])#返回False,True
    send_mail_image(mailto_list,u'发送图片测试',[r'D:\7.jpg',r'D:\2.jpg'])
    pass


if __name__ == '__main__':  
    main()
    