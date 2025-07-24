import pandas as pd
from io import StringIO

df = pd.read_excel("MD/cincinnati_childrens/raw_final/raw_demographics.xlsx")

# Rename columns for easier handling
rename_columns = {
    'Honest Broker Subject ID': 'HONEST_BROKER_SUBJECT_ID',
    'The biological sex of the subject assigned at birth': 'SEX',
    'The ethnicity of the subject': 'ETHNICITY',
    'The race of the subject (choice=American Indian or Alaska Native)': 'American Indian or Alaska Native',
    'The race of the subject (choice=Asian)': 'Asian',
    'The race of the subject (choice=Black or African American)': 'Black or African American',
    'The race of the subject (choice=Native Hawaiian or other Pacific Islander)': 'Native Hawaiian or other Pacific Islander',
    'The race of the subject (choice=White)': 'White',
    'The race of the subject (choice=Unknown)': 'Unknown',
    'The race of the subject (choice=Not Reported)': 'Not Reported'
}

df.rename(columns=rename_columns, inplace=True)

# List of race columns
race_columns = [
    'American Indian or Alaska Native',
    'Asian',
    'Black or African American',
    'Native Hawaiian or other Pacific Islander',
    'White',
    'Unknown',
    'Not Reported'
]

# Replace NaNs with blanks
df[race_columns + ['SEX', 'ETHNICITY']] = df[race_columns + ['SEX', 'ETHNICITY']].fillna('')

# Create long-form rows
long_rows = []
for _, row in df.iterrows():
    base = {
        'HONEST_BROKER_SUBJECT_ID': row['HONEST_BROKER_SUBJECT_ID'],
        'SEX': row['SEX'],
        'ETHNICITY': row['ETHNICITY']
    }
    has_checked = False
    for race in race_columns:
        if str(row[race]).strip().lower() == 'checked':
            has_checked = True
            long_rows.append({**base, 'RACE': race})
    if not has_checked:
        long_rows.append({**base, 'RACE': ''})

# Final long-form DataFrame
long_df = pd.DataFrame(long_rows)

print(long_df.to_string(index=False))

long_df.to_excel('MD/cincinnati_childrens/_final/demographics.xlsx', index=False)
print("✓ Data exported successfully.")
