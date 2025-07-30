import json, os, yaml
import pandas as pd

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
        return isinstance(value, (str, int, float))
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

def evaluate_condition(value, operator):
    if operator == "null":
        return pd.isna(value) or str(value).strip().lower() in ["", "nan"]
    elif operator == "not_null":
        return not (pd.isna(value) or str(value).strip().lower() in ["", "nan"])
    else:
        raise ValueError(f"Unsupported operator: {operator}")

def apply_custom_yaml_rules(df, table_name, rules, file_errors):
    if table_name not in rules:
        return

    for idx, row in df.iterrows():
        subject_id = str(row.get("HONEST_BROKER_SUBJECT_ID", "<missing>")).strip()

        for rule in rules[table_name]:
            if_cond = rule.get("if", {})
            then_cond = rule.get("then", {})
            description_template = rule.get("description", "Custom rule failed")

            if_field = if_cond.get("field")
            if_op = if_cond.get("operator")
            then_field = then_cond.get("field")
            then_op = then_cond.get("operator")

            if if_op is None or then_op is None:
                print(f"Warning: Skipping rule due to missing operator in table '{table_name}': {rule}")
                continue

            if_val = row.get(if_field)
            then_val = row.get(then_field)

            if evaluate_condition(if_val, if_op) and not evaluate_condition(then_val, then_op):
                try:
                    description = description_template.format(**row)
                except KeyError as e:
                    missing_key = str(e).strip("'")
                    fallback = row.get(missing_key, "<missing>")
                    description = description_template.replace(f"{{{missing_key}}}", str(fallback))

                file_errors.append({
                    "HONEST_BROKER_SUBJECT_ID": subject_id,
                    "Table": table_name,
                    "Variable": then_field,
                    "Error": f"ConditionalStatement Error: {description}"
                })


with open("MD/md_v1.2.json", "r") as f:
    data_dict = json.load(f)

data_dict = trim_json(data_dict)

with open("MD/conditional_statement.yaml", "r") as f:
    custom_rules = yaml.safe_load(f)

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

excel_files = [
    "biometrics.xlsx", "demographics.xlsx", "disease_characteristics.xlsx",
    "family_medical_history.xlsx", "genetic_analysis.xlsx", "medical_history.xlsx", "subject_characteristics.xlsx",
    "testing.xlsx", "timing.xlsx",  "treatment.xlsx"
]

input_dir = "MD/cincinnati_childrens/_final"
all_errors = []
files_with_errors = set()

for file in excel_files:
    file_path = os.path.join(input_dir, file)
    table_name = os.path.splitext(file)[0].lower()
    file_errors = []

    try:
        df = pd.read_excel(file_path, dtype=str)

        if "HONEST_BROKER_SUBJECT_ID" in df.columns:
            df["HONEST_BROKER_SUBJECT_ID"] = (
                df["HONEST_BROKER_SUBJECT_ID"]
                .fillna("")
                .astype(str)
                .str.strip()
                .str.replace(r"\.0$", "", regex=True)
            )
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
                expected_vars = sorted([
                    var_info["__original_var_name__"]
                    for (domain, var_name), var_info in variables.items()
                    if domain == table_name
                ])
                file_errors.extend([
                    {
                        "HONEST_BROKER_SUBJECT_ID": subject_id,
                        "Table": table_name,
                        "Variable": col,
                        "Error": f"Invalid Variable: '{col}' with invalid PermissibleValue: '{value_str}'"
                    },
                    {
                        "HONEST_BROKER_SUBJECT_ID": subject_id,
                        "Table": table_name,
                        "Variable": col,
                        "Error": f"Invalid Variable: '{col}'. Expecting: {', '.join(expected_vars)}"
                    }
                ])
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
                    "Error": f"Invalid DataType: '{value_str}'. Expecting: {var_type}"
                })
                continue

            # if var_type == "String" and col_key != "honest_broker_subject_id":
            #     file_errors.append({
            #         "HONEST_BROKER_SUBJECT_ID": subject_id,
            #         "Table": table_name,
            #         "Variable": col,
            #         "Error": f"Warning: Variable '{col}' is a 'String' DataType"
            #     })

            if var_type == "Enum" and not is_valid_enum(value_str, permissible_values):
                file_errors.append({
                    "HONEST_BROKER_SUBJECT_ID": subject_id,
                    "Table": table_name,
                    "Variable": col,
                    "Error": f"Invalid PermissibleValue: '{value_str}'"
                })

    apply_custom_yaml_rules(df, table_name, custom_rules, file_errors)

    if file_errors:
        all_errors.extend(file_errors)
        files_with_errors.add(file)

files_with_no_errors = set(excel_files) - files_with_errors
if files_with_no_errors:
    print(f"✓ No QC errors found for files: {', '.join(sorted(files_with_no_errors))}")

if all_errors:
    df_errors = pd.DataFrame(all_errors)

    df_errors["HONEST_BROKER_SUBJECT_ID"] = df_errors["HONEST_BROKER_SUBJECT_ID"].astype(str).str.strip()
    df_errors["Table"] = df_errors["Table"].astype(str).str.strip().str.lower()
    df_errors["Variable"] = df_errors["Variable"].astype(str).str.strip().str.upper()
    df_errors["Error"] = df_errors["Error"].astype(str).str.strip()
    df_errors["Total Error Count"] = df_errors.groupby(["Table", "Variable", "Error"])["Error"].transform("count")

    df_errors = df_errors.drop_duplicates(subset=["HONEST_BROKER_SUBJECT_ID", "Table", "Variable", "Error"])
    df_errors = df_errors.sort_values(by=["Table", "Variable", "Error"])

    # output_file = "MD/cincinnati_childrens/quality_check/qc_cincinnati_childrens.txt"
    # with open(output_file, "w", encoding="utf-8") as f:
    #     for _, row in df_errors.iterrows():
    #         f.write(f"{row.to_dict()}\n")
    # print(f"✓ QC errors saved to {output_file}.")

    output_xlsx = "MD/cincinnati_childrens/quality_check/qc_cincinnati_childrens.xlsx"
    df_errors.to_excel(output_xlsx, index=False)
    print(f"✓ QC errors saved to {output_xlsx}.")
else:
    print("✓ No QC errors found in any files.")
