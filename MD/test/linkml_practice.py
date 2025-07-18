import json
import yaml

# Load your JSON file
with open("md_v1.0.json") as f:
    data = json.load(f)

# Define the field groups and their class names
field_groups = {
    "subject_characteristics": {
        "data": data['domains']['protocol']['subject_characteristics'],
        "class_name": "SubjectCharacteristics"
    },
    "timing": {
        "data": data['domains']['protocol'].get('timing', {}),
        "class_name": "Timing"
    },
    "family_medical_history": {
        "data": data['domains']['protocol'].get('family_medical_history', {}),
        "class_name": "FamilyMedicalHistory"
    },
    "demographics": {
    "data": data['domains']['protocol'].get('demographics', {}),
    "class_name": "Demographics"
    },
    "medical_history": {
    "data": data['domains']['protocol'].get('medical_history', {}),
    "class_name": "MedicalHistory"
    },
    "biometrics": {
    "data": data['domains']['testing'].get('biometrics', {}),
    "class_name": "Biometrics"
    },
    "biospecimen": {
    "data": data['domains']['testing'].get('biospecimen', {}),
    "class_name": "Biospecimen"
    },
    "genetic_analysis": {
    "data": data['domains']['testing'].get('genetic_analysis', {}),
    "class_name": "GeneticAnalysis"
    },
    "testing": {
    "data": data['domains']['testing'].get('testing', {}),
    "class_name": "Testing"
    },
    "disease_characteristics": {
    "data": data['domains']['disease_attributes'].get('disease_characteristics', {}),
    "class_name": "DiseaseCharacteristics"
    },
    "treatment": {
    "data": data['domains']['treatment'].get('treatment', {}),
    "class_name": "Treatment"
    }  
}

# Initialize LinkML schema
linkml_schema = {
    "id": "https://docs.google.com/spreadsheets/d/15ECEMspvSEbwH875PJF82B9A_vG7qh8j4PlSei0_P-w/edit?gid=1651440316#gid=1651440316",
    "name": "Monogenic Diabetes",
    "description": "Generated from Monogenic Diabetes data dictionary",
    "prefixes": {
        "ex": ""
    },
    "default_prefix": "ex",
    "imports": ["linkml:types"],
    "classes": {},
    "enums": {}
}

# Define the Patient class, which will reference the grouped classes
linkml_schema["classes"]["Patient"] = {
    "description": "Auto-generated class for patient",
    "attributes": {
        group_name: {
            "description": f"{info['class_name']} section",
            "range": info["class_name"]
        }
        for group_name, info in field_groups.items()
    }
}

# Function to process a field group into a separate class
def process_group(group_name, fields, class_name, schema):
    schema["classes"][class_name] = {
        "description": f"{group_name} fields",
        "attributes": {}
    }

    for field_name, field_info in fields.items():
        attr = {
            "description": field_info.get("description", ""),
            "range": "string"
        }

        field_type = field_info.get("type", "String")

        if field_type == "Decimal":
            attr["range"] = "float"
        elif field_type == "Integer":
            attr["range"] = "integer"
        elif field_type == "Enum":
            enum_name = f"{class_name}_{field_name}_Enum"
            attr["range"] = enum_name
            pv = field_info.get("permissible_values", {})
            schema["enums"][enum_name] = {
                "permissible_values": {
                    k.strip(): {
                        "description": v.get("description", "")
                    } for k, v in pv.items()
                }
            }

        schema["classes"][class_name]["attributes"][field_name] = attr

# Build schema classes from field groups
for group_name, group_info in field_groups.items():
    process_group(group_name, group_info["data"], group_info["class_name"], linkml_schema)

# Write to YAML
with open("patient_schema.yaml", "w") as f:
    yaml.dump(linkml_schema, f, sort_keys=False)
