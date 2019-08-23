#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pickle
import pyzmail
import re
import filter2
import jieba
from spamEmail import spamEmailBayes
from imapclient import IMAPClient



class Imapmail(object):
    '''
    定义类Imapmail实现代理登录邮箱，监听,获取往期邮件等功能
    '''
    def __init__(self):  # 初始化数据
        self.server_address = None  # imap地址 例如imap.163.com
        self.user = None  # 邮箱账号
        self.pass_wd = None  # 邮箱密码
        self.prot = None
        self.ssl = None
        self.timeout = None  # 连接超时最大时间
        self.save_path = 'D:\k_g'  # 附件本地保存位置
        self.server = None  # imap客户端 用于与imap服务器交互
        self.result = list()  # 某标签（ALL,UNSEEN等）的全部邮件
        self.size = 0  # 邮件的数量
        self.previous = 0  # 上一次扫描邮件的数量
        self.messageObj = None  # 存储单封邮件的内容

        self.white_list = [' ']  # 本地白名单
        self.black_list = [' ']  # 本地黑名单

        #  初始化本地白名单 黑名单
        pickle_file_white = open('white_list.pkl', 'wb')
        pickle.dump(self.white_list, pickle_file_white)
        pickle_file_white.close()
        pickle_file_black = open('black_list.pkl', 'wb')
        pickle.dump(self.black_list, pickle_file_black)
        pickle_file_black.close()

        #  加载本地白名单 黑名单
        # pickle_file_white = open('white_list.pkl', 'rb')
        # self.white_list = pickle.load(pickle_file_white)
        # pickle_file_black = open('black_list.pkl', 'rb')
        # self.black_list = pickle.load(pickle_file_black)

    def client(self):  # 链接imap服务器 得到server
        try:
            self.server = IMAPClient(self.server_address, self.prot, self.ssl, timeout=self.timeout)
            return self.server
        except BaseException as e:
            return "ERROR: >>> " + str(e)

    def login(self):  # 邮箱登录
        try:
            self.server.login(self.user, self.pass_wd)
        except BaseException as e:
            return 0

    def get_mail_dir(self):  # 获取邮箱目录 暂不使用
        # 获取目录列表 [((), b'/', 'INBOX'), ((b'\\Drafts',), b'/', '草稿箱'),]
        dir_list = self.server.list_folders()
        return dir_list

    def init(self):  # 监听机制初始化 设置初始邮件数量
        self.server.select_folder('INBOX', readonly=True)  # 选择目录 readonly=True 只读,不修改,这里只选择了 收件箱
        self.result = self.server.search('all')  # 获取所有邮件总数目 [1,2,3,....]
        self.previous = len(self.result)
    def get_result(self):  # 循环监听 更改邮件数量
        self.server.select_folder('INBOX', readonly=False)  # 选择目录 readonly=True 只读,不修改,这里只选择了 收件箱
        self.result = self.server.search('all')  # 获取所有邮件总数目 [1,2,3,....]
        self.size = len(self.result)
        return self.size

    def get_attach(self, mg):  # 获取附件
        if not os.path.exists(self.save_path):  # 判断下载目录是否存在，不存在就创建一个
            os.mkdir(self.save_path)
        num = 0
        for part in mg.mailparts:
            if part.filename:
                num += 1
                filename_save = mg.get_address('from')[1] + '_' + part.filename
                down_path = os.path.join(self.save_path, filename_save)
                print('附件保存地址为：%s' % down_path)
                with open(down_path, 'wb') as f:
                    f.write(part.get_payload())
    def get_content(self,_sm):
        data = self.server.fetch(_sm, ['ENVELOPE'])
        envelope = data[_sm][b'ENVELOPE']
        dates = envelope.date
        msg_dict = self.server.fetch(_sm, ['BODY[]'])  # 获取邮件内容
        mail_body = msg_dict[_sm][b'BODY[]']  # 获取邮件内容
        ip = (re.search(
            r'(?:(?:[01]?\d?\d?|2[0-4]\d|25[0-5])\.){3}(?:[01]?\d?\d?|2[0-4]\d|25[0-5])',
            str(mail_body))).group()
        self.messageObj = pyzmail.PyzMessage.factory(mail_body)
        subject = self.messageObj.get_subject()
        send = str(self.messageObj.get_addresses('from')[0][1])
        send_time = str(dates)
        print("主题：" + subject)
        print('发件人：' + send)
        print('时间：' + send_time)
        print('主要内容：')
        message_Content = '内容为空'
        mail = {'垃圾':0,'主题': subject, '发件人': send, '时间': send_time,
                'IP地址': ip,'主要内容': message_Content}
        if self.messageObj.text_part is not None:
            message_Content = self.messageObj.text_part.get_payload().decode(self.messageObj.text_part.charset)
            mail['主要内容'] = message_Content
            # print(message_Content)
        elif self.messageObj.html_part is not None:
            message_Content = self.messageObj.html_part.get_payload().decode(self.messageObj.text_part.charset)
            print(message_Content)
            mail['主要内容'] = message_Content
        else:
            pass
        return mail

    def get_new_mail(self):  # 监听最新邮件
        count = 0
        self.get_result()
        mails = list()
        temp = self.previous
        count = self.size - self.previous
        self.previous = self.size
        if count == 0:
            print('邮件总数:' + str(self.size))
        else:
            print('邮件总数:' + str(self.size))
            for _sm in self.result[temp:self.size]:
                mail = self.get_content(_sm)
                if mail['发件人'] in self.white_list:
                    pass
                elif mail['发件人'] in self.black_list:
                    self.server.delete_messages(_sm)
                    self.previous -= 1
                    mail['垃圾'] = 1
                    mails.append(mail)
                else:
                    # 由公共黑名单或者算法进行判断
                    # 根据结果更新词条垃圾的值
                    normDict, spamDict = filter2.Get_Dict('normal.txt', 'spam.txt')
                    div = filter2.Get_Email_Div(mail['主要内容'])
                    filter2.Get_Bayes_Num(div, spamDict, normDict, 7063, 7775)
        return mails

    def get_all_mails(self):
        self.get_result()
        if self.size == 0:
            print('收件箱为空')
        else:
            for _sm in self.result:
                mail = self.get_content(_sm)
                if mail['发件人'] in self.white_list:
                    pass
                elif mail['发件人'] in self.black_list:
                    self.server.delete_messages(_sm)
                    mail['垃圾'] = 1
                else:
                    # 由公共黑名单或者算法进行判断
                    pass
                self.get_attach(self.messageObj)
                #self.server.delete_messages(_sm)

    def close(self):  # 断开连接
        self.server.logout()

    def add_white(self, name):  # 添加本地白名单
        if name not in self.white_list:
            self.white_list.append(name)
            pickle_file = open('white_list.pkl', 'wb')
            pickle.dump(self.white_list, pickle_file)
            pickle_file.close()

    def add_black(self, name):  # 添加本地黑名单
        if name not in self.black_list:
            self.black_list.append(name)
            pickle_file = open('white_list.pkl', 'wb')
            pickle.dump(self.black_list, pickle_file)
            pickle_file.close()


if __name__ == "__main__":  # 测试用数据
    imap = Imapmail()
    imap.user = "seu_xuzhipeng@163.com"  # 邮箱账号 验证码
    imap.pass_wd = "zsyxzp06270314"  # 邮箱密码
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
