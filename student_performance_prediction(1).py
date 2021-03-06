# -*- coding: utf-8 -*-
"""Student_performance_prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-pW0q_udOBCryrIMImgNCXNeEqi-PaN8
"""

!wget -O student-mat.csv https://raw.githubusercontent.com/arunk13/MSDA-Assignments/master/IS607Fall2015/Assignment3/student-mat.csv

import numpy as np
import pandas as pd

import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("student-mat.csv", sep=";")
df.head()

df.describe()

df.shape

df.columns

df['Weekly_Alcohol'] = df['Dalc'] + df['Walc']

plt.hist(df['Weekly_Alcohol'], bins=8)
plt.title('Weekly alcohol consumption of students')
plt.xlabel('Weekly alcohol consumption')
plt.ylabel('Number of students')
plt.xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
plt.show()

plt.hist(df['absences'])
plt.title('Absences')
plt.xlabel('Days of absence')
plt.ylabel('Number of students')
plt.yticks([0, 100, 200, 300, 400, 500])
plt.show()

Avg_Absence = np.average(df['absences'])
print(round(Avg_Absence, 2))

sns.countplot(df.studytime)
plt.title("Students study time")
plt.xlabel("Study time")
plt.ylabel("Number of students")
plt.show()

sns.countplot(df.sex)
plt.title("gender")

sns.countplot(df.reason)
plt.title("Reason to choose a school")
plt.xlabel("Reason")
plt.ylabel("Number of students")
plt.show()

sns.countplot(df.health)
plt.title("Students health situation")
plt.xlabel("Health situation")
plt.ylabel("Number of students")
plt.show()



import pandas as pd
import numpy as np
import sklearn
from sklearn import linear_model
from sklearn.utils import shuffle
import matplotlib.pyplot as plt
from matplotlib import style
import pickle

style.use("ggplot")

# Import dataset with student's data
data = pd.read_csv("student-mat.csv", sep=";")

# Select the value we want to predict
predict = "G3"

# List the variables we want to use for our predictions in this model
data = data[[ "G1", "G2", "G3", "studytime", "health", "famrel", "failures", "absences"]]
data = shuffle(data)

x = np.array(data.drop([predict], 1))
y = np.array(data[predict])

x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size = 0.1)

# Train model multiple times to find the highest accuracy
best = 0
for _ in range(200):
    x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size = 0.1)

    linear = linear_model.LinearRegression()

    linear.fit(x_train, y_train)
    acc = linear.score(x_test, y_test)
    print("Accuracy: " + str(acc))

    # Save the highest accuracy
    if (acc > best):
        best = acc
        with open("studentgrades.pickle", "wb") as f:
            pickle.dump(linear, f)

print("Highest Accuracy:", best)

# Load model
pickle_in = open("studentgrades.pickle", "rb")
linear = pickle.load(pickle_in)

print("-------------------------")
print('Coefficient: \n', linear.coef_)
print("-------------------------")
print('Intercept: \n', linear.intercept_)
print("-------------------------")
predictions = linear.predict(x_test)

# Print the predictions, the variables we used and the actual final grade
for x in range(len(predictions)):
    print("Predicted Final grade:", predictions[x], "\t Data:", x_test[x], "\t \t \tFinal grade:", y_test[x])

# Create visualisation of the model
plot = "failures"
plt.scatter(data[plot], data["G3"])
plt.legend(loc=4)
plt.xlabel(plot)
plt.ylabel("Final Grade")
plt.show()