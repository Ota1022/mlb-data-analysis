for stats in [american_yearly_totals_df,national_yearly_totals_df,american_yearly_totals_df_first_60,national_yearly_totals_df_first_60]:
    for i in range(len(stats)):
        if stats.iloc[i,9].astype(int) <=5:
            stats.loc[i,'Top5'] = 1
        else:
            stats.loc[i,'Top5'] = 0
            
            
            
train_data=pd.merge(train_data[['Year', 'Name','Top5']],train_data_first_60,on=['Year', 'Name'])
test_data=pd.merge(test_data[['Year', 'Name','Top5']],test_data_first_60,on=['Year', 'Name'])
import lightgbm as lgb
# Select features and target for the model
# X_train = train_data_first_60[['age','Years_since_debut','tall','bt','Home Tm','Away Tm','Rank','SS','HP2F','PA','AB','R','2B','3B','HR','RBI','BB','SO','SB','CS','HBP','AVG','OBP','SLG','OPS']]
# X_train = train_data_first_60[['age','Years_since_debut','tall','Home Tm','Away Tm','Rank','SS','HP2F','PA','R','2B','3B','HR','RBI','BB','SO','SB','CS']]
X_train = train_data[['age','Years_since_debut','tall','Home Tm','Away Tm','SS','HP2F','PA','R','2B','3B','HR','BB','SO','SB','CS']]
y_train = train_data['Top5_x']

cfmodel = lgb.LGBMClassifier()
cfmodel.fit(X_train, y_train)

X_test = test_data[['age','Years_since_debut','tall','Home Tm','Away Tm','SS','HP2F','PA','R','2B','3B','HR','BB','SO','SB','CS']]
# X_test = test_data_first_60[['age','Years_since_debut','tall','Home Tm','Away Tm','Rank','SS','HP2F','PA','R','2B','3B','HR','RBI','BB','SO','SB','CS']]
# X_test = test_data_first_60[['age','Years_since_debut','tall','bt','Home Tm','Away Tm','Rank','SS','HP2F','PA','AB','R','2B','3B','HR','RBI','BB','SO','SB','CS','HBP','AVG','OBP','SLG','OPS']]
y_test = test_data['Top5_x'].values
y_pred = cfmodel.predict(X_test)
y_prob = cfmodel.predict_proba(X_test)


results_2022 = test_data[['Year', 'Name']].copy()
results_2022['Predicted_rank'] = y_pred
results_2022['Actual_rank'] = y_test
results_2022['predicted'] =y_prob[:, 1]

results_2022.head(20)
