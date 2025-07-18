import pandas as pd

df = pd.read_csv("csv/biometrics.csv")

#strip column names
df.columns = df.columns.str.strip()

#store subject ID
subject_id = df['Honest Broker Subject ID']

#determine how many family member columns there are
columns_per_member = 8 #8 columns per member
member_blocks = (df.shape[1] - 1) // columns_per_member #first column is honest broker so we excluded it by using -1 because it's not a repeating family member data

#reshaping/melting into a long format which gives one row per family member 
records = []
for idx, row in df.iterrows():
    subject_id = row['Honest Broker Subject ID']
    subject_has_data = False 

    for i in range(member_blocks):
            offset = 1 + i * columns_per_member
            age_at_col = df.columns[offset]
            age_unit_col = df.columns[offset + 1]
            age_precision_col = df.columns[offset + 2]
            measurement_col = df.columns[offset + 3]
            measurement_numeric_col = df.columns[offset + 4]
            measurement_unit_col = df.columns[offset + 5]
            z_score_col = df.columns[offset + 6]

            age_at = row[age_at_col]
            age_unit = row[age_unit_col]
            age_precision = row[age_precision_col]
            measurement = row[measurement_col]
            measurement_numeric = row[measurement_numeric_col]
            measurement_unit = row[measurement_unit_col]
            z_score = row[z_score_col]

            fields = [
                age_at, age_unit, age_precision, measurement, measurement_numeric, measurement_unit, z_score 
             ]

            if any(pd.notna(field) for field in fields):
                subject_has_data = True
                records.append({
                    'HONEST_BROKER_SUBJECT_ID': subject_id,
                    'AGE_AT': age_at,
                    'AGE_UNIT': age_unit,
                    'AGE_PRECISION': age_precision,
                    'MEASUREMENT_TYPE': measurement,
                    'MEASUREMENT_NUMERIC': measurement_numeric,
                    'MEASUREMENT_UNIT': measurement_unit,
                    'Z_SCORE' : z_score
                })

    #if no data rows were collected, add a single blank row with just the honest broker subject id data
    if not subject_has_data:
        records.append({
                'HONEST_BROKER_SUBJECT_ID': subject_id,
                'AGE_AT': '',
                'AGE_UNIT': '',
                'AGE_PRECISION': '',
                'MEASUREMENT_TYPE': '',
                'MEASUREMENT_NUMERIC': '',
                'MEASUREMENT_UNIT': '',
                'Z_SCORE' : ''
        })

df = pd.DataFrame(records)

#replace NaN
df = df.fillna('')

print(df.to_string(index=False))

df.to_excel('_final/biometrics.xlsx', index=False)
print("✓ Data exported successfully.")
