import jieba
import sys
import os
import re

#判断邮件中的字符是不是中文
def check_contain_chinese(check):
	'''

	:param check:
	:return: True
	         Flase
	'''
	for ch in check:
		print(ch)
		if u'\u4e00'<=ch and ch<=u'\u9fa5':
			return True
	return False

#加载邮件数据的label
def load_label_files(label_file):
	label_dict={}
	for line in open(label_file).readlines():
		list1=line.strip().split('..')
		label_dict[list1[1].strip()]=list1[0].strip()
	return label_dict

#数据label的位置
label_path=r'C:\Users\admin\Desktop\CNN_Filter\trec06c\delay\index'

def load_stop_train(stop_word_path):
	stop_dict={}
	for line in open(stop_word_path):
		stop_dict[line]=1
	return stop_dict

#停用词的位置
stop_words_path=r'C:\Users\admin\Desktop\CNN_Filter\中文停用词表.txt'

#生成spam ham文件
def read_files(file_path,label_dict,stop_dict,spam_file_path,ham_file_path):
		parents = os.listdir(file_path)
		spam_file = open(spam_file_path,'a')
		ham_file = open(ham_file_path,'a')
		for parent in parents:
			child = os.path.join(file_path,parent)
			if os.path.isdir(child):
				read_files(child,label_dict,stop_dict,spam_file_path,ham_file_path)
			else:
				print (child[10:])
				label = "unk"
				if child[10:] in label_dict:
					label = label_dict[child[10:]]
				# deal file
				temp_list = []
				for line in open(child).readlines():
					line = line.strip().decode("gbk",'ignore').encode('utf-8')
					if not check_contain_chinese(line):
						continue
					seg_list = jieba.cut(line, cut_all=False)
					for word in seg_list:
						if word in stop_dict:
							continue
						else:
							temp_list.append(word)
				line = " ".join(temp_list)
				print(label)
				if label == "spam":
					spam_file.write(line.encode("utf-8","ignore") + "\n")
				if label == "ham":
					ham_file.write(line.encode("utf-8","ignore")+"\n")

spam_file_path=r'C:\Users\admin\Desktop\CNN_Filter\Spam.txt'
ham_file_path=r'C:\Users\admin\Desktop\CNN_Filter\Ham.txt'
file_path=r'C:\Users\admin\Desktop\CNN_Filter\trec06c'

label_dict=load_label_files(label_path)
stop_dict=load_stop_train(stop_words_path)

read_files(file_path,label_dict,stop_dict,spam_file_path,ham_file_path)
