import pandas as pd
import re

# Read Excel
df = pd.read_excel("MD/cincinnati_childrens/raw/concat.xlsx")
df.columns = df.columns.str.strip()

# Drop all 'Complete?' columns
df = df.drop(columns=[col for col in df.columns if 'Complete?' in col])

# Replace NaNs
df = df.fillna('')

# Drop completely empty rows
df = df.dropna(how='all')

# Define mapping patterns 
rename_map = {
    'Diabetes diagnosis event': 'TIMEPOINT',    #time point
    'The age of the subject at the indicated time point.': 'AGE_AT',
    'The unit of age of the subject at the indicated time point.': 'AGE_UNIT',
    'The precision of age of the subject at the indicated time point.': 'AGE_PRECISION',
    'Add another timepoint?': 'ADD_TP', 
    'Add additional family member?' : 'ADD_FM', #family medical history
    'The relation of this family member to the patient' : 'RELATION',
    'If this family member is also in the data commons, enter their data commons honest broker subject ID' : 'RELATION_HONEST_BROKER_SUBJECT_ID',
    'Diabetes status of this family member' : 'CONDITION',
    'For family members with monogenic diabetes, was this diagnosis confirmed by a genetic test or is this a clinical diagnosis only?' : 'SOURCE',
    'The age of the subject when the medical condition developed' : 'AGE_AT',   #medical history
    'The unit of the age of the subject when the medical condition developed' : 'AGE_UNIT',
    'The precision of the age of the subject when the medical condition developed' : 'AGE_PRECISION',
    'Condition' : 'CONDITION',
    'ICD code' : 'ICD CODE',
    'Add additional condition?' : 'ADD_MH',
    'The age of the subject when the testing was completed' : 'AGE_AT', #biometrics
    'The unit of the age of the subject when the testing was completed' : 'AGE_UNIT',
    'The precision of the age of the subject when the testing was completed.' : 'AGE_PRECISION',
    'Type of general biometric measurement' : 'MEASUREMENT_TYPE',
    'The numeric value of the general biometric measurement.' : 'MEASUREMENT_NUMERIC',
    "The units for the numeric VALUE recorded for the subject's general biometric measurement." : 'MEASUREMENT_UNIT',
    'BMI Z score' : 'Z_SCORE',
    'Add additional test result?' : 'ADD_BIOMETRICS',
    'The age of the subject when the test was completed' : 'AGE_AT',    #testing 
    'The unit of the age of the subject when the test was completed': 'AGE_UNIT',
    'The precision of the age of the subject when the test was completed' : 'AGE_PRECISION',
    'The type of test being administered to/by the subject' : 'TEST_TYPE',
    'The method or setting through which the testing was obtained' : 'METHOD',
    'The type of measurement (ex: 14 day average, point measurement, etc.)' : 'MEASUREMENT_TYPE',
    "Result modifier (used for measurements that include 'greater than', 'less than', '>', '" : 'RESULT_MODIFIER',
    'The numeric result of the test that was performed' : 'RESULT_NUMERIC',
    'The unit of the test result' : 'RESULT_UNIT',
    'Reference Range  the range or specific value that indicates a normal result for this test' : 'REFERENCE_RANGE',
    'Result Interpretation - the categorical result of the test administered to/by the subject.' : 'REFERENCE_INTERPRETATION',
    'Fasting Status - what was the fasting status of the subject when the test was performed.' : 'FASTING_STATUS',
    '(For OGTT) - How long between glucose administration and blood glucose measurement?' : 'POST_GLUCOSE_TIMEPOINT',
    '(For OGTT) The unit of time used to measure the time between glucose administration and blood glucose measurement' : 'POST_GLUCOSE_TIMEPOINT_UNIT',
    'Add an additional test result?' : 'ADD_TESTING',
    'The age of the subject related to the disease characteristic' : 'AGE_AT',   #disease characteristics
    'The unit of the age of the subject related to the disease characteristic' : 'AGE_UNIT',
    'The precision of the age of the subject related to the disease characteristic' : 'AGE_PRECISION',
    'Has the subject ever had a diagnosis of gestational diabetes, prediabtes, or diabetes?' : 'DIABETES_STATUS',
    'How often has the subject had MILD/MODERATE hypoglycemia (low blood sugars around 70 mg/dl and not associated with seizures or loss of consciousness)?' : 'HYPOGLYCEMIA_FREQUENCY',
    'How often has the subject had SEVERE hypoglycemia (low blood sugar)? For children (under 18 years old), this means they were partially or completely unconscious and/or having seizures. For adults (over 18 years old), this means they were partially or completely unconscious and/or having seizures and/or otherwise not able to help with their own care.' : 'SEVERE_HYPOGLYCEMIA_FREQUENCY',
    'Has the subject had diabetic ketoacidosis (DKA) ?' : 'DKA',
    'The percentage of time the subject was within target glucose range on a CGM report' : 'TIME_IN_RANGE',
    'Were the glucose range value parameters on the CGM report standard or non-standard?' : 'CGM_RANGE',
    "Since the subject's initial diagnosis of diabetes or high blood sugars, has the subject substantially changed what they eat, how much they eat, or when they eat, to try to reach 'goal' blood sugars?" : 'DIET',
    "Since the subject's initial diagnosis of diabetes or high blood sugars, has the subject substantially changed how much movement (exercise) they do, to try to reach 'goal' blood sugars?" : 'EXERCISE',
    'Add additional event for a disease characteristic?' : 'ADD_DISEASE_CHARACTERISTICS',
    'The age of the subject when they started the regimen that includes the medication indicated by the MEDICATION field.' : 'AGE_AT_START',
    'The age of the subject when they stopped the regimen that includes the medication indicated by the MEDICATION field.' : 'AGE_AT_STOP',
    'The unit used by the numeric AGE_AT_START and AGE_AT_STOP fields.' : 'AGE_UNIT',
    'The precision of the AGE_AT_START or AGE_AT_STOP fields' : 'AGE_PRECISION',
    'If the regimen that includes the medication indicated by the MEDICATION field has been stopped, please indicate the reason for stopping.' : 'REASON_STOP',
    'Please list the type diabetes medication used to treat the subject.' : 'DM_MEDICATION_CLASS',
    'Please list the type of non-diabetes medication used to treat the subject' : 'MEDICATION_CLASS_OTHER',
    'Name of the medication indicated by medication type field' : 'MEDICATION_NAME',
    'The RxNorm code for medication' : 'MEDICATION_CODE',
    'The concentration of the insulin medication' : 'MEDICATION_CONCENTRATION',
    'The dose of the medication indicated by the medication name field.' : 'MEDICATION_DOSE',
    'Units of the medication indicated by medication name field' : 'MEDICATION_UNIT',
    'Frequency the subject administered the medication indicated by the medication field' : 'FREQUENCY',
    'The route by which the medication indicated by the medication field is administered.' : 'ROUTE',
    'Add additional medication?': 'ADD_MED'
}

# Exact renames for base columns (WILL NOT HAVE ADDITIONAL TIMEPOINTS)
static_renames = {
    'Honest Broker Subject ID': 'HONEST_BROKER_SUBJECT_ID',
    'Data Contributor': 'DATA_CONTRIBUTOR_ID',  #subject characteristics
    'Data Source': 'DATA_SOURCE',
    'The last known survival status of the subject': 'LAST_KNOWN_SURVIVAL_STATUS',
    'Age of the subject at last contact': 'AGE_LAST_CONTACT',
    'Unit of age of at last contact': 'AGE_LAST_CONTACT_UNIT',
    'Precision of age of last contact': 'AGE_LAST_CONTACT_PRECISION',
    'The age of the subject when the genetic test was performed' : 'AGE_AT',    #genetic analysis
    'The unit of the age of the subject when the genetic test was performed' : 'AGE_UNIT',
    'The precision of the age of the subject when the genetic test was performed' : 'AGE_PRECISION',
    "Is this genetic alteration a cause for the subject's diabetes?" : 'CAUSITIVE_ALTERATION',
    'What type of sample was used for this genetic analysis?' : 'SAMPLE_TYPE',
    'Where was this genetic test performed?' : 'LABORATORY_NAME',
    'The genetic testing method/technique used to generate the observed results.' : 'METHOD',
    'The chromosome on which the observed mutation is located.' : 'CYTOGENETIC_LOCATION',
    'The gene targeted for mutation analysis, identified in HUGO Gene Nomenclature Committee (HGNC) notation.' : 'GENE',
    'The type of variation detected by this genetic analysis.' : 'ALTERATION_TYPE',
    'Alteration Effect' : 'ALTERATION_EFFECT',
    'Alteration Region' : 'ALTERATION_REGION',
    'HGVS Accession number' : 'HGVS_ACCESSION',
    'If this alteration is described at the sequence/chromosome level, this is its representation in HGVS nomenclature (cHGVS).' : 'HGVS_CODING',
    'If this alteration is described at the translational product level, this is its representation in HGVS nomenclature (pHGVS)' : 'HGVS_PROTEIN',
    'If this alteration is described at the genome level, this is its representation in HGVS nomenclature (gHGVS)' : 'HGVS_GENOMIC',
    'An international standard for human chromosome nomenclature, which includes band names, symbols and abbreviated terms used in the description of human chromosome and chromosome abnormalities.' : 'ISCN',
    'The initial reported ACMG clinical significance of this genetic variation.' : 'ALLELIC_STATE',
    'The incidence of this mutation in the sample (%).' : 'MAF_NUMERIC',
    'Does this subject have two or more genetically different sets of cells in their body?' : 'MOSAICISM',
    'An ID to an external knowledge base that holds additional information about this genetic variant.' : 'EXTERNAL_REF_ID',
    'The name of the external knowledge base from which the external ID is drawn.' : 'EXTERNAL_REF_ID_SYSTEM',

}

demo_columns = {
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

df.rename(columns=demo_columns, inplace=True)

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

# First apply the static renames
df.rename(columns=static_renames, inplace=True)

# Determine the race for each row
race_values = []
for _, row in df.iterrows():
    selected = ''
    for race in race_columns:
        if str(row[race]).strip().lower() == 'checked':
            selected = race
            break
    race_values.append(selected)

# Add as a new column to the original DataFrame
df['RACE'] = race_values

# Drop the original race checkbox columns if no longer needed
df.drop(columns=race_columns, inplace=True)

# Now rename repeated column patterns
new_columns = []
for col in df.columns:
    base = re.sub(r'\.\d+$', '', col).strip()
    if base in rename_map:
        new_columns.append(rename_map[base])
    else:
        new_columns.append(col)  # keep as-is if no match

df.columns = new_columns

# Save the cleaned file
df.to_excel("MD/cincinnati_childrens/_final/concat.xlsx", index=False)
print("✓ Data exported successfully.")
