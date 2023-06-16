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
american2013 = pd.read_csv("american2013.csv")
american2014 = pd.read_csv("american2014.csv")
american2015 = pd.read_csv("american2015.csv")
american2022 = pd.read_csv("american2022.csv")
american2023 = pd.read_csv("american2023.csv")

american2011["Year"] = 2011
american2013["Year"] = 2013
american2014["Year"] = 2014
american2015["Year"] = 2015
american2022["Year"] = 2022
american2023["Year"] = 2023

data_frames = [
    american2011,
    american2013,
    american2014,
    american2015,
    american2022,
    american2023,
]
years = [2011, 2013, 2014, 2015, 2022, 2023]

total_hits_all_years = (
    pd.concat(data_frames).groupby(["Year", "Name"])["H"].sum().reset_index()
)

for i in range(len(data_frames)):
    data_frames[i]["Year"] = years[i]
    data_frames[i]["Game_ID"] = data_frames[i].groupby(["Name"]).cumcount() + 1
    data_frames[i] = data_frames[i][data_frames[i]["Game_ID"] <= 60]

    data_frames[i] = (
        data_frames[i]
        .groupby(["Year", "Name"])
        .agg(
            {
                "AB": "sum",
                "R": "sum",
                "H": "sum",
                "TB": "sum",
                "2B": "sum",
                "3B": "sum",
                "HR": "sum",
                "RBI": "sum",
                "BB": "sum",
                "IBB": "sum",
                "SO": "sum",
                "SB": "sum",
                "CS": "sum",
            }
        )
        .reset_index()
    )
    data_frames[i] = data_frames[i].merge(
        total_hits_all_years, on=["Year", "Name"], suffixes=("", "_total")
    )
    data_frames[i] = data_frames[i].drop(columns="H")

data_2011 = data_frames[0]
data_2013 = data_frames[1]
data_2014 = data_frames[2]
data_2015 = data_frames[3]
data_2022 = data_frames[4]
data_2023 = data_frames[5]

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

model_2015 = LinearRegression()
model_2015.fit(
    data_2015.drop(columns=["Name", "Year", "H_total"]), data_2015["H_total"]
)

X_test = data_2022.drop(columns=["Name", "Year", "H_total"])

preds_2011 = model_2011.predict(X_test)
preds_2013 = model_2013.predict(X_test)
preds_2014 = model_2014.predict(X_test)
preds_2015 = model_2015.predict(X_test)

final_preds = (preds_2011 + preds_2013 + preds_2014 + preds_2015) / 4.0
data_2022["Predicted_H_total"] = final_preds
sorted_data_2022 = data_2022.sort_values(by="H_total", ascending=False).reset_index(
    drop=True
)
sorted_data_2022

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

models = [model_2011, model_2013, model_2014, model_2015]
years = [2011, 2013, 2014, 2015]
data = [data_2011, data_2013, data_2014, data_2015]

for i, model in enumerate(models):
    y_true = data[i]["H_total"]
    y_pred = model.predict(data[i].drop(columns=["Name", "Year", "H_total"]))

    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_true, y_pred)

    print(f"Model {years[i]} Evaluation:")
    print(f"MAE: {mae}")
    print(f"MSE: {mse}")
    print(f"RMSE: {rmse}")
    print(f"R^2: {r2}")
    print("-------------------------")

y_true_final = data_2022["H_total"]
y_pred_final = data_2022["Predicted_H_total"]

mae_final = mean_absolute_error(y_true_final, y_pred_final)
mse_final = mean_squared_error(y_true_final, y_pred_final)
rmse_final = np.sqrt(mse_final)
r2_final = r2_score(y_true_final, y_pred_final)

print("Final Model Evaluation:")
print(f"MAE: {mae_final}")
print(f"MSE: {mse_final}")
print(f"RMSE: {rmse_final}")
print(f"R^2: {r2_final}")
print("-------------------------")

plt.figure(figsize=(10, 8))
plt.scatter(y_true_final, y_pred_final, color="blue")
plt.plot(
    [y_true_final.min(), y_true_final.max()],
    [y_true_final.min(), y_true_final.max()],
    "k--",
    lw=4,
)
plt.xlabel("Actual")
plt.ylabel("Predicted")
plt.title("Actual vs. Predicted Total Hits for Year 2023")
plt.show()
