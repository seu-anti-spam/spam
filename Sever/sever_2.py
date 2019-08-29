import socket
import threading
import filter2
import pickle
ADDRESS=('localhost',8000)
#负责监听的socket
g_socket_sever=None
#连接池
g_conn_pool=[]

sem=threading.Semaphore(3)

def Get_Dict():
	normDict, spamDict = filter2.Get_Dict('normal.txt', 'spam.txt')
	pickle_file = open('health_dic.pkl', 'rb')
	health_dic = pickle.load(pickle_file)
	pickle_file.close()
	pickle_file = open('health_dic.pkl', 'rb')
	spam_dic = pickle.load(pickle_file)
	pickle_file.close()
	return normDict,spamDict,health_dic,spam_dic

normDict, spamDict, health_dic, spam_dic = Get_Dict()

def init():
	"""
	初始化
	"""
	global g_socket_sever
	g_socket_sever=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	g_socket_sever.bind(ADDRESS)
	g_socket_sever.listen(5)
	print("服务端已经启动，等待用户连接")

def accept_client():
	"""
	接受新连接
	"""
	while True:
		client,address=g_socket_sever.accept()
		g_conn_pool.append(client)
		thread=threading.Thread(target=communcate,args=(client,))
		thread.setDaemon(True)
		thread.start()

def communcate(client):
	"""
	消息处理
	:param client
	"""
	print(len(g_conn_pool))
	sem.acquire()
	client.sendall("连接服务器成功".encode(encoding='utf-8'))
	while True:
		'''bytes = client.recv(1024)
		print("客户端消息:", bytes.decode(encoding='utf8'))
		if len(bytes) == 0:
			client.close()
			# 删除连接
			g_conn_pool.remove(client)
			print("有一个客户端下线了。")
			break
		msg = bytes.decode(encoding='utf-8')
		result = filter2.test(msg, spamDict, normDict, health_dic, spam_dic)
		print("是不是spam：" + str(result))'''
		msg=client.recv(1024)
		print("客户端消息:", msg.decode(encoding='utf8'))
	sem.release()


if __name__ == '__main__':
	init()
	thread=threading.Thread(target=accept_client())
	thread.start()
	while True:
		pass

