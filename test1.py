import calendar
import warnings
from datetime import datetime

import japanize_matplotlib
import lightgbm as lgb
import matplotlib.pyplot as plt
import missingno as msno
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats
from sklearn import metrics
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.preprocessing import StandardScaler

pd.set_option("display.max_columns", 100)
pd.options.mode.chained_assignment = None
warnings.filterwarnings("ignore")

american2011 = pd.read_csv("american2011.csv")
american2012 = pd.read_csv("american2012.csv")
american2013 = pd.read_csv("american2013.csv")
american2014 = pd.read_csv("american2014.csv")
american2015 = pd.read_csv("american2015.csv")

american2011["Year"] = 2011
american2012["Year"] = 2012
american2013["Year"] = 2013
american2014["Year"] = 2014
american2015["Year"] = 2015

df = pd.concat(
    [american2011, american2012, american2013, american2014, american2015]
).reset_index(drop=True)

float_columns = [
    "Rank",
    "AB",
    "R",
    "H",
    "TB",
    "2B",
    "3B",
    "HR",
    "RBI",
    "BB",
    "IBB",
    "SO",
    "SB",
    "CS",
    "AVG",
    "OBP",
    "SLG",
    "HBP",
    "SAC",
    "SF",
    "Year",
]
str_columns = ["Name", "Date", "Team", "OPP"]

df[float_columns] = df[float_columns].astype(float)
df[str_columns] = df[str_columns].astype(str)

df[["Month", "Day"]] = df["Date"].str.split(" ", expand=True)[[0, 1]]
df["Month"] = (
    df["Month"]
    .map(
        {
            "Jan": 1,
            "Feb": 2,
            "Mar": 3,
            "Apr": 4,
            "May": 5,
            "Jun": 6,
            "Jul": 7,
            "Aug": 8,
            "Sep": 9,
            "Oct": 10,
            "Nov": 11,
            "Dec": 12,
        }
    )
    .astype("Int64")
)
df["Day"] = pd.to_numeric(df["Day"].str.replace(",", ""), errors="coerce").astype(
    "Int64"
)

df["Home"] = np.where(df["OPP"].str.contains("@"), 1, 0)
df["Away"] = np.where(df["OPP"].str.contains("vs"), 1, 0)
df["OPP"] = df["OPP"].str.replace("@ ", "").str.replace("vs ", "")
df = df.drop(["Date"], axis=1)

df["1B"] = df["H"] - df["2B"] - df["3B"] - df["HR"]

df_yearly = (
    df.groupby(["Year", "Name"])
    .agg(
        {
            "AB": "sum",
            # 'R': 'sum',
            "H": "sum",
            # 'TB': 'sum',
            "BB": "sum",
            # 'HBP': 'sum',
            # 'SF': 'sum',
            # '1B': 'sum',
            # '2B': 'sum',
            # '3B': 'sum',
            # 'HR': 'sum'
            "RBI": "sum",
            "SO": "sum",
            "SB": "sum",
        }
    )
    .reset_index()
)

# df_yearly['AVG'] = df_yearly['H'] / df_yearly['AB']
# df_yearly['OBP'] = (df_yearly['H'] + df_yearly['BB'] + df_yearly['HBP']) / (df_yearly['AB'] + df_yearly['BB'] + df_yearly['HBP'] + df_yearly['SF'])
# df_yearly['SLG'] = (df_yearly['1B'] + 2*df_yearly['2B'] + 3*df_yearly['3B'] + 4*df_yearly['HR']) / df_yearly['AB']

data_2011 = df_yearly[df_yearly["Year"] == 2011].reset_index()
data_2013 = df_yearly[df_yearly["Year"] == 2013].reset_index()
data_2014 = df_yearly[df_yearly["Year"] == 2014].reset_index()
data_2015 = df_yearly[df_yearly["Year"] == 2015].reset_index()

X_train_2011 = data_2011.drop(columns=["Name", "Year", "H"])
final_2011 = data_2011[["Name", "Year", "H"]].copy()
y_train_2011 = data_2011[["H"]]
y_train_2011 = y_train_2011["H"]
model_2011 = LinearRegression()
scores = cross_val_score(
    model_2011, X_train_2011, y_train_2011, scoring="neg_mean_absolute_error", cv=5
)
mean_score = np.mean(-scores)
# print('Mean Absolute Error with 5-fold cross-validation:', mean_score)
X_train, X_test, y_train, y_test = train_test_split(
    X_train_2011, y_train_2011, test_size=0.2, random_state=0
)
model_2011.fit(X_train, y_train)
y_pred = model_2011.predict(X_test)
# print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))
y_pred_all = model_2011.predict(X_train_2011)
final_2011["Predicted_H"] = y_pred_all
# print(final_2011)

X_train_2013 = data_2013.drop(columns=["Name", "Year", "H"])
final_2013 = data_2013[["Name", "Year", "H"]].copy()
y_train_2013 = data_2013[["H"]]
y_train_2013 = y_train_2013["H"]
model_2013 = LinearRegression()
scores = cross_val_score(
    model_2013, X_train_2013, y_train_2013, scoring="neg_mean_absolute_error", cv=5
)
mean_score = np.mean(-scores)
# print('Mean Absolute Error with 5-fold cross-validation:', mean_score)
X_train, X_test, y_train, y_test = train_test_split(
    X_train_2013, y_train_2013, test_size=0.2, random_state=0
)
model_2013.fit(X_train, y_train)
y_pred = model_2013.predict(X_test)
# print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))
y_pred_all = model_2013.predict(X_train_2013)
final_2013["Predicted_H"] = y_pred_all

X_train_2014 = data_2014.drop(columns=["Name", "Year", "H"])
final_2014 = data_2014[["Name", "Year", "H"]].copy()
y_train_2014 = data_2014[["H"]]
y_train_2014 = y_train_2014["H"]
model_2014 = LinearRegression()
scores = cross_val_score(
    model_2014, X_train_2014, y_train_2014, scoring="neg_mean_absolute_error", cv=5
)
mean_score = np.mean(-scores)
# print('Mean Absolute Error with 5-fold cross-validation:', mean_score)
X_train, X_test, y_train, y_test = train_test_split(
    X_train_2014, y_train_2014, test_size=0.2, random_state=0
)
model_2014.fit(X_train, y_train)
y_pred = model_2014.predict(X_test)
# print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))
y_pred_all = model_2014.predict(X_train_2014)
final_2014["Predicted_H"] = y_pred_all
# print(final_2014)

X_train_2015 = data_2015.drop(columns=["Name", "Year", "H"])
final_2015 = data_2015[["Name", "Year", "H"]].copy()
y_train_2015 = data_2015[["H"]]
y_train_2015 = y_train_2015["H"]

preds_2011 = model_2011.predict(X_train_2015)
preds_2013 = model_2013.predict(X_train_2015)
preds_2014 = model_2014.predict(X_train_2015)

final_preds = (preds_2011 + preds_2013 + preds_2014) / 3.0
final_2015["Predicted_H"] = final_preds
print(final_2015)
