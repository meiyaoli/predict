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

def extract_suffix_number(error_msg):
    match = re.search(r"BCH-(\d+)", error_msg)
    return int(match.group(1)) if match else float('inf')

# Load and trim the JSON data dictionary
with open("MD/validation/md_v1.0.json", "r") as f:
    data_dict = json.load(f)

data_dict = trim_json(data_dict)

# Flatten dictionary
variables = {}
for domain_group_name, domain_group in data_dict.get("domains", {}).items():
    for domain_name, domain in domain_group.items():
        for var_name, var_info in domain.items():
            key = (domain_name.strip().lower(), var_name.strip().lower())
            perm_vals = var_info.get("permissible_values", {})
            normalized_perm_vals = {k.strip(): v for k, v in perm_vals.items()}
            var_info["permissible_values"] = normalized_perm_vals
            var_info["__original_var_name__"] = var_name.strip()
            variables[key] = var_info

# File inputs
excel_files = [
    "biometrics.xlsx", "demographics.xlsx", "disease_characteristics.xlsx",
    "family_medical_history.xlsx", "genetic_analysis.xlsx", "testing.xlsx", "treatment.xlsx"
]

input_dir = "MD/BostonChildrens"
all_errors = []

for file in excel_files:
    file_path = os.path.join(input_dir, file)
    table_name = os.path.splitext(file)[0].lower()

    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        all_errors.append({
            "HONEST_BROKER_SUBJECT_ID": "<file level error>",
            "Table": table_name,
            "Variable": "",
            "Error": f"❌ Failed to read file: {e}"
        })
        continue

    for idx, row in df.iterrows():
        subject_id = str(row.get("HONEST_BROKER_SUBJECT_ID", "<missing>")).strip()

        for col in df.columns:
            col_key = col.strip().lower()
            value = row[col]
            value_str = str(value).strip() if not pd.isna(value) else ""

            var_def = variables.get((table_name, col_key))

            if not var_def:
                all_errors.append({
                    "HONEST_BROKER_SUBJECT_ID": subject_id,
                    "Table": table_name,
                    "Variable": col,
                    "Error": f"Invalid Variable '{col}' with invalid PermissibleValue '{value_str}'"
                })

                expected_vars = sorted([
                    var_info["__original_var_name__"]
                    for (domain, var_name), var_info in variables.items()
                    if domain == table_name
                ])

                all_errors.append({
                    "HONEST_BROKER_SUBJECT_ID": subject_id,
                    "Table": table_name,
                    "Variable": col,
                    "Error": f"Invalid Variable '{col}'. Expected one of: {', '.join(expected_vars)}"
                })
                continue

            var_type = var_def.get("type")
            permissible_values = var_def.get("permissible_values", {}).keys()

            if value_str == "" or value_str.lower() == "nan":
                continue

            if not is_valid_type(value_str, var_type):
                all_errors.append({
                    "HONEST_BROKER_SUBJECT_ID": subject_id,
                    "Table": table_name,
                    "Variable": col,
                    "Error": f"Invalid DataType '{value_str}' (expected {var_type})"
                })
                continue

            if var_type == "String" and col_key != "honest_broker_subject_id":
                all_errors.append({
                    "HONEST_BROKER_SUBJECT_ID": subject_id,
                    "Table": table_name,
                    "Variable": col,
                    "Error": f"Warning: Variable '{col}' is a 'String' DataType"
                })

            if var_type == "Enum" and not is_valid_enum(value_str, permissible_values):
                all_errors.append({
                    "HONEST_BROKER_SUBJECT_ID": subject_id,
                    "Table": table_name,
                    "Variable": col,
                    "Error": f"Invalid PermissibleValue '{value_str}'"
                })

# Save and count unique errors
if all_errors:
    df_errors = pd.DataFrame(all_errors)

    df_errors["HONEST_BROKER_SUBJECT_ID"] = df_errors["HONEST_BROKER_SUBJECT_ID"].astype(str).str.strip()
    df_errors["Table"] = df_errors["Table"].astype(str).str.strip().str.lower()
    df_errors["Variable"] = df_errors["Variable"].astype(str).str.strip().str.upper()
    df_errors["Error"] = df_errors["Error"].astype(str).str.strip()

    df_errors["Count"] = df_errors.groupby(["Table", "Variable", "Error"])["Error"].transform("count")

    # Sorting to show 'Expected one of' errors first within each table
    df_errors["__priority__"] = df_errors["Error"].apply(lambda x: 0 if "Expected one of:" in x else 1)
    df_errors["__suffix_sort__"] = df_errors["Error"].apply(extract_suffix_number)

    df_errors = df_errors.drop_duplicates(subset=["HONEST_BROKER_SUBJECT_ID", "Table", "Variable", "Error"])
    df_errors = df_errors.sort_values(by=["Table", "Variable", "__priority__", "__suffix_sort__", "Error"])
    df_errors = df_errors.drop(columns=["__priority__", "__suffix_sort__"])

    # Save to text
    output_file = "MD/validation/BCH.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        for _, row in df_errors.iterrows():
            f.write(f"{row.to_dict()}\n")

    print(f"✓ Validation errors saved to {output_file}.")

    # # Save to Excel
    # output_file = "MD/validation/BCH.xlsx"
    # df_errors.to_excel(output_file, index=False)
    # print(f"✓ Validation errors saved to {output_file}.")


