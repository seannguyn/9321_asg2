import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.utils import shuffle
from sklearn.metrics import precision_score, accuracy_score, recall_score
from sklearn.tree import DecisionTreeClassifier
from collections import defaultdict
from collections import defaultdict
from copy import deepcopy
import random


class DecisionTree:
    def __init__(self,dbname=None,theta={'h':10,'u':1,'t':4},split_percentage=0.9):
        self.db=dbname
        self.theta=theta
        self.split_percentage=split_percentage
    def load_data(self):
        usecols=['Bedroom2','Bathroom','Car','Type','Price','Suburb']
        self.df = pd.DataFrame(self.db,columns = usecols)
        self.df.dropna(axis=0,how='any',inplace=True) 
        self.df = shuffle(self.df)
##        self.df['Price']=self.df['Price']/1000000
      
        self.df.replace(self.theta,inplace=True) 
        data_x = self.df.drop('Suburb', axis=1).values
        data_y = self.df['Suburb'].values

        split_point = int(len(data_x) * self.split_percentage)
        data_X_train = data_x[:split_point]
        data_y_train = data_y[:split_point]
        data_X_test = data_x[split_point:]
        data_y_test = data_y[split_point:]

        return data_X_train, data_y_train, data_X_test, data_y_test

    def DecisionTree_Training(self,data_X_test):
        data_X_train, data_y_train, _, _ = self.load_data()
        DecisionTree=DecisionTreeClassifier()
        DecisionTree.fit(data_X_train, data_y_train)
        DecisionTreepre = DecisionTree.predict(data_X_test)

        return DecisionTreepre

    def check_accuracy(self):
        _ ,_ ,data_X_test, data_y_test = self.load_data()
        DecisionTreepre=self.DecisionTree_Training(data_X_test)
        print("the accuracy of DecisionTree:\t", accuracy_score(data_y_test, DecisionTreepre))

    def make_suggestion(self,data_X_test):
        suggestion=self.DecisionTree_Training(data_X_test)
##        print(suggestion)
        return suggestion


class suggestion:
    def __init__ (self,csv_file=None,theta={'h':10,'u':1,'t':4},in_put=None):
        self.csv_file=csv_file
        self.d1=DecisionTree(csv_file,theta,0.9)
        self.in_put=in_put
    def make_suggestions(self):
        _ ,_ ,data_X_test, data_y_test = self.d1.load_data()
        ##in_put is a list with the format ['Bedroom2', 'Bathroom', 'Car', 'Type', 'Price']                .... 'Suburb'
##        in_put=data_X_test[0:1]
        output=[]
        while len(output)<5:
            temp=deepcopy(self.in_put[0])
            bias=random.randint(5,15)*10000
            temp[-1]+=bias
            temp=[temp]
            result=self.d1.make_suggestion(temp)
            if result!=self.in_put[0][0] :#dif sub
                temp=list(temp[0])+list(result)
                output.append(temp)
        return output
       
       
    


    
    


