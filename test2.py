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

# Preprocess each yearly data
data_frames = [american2011, american2012, american2013, american2014, american2015]

# Create a dataframe with total hits per player per year for all years
total_hits_all_years = (
    pd.concat(data_frames).groupby(["Year", "Name"])["H"].sum().reset_index()
)

for i in range(len(data_frames)):
    data_frames[i]["Year"] = 2011 + i
    data_frames[i]["Game_ID"] = data_frames[i].groupby(["Name"]).cumcount() + 1
    data_frames[i] = data_frames[i][
        data_frames[i]["Game_ID"] <= 60
    ]  # Select the first 60 games for each player
    # Sum up the stats for the first 60 games
    data_frames[i] = (
        data_frames[i]
        .groupby(["Year", "Name"])
        .agg(
            {
                "AB": "sum",
                "H": "sum",
                "BB": "sum",
                "RBI": "sum",
                "SO": "sum",
                "SB": "sum",
            }
        )
        .reset_index()
    )
    # Map the total hits for the year from the total_hits_all_years dataframe
    data_frames[i] = data_frames[i].merge(
        total_hits_all_years, on=["Year", "Name"], suffixes=("", "_total")
    )
    # Drop the H column (we're going to predict H_total)
    data_frames[i] = data_frames[i].drop(columns="H")

data_2011 = data_frames[0]
data_2013 = data_frames[2]
data_2014 = data_frames[3]
data_2015 = data_frames[4]

# Model training for each year (excluding 2015)
model_2011 = LinearRegression()
model_2011.fit(
    data_2011.drop(columns=["Name", "Year", "H_total"]), data_2011["H_total"]
)

model_2013 = LinearRegression()
model_2013.fit(
    data_2013.drop(columns=["Name", "Year", "H_total"]), data_2013["H_total"]
)

model_2014 = LinearRegression()
model_2014.fit(
    data_2014.drop(columns=["Name", "Year", "H_total"]), data_2014["H_total"]
)

# Predict for 2015
X_test = data_2015.drop(columns=["Name", "Year", "H_total"])

preds_2011 = model_2011.predict(X_test)
preds_2013 = model_2013.predict(X_test)
preds_2014 = model_2014.predict(X_test)

final_preds = (preds_2011 + preds_2013 + preds_2014) / 3.0
data_2015["Predicted_H_total"] = final_preds
