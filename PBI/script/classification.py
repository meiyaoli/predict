import pandas as pd
import numpy as np

csv_file = "PBI - redcap/raw/raw_classification.csv"
df = pd.read_csv(csv_file)

# Function to determine Field Type based on Data Type and Permissible Values
def determine_field_type(row):
    data_type = row.get('Data Type', '')
    choices = row.get('Permissible Values', '')
    
    if data_type == 'Alphanumeric':
        # If choices exist and are not empty → dropdown, else text
        return 'dropdown' if pd.notna(choices) and str(choices).strip() else 'text'
    elif data_type == 'Numeric Values':
        return 'text'
    else:
        return ''

# Initialize redcap_df with mapped and direct columns
redcap_df = pd.DataFrame({
    'Variable / Field Name': df.get('Variable Name', ''),
    'Form Name': df.get('Subdomain Name', ''),
    'Section Header': '',
    'Field Type': df.apply(determine_field_type, axis=1),
    'Field Label': df.get('Question Text', ''),
    'Choices, Calculations, OR Slider Labels': df.get('Permissible Values', ''),
    'Field Note': df.get('Disease Specific Instructions', ''),
    'Text Validation Type OR Show Slider Number': '',
    'Text Validation Min': df.get('Min Value', ''),
    'Text Validation Max': df.get('Max Value', ''),
    'Identifier?': '',
    'Branching Logic (Show field only if...)': '',
    'Required Field?': '',
    'Custom Alignment': '',
    'Question Number (surveys only)': '',
    'Matrix Group Name': '',
    'Matrix Ranking?': '',
    'Field Annotation': df.get('CDE ID', '')
})

# Set validation types based on original 'Data Type'
redcap_df['Text Validation Type OR Show Slider Number'] = np.where(
    df['Data Type'] == 'Numeric Values', 'number', ''
)

# Convert the PVs
def convert_choices(cell):
    if pd.isna(cell):
        return ''
    items = [item.strip() for item in cell.split(';') if item.strip()]
    return ' | '.join([f"{i+1}, {item}" for i, item in enumerate(items)])

redcap_df['Choices, Calculations, OR Slider Labels'] = redcap_df['Choices, Calculations, OR Slider Labels'].apply(convert_choices)

# Convert to lowercase
redcap_df['Variable / Field Name'] = redcap_df['Variable / Field Name'].str.lower()
redcap_df['Form Name'] = redcap_df['Form Name'].str.lower()

# Save to CSV for REDCap upload
redcap_df.to_csv("PBI - redcap/_final/classification.csv", index=False)