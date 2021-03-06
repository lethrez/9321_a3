import tensorflow as tf
import numpy as np
import pandas as pd
import time
from keras.models import Sequential
from keras.layers import Dense
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.metrics import confusion_matrix

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.externals import joblib
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier

from sklearn.feature_selection import SelectFromModel

from sklearn.tree import export_graphviz

# WHEN RUNNING MODEL
#from model import clean_model
#from model import meanAndSd
#from model import prediction_clean_data
# WHEN RUNNING BE
from model.model import clean_model
from model.model import meanAndSd
from model.model import prediction_clean_data

#import matplotlib.pyplot as plt



"""
Graph Random forest generator 
"""
def graph_random_forest(data):
    past = time.time()
    X, y = np.split(data, [-1], axis=1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1000)
    model = RandomForestClassifier(max_depth=110, max_features=3, min_samples_leaf=3,
                                   min_samples_split=10, n_estimators=100, random_state=0)
    model.fit(X_train, y_train.values.ravel())
    feat_importance = model.feature_importances_

    indices = np.argsort(feat_importance)[::-1]
    names = [X.columns[i] for i in indices]
    top_10_names = names[:10]
    top_10_features = feat_importance[indices][:10]
    """
    t = ((1, 'a'),(2, 'b'))
    >>> dict((y, x) for x, y in t)
    {'a': 1, 'b': 2}
    """

    a = list()
    for i in range(len(top_10_names)):
        #b["x"]= top_10_names[i]
        #d["y"]= top_10_features[i]
        b = ("x",top_10_names[i])
        d = ("y", top_10_features[i])
        t = (b ,d)
        dicc = dict((x,y) for x,y in t)
        a.append(dicc)
    return a
    """
    To print in matlob values 
    """
    #plt.bar(range(len(10)), top_10_features)
    #plt.xticks(range(len(10)), top_10_names, fontsize=8)
    #plt.title("Top 10 Important Feature")
    #plt.show()

    dictionary = dict(zip(names, feat_importance[indices]))

    dict_columns = {}
    for k,v in dictionary.items():
        if '_' in k:
            a = k.split("_")[0]
            #check if it is in dict
            if a in dict_columns:
                dict_columns[a] = dictionary[k] + dict_columns[a]
            else:
                dict_columns[a]= v
        else:
            a = k
            if a in dict_columns:
                dict_columns[a] = dictionary[k] + dict_columns[a]
            else:
                dict_columns[a] = v
    dict_columns= dict(sorted(dict_columns.items(), key=lambda x: x[1],reverse=True))

    x_feature = list(dict_columns.keys())
    x_values = list(dict_columns.values())
    dict_columns = dict(zip(x_feature,x_values))

    """  to print in matlob"""
    #plt.bar(range(len(x_values)), x_values)
    #plt.xticks(range(len(x_values)), x_feature, fontsize=8)
    #plt.title("Top 10 Important Feature")
    #plt.show()


def graph_random_forest_non_cat(data):
    X, y = np.split(data, [-1], axis=1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1000)
    model = RandomForestClassifier(max_depth=110, max_features=3, min_samples_leaf=3,
                                   min_samples_split=10, n_estimators=100, random_state=0)
    model.fit(X_train, y_train.values.ravel())
    feat_importance = model.feature_importances_

    indices = np.argsort(feat_importance)[::-1]
    names = [X.columns[i] for i in indices]
    dictionary = dict(zip(names, feat_importance[indices]))

    dict_columns = {}
    for k, v in dictionary.items():
        if '_' in k:
            a = k.split("_")[0]
            # check if it is in dict
            if a in dict_columns:
                dict_columns[a] = dictionary[k] + dict_columns[a]
            else:
                dict_columns[a] = v
        else:
            a = k
            if a in dict_columns:
                dict_columns[a] = dictionary[k] + dict_columns[a]
            else:
                dict_columns[a] = v
    dict_columns = dict(sorted(dict_columns.items(), key=lambda x: x[1], reverse=True))

    x_feature = list(dict_columns.keys())
    x_values = list(dict_columns.values())



    a = list()
    for i in range(len(x_feature)):


        b = ("x", x_feature[i])
        d = ("y", x_values[i])
        t = (b, d)
        dicc = dict((x, y) for x, y in t)
        a.append(dicc)

    return a



def train_random_forest(data, X_pred):
    past = time.time()
    X, y = np.split(data, [-1], axis=1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state= 1000)
    model = RandomForestClassifier(max_depth=110,max_features=3,min_samples_leaf=3,
                                   min_samples_split=10,n_estimators=100, random_state= 0)
    model.fit(X_train, y_train.values.ravel())
    y_pred=model.predict(X_test)
    matrix=confusion_matrix(y_test, y_pred)
    feat_importance = model.feature_importances_
    base_accuracy = float((matrix[0][0] + matrix[1][1]) / (sum(matrix[0]) + sum(matrix[1])))
    #graph_random_forest(X,feat_importance)

    #save model for graph generator
    return {
        "model": "Random Forest",
        "accuracy": base_accuracy,
        "time": time.time() - past,
        "prediction": model.predict(X_pred)[0],
    }
def knn(data,X_pred):
    past = time.time()
    X, y = np.split(data, [-1], axis=1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    knn_model = KNeighborsClassifier(n_neighbors=4)
    knn_model.fit(X_train, y_train.values.ravel())
    y_pred=knn_model.predict(X_test)
    matrix=confusion_matrix(y_test, y_pred)
    return {
        "model": "KNN 4 neighbours",
        "accuracy": float((matrix[0][0]+matrix[1][1])/(sum(matrix[0])+sum(matrix[1]))),
        "time": time.time()-past,
        "prediction" : knn_model.predict(X_pred)[0],
    }

def logreg(data,X_pred):
    past = time.time()
    X, y = np.split(data, [-1], axis=1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    lr = LogisticRegression(solver="liblinear", max_iter=100)
    lr.fit(X_train,y_train.values.ravel())
    y_pred=lr.predict(X_test)
    matrix=confusion_matrix(y_test, y_pred)
    return {
        "model": "Logistic Regression",
        "accuracy": float((matrix[0][0]+matrix[1][1])/(sum(matrix[0])+sum(matrix[1]))),
        "time": time.time()-past,
        "prediction" : lr.predict(X_pred)[0],
    }

def logregcoeff(data):
    X, y = np.split(data, [-1], axis=1)
    lr = LogisticRegression(solver="liblinear", max_iter=100)
    lr.fit(X,y.values.ravel())
    data = {}
    for i in range(len(X.columns)):
        data[X.columns[i]] = lr.coef_[0][i]
    data["intercept"] = lr.intercept_[0]
    return data

def dnn(data,X_pred):
    past = time.time()
    X, y = np.split(data, [-1], axis=1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    classifier = Sequential()
    classifier.add(Dense(20, activation='relu', kernel_initializer="random_normal",input_dim=len(X.columns)))
    classifier.add(Dense(10, activation='relu', kernel_initializer="random_normal"))
    classifier.add(Dense(1, activation='sigmoid', kernel_initializer="random_normal"))
    classifier.compile(optimizer ='adam',loss='binary_crossentropy', metrics =['accuracy'])
    classifier.fit(X_train,y_train, batch_size=10, epochs=50)
    y_pred=(classifier.predict(X_test) > 0.5)
    matrix=confusion_matrix(y_test, y_pred)
    return {
        "model": "Deep Neural Network",
        "accuracy": float((matrix[0][0]+matrix[1][1])/(sum(matrix[0])+sum(matrix[1]))),
        "time": time.time()-past,
        "prediction" : int((classifier.predict(X_pred)>0.5)[0][0]),
    }


"""
Pca with random forest 
Dimensional reduction 
"""
def feature_extraction_with_random_forest(data,X_pred):
    past = time.time()
    X, y = np.split(data, [-1], axis=1)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1000)

    model = RandomForestClassifier(max_depth=110, max_features=3, min_samples_leaf=3,
                                   min_samples_split=10, n_estimators=100, random_state=0)
    model.fit(X_train, y_train.values.ravel())

    y_pred = model.predict(X_test)
    matrix = confusion_matrix(y_test, y_pred)
    feat_importance = model.feature_importances_
    indices = np.argsort(feat_importance)[::-1]
    names = [X.columns[i] for i in indices]
    top__names = names
    top__features = feat_importance[indices]
    """
    for feature in zip(top__names,top__features):
        print(feature)
    """
    #selecting model of high importance

    selected_model = SelectFromModel(model,threshold= 0.03)
    selected_model.fit(X_train,y_train.values.ravel())
    """
    for feature_list_index in selected_model.get_support(indices=True):
        print(X.columns[feature_list_index])
    """
    X_important_train = selected_model.transform(X_train)
    X_important_test = selected_model.transform(X_test)

    X_important_pred = selected_model.transform(X_pred)

    model_important = RandomForestClassifier(max_depth=110, max_features=3, min_samples_leaf=3,
                                   min_samples_split=10, n_estimators=100, random_state=0)

    model_important.fit(X_important_train,y_train.values.ravel())

    y_pred = model_important.predict(X_important_test)
    matrix_important = confusion_matrix(y_test, y_pred)

    base_accuracy = float((matrix[0][0] + matrix[1][1]) / (sum(matrix[0]) + sum(matrix[1])))
    # graph_random_forest(X,feat_importance)
    feature_selection_accuracy = float((matrix_important[0][0] + matrix_important[1][1]) / (sum(matrix_important[0]) + sum(matrix_important[1])))
    # save model for graph generator
    return {
        "model": "Random Forest with Feature Extraction",
        # "Base accuracy": base_accuracy,
        "accuracy": feature_selection_accuracy,
        "time": time.time() - past,
        # "prediction by base model": model.predict(X_pred)[0],
        "prediction":model_important.predict(X_important_pred)[0]

    }
