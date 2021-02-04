
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.datasets import load_breast_cancer
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
from sklearn import tree
import pandas as pd
from sklearn.datasets import load_iris


import __Loader_support as LS
import _UIConstants_support as UICS

data = load_iris()


path_dataset = "D:\Candy\Documents\GitHub\OOTO-Miner-Python-V3\_input\Short 16 - Uniandes_Dataset.csv"
# path_dataset = "D:\Candy\Documents\GitHub\OOTO-Miner-Python-V3\_input\Converted Dataset.csv"
df = pd.read_csv(path_dataset)

# print(df)
# df = pd.DataFrame(data.data, columns = data.feature_names)
df['target'] = df['b1']


# df = pd.DataFrame(data.data, columns=data.feature_names)
# df['target'] = data.target

# X_train, X_test, Y_train, Y_test = train_test_split(df[data.feature_names], df['target'], random_state=0)
X_train, X_test, Y_train, Y_test = train_test_split(df[df.columns], df['target'], random_state = 0)



# Step 1: Import the model you want to use
# This was already imported earlier in the notebook so commenting out
#from sklearn.tree import DecisionTreeClassifier
# Step 2: Make an instance of the Model
clf = DecisionTreeClassifier(max_depth = 2,
                             random_state = 0)
# Step 3: Train the model on the data
print("X train")
print(X_train)
print("Y train")
print(Y_train)
clf.fit(X_train, Y_train)
# Step 4: Predict labels of unseen (test) data
# Not doing this step in the tutorial
# clf.predict(X_test)

tree.plot_tree(clf)

fn = df.columns  # ['sepal length (cm)', 'sepal width (cm)', 'petal length (cm)', 'petal width (cm)']
# cn = ['setosa', 'versicolor', 'virginica']
fig, axes = plt.subplots(nrows = 1, ncols = 1, figsize = (4, 4), dpi = 300)

tree.plot_tree(clf,
               feature_names = fn,
               # class_names = cn,
               filled = True)
# tree.plot_tree(clf,
#                feature_names = fn,
#                class_names = cn,
#                filled = True)
fig.savefig('imagename.png')


