# coding=utf-8

import numpy as np
from cleanText import cleanString
from sklearn.svm import LinearSVC
from sklearn.metrics import confusion_matrix, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from joblib import dump, load
import pickle
from Bayes import Spam_Bayes
import os

# Get the original dataset
def store():

    # workBookOld = openpyxl.load_workbook('DataSet.xlsx')
    # dataSheetOld = workBookOld['Data set']
    #
    # xData = []
    # yData = []
    #
    # rows = dataSheetOld.max_row
    #
    # for i in range(2, rows+1):
    #
    #     if (str(dataSheetOld.cell(row = i, column = 2).value) != 'None'):
    #         xData.append(str(cleanString(dataSheetOld.cell(row = i, column = 1).value)))
    #         if (str(dataSheetOld.cell(row = i, column = 2).value) == "1"):
    #             yData.append(1)
    #         else:
    #             yData.append(0)

    xData = []
    yData = []
    for x in range(1, 12911):
        f = open('E:/2019实训/EnglishData/normal/' + str(x), 'r', errors='ignore')
        xData.append(str(cleanString(f.read())))
        yData.append(0)
        print(x)
        f.close()
    for x in range(1, 24913):
        f = open('E:/2019实训/EnglishData/spam/' + str(x), 'r', errors='ignore')
        xData.append(str(cleanString(f.read())))
        yData.append(1)
        print(x)
        f.close()

    # NOTE: to train data on the entire dataset, simply return xData and yData
    # Splitting the data like this is to obtain test cases and calculate the F-score of the learning algorithm
    xTrain, xTest, yTrain, yTest = train_test_split(xData, yData, test_size=0.2, random_state=0)
    return xTrain, xTest, yTrain, yTest


# Calculating the F-score
def calcFScore(xTest, yTest, model, vectorizer):
    
    xTestMatrix = vectorizer.transform(xTest)
    yTestMatrix = np.asarray(yTest)

    result = model.predict(xTestMatrix)
    matrix = confusion_matrix(yTestMatrix, result)

    fScore = f1_score(yTestMatrix, result, pos_label = 0)
    precision = precision_score(yTestMatrix, result, pos_label=0)
    recall = recall_score(yTestMatrix, result, pos_label=0)
    return fScore, precision, recall, matrix

# Test new data for Spam
def predict(emailBody, model, vectorizer):

    featureMatrix = vectorizer.transform([cleanString(emailBody)])
    result = model.predict(featureMatrix)
    print("Predicting...")

    if (1 in result):
        return "Spam"
    else:
        return "Not Spam"

def train():
    model = LinearSVC(class_weight='balanced')

    # Create training data
    xTrain, xTest, yTrain, yTest = store()

    vectorizer = TfidfVectorizer(stop_words='english', max_df=75,decode_error="replace")
    yTrainMatrix = np.asarray(yTrain)
    xTrainMatrix = vectorizer.fit_transform(xTrain)

    # Training SVM classifier
    model.fit(xTrainMatrix, yTrainMatrix)
    fScore, precision, recall, matrix = calcFScore(xTest, yTest, model, vectorizer)

    dump(model, 'model.joblib')
    feature_path = 'vectorizer.pkl'
    with open(feature_path, 'wb') as fw:
        pickle.dump(vectorizer.vocabulary_, fw)

    print(fScore, precision, recall)
    print(matrix)

# Test
def test(model,vectorizer):
    f=open("test.txt")
    content=f.read()
    f.close()
    result=predict(content,model,vectorizer)
    print(result)

def accuracy(model,vectorizer):
    allnum=0
    cornum=0
    bayes=Spam_Bayes()
    # path=os.listdir('E:/2019实训/endata1/train0/')
    # for x in path:
    #     f = open('E:/2019实训/endata1/train0/' + x, 'r', errors='ignore')
    #     test = f.read()
    #     f.close()
    #     allnum+=1
    #     result1=predict(test,model,vectorizer)
    #     result2=bayes.test(test)
    #     if result1=="Not Spam" and result2=="Not Spam":
    #         print(x+"——"+"Not Spam")
    #         if int(x)<1000:
    #             cornum+=1
    #     else:
    #         print(x+"——"+"Spam")
    #         if int(x)>1000:
    #             cornum+=1
    # print('准确率：' + str(cornum/allnum))
    for x in range(1,352):
        f = open('E:/2019实训/endata1/spam/' + str(x), 'r', errors='ignore')
        test = f.read()
        f.close()
        allnum+=1
        result1 = predict(test, model, vectorizer)
        result2=bayes.test(test)
        if result1 == "Not Spam" and result2 == "Not Spam":
            print(str(x)+"——"+"Not Spam")
        else:
            print(str(x)+"——"+"Spam")
            cornum += 1
    print('准确率：' + str(cornum/allnum))

if __name__ == '__main__':
    model = load('model.joblib')
    path = 'vectorizer.pkl'
    vectorizer = CountVectorizer(decode_error="replace", vocabulary=pickle.load(open(path, "rb")))
#    test(model, vectorizer)
    accuracy(model, vectorizer)