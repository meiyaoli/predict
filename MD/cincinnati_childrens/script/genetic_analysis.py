import pandas as pd

df = pd.read_excel("MD/cincinnati_childrens/raw_final/raw_genetic_analysis.xlsx")

#strip column names
df.columns = df.columns.str.strip()

#drop unnecessary columns
df.drop(columns=['Complete?'], inplace=True)

#store subject ID
subject_id = df['Honest Broker Subject ID']

#replace NaN
df = df.fillna('')

#renaming the columns to match dictionary
df.rename(columns={
    'Honest Broker Subject ID': 'HONEST_BROKER_SUBJECT_ID',
    'The age of the subject when the genetic test was performed': 'AGE_AT',
    'The unit of the age of the subject when the genetic test was performed': 'AGE_UNIT',
    'The precision of the age of the subject when the genetic test was performed': 'AGE_PRECISION',
    "Is this genetic alteration a cause for the subject's diabetes?": 'CAUSITIVE_ALTERATION',
    'Is the genetic alteration present or absent?': 'STATUS',
    'What type of sample was used for this genetic analysis?': 'SAMPLE_TYPE',
    'Where was this genetic test performed?': 'LABORATORY_NAME',
    'The genetic testing method/technique used to generate the observed results.': 'METHOD',
    'The chromosome on which the observed mutation is located.': 'CYTOGENETIC_LOCATION',
    'The gene targeted for mutation analysis, identified in HUGO Gene Nomenclature Committee (HGNC) notation.': 'GENE',
    'The type of variation detected by this genetic analysis.': 'ALTERATION_TYPE',
    'Alteration Effect': "ALTERATION_EFFECT",
    'Alteration Region': 'ALTERATION_REGION',
    'HGVS Accession number': 'HGVS_ACCESSION',
    'If this alteration is described at the sequence/chromosome level, this is its representation in HGVS nomenclature (cHGVS).': "HGVS_CODING",
    'If this alteration is described at the translational product level, this is its representation in HGVS nomenclature (pHGVS)': 'HGVS_PROTEIN',
    'If this alteration is described at the genome level, this is its representation in HGVS nomenclature (gHGVS)': "HGVS_GENOMIC",
    'An international standard for human chromosome nomenclature, which includes band names, symbols and abbreviated terms used in the description of human chromosome and chromosome abnormalities.': "ISCN",
    'The initial reported ACMG clinical significance of this genetic variation.': 'REPORTED_SIGNIFICANCE',
    'Allelic state - the specific combination of alleles (gene variants) that an individual possesses at a particular genetic locus (location on a chromosome).': 'ALLELIC_STATE',
    'The incidence of this mutation in the sample (%).': 'MAF_NUMERIC',
    'Does this subject have two or more genetically different sets of cells in their body?': 'MOSAICISM',
    'An ID to an external knowledge base that holds additional information about this genetic variant.': 'EXTERNAL_REF_ID',
    'The name of the external knowledge base from which the external ID is drawn.': 'EXTERNAL_REF_ID_SYSTEM'
}, inplace=True)

print(df.to_string(index=False))

df.to_excel('MD/cincinnati_childrens/_final/genetic_analysis.xlsx', index=False)
print("✓ Data exported successfully.")
