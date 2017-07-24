#!/usr/bin/python
from sklearn import datasets
from sklearn.semi_supervised import LabelPropagation
from sklearn import svm
from sklearn.svm import LinearSVC
from sklearn.model_selection import GridSearchCV, KFold, cross_val_score, train_test_split
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix
from sklearn import metrics
from sklearn.metrics import roc_auc_score
from sklearn.cross_validation import cross_val_predict
import numpy as np
#this block is storing the file names
data_set = []
with open('/home/rahman/Documents/MT/data_file.txt', 'r') as f:
 
    first_line = f.readline()

    while first_line:
        index = first_line.find(" ")
        file_name = first_line[0:index]
        data_set.append(file_name)
        first_line = f.readline()

data_matrix = np.zeros((62,3600))

#this block is storing the feature counts in "data_matrix"  for each file
with open('/home/rahman/Documents/MT/data_file.txt', 'r') as f:
    first_line = f.readline()
    column = 0
    row = 0
    starting_index = 33
    while first_line:
        index = first_line.find(" ", 33)
        while not index == -1:
            element = first_line[starting_index:index]
            starting_index = index + 1
            index = first_line.find(" ", index+1)
            
            if element:
                element = float(element)
                data_matrix[row][column] = element
                column = column + 1


        first_line = f.readline()
        row = row + 1
        column = 0

#read in the labels.txt file and store them in a labels matrix
labels = []
with open('/home/rahman/Documents/MT/labels_add.txt', 'r') as f:
    first_line = f.readline()
    
    while first_line:
        first_line = first_line.strip('\n')
        labels.append(first_line)
        first_line = f.readline()

labels = map(int, labels)

train_data, test_data, train_labels, test_labels = train_test_split(data_matrix, labels, test_size = .25, random_state = 42)
model = svm.LinearSVC()
model.fit(train_data, train_labels)
print(LinearSVC.score( model, test_data, test_labels))
y=(LinearSVC.predict(model,test_data))


#model =tree.DecisionTreeClassifier()
#model.fit(train_data, train_labels)
#print(DecisionTreeClassifier.score(model, test_data, test_labels))
print train_labels
print test_labels
#y=(DecisionTreeClassifier.predict(model,test_data))
print y
score=cross_val_predict(estimator=model, X=data_matrix, y=labels, cv=6)
print labels
print score
print (roc_auc_score(labels,score,None))
print (confusion_matrix(labels,score))
f,t,th= (metrics.roc_curve(labels,score))
print f


