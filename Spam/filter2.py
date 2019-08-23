from spamEmail import spamEmailBayes
import re

#spam类对象
spam=spamEmailBayes()
#停用词
stopList=spam.getStopWords()
#获取训练集中正常邮件与垃圾邮件的数量
normFilelen=7063
spamFilelen=7775


#正常词汇频率 垃圾邮件词汇频率
def Get_Dict(normal_email,spam_email):
    normDict = {}
    spamDict = {}
    with open(normal_email,'r') as f:
        for line in f.readlines():
            line = line.strip()
            k1 = line.split(' ')[0]
            v1 = int(line.split(' ')[1])
            normDict[k1] = v1
    with open(spam_email,'r') as f:
        for line in f.readlines():
            line = line.strip()
            k1 = line.split(' ')[0]
            v1 = int(line.split(' ')[1])
            spamDict[k1] = v1
    return  normDict,spamDict

#获取邮件内容
def Get_Email(fileName):
    with open(fileName,'r') as f:
        Email_Content=f.read()
    return Email_Content
#获取邮件分词后,然后统计词频的成果
def Get_Email_Div(content):
    wordsList=[]
    rule=re.compile(r"[^\u4e00-\u9fa5]")
    content = rule.sub("", content)
    spam.get_word_list(content, wordsList, stopList)
    testDict = {}
    spam.addToDict(wordsList, testDict)
    return testDict

def Get_Bayes_Num(testDict, spamDict, normDict, normFilelen, spamFilelen):
    wordProbList=spam.getTestWords(testDict, spamDict, normDict, normFilelen, spamFilelen)
    p=spam.calBayes(wordProbList,spamDict,normDict)
    print(p)



if __name__ == '__main__':
    spamDict, normDict=Get_Dict('normal.txt','spam.txt')
    content=Get_Email('a.txt')
    div=Get_Email_Div(content)
    print(normFilelen)
    print(spamFilelen)
    Get_Bayes_Num(div, spamDict, normDict, normFilelen, spamFilelen)
