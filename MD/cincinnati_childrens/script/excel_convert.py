import pandas as pd

df = pd.read_csv("MD/cincinnati_childrens/raw/cincinnati_childrens_hospital.csv", dtype=str)  # Read everything as string

# Save as Excel
df.to_excel("MD/cincinnati_childrens/raw/cincinnati_childrens_hospital.xlsx", index=False)
