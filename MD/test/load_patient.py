from linkml_runtime.loaders import yaml_loader
from patient_model import Patient

# Load the patient from the YAML file
patient: Patient = yaml_loader.load("MD/test/sample_patient.yaml", target_class=Patient)

# Access attributes
print(patient.subject_characteristics.DATA_CONTRIBUTOR_ID)  # Enum value
print(patient.timing.TIMEPOINT)  # Enum value
print(patient.family_medical_history.CONDITION)
