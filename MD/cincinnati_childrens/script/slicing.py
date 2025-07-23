import pandas as pd
from openpyxl import Workbook
from openpyxl import load_workbook, Workbook

input_file = "MD/cincinnati_childrens/raw/cincinnati_childrens_hospital.xlsx"    
output_file = "MD/cincinnati_childrens/_final/output.xlsx"

wb_in = load_workbook(filename=input_file)
ws_in = wb_in.active

# extracting the header
header = [cell.value.strip() if isinstance(cell.value, str) else cell.value for cell in ws_in[1]]

# extracting all data except header
data_rows = list(ws_in.iter_rows(min_row=2, values_only=True))

complete_indices = [i for i, col in enumerate(header) if col == "Complete?"]

# grabbing honest broker subject id for each sheet
try:
    id_index = header.index("Honest Broker Subject ID")
except ValueError:
    raise ValueError("❌ 'Honest Broker Subject ID' not found.")

wb_out = Workbook()
wb_out.remove(wb_out.active)  

start_idx = id_index + 1

for block_num, end_idx in enumerate(complete_indices, start=1):
    wb_out = Workbook()
    ws_out = wb_out.active
    ws_out.title = "Data"

    # identifying columns for this block (ID + block)
    col_indices = [id_index] + list(range(start_idx, end_idx + 1))
    block_header = [header[i] for i in col_indices]
    ws_out.append(block_header)

    for row in data_rows:
        block_row = [row[i] if i < len(row) else None for i in col_indices]
        ws_out.append(block_row)

    output_path = f"MD/cincinnati_childrens/_final/block_{block_num}.xlsx"
    wb_out.save(output_path)
    print(f"✓ Saved Block {block_num} to {output_path}")

    # starting the next iteration
    start_idx = end_idx + 1