#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pyzmail
import re
import Lgmail

from socket import *
from smtplib import SMTP_SSL
from imapclient import IMAPClient
from email.mime.text import MIMEText

white_list = []  # 本地白名单
black_list = []  # 本地黑名单
special_list = []  # 本地特别关心表
save_path = 'C:\\attach'  # 附件本地保存位置

class Imapmail(object):
    '''
    定义类Imapmail实现代理登录邮箱，监听,获取往期邮件等功能
    '''
    def __init__(self):  # 初始化数据
        self.ID = 0
        self.server_address = None  # imap地址 例如imap.163.com
        self.user = None  # 邮箱账号
        self.password = None  # 邮箱密码
        self.prot = None
        self.ssl = None
        self.timeout = None  # 连接超时最大时间

        self.server = None  # imap客户端 用于与imap服务器交互
        self.result = list()  # 某标签（ALL,UNSEEN等）的全部邮件
        self.size = 0  # 邮件的数量
        self.previous = 0  # 上一次扫描邮件的数量
        self.messageObj = None  # 存储单封邮件的内容

        self.received_mails = {'垃圾邮件': list(), '正常邮件': list()}  # 存储往期邮件



    def client(self):  # 链接imap服务器 得到server
        try:
            self.server = IMAPClient(self.server_address, self.prot, self.ssl, timeout=self.timeout)
            return self.server
        except BaseException as e:
            return "ERROR: >>> " + str(e)

    def login(self):  # 邮箱登录
        try:
            self.server.login(self.user, self.password)
            # global save_paths
            # #  加载附件下载地址
            # pickle_file_save_path = open('save_paths.pkl', 'rb')
            # save_paths = pickle.load(pickle_file_save_path)
            # #  附件下载地址
            # if self.user not in save_paths.keys():
            #     save_paths.update({self.user: 'D:\\k_g'})
            #     pickle_file = open('save_paths.pkl', 'wb')
            #     pickle.dump(save_paths, pickle_file)
            #     pickle_file.close()

        except BaseException as e:
            return 0

    def get_mail_dir(self):  # 获取邮箱目录 暂不使用
        # 获取目录列表 [((), b'/', 'INBOX'), ((b'\\Drafts',), b'/', '草稿箱'),]
        dir_list = self.server.list_folders()
        return dir_list

    def init(self):  # 监听机制初始化 设置初始邮件数量
        self.server.select_folder('INBOX', readonly=False)  # 选择目录 readonly=True 只读,不修改,这里只选择了 收件箱
        self.result = self.server.search('all')  # 获取所有邮件总数目 [1,2,3,....]
        self.previous = len(self.result)

    def get_result(self):  # 循环监听 更改邮件数量
        #  self.server.select_folder('INBOX', readonly=False)  # 选择目录 readonly=True 只读,不修改,这里只选择了 收件箱
        self.result = self.server.search('all')  # 获取所有邮件总数目 [1,2,3,....]
        self.size = len(self.result)
        return self.size

    def if_exist_attach(self, mg):
        msg_dict = self.server.fetch(mg, ['BODY[]'])  # 获取邮件内容
        mail_body = msg_dict[mg][b'BODY[]']  # 获取邮件内容
        message = pyzmail.PyzMessage.factory(mail_body)
        flag = 0
        for part in message.mailparts:
            if part.filename:
                flag = 1
        if flag == 1:
            return 1
        else:
            return 0

    def get_attach(self, mg):  # 获取附件
        global save_paths
        if not os.path.exists(save_path):  # 判断下载目录是否存在，不存在就创建一个
            os.mkdir(save_path)
        msg_dict = self.server.fetch(mg, ['BODY[]'])  # 获取邮件内容
        mail_body = msg_dict[mg][b'BODY[]']  # 获取邮件内容
        message = pyzmail.PyzMessage.factory(mail_body)
        num = 0
        for part in message.mailparts:
            if part.filename:
                num += 1
                filename_save = message.get_address('from')[1] + '_' + part.filename
                down_path = os.path.join(save_path, filename_save)
                with open(down_path, 'wb') as f:
                    f.write(part.get_payload())

    def get_content(self, mg):
        data = self.server.fetch(mg, ['ENVELOPE'])
        envelope = data[mg][b'ENVELOPE']
        dates = envelope.date
        msg_dict = self.server.fetch(mg, ['BODY[]'])  # 获取邮件内容
        mail_body = msg_dict[mg][b'BODY[]']  # 获取邮件内容
        ip = (re.search(
            r'(?:(?:[01]?\d?\d?|2[0-4]\d|25[0-5])\.){3}(?:[01]?\d?\d?|2[0-4]\d|25[0-5])',
            str(mail_body))).group()
        self.messageObj = pyzmail.PyzMessage.factory(mail_body)
        subject = self.messageObj.get_subject()
        send = str(self.messageObj.get_addresses('from')[0][1])
        send_time = str(dates)
        to = str(self.messageObj.get_addresses('to')[0][1])
        message_Content = '内容为空'
        mail = {'垃圾': 0, '主题': subject, '发件人': send, '收件人' : to, '时间': send_time,
                'IP地址': ip, '主要内容': message_Content, '邮件': None, '附件': 0}
        if self.if_exist_attach(mg):
            mail['附件'] = 1
        else:
            mail['附件'] = 0
        self.ID += 1
        if self.messageObj.text_part is not None:
            message_Content = self.messageObj.text_part.get_payload().decode(self.messageObj.text_part.charset)
            temp = ' '.join(message_Content.split())
            mail['主要内容'] = temp
        # if self.messageObj.html_part is not None:
        #   message_Content = self.messageObj.html_part.get_payload().decode(self.messageObj.text_part.charset)
        #    mail['主要内容'] = message_Content
        else:
            pass
        return mail

    def get_new_mail(self):  # 监听最新邮件
        count = 0
        self.get_result()
        mails = list()
        temp = self.previous  # 11
        count = len(self.result) - self.previous
        self.previous = len(self.result)
        if count == 0:
            print('邮件总数:' + str(self.size))
        else:
            print('邮件总数:' + str(self.size))
            address = '42.159.155.29'
            port = 8000
            s = socket(AF_INET, SOCK_STREAM)
            try:
                s.connect((address, port))
                for each_mail in self.result[temp:self.size]:
                    mail = self.get_content(each_mail)
                    if mail['发件人'] in special_list:
                        mail['垃圾'] = 2  # 特别关心
                        self.received_mails['正常邮件'].append(mail)
                    elif mail['发件人'] in black_list:
                        mail['垃圾'] = 1
                        self.received_mails['垃圾邮件'].append(mail)
                    elif mail['发件人'] in white_list:
                        mail['垃圾'] = 0
                        self.received_mails['正常邮件'].append(mail)
                    else:
                        mail['邮件'] = each_mail
                        # 由公共黑名单或者算法进行判断
                        # 根据结果更新词条垃圾的值
                        # 云端判断邮件垃圾与否
                        temp = dict()
                        temp.update({'功能': 'mail'})
                        temp.update({'邮件': mail})
                        temp.update({'公共黑名单': 1})
                        s.send(str(temp).encode('utf-8'))
                        result = int(s.recv(1024).decode('utf-8'))
                        s.send(str({'功能':'exit'}).encode('utf-8'))
                        if result == 1:
                            mail['垃圾'] = 1
                            #  self.send_back(mail)
                        else:
                            pass
                        mails.append(mail)
            except BaseException as e:
                print(e)
            finally:
                # 断开连接
                s.close()
        return mails

    def delete_mail(self, mail):
        self.server.delete_messages(mail)

    def get_all_mails(self, s):
        self.get_result()
        if self.size == 0:
            print('收件箱为空')
        else:
            for each_mail in self.result:
                mail = self.get_content(each_mail)
                mail['邮件'] = each_mail
                temp = mail.copy()
                temp.pop('邮件')
                temp.pop('垃圾')
                if temp in Lgmail.extra_list:
                    mail['垃圾'] = 0
                    self.received_mails['正常邮件'].append(mail)
                elif mail['发件人'] in black_list:
                    mail['垃圾'] = 1
                    self.received_mails['垃圾邮件'].append(mail)
                elif mail['发件人'] in white_list:
                    mail['垃圾'] = 0
                    self.received_mails['正常邮件'].append(mail)
                else:
                    # 由公共黑名单或者算法进行判断
                    # 由公共黑名单或者算法进行判断
                    # 根据结果更新词条垃圾的值
                    temp = dict()
                    temp.update({'功能':'mail'})
                    temp.update({'邮件': mail})
                    temp.update({'公共黑名单':0})
                    s.send(str(temp).encode('utf-8'))
                    result = int(s.recv(1024).decode('utf-8'))
                    if result == 1:
                        mail['垃圾'] = 1
                        self.received_mails['垃圾邮件'].append(mail)
                    else:
                        self.received_mails['正常邮件'].append(mail)
        return self.received_mails

    def number(self, content):
        allnum = 0
        chnum = 0
        ennum = 0
        for i in content:
            if '\u4e00' <= i <= '\u9fff':
                chnum += 1
                allnum += 1
            if (u'\u0041' <= i <= u'\u005a') or (u'\u0061' <= i <= u'\u007a'):
                ennum += 1
                allnum += 1
        chp = chnum / allnum
        return chnum, ennum, allnum, chp

    def close(self):  # 断开连接
        self.server.logout()

    def add_white(self, name):  # 添加用户白名单
        global white_list
        if name not in white_list:
            white_list.append(name)


    def add_black(self, name):  # 添加用户黑名单
        global black_list
        if name not in black_list:
            black_list.append(name)

    def add_special(self, name):  # 添加用户特别关心
        global special_list
        if name not in special_list:
            special_list.append(name)

    def send_back(self, mail):  # 自动恢复垃圾邮件
        sender_user = self.user  # 自动回复的发件人
        sender_password = self.password  # 密码
        sender_smtp = 'smtp.'+self.user.split('@')[-1]  # 发送方的smtp地址
        receive_user = mail['发件人']  # 收件人的邮箱地址
        message = MIMEText('你这个辣鸡', 'plain', 'utf-8')  # 邮件对象
        message['From'] = sender_user  # 设置发件人
        message['TO'] = receive_user  # 设置收件人
        message['Subject'] = '测试邮件'  # 设置主题
        with SMTP_SSL(host=sender_smtp, port=465) as smtp:
            # 连接smtp服务器
            smtp.login(user=sender_user, password=sender_password)
            smtp.sendmail(from_addr=self.user, to_addrs=receive_user, msg=message.as_string())
            smtp.quit()


if __name__ == "__main__":  # 测试用数据
    imap = Imapmail()
    imap.user = "seu_xuzhipeng@163.com"  # 邮箱账号 验证码
    imap.password = "zsyxzp06270314"  # 邮箱密码
    imap.server_address = 'imap.' + imap.user.split('@')[-1]  # 邮箱地址
    if imap.user.split('@')[-1] in ['163.com', 'qq.com', '126.com']:
        imap.client()
        e = imap.login()
        if e == 0:
            print('账号或者密码错误')
        else:
            imap.get_all_mails()
            imap.get_new_mail()
            imap.close()
    else:
        print('邮箱格式不正确')
