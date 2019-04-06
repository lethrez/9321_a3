import tensorflow as tf
import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

from sklearn.linear_model import LogisticRegression

from sklearn.neighbors import KNeighborsClassifier
from sklearn.externals import joblib
import pickle

# WHEN RUNNING MODEL
from model import clean_model
from model import meanAndSd
from model import prediction_clean_data
# WHEN RUNNING BE
# from model.model import clean_model
# from model.model import meanAndSd
# from model.model import prediction_clean_data
import matplotlib.pyplot as plt



def save_model(model , filename ):
    joblib.dump(model,filename)



def train_knn(data):
    X, y = np.split(data, [-1], axis=1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    knn_model = KNeighborsClassifier(n_neighbors=4)
    knn_model.fit(X_train, y_train.values.ravel())
    y_pred=knn_model.predict(X_test)
    matrix=confusion_matrix(y_test, y_pred)
    return {
        "message": f"KNN prediction accuracy:{(matrix[0][0]+matrix[1][1])/(sum(matrix[0])+sum(matrix[1]))}" ,
        "no_correct" : matrix[0][0],
        "no_incorrect" : matrix[0][1],
        "yes_correct" : matrix[1][1],
        "yes_incorrect" : matrix[1][0],
    }
    #save the model
    #with open("model_knn",'wb') as f:
        #pickle.dump(knn_model)
    # save_model(knn_model,"knn_model.sav")

def logregcoeff(data):
    X, y = np.split(data, [-1], axis=1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    lr = LogisticRegression(solver="liblinear", max_iter=100)
    lr.fit(X_train,y_train.values.ravel())
    y_pred=lr.predict(X_test)
    matrix=confusion_matrix(y_test, y_pred)
    return {
        "message": f"KNN prediction accuracy:{(matrix[0][0]+matrix[1][1])/(sum(matrix[0])+sum(matrix[1]))}" ,
        "no_correct" : matrix[0][0],
        "no_incorrect" : matrix[0][1],
        "yes_correct" : matrix[1][1],
        "yes_incorrect" : matrix[1][0],
    }
    # print(y_pred[0])
    # print(sigmoid(0))
    
    # calculates propbability..
    # print(sigmoid(lr.intercept_[0] + sum([X_test.iloc[0][i]*lr.coef_[0][i] for i in range(len(X_test.iloc[0]))])))
    
    # print(lr.coef_, lr.intercept_)
    # print(confusion_matrix(y_test, y_pred))
    # print([i for i in range(len(X_test.iloc[0]))])
    # print( X.colums[i] for i in range(len(X.columns)))
    data = {}
    for i in range(len(X.columns)):
        data[X.columns[i]] = lr.coef_[0][i]
    data["intercept"] = lr.intercept_[0]
    return data



"""
Parameters:
            :arg Analytics : Takes Pandas data frame 
            :arg normalised_data: which is already generated so don't change unless we have new data
            :arg fil : saved model file, default is knn_model
"""


def predict_Data(analytics, normalised_data = "normalised.csv",file = "knn_model.sav"):
    normalised_data = pd.read_csv("./../data/{}".format(normalised_data))
    #splitting categorical values
    #to normalise we need to reduce the age  testbps chol thalach oldpeak
    #iteratively
    x_test = prediction_clean_data(analytics,normalised_data)
     #finally load and predict data
    model = joblib.load(file)
    result = model.predict(x_test)
    return result

def train_random_forest():
    pass

def logreg(data):
    X, y = np.split(data, [-1], axis=1)
    lr = LogisticRegression(solver="liblinear", max_iter=100)
    lr.fit(X,y.values.ravel())
    data = {}
    for i in range(len(X.columns)):
        data[X.columns[i]] = lr.coef_[0][i]
    data["intercept"] = lr.intercept_[0]
    return data

    

def sigmoid(x):
    return 1 / (1 + np.e**(-x))

def dnn(data):
    X, y = np.split(data, [-1], axis=1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    classifier = Sequential()
    classifier.add(Dense(20, activation='relu', kernel_initializer="random_normal",input_dim=len(X.columns)))
    classifier.add(Dense(10, activation='relu', kernel_initializer="random_normal"))
    classifier.add(Dense(1, activation='sigmoid', kernel_initializer="random_normal"))
    classifier.compile(optimizer ='adam',loss='binary_crossentropy', metrics =['accuracy'])
    classifier.fit(X_train,y_train, batch_size=10, epochs=100)
    y_pred=(classifier.predict(X_test) > 0.5)
    #print(confusion_matrix(y_test, y_pred))


def pca():
    pass



if __name__=="__main__":
    # like os method, assumes file is run from file location #
    model = pd.read_csv("./../data/model.csv")
    print(train_knn(model))
    # dnn(model)
    # print(logreg(model))
    #logreg(model)
    ## all testing after this one
    #print (analytics)
    #normalise new data
    #dnn(model, 2)

