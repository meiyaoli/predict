import pandas as pd

df = pd.read_csv("csv/family_medical_history.csv")

#strip column names
df.columns = df.columns.str.strip()

#store subject ID
subject_id = df['Honest Broker Subject ID']

#determine how many family member columns there are
columns_per_member = 5 #5 columns per member
member_blocks = (df.shape[1] - 1) // columns_per_member #first column is honest broker so we excluded it by using -1 because it's not a repeating family member data

#reshaping into a table format which gives one row per family member 
records = []

for idx, row in df.iterrows():
    subject_id = row['Honest Broker Subject ID']
    subject_has_data = False 

    for i in range(member_blocks):
        offset = 1 + i * columns_per_member
        rel_col = df.columns[offset]
        rel_id_col = df.columns[offset + 1]
        cond_col = df.columns[offset + 2]
        source_col = df.columns[offset + 3]

        relation = row[rel_col]
        relation_id = row[rel_id_col]
        condition = row[cond_col]
        source = row[source_col]

        if pd.notna(relation) or pd.notna(condition) or pd.notna(source):
            subject_has_data = True
            records.append({
                'HONEST_BROKER_SUBJECT_ID': subject_id,
                'RELATION': relation,
                'RELATION_HONEST_BROKER_SUBJECT_ID': relation_id,
                'CONDITION': condition,
                'SOURCE': source
            })

    #if no data rows were collected, add a single blank row with just the honest broker subject id data
    if not subject_has_data:
        records.append({
            'HONEST_BROKER_SUBJECT_ID': subject_id,
            'RELATION': '',
            'RELATION_HONEST_BROKER_SUBJECT_ID': '',
            'CONDITION': '',
            'SOURCE': ''
        })

df = pd.DataFrame(records)

#clean RELATION_HONEST_BROKER_SUBJECT_ID to a whole numner, removing .0 at the end
df['RELATION_HONEST_BROKER_SUBJECT_ID'] = (
    df['RELATION_HONEST_BROKER_SUBJECT_ID']
    .apply(lambda x: str(int(x)) if pd.notnull(x) and isinstance(x, float) and x == int(x) else str(x) if pd.notna(x) else '')
)

#replace NaN
df = df.fillna('')

print(df.to_string(index=False))

# df.to_excel('_final/family_medical_history.xlsx', index=False)
# print("✓ Data exported successfully.")
