import jieba;
import os;
import re;
import nltk;
class spamEmailBayes:
    #获得停用词表
    def getStopWords(self):
        stopList=[]
        for line in open("中文停用词表.txt"):
            stopList.append(line[:len(line)-1])
        for line in open("stopWords.txt"):
            stopList.append(line[:len(line) - 1])
        return stopList;
    #获得词典
    def get_word_list(self,content,wordsList,stopList):
        #分词结果放入res_list
        zhPattern = re.compile(u'[\u4e00-\u9fa5]+')
        match = zhPattern.search(content)
        if match:
            res_list = list(jieba.cut(content))
        else:
            res_list = nltk.word_tokenize(content)
        for i in res_list:
            if i not in stopList and i.strip()!='' and i!=None:
                if i not in wordsList:
                    wordsList.append(i)
                    
    #若列表中的词已在词典中，则加1，否则添加进去
    def addToDict(self,wordsList,wordsDict):
        for item in wordsList:
            if item in wordsDict.keys():
                wordsDict[item]+=1
            else:
                wordsDict.setdefault(item,1)
    #获得文件里面文档的列表
    def get_File_List(self,filePath):
        filenames=os.listdir(filePath)
        return filenames
    
    #通过计算每个文件中p(s|w)来得到对分类影响最大的15个词
    def getTestWords(self,testDict,spamDict,normDict,normFilelen,spamFilelen):
        wordProbList={}
        for word,num  in testDict.items():
            if word in spamDict.keys() and word in normDict.keys():
                #该文件中包含词个数
                pw_s=spamDict[word]/spamFilelen
                pw_n=normDict[word]/normFilelen
                ps_w=pw_s/(pw_s+pw_n) 
                wordProbList.setdefault(word,ps_w)
            if word in spamDict.keys() and word not in normDict.keys():
                pw_s=spamDict[word]/spamFilelen
                pw_n=0.01
                ps_w=pw_s/(pw_s+pw_n) 
                wordProbList.setdefault(word,ps_w)
            if word not in spamDict.keys() and word in normDict.keys():
                pw_s=0.01
                pw_n=normDict[word]/normFilelen
                ps_w=pw_s/(pw_s+pw_n) 
                wordProbList.setdefault(word,ps_w)
            if word not in spamDict.keys() and word not in normDict.keys():
                #若该词不在脏词词典中，概率设为0.4
                wordProbList.setdefault(word,0.4)
        words=sorted(wordProbList.items(), key=lambda d: d[1], reverse=True)[0:15]
        '''
        wordsDict={}
        for item in words:
            wordsDict[item[0]]=item[1]
        return wordsDict
        '''
        return (wordProbList)
    
    #计算贝叶斯概率
    def calBayes(self,wordList,spamdict,normdict):
        ps_w = 1
        ps_n = 1
        for word, prob in wordList.items():
            ps_w *= (prob)
            ps_n *= (1 - prob)
        print(ps_w)
        print(ps_n)
        p = ps_w / (ps_w + ps_n)
        return p
    #计算预测结果正确率
    def calAccuracy(self,testResult):
        rightCount=0
        errorCount=0
        for name ,catagory in testResult.items():
            if (int(name)<1000 and catagory==0) or(int(name)>1000 and catagory==1):
                rightCount+=1
            else:
                errorCount+=1
        return rightCount/(rightCount+errorCount)