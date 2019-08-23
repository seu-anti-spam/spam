# coding: utf8


import poplib,time
from email.parser import Parser
import base64
import re
import getpass


class MailInfo(object):
    """
    用于临时保存邮件信息的类
    """
    def __init__(self):
        self.index = 0
        self.size = 0
        self.status = ""
        self.data = ""
        # self.details = None


class MailDetails(object):
    """
    包括邮件的发件人的昵称， 发件人的账号
    收件人的昵称，收件人的账号
    信件的主题
    信件发送到服务器上的时间
    信件的正文
    """
    def __init__(self):
        self.from_nickname = ""
        self.from_account  = ""
        self.to_nickname = ""
        self.to_account = ""
        self.subject = ""
        self.receivedtime = ""
        self.text_content = ""
        self.html_content = ""


def login_in(useraccount, password, debuglevel=1):
    """
    :param useraccount: 邮件用户名
    :param password:    邮件接收授权码
    :param limits:      要接收的信件数目. 默认按时间最新排序
    :return:            email.message.Message对象。已是被解析过的数据，可使用Message对象的api方法进一步操作。
    """

    # 邮件服务器地址, 可以通过邮箱账号来分析得到
    pop3_server = 'pop.'+useraccount.split('@')[-1]
    # 开始连接到服务器
    server = poplib.POP3(pop3_server)
    # 可选项： 打开或者关闭调试信息，1为打开，会在控制台打印客户端与服务器的交互信息
    server.set_debuglevel(debuglevel)
    # 可选项： 打印POP3服务器的欢迎文字，验证是否正确连接到了邮件服务器
    #print(server.getwelcome().decode('utf8'))
    # 开始进行身份验证
    server.user(useraccount)
    server.pass_(password)
    # 使用list()返回所有邮件的编号，默认为字节类型的串
    return server
def get_msg(server):
    resp, mails, octets = server.list()
    print('邮件总数： {}'.format(len(mails)))
    # 总的邮件数
    total_mail_numbers = len(mails)
    # 获取最新的limits封邮件, 最多获取全部的邮件，用一个列表保存
    recv_mails = []
    for item in mails:
        # 为每一封邮件进行实例化处理
        mailinfo = MailInfo()
        index, size = decode_byte(item).split(' ')
        mailinfo.index = index
        mailinfo.size = size
        resp_status, mail_lines, mail_octets = server.retr(index)
        mailinfo.status = resp_status
        content_charset = get_rawcontent_charset(mail_lines)
        msg = parse_raw_mail_data(mail_lines, charset='utf-8')
        mailinfo.data = msg
        # print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"+str(type(msg)))
        # maildetails = get_mail_details(msg)
        # mailinfo.details = maildetails
        recv_mails.append(mailinfo)

    # 关闭与服务器的连接，释放资源
    server.close()

    # 返回获取到的limits封邮件详情
    return recv_mails



def get_mail_details(msg):
    # 新建一个Bean对象
    maildetails = MailDetails()

    # 获取发件人详情
    fromstr = msg.get('From')
    # print(fromstr)
    from_nickname, from_account = get_mail_info(fromstr)
    maildetails.from_nickname = from_nickname
    maildetails.from_account = from_account
    #print(from_nickname, from_account)
    # 获取收件人详情
    tostr = msg.get('To')
    to_nickname, to_account = get_mail_info(tostr)
    # print(to_account, to_nickname)
    maildetails.to_nickname = to_nickname
    maildetails.to_account = to_account


    # 获取主题信息，也就是标题内容
    subject = msg.get('Subject')
    if '?' not in subject:
        maildetails.subject=subject
    else:
        maildetails.subject = decode_base64(subject.split("?")[3], charset=subject.split("?")[1])
    # 获取时间信息，也即是邮件被服务器收到的时间
    received_time = msg.get("Date")
    # print(received_time)
    maildetails.receivedtime = received_time

    parts = msg.get_payload()
    # print('8'*9, parts[0].as_string())
    content_type = parts[0].get_content_type()
    content_charset = parts[0].get_content_charset()
    # parts[0] 默认为文本信息，而parts[1]默认为添加了HTML代码的数据信息
    content = parts[0].as_string().split('base64')[-1]
    # print('Content*********', decode_base64(content, content_charset))
    maildetails.text_content = decode_base64(content, content_charset)
    content = parts[1].as_string().split('base64')[-1]
    # print('HTML Content:', decode_base64(content, content_charset))
    maildetails.html_content = decode_base64(content, content_charset)

    return maildetails

# 为base64编码的串进行解码操作，返回字符串信息
def decode_base64(s, charset='utf8'):
    return str(base64.decodebytes(s.encode(encoding=charset)), encoding=charset)

# 获取FROM， TO等字段的解析详情
def get_mail_info(s):
    # print("++++++++++++++++++++++++++++++++++++++++++++++++++++++"+str(type(s)))
    nickname, account = s.split(" ")
    # 获取字串的编码信息
    charset = nickname.split('?')[1]
    # print('编码：{}'.format(charset))
    nickname = nickname.split('?')[3]
    nickname = str(base64.decodebytes(nickname.encode(encoding=charset)), encoding=charset)
    account = account.lstrip('<')
    account = account.rstrip('>')
    return nickname, account

# 因为邮件中格式是由英文确定的，所以在此处查找文本的编码时可以使用utf8作为临时解码集，用于查找文本正文编码信息
def get_rawcontent_charset(rawcontent):
    for item in rawcontent:
        if decode_byte(item).find('charset='):
            charset = []
            charset = re.findall(re.compile('charset="(.*)"'), decode_byte(item))
            for item in charset:
                if item is not None:
                    return item


# 返回被email.Parser模块解码后的邮件数据信息
def parse_raw_mail_data(raw_lines, charset='utf8'):
    msg_content = b'\r\n'.join(raw_lines).decode(encoding=charset)
    return Parser().parsestr(text=msg_content)

# 将字节数据通过相应的编码转换成字符串类型的数据
def decode_byte(bstr, charset='utf8'):
    return bstr.decode(charset)


if __name__ == '__main__':
    useraccount = 'seu_xuzhipeng@163.com'
    password = 'zsyxzp06270314'
    #debug_level = int(input('the debug level, default is on which is number 1'))

    # 获取到limits限制下的所有的邮件
    server = login_in(useraccount=useraccount, password=password, debuglevel=1)
    mails = get_msg(server)
    # 进入循环操作体
    previous=len(mails)
    count = 0
    while True:
        count=len(mails)-previous
        print(count)
        if(count==0):
            print('邮件总数:'+str(len(mails)))
        else:
            # 输出获取到的邮件的主题，给出相应下标，让用户进行选择
            #for index, mail in enumerate(mails):
            #   print("["+'主题'+": "+decode_byte(mail.status)+"]", end='\t')
            # 给出可选菜单，让用户选择输出哪些字段的值，另新增全字段显示ALL
            for each in range(count):
                maildetails = get_mail_details(mails[each].data)
                print('主题:'+maildetails.subject)
                print("发件人："+ maildetails.from_account)
                print('时间：'+maildetails.receivedtime)
                print('内容:'+maildetails.text_content)
            # 询问是否退出邮件查询系统，是则退出，否则继续进行下一步的查询操作
            #userinput = input('ready to exit? (Y/N)')
            #exitcode = 1 if (userinput=='Y' or userinput=='y') else 0
            previous=len(mails)
        time.sleep(1)
        #server = login_in(useraccount=useraccount, password=password, debuglevel=1)
        mails = get_msg(server)
