import pandas as pd

df = pd.read_excel("MD/cincinnati_childrens/raw_final/raw_testing.xlsx")

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
        age_at_col = df.columns[offset]
        age_unit_col = df.columns[offset + 1]
        age_precision_col = df.columns[offset + 2]
        test_type_col = df.columns[offset + 3]
        method_col = df.columns[offset + 4]
        measurement_type_col = df.columns[offset + 5]
        result_modifier_col = df.columns[offset + 6]
        result_numeric_col = df.columns[offset + 7]
        result_unit_col = df.columns[offset + 8]
        reference_range_col = df.columns[offset + 9]
        result_interpretation_col = df.columns[offset + 10]
        fasting_status_col = df.columns[offset + 11]
        post_glucose_timepoint_col = df.columns[offset + 12]
        post_glucose_timepoint_unit_col = df.columns[offset + 13]

        age_at = row[age_at_col]
        age_unit = row[age_unit_col]
        age_precision = row[age_precision_col]
        test_type = row[test_type_col]
        method = row[method_col]
        measurement_type = row[measurement_type_col]
        result_modifier = row[result_modifier_col]
        result_numeric = row[result_numeric_col]
        result_unit = row[result_unit_col]
        reference_range = row[reference_range_col]
        result_interpretation = row[result_interpretation_col]
        fasting_status = row[fasting_status_col]
        post_glucose_timepoint = row[post_glucose_timepoint_col]
        post_glucose_timepoint_unit = row[post_glucose_timepoint_unit_col]


        fields = [
            age_at, age_unit, age_precision, test_type, method, measurement_type, result_modifier, result_numeric, result_unit, reference_range, 
            result_interpretation, fasting_status, post_glucose_timepoint, post_glucose_timepoint_unit
        ]

        if any(pd.notna(field) for field in fields):
            subject_has_data = True
            records.append({
                'HONEST_BROKER_SUBJECT_ID': subject_id,
                'AGE_AT': age_at,
                'AGE_UNIT': age_unit,
                'AGE_PRECISION': age_precision,
                'TEST_TYPE': test_type,
                'METHOD': method,
                'MEASUREMENT_TYPE': measurement_type,
                'RESULT_MODIFIER': result_modifier,
                'RESULT_NUMERIC': result_numeric,
                'RESULT_UNIT': result_unit,
                'REFERENCE_RANGE': reference_range,
                'RESULT_INTERPRETATION': result_interpretation,
                'FASTING_STATUS': fasting_status,
                'POST_GLUCOSE_TIMEPOINT': post_glucose_timepoint,
                'POST_GLUCOSE_TIMEPOINT_UNIT': post_glucose_timepoint_unit
            })

    #if no data rows were collected, add a single blank row with just the honest broker subject id data
    if not subject_has_data:
        records.append({
                'HONEST_BROKER_SUBJECT_ID': subject_id,
                'AGE_AT': '',
                'AGE_UNIT': '',
                'AGE_PRECISION': '',
                'TEST_TYPE': '',
                'METHOD': '',
                'MEASUREMENT_TYPE': '',
                'RESULT_MODIFIER': '',
                'RESULT_NUMERIC': '',
                'RESULT_UNIT': '',
                'REFERENCE_RANGE': '',
                'RESULT_INTERPRETATION': '',
                'FASTING_STATUS': '',
                'POST_GLUCOSE_TIMEPOINT': '',
                'POST_GLUCOSE_TIMEPOINT_UNIT': ''
        })

df = pd.DataFrame(records)

#replace NaN
df = df.fillna('')

print(df.to_string(index=False))

df.to_excel('MD/cincinnati_childrens/_final/testing.xlsx', index=False)
print("✓ Data exported successfully.")
