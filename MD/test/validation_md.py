import json
import csv

# --- Validation functions ---
def is_valid_type(value, expected_type):
    if value == "":
        return True  # Allow empty cells
    if expected_type == "String":
        return isinstance(value, str)
    elif expected_type == "Decimal":
        try:
            float(value)
            return True
        except ValueError:
            return False
    elif expected_type == "Enum":
        return True  # Enum is checked separately
    else:
        return True  # Assume valid if unknown type

table_name = "subject_characteristics"

def is_valid_enum(value, permissible_values):
    if value == "":
        return True  # Allow empty
    return value in permissible_values

with open("MD/test/md_v1.0.json", "r") as f:
    data_dict = json.load(f)

# Extract variable definitions from the JSON
variables = {}
for domain_group in data_dict.get("domains", {}).values():
    for domain in domain_group.values():
        for var_name, var_info in domain.items():
            variables[var_name] = var_info

# --- Load CSV data ---
with open("MD/test/subject_characteristics.csv", newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    csv_rows = list(reader)

# --- Validate CSV rows ---
errors = []

for row in csv_rows:
    subject_id = row.get("HONEST_BROKER_SUBJECT_ID", "<missing>").strip()
    for col, value in row.items():
        var_def = variables.get(col.strip())
        if not var_def:
            continue  # Skip columns not defined in dictionary

        value = value.strip()
        var_type = var_def.get("type")
        permissible_values = var_def.get("permissible_values", {}).keys()

        # Type validation
        if not is_valid_type(value, var_type):
            errors.append(
                f"{table_name}, HONEST_BROKER_SUBJECT_ID '{subject_id}', '{col}': Invalid DataType '{value}' (expected {var_type})"
            )

        # Enum validation
        if var_type == "Enum" and not is_valid_enum(value, permissible_values):
            errors.append(
                f"{table_name}, HONEST_BROKER_SUBJECT_ID '{subject_id}', '{col}': Invalid PermissibleValue '{value}'"
            )

# --- Output results ---
if errors:
    print("❌ Validation errors:")
    for err in errors:
        print(err)
else:
    print("✅ All rows validated successfully.")
