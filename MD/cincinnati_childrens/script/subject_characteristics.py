import pandas as pd

df = pd.read_excel("MD/cincinnati_childrens/raw_final/raw_subject_characteristics.xlsx")

#strip whitespace/trailing
df.columns = df.columns.str.strip()

#drop unnecessary columns
df.drop(columns=['Complete?'], inplace=True)

#replace NaN
df = df.fillna('')

#drop empty rows
df = df.dropna(how='all')

#renaming the columns to match dictionary
df.rename(columns={
    'Honest Broker Subject ID': 'HONEST_BROKER_SUBJECT_ID',
    'Data Contributor': 'DATA_CONTRIBUTOR_ID',
    'Data Source': 'DATA_SOURCE',
    'The last known survival status of the subject': 'LAST_KNOWN_SURVIVAL_STATUS',
    'Age of the subject at last contact': 'AGE_LAST_CONTACT',
    'Unit of age of at last contact': 'AGE_LAST_CONTACT_UNIT',
    'Precision of age of last contact': 'AGE_LAST_CONTACT_PRECISION'
}, inplace=True)

print(df.to_string(index=False))

df.to_excel('MD/cincinnati_childrens/_final/subject_characteristics.xlsx', index=False)
print("✓ Data exported successfully.")
