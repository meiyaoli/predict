import json
import pandas as pd
from collections import OrderedDict
from datetime import datetime

info_map = {
    "Title": "title",
    "Name": "name",
    "Release Notes": "release_notes",
    "Parent Data Model": "parent_data_model",
    "License": "license",
    "D4CG Data Modeling Wiki": "wiki",
    "Disease Consortium Information": "consortium_info",
    "Description": "description",
    "Total Variables": "total"
}

df_raw = pd.read_csv("_dictionaries/NPC/npc_v1.1.csv", header=None)

info = {}
for _, row in df_raw.iterrows():
    if row[0] == "INFO":
        label = str(row[1]).strip()
        value = str(row[2]).strip() if pd.notna(row[2]) else ""
        key = info_map.get(label)
        if key:
            info[key] = value

header_row_idx = df_raw[df_raw[0] == "RowType"].index[0]
headers = df_raw.iloc[header_row_idx].tolist()

df = df_raw.iloc[header_row_idx + 1:].copy()
df.columns = headers
df.reset_index(drop=True, inplace=True)

variable_count = (df["RowType"] == "VD").sum()
info["total"] = str(variable_count)

def parse(m, row, index, col_name, i):
    try:
        val = str(row[index]).strip()
        return "" if val.lower() == "nan" else val
    except IndexError:
        print(f"Missing {col_name} in row {i + 1} of {m.dg}")
        return ""

class Model:
    def __init__(self, name, sheet_id, dg, date):
        self.dg = dg
        self.meta = {"name": name, "timestamp": date, "sheet_id": sheet_id}
        self.info = {
            "title": "", "name": "", "release_notes": "", "parent_data_model": "",
            "license": "", "wiki": "", "consortium_info": "", "description": "", "total": ""
        }
        self.variables = OrderedDict()

    def __str__(self):
        model = {
            "meta": self.meta,
            "info": self.info,
            "domains": {}
        }
        for (dom, tbl, vname), var in self.variables.items():
            model["domains"].setdefault(dom, {}).setdefault(tbl, {})[vname] = var.__str__()
        return json.dumps(model, indent=4)

class Variable:
    def __init__(self, m, row, domain, table, i):
        self.domain = domain
        self.table = table
        self.name = parse(m, row, 1, "VariableName", i)
        self.type = parse(m, row, 2, "DataType", i)
        self.tier = parse(m, row, 3, "Tier", i)
        self.desc = parse(m, row, 4, "VariableDescription", i)
        self.codes = list(filter(None, parse(m, row, 5, "VariableCode", i).split("|")))
        self.inotes = list(filter(None, parse(m, row, 9, "ImplementationNotes", i).split("|")))
        self.mappings = list(filter(None, parse(m, row, 10, "Mappings", i).split("|")))
        self.values = OrderedDict()
        self.coded = self.type in ("Enum", "Code")

    def __str__(self):
        d = {
            "type": self.type,
            "tier": self.tier,
            "description": self.desc,
            "codes": self.codes,
            "implementation_notes": self.inotes,
            "mappings": self.mappings
        }
        if self.coded:
            d["permissible_values"] = {v.name: v.__str__() for v in self.values.values()}
        return d

class Value:
    def __init__(self, m, row, i):
        self.name = parse(m, row, 6, "PermissibleValue", i)
        self.desc = parse(m, row, 7, "ValueDescription", i)
        self.codes = list(filter(None, parse(m, row, 8, "ValueCode", i).split("|")))
        self.inotes = list(filter(None, parse(m, row, 9, "ImplementationNotes", i).split("|")))
        self.mappings = list(filter(None, parse(m, row, 10, "Mappings", i).split("|")))

    def __str__(self):
        return {
            "description": self.desc,
            "codes": self.codes,
            "implementation_notes": self.inotes,
            "mappings": self.mappings
        }


model = Model(name=info.get("name", "npc_v1.1"), sheet_id="", dg="npc_v1.1.csv", date=datetime.today().strftime("%Y%m%d"))
model.info.update(info)

current_domain = None
current_table = None
last_var_name = None

for i, row in df.iterrows():
    rowtype = str(row.get("RowType", "")).strip()

    if rowtype == "DD":
        current_domain = str(row.get("VariableName", "")).strip().replace(" ", "_").lower()
        continue
    elif rowtype == "TD":
        current_table = str(row.get("VariableName", "")).strip().replace(" ", "_").lower()
        continue
    elif rowtype == "VD":
        if current_domain and current_table:
            var = Variable(model, row, current_domain, current_table, i)
            last_var_name = var.name
            model.variables[(current_domain, current_table, last_var_name)] = var
    elif rowtype == "PD":
        raw_var_name = row.get("VariableName", "")
        var_name = str(raw_var_name).strip() if pd.notna(raw_var_name) else last_var_name
        key = (current_domain, current_table, var_name)
        if key in model.variables:
            model.variables[key].values[Value(model, row, i).name] = Value(model, row, i)

with open("_dictionaries/NPC/npc_v1.1.json", "w") as f:
    f.write(str(model))

print("✅ 'npc_v1.1.json' is saved")
