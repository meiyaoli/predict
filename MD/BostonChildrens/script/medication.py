import pandas as pd

df = pd.read_csv("csv/medication.csv")

#strip column names
df.columns = df.columns.str.strip()

#store subject ID
subject_id = df['Honest Broker Subject ID']

#determine how many family member columns there are
columns_per_member = 15 #15 columns per member
member_blocks = (df.shape[1] - 1) // columns_per_member #first column is honest broker so we excluded it by using -1 because it's not a repeating family member data

#reshaping/melting into a long format which gives one row per family member 
records = []

for idx, row in df.iterrows():
    subject_id = row['Honest Broker Subject ID']
    subject_has_data = False 

    for i in range(member_blocks):
        offset = 1 + i * columns_per_member
        age_at_start_col = df.columns[offset]
        age_at_stop_col = df.columns[offset + 1]
        age_unit_col = df.columns[offset + 2]
        age_precision_col = df.columns[offset + 3]
        reason_stop_col = df.columns[offset + 4]
        dm_medication_class_col = df.columns[offset + 5]
        medication_class_other_col = df.columns[offset + 6]
        medication_name_col = df.columns[offset + 7]
        medication_code_col = df.columns[offset + 8]
        medication_concentration_col = df.columns[offset + 9]
        medication_dose_col = df.columns[offset + 10]
        medication_unit_col = df.columns[offset + 11]
        frequency_col = df.columns[offset + 12]
        route_col = df.columns[offset + 13]

        age_at_start_col = row[age_at_start_col]
        age_at_stop = row[age_at_stop_col]
        age_unit = row[age_unit_col]
        age_precision = row[age_precision_col]
        reason_stop = row[reason_stop_col]
        dm_medication_class = row[dm_medication_class_col]
        medication_class_other = row[medication_class_other_col]
        medication_name = row[medication_name_col]
        medication_code = row[medication_code_col]
        medication_concentration = row[medication_concentration_col]
        medication_dose = row[medication_dose_col]
        medication_unit = row[medication_unit_col]
        frequency = row[frequency_col]
        route = row[route_col]


        fields = [
            age_at_start_col, age_at_stop, age_unit, age_precision, reason_stop, dm_medication_class, medication_class_other, medication_name,
            medication_code, medication_concentration, medication_dose, medication_unit, frequency, route
        ]

        if any(pd.notna(field) for field in fields):
            subject_has_data = True
            records.append({
                'HONEST_BROKER_SUBJECT_ID': subject_id,
                'AGE_AT_START': age_at_start_col,
                'AGE_AT_STOP': age_at_stop,
                'AGE_UNIT': age_unit,
                'AGE_PRECISION': age_precision,
                'REASON_STOP': reason_stop,
                'DM_MEDICATION_CLASS': dm_medication_class,
                'MEDICATION_CLASS_OTHER': medication_class_other,
                'MEDICATION_NAME': medication_name,
                'MEDICATION_CODE': medication_code,
                'MEDICATION_CONCENTRATION': medication_concentration,
                'MEDICATION_DOSE': medication_dose,
                'MEDICATION_UNIT': medication_unit,
                'FREQUENCY': frequency,
                'ROUTE': route

            })

    #if no data rows were collected, add a single blank row with just the honest broker subject id data
    if not subject_has_data:
        records.append({
                'HONEST_BROKER_SUBJECT_ID': subject_id,
                'AGE_AT_START': '',
                'AGE_AT_STOP': '',
                'AGE_UNIT': '',
                'AGE_PRECISION': '',
                'REASON_STOP': '',
                'DM_MEDICATION_CLASS': '',
                'MEDICATION_CLASS_OTHER': '',
                'MEDICATION_NAME': '',
                'MEDICATION_CODE': '',
                'MEDICATION_CONCENTRATION': '',
                'MEDICATION_DOSE': '',
                'MEDICATION_UNIT': '',
                'FREQUENCY': '',
                'ROUTE': ''
        })

df = pd.DataFrame(records)

#replace NaN
df = df.fillna('')

print(df.to_string(index=False))

df.to_excel('_final/medication.xlsx', index=False)
print("✓ Data exported successfully.")
