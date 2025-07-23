import pandas as pd

df = pd.read_csv("csv/medical_history.csv")

#strip column names
df.columns = df.columns.str.strip()

#store subject ID
subject_id = df['Honest Broker Subject ID']

#determine how many family member columns there are
columns_per_member = 6 #6 columns per member
member_blocks = (df.shape[1] - 1) // columns_per_member #first column is honest broker so we excluded it by using -1 because it's not a repeating family member data

#reshaping/melting into a long format which gives one row per condition
records = []

for idx, row in df.iterrows():
    subject_id = row['Honest Broker Subject ID']
    subject_has_data = False 

    for i in range(member_blocks):
        offset = 1 + i * columns_per_member
        age_at_col = df.columns[offset]
        age_unit_col = df.columns[offset + 1]
        age_precision_col = df.columns[offset + 2]
        condition_col = df.columns[offset + 3]
        icd_code_col = df.columns[offset + 4]

        age_at = row[age_at_col]
        age_unit = row[age_unit_col]
        age_precision = row[age_precision_col]
        condition = row[condition_col]
        icd_code = row[icd_code_col]

        if pd.notna(age_at) or pd.notna(age_unit) or pd.notna(age_precision) or pd.notna(condition) or pd.notna(icd_code):
            subject_has_data = True
            records.append({
                'HONEST_BROKER_SUBJECT_ID': subject_id,
                'AGE_AT': age_at,
                'AGE_UNIT': age_unit,
                'AGE_PRECISION': age_precision,
                'CONDITION': condition,
                'ICD_CODE': icd_code
            })

    #if no data rows were collected, add a single blank row with just the honest broker subject id data
    if not subject_has_data:
        records.append({
                'HONEST_BROKER_SUBJECT_ID': subject_id,
                'AGE_AT': '',
                'AGE_UNIT': '',
                'AGE_PRECISION': '',
                'CONDITION': '',
                'ICD_CODE': ''
        })

df = pd.DataFrame(records)

#replace NaN
df = df.fillna('')

print(df.to_string(index=False))

# df.to_excel('_final/medical_history.xlsx', index=False)
# print("✓ Data exported successfully.")
