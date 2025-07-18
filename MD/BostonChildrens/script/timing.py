import pandas as pd

df = pd.read_csv("csv/timing.csv")

#strip whitespace/trailing
df.columns = df.columns.str.strip()

#determine how many family member columns there are
columns_per_member = 5 #5 columns per member
member_blocks = (df.shape[1] - 1) // columns_per_member #first column is honest broker so we excluded it by using -1 because it's not a repeating family member data

#reshaping/melting into a long format which gives one row per family member 
records = []

for idx, row in df.iterrows():
    subject_id = row['Honest Broker Subject ID']
    subject_has_data = False 

    for i in range(member_blocks):
        offset = 1 + i * columns_per_member
        timepoint_col = df.columns[offset]
        age_at_col = df.columns[offset + 1]
        age_unit_col = df.columns[offset + 2]
        age_precision_col = df.columns[offset + 3]

        timepoint = row[timepoint_col]
        age_at = row[age_at_col]
        age_unit = row[age_unit_col]
        age_precision = row[age_precision_col]

        if pd.notna(timepoint) or pd.notna(age_at) or pd.notna(age_unit) or pd.notna(age_precision):
            subject_has_data = True
            records.append({
                'HONEST_BROKER_SUBJECT_ID': subject_id,
                'TIMEPOINT': timepoint,
                'AGE_AT': age_at,
                'AGE_UNIT': age_unit,
                'AGE_PRECISION': age_precision
            })

    #if no data rows were collected, add a single blank row with just the honest broker subject id data
    if not subject_has_data:
        records.append({
            'HONEST_BROKER_SUBJECT_ID': subject_id,
                'TIMEPOINT': '',
                'AGE_AT':'',
                'AGE_UNIT': '',
                'AGE_PRECISION': ''
        })

df_clean = pd.DataFrame(records)

#replace NaN
df_clean.fillna('', inplace=True)

print(df_clean.to_string(index=False))

# df_clean.to_excel('_final/timing.xlsx', index=False)
# print("✓ Data exported successfully.")
