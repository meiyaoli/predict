import pandas as pd

df1 = pd.read_csv('PBI - redcap/_final/demographics.csv')
df2 = pd.read_csv('PBI - redcap/_final/classification.csv')
df3 = pd.read_csv('PBI - redcap/_final/discharge.csv')
df4 = pd.read_csv('PBI - redcap/_final/end_points.csv')
df5 = pd.read_csv('PBI - redcap/_final/general_health_history.csv')
df6 = pd.read_csv('PBI - redcap/_final/history_of_disease.csv')
df7 = pd.read_csv('PBI - redcap/_final/imaging_diagnostics.csv')
df8 = pd.read_csv('PBI - redcap/_final/lab.csv')
df9 = pd.read_csv('PBI - redcap/_final/identification.csv')
# df10 = pd.read_csv('PBI - redcap/_final/second_insults.csv')
df11 = pd.read_csv('PBI - redcap/_final/surgeries_other_procedures.csv')
df12 = pd.read_csv('PBI - redcap/_final/therapies.csv')
df13 = pd.read_csv('PBI - redcap/_final/vitals.csv')

combined_df = pd.concat(
    [df1, df2, df3, df4, df5, df6, df7, df8, df9, df11, df12, df13], ignore_index=True)

combined_df.to_csv('PBI - redcap/_final/_combined.csv', index=False)
