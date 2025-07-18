import json
import pandas as pd
import os
import re

def trim_json(data):
    if isinstance(data, dict):
        return {k.strip(): trim_json(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [trim_json(item) for item in data]
    elif isinstance(data, str):
        return data.strip()
    else:
        return data

def normalize_str(s):
    if not isinstance(s, str):
        s = str(s)
    return s.strip().lower()

def is_valid_type(value, expected_type):
    if pd.isna(value) or value == "" or str(value).lower() == "nan":
        return True 
    if expected_type == "String":
        return isinstance(value, str) or isinstance(value, int) or isinstance(value, float)
    elif expected_type == "Decimal":
        try:
            float(value)
            return True
        except ValueError:
            return False
    elif expected_type == "Enum":
        return True 
    return True

def is_valid_enum(value, permissible_values):
    if pd.isna(value) or value == "" or str(value).lower() == "nan":
        return True
    value_norm = normalize_str(value)
    permissible_norm = [normalize_str(pv) for pv in permissible_values]
    return value_norm in permissible_norm

# Load and trim the JSON data dictionary
with open("CNS/cns_v1.2.json", "r") as f:
    data_dict = json.load(f)

data_dict = trim_json(data_dict)

# Flatten dictionary
variables = {}
for domain_group_name, domain_group in data_dict.get("domains", {}).items():
    for table_name, domain in domain_group.items():
        table_name_key = table_name.strip().lower()
        for var_name, var_info in domain.items():
            key = (table_name_key, var_name.strip().lower())
            perm_vals = var_info.get("permissible_values", {})
            normalized_perm_vals = {k.strip(): v for k, v in perm_vals.items()}
            var_info["permissible_values"] = normalized_perm_vals
            var_info["__original_var_name__"] = var_name.strip()
            variables[key] = var_info

# File inputs
csv_files = [
    "subject_characteristics.csv", "time_period.csv", "demographics.csv", "survival_characteristics.csv", "disease_site_assessment.csv", 
    "staging.csv", "diagnosis.csv", "medication.csv", "radiation_therapy.csv", "biopsy_and_surgical_procedures.csv"
]

input_dir = "CNS/PNET4/raw"
all_errors = []
files_with_errors = set()

for file in csv_files:
    file_path = os.path.join(input_dir, file)
    table_name = os.path.splitext(file)[0].lower()
    file_errors = []

    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"❌ Could not read file '{file_path}': {e}")
        continue

    for idx, row in df.iterrows():
        subject_id = str(row.get("HONEST_BROKER_SUBJECT_ID", "<missing>")).strip()

        for col in df.columns:
            col_key = col.strip().lower()
            value = row[col]
            value_str = str(value).strip() if not pd.isna(value) else ""

            var_def = variables.get((table_name, col_key))

            if not var_def:
                error1 = {
                    "HONEST_BROKER_SUBJECT_ID": subject_id,
                    "Table": table_name,
                    "Variable": col,
                    "Error": f"Invalid Variable '{col}' with invalid PermissibleValue '{value_str}'"
                }
                error2 = {
                    "HONEST_BROKER_SUBJECT_ID": subject_id,
                    "Table": table_name,
                    "Variable": col,
                    "Error": f"Invalid Variable '{col}'. Expected one of: {', '.join(sorted([var_info['__original_var_name__'] for (domain, var_name), var_info in variables.items() if domain == table_name]))}"
                }
                file_errors.extend([error1, error2])
                continue

            var_type = var_def.get("type")
            permissible_values = var_def.get("permissible_values", {}).keys()

            if value_str == "" or value_str.lower() == "nan":
                continue

            if not is_valid_type(value_str, var_type):
                file_errors.append({
                    "HONEST_BROKER_SUBJECT_ID": subject_id,
                    "Table": table_name,
                    "Variable": col,
                    "Error": f"Invalid DataType '{value_str}' (expected {var_type})"
                })
                continue

            if var_type == "String" and col_key != "honest_broker_subject_id":
                file_errors.append({
                    "HONEST_BROKER_SUBJECT_ID": subject_id,
                    "Table": table_name,
                    "Variable": col,
                    "Error": f"Warning: Variable '{col}' is a 'String' DataType"
                })

            if var_type == "Enum" and not is_valid_enum(value_str, permissible_values):
                file_errors.append({
                    "HONEST_BROKER_SUBJECT_ID": subject_id,
                    "Table": table_name,
                    "Variable": col,
                    "Error": f"Invalid PermissibleValue '{value_str}'"
                })

    if file_errors:
        all_errors.extend(file_errors)
        files_with_errors.add(file)
    # else:  # no errors, don't need to print now, will print at end summary

# At the end: print summary of files with no errors
files_with_no_errors = set(csv_files) - files_with_errors
if files_with_no_errors:
    print(f"✓ No validation errors found for files: {', '.join(sorted(files_with_no_errors))}")
else:
    print("✓ All files had validation errors.")

# Save all errors if any
if all_errors:
    df_errors = pd.DataFrame(all_errors)

    df_errors["HONEST_BROKER_SUBJECT_ID"] = df_errors["HONEST_BROKER_SUBJECT_ID"].astype(str).str.strip()
    df_errors["Table"] = df_errors["Table"].astype(str).str.strip().str.lower()
    df_errors["Variable"] = df_errors["Variable"].astype(str).str.strip().str.upper()
    df_errors["Error"] = df_errors["Error"].astype(str).str.strip()

    df_errors["Count"] = df_errors.groupby(["Table", "Variable", "Error"])["Error"].transform("count")

    df_errors = df_errors.drop_duplicates(subset=["HONEST_BROKER_SUBJECT_ID", "Table", "Variable", "Error"])
    df_errors = df_errors.sort_values(by=["Table", "Variable", "Error"])

    output_txt = "CNS/PNET4/PNET4.txt"
    with open(output_txt, "w", encoding="utf-8") as f:
        for _, row in df_errors.iterrows():
            f.write(f"{row.to_dict()}\n")
    print(f"✓ Validation errors saved to {output_txt}.")

    output_xlsx = "CNS/PNET4/PNET4.xlsx"
    df_errors.to_excel(output_xlsx, index=False)
    print(f"✓ Validation errors saved to {output_xlsx}.")
else:
    print("✓ No validation errors found in any files.")
