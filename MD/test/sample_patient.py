import pandas as pd
import yaml
import os

# Map of filenames to their top-level YAML keys
files_to_keys = {
    "subject_characteristics.xlsx": "subject_characteristics",
    "timing.xlsx": "timing",
    "family_medical_history.xlsx": "family_medical_history",
    "demographics.xlsx": "demographics",
    "medical_history.xlsx": "medical_history",
    "biometrics.xlsx": "biometrics",
    "genetic_analysis.xlsx": "genetic_analysis",
    "testing.xlsx": "testing",
    "disease_characteristics.xlsx": "disease_characteristics",
    "treatment.xlsx": "treatment"
}

# Directory containing the Excel files
data_dir = "_final"

# List to hold all patient data blocks
all_patients = []

# Process each file and key
for filename, key in files_to_keys.items():
    path = os.path.join(data_dir, filename)
    df = pd.read_excel(path, engine="openpyxl")

    for _, row in df.iterrows():
        patient = {key: {}}
        for col in df.columns:
            value = row[col]
            if pd.notna(value):
                if isinstance(value, (pd.Timestamp, pd.Timedelta)):
                    value = str(value)
                elif hasattr(value, "item"):
                    value = value.item()
                patient[key][col] = value
        all_patients.append(patient)


# Print the full list to YAML
with open("test/sample_patient.yaml", "w") as f:
    yaml.dump(all_patients, f, sort_keys=False, allow_unicode=True)
