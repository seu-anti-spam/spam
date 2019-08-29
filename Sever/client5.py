import socket  # 导入 socket 模块

s = socket.socket()  # 创建 socket 对象
s.connect(('localhost', 8000))
print(s.recv(1024).decode(encoding='utf8'))
#s.send("连接了".encode('utf8'))
while True:
 send = '5'
 s.send(send.encode('utf-8'))
 print(s.recv(1024).decode(encoding='utf8'))
