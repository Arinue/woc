#!/usr/bin/env python3
# _*_ coding=utf-8 _*_
#@Auther: Arinue
import time
import email_code

headers = {'Accept':'application/json, text/javascript, */*; q=0.01',
'X-Requested-With':'XMLHttpRequest',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36',
'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
'Origin':'https://www.woccloud.com',
'Sec-Fetch-Site':'same-origin',
'Sec-Fetch-Mode':'cors',
'Sec-Fetch-Dest':'empty',
'Referer':'https://www.woccloud.com/auth/login',
'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8,am;q=0.7'}

class Woc(object):
    def __init__(self,email,passwd):
        from requests import session
        self.email = email
        self.passwd = passwd
        self.session = session()

    def Login(self):
        '''账户登陆'''
        print('[*]  正在登陆...',end='')
        url = 'https://www.woccloud.com/auth/login'
        data = {'email':self.email,'passwd':self.passwd,'code':''}
        res = self.session.post(url, headers=headers, data=data)
        if r'\u767b\u5f55\u6210\u529f' in res.text:
            print('[+]  登陆成功')
            return self.session
        else:
            print('[-]  登陆失败')
            return self.session

    def Logoff(self):
        '''账户注销'''
        print('[*]  正在注销账户...')
        if self.Login().cookies:
            url = 'https://www.woccloud.com/user/kill'
            data = {'passwd':self.passwd}
            res = self.session.post(url, headers=headers, data=data)
            if r'\u60a8\u7684\u5e10\u53f7\u5df2\u7ecf\u4ece\u6211\u4eec\u7684\u7cfb\u7edf\u4e2d\u5220\u9664\u3002\u6b22\u8fce\u4e0b\u6b21\u5149\u4e34' in res.text:
                print('[+]  账户注销成功')
                return 1
            else:
                print('[-]  账户注销失败')
                # print(res.text)
                return 0
        else:
            print('[-]  cookies监测未通过！')

    def SendCode(self):
        '''发送邮箱验证码'''
        print('[*]  正在发送验证码...')
        url = 'https://www.woccloud.com//auth/send'
        data = {'email':self.email}
        res = self.session.post(url, headers=headers, data=data)
        if r'\u9a8c\u8bc1\u7801\u53d1\u9001\u6210\u529f\uff0c\u8bf7\u67e5\u6536\u90ae\u4ef6\u3002'in res.text:
            print('[+]  邮箱验证码发送成功！')
        else:
            print('[-]  邮箱验证码发送失败！')

    def Register(self):
        '''注册账户'''
        print('[*]  正在注册账户...')
        self.SendCode()
        time.sleep(10)
        emailcode = email_code.recv_email_by_pop3()
        print(emailcode)
        url = 'https://www.woccloud.com/auth/register'
        # print(self.session.cookies)
        data = {'email':self.email,'name':int(time.time()),'passwd':self.passwd,'repasswd':self.passwd,'code':'1reQ','emailcode':emailcode}#用时间做名称，避免重复
        res = self.session.post(url, headers=headers, data=data)
        if r'\u6ce8\u518c\u6210\u529f\uff01\u6b63\u5728\u8fdb\u5165\u767b\u5f55\u754c\u9762' in res.text:
            print('[+]  注册成功！')
        else:
            print('[-]  注册失败！')
            print(res.text)


if __name__ == '__main__':
    woc = Woc('2516092321@qq.com','Arinue1!')
    #先注销，再重新注册
    woc.Logoff()
    woc.Register()
