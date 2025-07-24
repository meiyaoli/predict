import pandas as pd

df = pd.read_excel("MD/cincinnati_childrens/raw_final/raw_disease_characteristics.xlsx")

#strip column names
df.columns = df.columns.str.strip()

#store subject ID
subject_id = df['Honest Broker Subject ID']

#determine how many family member columns there are
columns_per_member = 12 #5 columns per member
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
        diabetes_status_col = df.columns[offset + 3]
        hypoglycemia_frequency_col = df.columns[offset + 4]
        severe_hypoglycemia_frequency_col = df.columns[offset + 5]
        dka_col = df.columns[offset + 6]
        time_in_range_col = df.columns[offset + 7]
        cgm_range_col = df.columns[offset + 8]
        diet_col = df.columns[offset + 9]
        exercise_col= df.columns[offset + 10]

        age_at = row[age_at_col]
        age_unit = row[age_unit_col]
        age_precision = row[age_precision_col]
        diabetes_status = row[diabetes_status_col]
        hypoglycemia_frequency = row[hypoglycemia_frequency_col]
        severe_hypoglycemia_frequency = row[severe_hypoglycemia_frequency_col]
        dka = row[dka_col]
        time_in_range = row[time_in_range_col]
        cgm_range = row[cgm_range_col]
        diet = row[diet_col]
        exercise = row[exercise_col]

        fields = [
            age_at, age_unit, age_precision, diabetes_status, hypoglycemia_frequency, severe_hypoglycemia_frequency, dka, time_in_range, cgm_range,
            diet, exercise
        ]

        if any(pd.notna(field) for field in fields):
            subject_has_data = True
            records.append({
                'HONEST_BROKER_SUBJECT_ID': subject_id,
                'AGE_AT': age_at,
                'AGE_UNIT': age_unit,
                'AGE_PRECISION': age_precision,
                'DIABETES_STATUS': diabetes_status,
                'HYPOGLYCEMIA_FREQUENCY': hypoglycemia_frequency,
                'SEVERE_HYPOGLYCEMIA_FREQUENCY': severe_hypoglycemia_frequency,
                'DKA': dka,
                'TIME_IN_RANGE': time_in_range,
                'CGM_RANGE': cgm_range,
                'DIET': diet,
                'EXERCISE': exercise
            })

    #if no data rows were collected, add a single blank row with just the honest broker subject id data
    if not subject_has_data:
        records.append({
                'HONEST_BROKER_SUBJECT_ID': subject_id,
                'AGE_AT': '',
                'AGE_UNIT': '',
                'AGE_PRECISION': '',
                'DIABETES_STATUS': '',
                'HYPOGLYCEMIA_FREQUENCY': '',
                'SEVERE_HYPOGLYCEMIA_FREQUENCY': '',
                'DKA': '',
                'TIME_IN_RANGE': '',
                'CGM_RANGE': '',
                'DIET': '',
                'EXERCISE': ''
        })

df = pd.DataFrame(records)

#replace NaN
df = df.fillna('')

print(df.to_string(index=False))

df.to_excel('MD/cincinnati_childrens/_final/disease_characteristics.xlsx', index=False)
print("✓ Data exported successfully.")
