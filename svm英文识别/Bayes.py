#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from sklearn.feature_extraction.text import CountVectorizer
import pickle
from nltk.corpus import wordnet


class Spam_Bayes:
# 将text中的标点符号和数字过滤,小写化

    def Get_Dict(self):
        pickle_file = open('health_dic.pkl', 'rb')
        health_dic = pickle.load(pickle_file)
        pickle_file.close()
        pickle_file = open('spam_dic.pkl', 'rb')
        spam_dic = pickle.load(pickle_file)
        pickle_file.close()
        health_sum=11850459
        spam_sum=10244975
        return health_dic,spam_dic,health_sum,spam_sum

    def Filter_text(self,text):
        str = re.sub('[^a-zA-Z]', ' ', text)
        str = re.sub(r'\s+', ' ', str)
        s = str.split(" ")
        num = 0
        for i in s:
            if wordnet.synsets(i):
                num += len(i)
        return str.lower(), num


    # 统计垃圾邮件和健康邮件的词频
    def Count(self,text):
        vectorizer = CountVectorizer()
        L = ['']
        L[0] = text
        weight = vectorizer.fit_transform(L).toarray()
        word = vectorizer.get_feature_names()  # 所有文本的关键字
        return {word[j]: int(weight[0][j]) for j in range(len(word))}


    # 求词频字典的总频数
    def Sum(self,dic):
        n = 0
        for value in dic.values():
            n = n + value
        return n


    def Bayes_test(self,test, num):
        health_dic, spam_dic,health_sum,spam_sum=self.Get_Dict()
        test, numc = self.Filter_text(test)
        test_count = sorted(self.Count(test).items(), key=lambda x: x[1], reverse=True)

        # 提取前15个词作计算条件概率，代入贝叶斯联合公式
        # 如果长度不够，就取总词数
        if len(test_count) >= 15:
            r = 15
        else:
            r = len(test_count)
        P = []
        for n in range(r):
            word = test_count[n][0]
            if not spam_dic.get(word):
                P.append(0.4)
            # 如果有的词是第一次出现,无法计算P(S | W),就假定这个值等于0.4。
            # 因为垃圾邮件用的往往都是某些固定的词语，所以如果你从来没见过某个词，它多半是一个正常的词。
            elif not health_dic.get(word):
                word_ham = 0.003
                # 这个值可能还需要修正,资料中给出的值是1%
                # 如果某个词只出现在垃圾邮件中, 就假定，它在正常邮件的出现频率是0.3 %
                word_spam = spam_dic[word] / spam_sum
                P.append((word_spam * 0.5) / ((word_ham * 0.5) + (word_spam * 0.5)))

            else:
                word_spam = spam_dic[word] / spam_sum
                word_ham = health_dic[word] / health_sum
                P.append((word_spam * 0.5) / ((word_ham * 0.5) + (word_spam * 0.5)))
        # print(P)
        # 计算联合概率
        p1 = 1
        p2 = 1
        for n in range(r):
            p1 = p1 * P[n]
            p2 = p2 * (1 - P[n])
        p = (p1 / (p1 + p2))

        if (numc / num) < 0.2:
            p = 1
        return p

    def test(self,test):
        num = 0
        for i in test:
            if i.isalpha():
                num += 1
        print(num)
        p = self.Bayes_test(test, num)
        if p > 0.5:
            return "Spam"
        else:
            return "Not Spam"
