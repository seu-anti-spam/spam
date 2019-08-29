from spamEmail import spamEmailBayes
import re
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import wordnet

# spam类对象
spam = spamEmailBayes()
# 停用词
stopList = spam.getStopWords()
# 获取训练集中正常邮件与垃圾邮件的数量
normFilelen = 7063
spamFilelen = 7775


# 正常词汇频率 垃圾邮件词汇频率
def Get_Dict(normal_email, spam_email):
    normDict = {}
    spamDict = {}
    with open(normal_email, 'r') as f:
        for line in f.readlines():
            line = line.strip()
            k1 = line.split(' ')[0]
            v1 = int(line.split(' ')[1])
            normDict[k1] = v1
    with open(spam_email, 'r') as f:
        for line in f.readlines():
            line = line.strip()
            k2 = line.split(' ')[0]
            v2 = int(line.split(' ')[1])
            spamDict[k2] = v2
    return normDict, spamDict


# 获取邮件内容
def Get_Email(fileName):
    with open(fileName, 'r') as f:
        Email_Content = f.read()
    return Email_Content


# 获取邮件分词后,然后统计词频的成果
def Get_Email_Div(content):
    wordsList = []
    rule = re.compile(r"[^\u4e00-\u9fa5]")
    line = rule.sub("", content)
    spam.get_word_list(line, wordsList, stopList)
    testDict = {}
    spam.addToDict(wordsList, testDict)
    return testDict


def Get_Bayes_Num(testDict, spamDict, normDict, normFilelen, spamFilelen):
    wordProbList = spam.getTestWords(testDict, spamDict, normDict, normFilelen, spamFilelen)
    p = spam.calBayes(wordProbList, spamDict, normDict)
    if p > 0.9:
        return 1
    else:
        return 0


# add English Bayes
def Filter_text(text):
    str = re.sub('[^a-zA-Z]', ' ', text)
    str = re.sub(r'\s+', ' ', str)
    s = str.split(" ")
    num = 0
    for i in s:
        if wordnet.synsets(i):
            num += len(i)
    return str.lower(), num


# 统计垃圾邮件和健康邮件的词频
def Count(text):
    vectorizer = CountVectorizer()
    L = ['']
    L[0] = text
    weight = vectorizer.fit_transform(L).toarray()
    word = vectorizer.get_feature_names()  # 所有文本的关键字
    return {word[j]: int(weight[0][j]) for j in range(len(word))}


# 求词频字典的总频数
def Sum(dic):
    n = 0
    for value in dic.values():
        n = n + value
    return n


def Bayes(test, num, health_dic, spam_dic, health_sum, spam_sum):
    test, numc = Filter_text(test)
    test_count = sorted(Count(test).items(), key=lambda x: x[1], reverse=True)
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
    # 计算联合概率
    p1 = 1
    p2 = 1
    for n in range(r):
        p1 = p1 * P[n]
        p2 = p2 * (1 - P[n])
    p = (p1 / (p1 + p2))

    if (numc / num) < 0.2:
        p = 1

    if p > 0.5:
        pc = 1
    else:
        pc = 0
    return pc

def test(msg,spamDict,normDict,health_dic,spam_dic):
    chnum, ennum, allnum, chp = number(msg)
    if chp > 0.9:
        div = Get_Email_Div(msg)
        result = Get_Bayes_Num(div, spamDict, normDict, 7063, 7775)
    else:
        health_sum = 11850459
        spam_sum = 10244975
        result = Bayes(msg, ennum, health_dic, spam_dic, health_sum, spam_sum)
    return result

def number(content):
    allnum = 0
    chnum = 0
    ennum = 0
    for i in content:
        if '\u4e00' <= i <= '\u9fff':
            chnum += 1
            allnum += 1
        if (i >= u'\u0041' and i <= u'\u005a') or (i >= u'\u0061' and i <= u'\u007a'):
            ennum += 1
            allnum += 1
    if allnum!=0:
        chp = chnum / allnum
    else:
        chp=0
    return chnum, ennum, allnum, chp