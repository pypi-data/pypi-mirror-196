from . import _np, _pd, _re, _os
from .e import efile2int

autoREG = """
e 8000ld9c  > bb.txt
e 8900laa   > modem.txt
e 8a00la3   > rf.txt
e 8b00l1b   > codec.txt

e 8336l16   > lpm.txt

e 801c 0
e 83a1l4    > "LDO Control.txt"

e 801c 1
e 8380l4    > "CHARGER CTRL.txt"

e 801c 2
e 8380l4    > "XO32K CONTROL.txt"

e 801c 4
e 8380l4    > CHARGER_WAKE_CTRL.txt

e 81f2 1
e 8389l4    > TS_ANA_CTRL.txt
e 81f2 0
e 81f2 2
e 8389l4    > TS_FIR_CTRL.txt
e 81f2 0
e 81f2 4
e 8389l4    > TS_CAL_CTRL1.txt
e 81f2 0
e 81f2 8
e 8389l4    > TS_CAL_CTRL2.txt
e 81f2 0
e 81f2 10
e 8389l4    > TS_CAL_CTRL3.txt
e 81f2 0
e 81f2 20
e 8389l4    > TS_CAL_CTRL4.txt
e 81f2 0
e 81f2 40
e 8389l4    > TS_CMP_CTRL1.txt
e 81f2 0
e 81f2 80
e 8389l4    > TS_CMP_CTRL2.txt
e 81f2 0

e 81f3 1
e 8389l4    > TS_CAL_CFG.txt
e 81f3 0
e 81f3 2
e 8389l4    > TS_BL_CTRL1.txt
e 81f3 0
e 81f3 4
e 8389l4    > TS_BL_CTRL2.txt
e 81f3 0
e 81f3 8
e 8389l4    > TS_BL_CTRL3.txt
e 81f3 0
e 81f3 10
e 8389l4    > TS_BL_CTRL4.txt
e 81f3 0
"""

file_dict = {
    "dig.txt"           :   "bb.txt",
    "xo32.txt"          :   "XO32K CONTROL.txt",
    "lpm_ldo.txt"       :   "LDO Control.txt",
    "charge.txt"        :   "CHARGER CTRL.txt",
    "TS_AnalogCTRL.txt" :   "TS_ANA_CTRL.txt",
    "TS_FIRCTRL.txt"    :   "TS_FIR_CTRL.txt",
    "TS_CAL1CTRL.txt"   :   "TS_CAL_CTRL1.txt",
    "TS_CAL2CTRL.txt"   :   "TS_CAL_CTRL2.txt",
    "TS_CAL3CTRL.txt"   :   "TS_CAL_CTRL3.txt",
    "TS_CAL4CTRL.txt"   :   "TS_CAL_CTRL4.txt",
    "TS_CMP1CTRL.txt"   :   "TS_CMP_CTRL1.txt",
    "TS_CMP2CTRL.txt"   :   "TS_CMP_CTRL2.txt",
    "TS_CALCFG.txt"     :   "TS_CAL_CFG.txt",
    "TS_BL1CTRL.txt"    :   "TS_BL_CTRL1.txt",
    "TS_BL2CTRL.txt"    :   "TS_BL_CTRL2.txt",
    "TS_BL3CTRL.txt"    :   "TS_BL_CTRL3.txt",
    "TS_BL4CTRL.txt"    :   "TS_BL_CTRL4.txt",
}
def rename(folder, file_dict):
    for r,d,f in _os.walk(folder):
        for i in f:
            if i in file_dict:
                _os.rename(r+"/"+i, r+"/"+file_dict[i])

def read_ycreg_excel(filename, sheet_name, addr_name, width_name, header=0, drop_list=[]):
    drop_list += ["initVal\n（HEX）","Owner","Isolation","Pad","No buffer net","Memory dump","GPIO Monitor","Scan Static","original","access"]
    table = _pd.read_excel(filename,sheet_name=sheet_name,header=header)
    table = table.drop(drop_list,axis=1, errors="ignore")
    table = table.rename(columns={addr_name:"addr",width_name:"width"})
    table["addr"] = [str(i).lower() for i in table["addr"]]
    table = table.replace("nan",_np.nan)
    first_all_nan_row = _np.where(table.isna().all(axis=1))[0]
    if first_all_nan_row.size > 0:
        table = table[:first_all_nan_row[0]]

    width_index = _np.where(table.columns == "width")[0][0]
    for col in table.columns[:width_index]:
        table[col] = table[col].fillna(method="ffill")
    return table

def parse_width(width):
    if isinstance(width, (_np.integer, int)):
        return width, width
    if (not width) or (width == "nan"):
        return -1,-1
    width = width.replace("[","").replace("]","").replace(" ","")
    width = width.split(":")
    start, stop = (int(width[1]), int(width[0])) if len(width)==2 else (int(width[0]), int(width[0]))
    return start, stop

def efile_to_hashmap(filename):
    data, addr = efile2int(filename,"u1")
    reg_map = {}
    for d,a in zip(data,addr):
        reg_map[f"{int(a,16):04x}"] = d
    return reg_map

def parse_reg(addr, reg_map, start, stop):
    length_byte = (stop // 8) + 1
    if length_byte > 8:
        return "too large"

    reg = reg_map.get(addr,-1)
    if reg >= 0:
        binary = _np.binary_repr(reg, 8)
        for j in range(1, length_byte):
            read_addr = f"{int(addr,16)+j:x}"
            read_value = reg_map.get(read_addr,0)
            binary = _np.binary_repr(read_value, 8) + binary       
                     
        bitwidth = length_byte*8
        reg_bin = binary[bitwidth-stop-1:bitwidth-start]
        length = int(_np.ceil((len(reg_bin)) / 8))
        
        return f"{int(reg_bin,2):0{length*2}x}"# if stop-start >= 7 else f"0b{reg_bin}"
    else:
        return "nan"

def parse_table(table, index, reg_map, new_column):        
    for i in index:    
        try:
            start, stop = parse_width(table.loc[i,"width"])
            if start >= 0 and not _pd.isna(table.loc[i,"addr"]):            
                addr = _re.search(r"[\da-f]{4}",table.loc[i,"addr"])
                if addr is not None:     
                    addr = addr.group()
                    table.loc[i,new_column] = parse_reg(addr, reg_map, start, stop)
        except:
            print(f"Unable to parse table line{i}: \n{table.loc[i]}")

def parse_lpm_type(table, type_name, efilename, new_column):
    lpm_reg_map = efile_to_hashmap(efilename)
    lpm_table = table[table["Type"] == type_name]
    parse_table(table, lpm_table.index, lpm_reg_map, new_column)

def compare_reg(table, compare_list):
    for new_column in compare_list:
        table[new_column] = _np.zeros(len(table),str)
        reg_map = efile_to_hashmap(new_column)
        parse_table(table, range(len(table)), reg_map, new_column)

    diff = table[compare_list[0]] != table[compare_list[0]]
    for comp in compare_list:
        diff |= (table[compare_list[0]] != table[comp])
    return table[diff]

def compare_lpmreg(table, compare_folder_list):
    for new_column in compare_folder_list:
        table[new_column] = _np.zeros(len(table),str)
        lpm_regmap = {}
        for f in _os.listdir(new_column):
            if f[:3] == "lpm":
                lpm_regmap |= efile_to_hashmap(f"{new_column}/{f}")    
        parse_table(table, range(len(table)), lpm_regmap, new_column)
        lpm_type_names = [
            "LDO Control",
            "XO32K CONTROL",
            "CHARGER CTRL",
            "CHARGER CTRL",
            "TS_ANA_CTRL",
            "TS_FIR_CTRL",
            "TS_CAL_CTRL1",
            "TS_CAL_CTRL2",
            "TS_CAL_CTRL3",
            "TS_CAL_CTRL4",
            "TS_CMP_CTRL1",
            "TS_CMP_CTRL2",
            "TS_CAL_CFG",
            "TS_BL_CTRL1",
            "TS_BL_CTRL2",
            "TS_BL_CTRL3",
            "TS_BL_CTRL4",
        ]
        for name in lpm_type_names:
            try:
                parse_lpm_type(table, name, f"{new_column}/{name}.txt", new_column)
            except FileNotFoundError:
                print(f"{new_column}/{name}.txt is not found")

    diff = table[compare_folder_list[0]] != table[compare_folder_list[0]]
    for comp in compare_folder_list:
        diff |= (table[compare_folder_list[0]] != table[comp])
    return table[diff]

def compare_bb(compare_list, bbreg=r"E:\Work\Yichip\1121G\Docs\svn\4_Register\yc1121G-bbreg.xlsx"):
    table = read_ycreg_excel(bbreg, "bb", "地址", "位置", 0)
    return compare_reg(table, compare_list)

def compare_rfreg(compare_list, sheet_name, rfreg=r"E:\Work\Yichip\1121G\Docs\svn\4_Register\yc1121G_rfreg.xlsx"):
    table = read_ycreg_excel(rfreg, sheet_name, "addr", "width", 0)
    return compare_reg(table, compare_list)

def compare_lpm(compare_folder_list, bbreg=r"E:\Work\Yichip\1121G\Docs\svn\4_Register\yc1121G-bbreg.xlsx"):
    table = read_ycreg_excel(bbreg, "lpm", "Read Address", "Bit", 1, ["Write Address","Unnamed: 7"])
    return compare_lpmreg(table, compare_folder_list)

def compare_autoREG(compare_folder_list):
    bb = compare_bb([f+"/bb.txt" for f in compare_folder_list])
    rf = compare_rfreg([f+"/rf.txt" for f in compare_folder_list], "RF")
    modem = compare_rfreg([f+"/modem.txt" for f in compare_folder_list], "MODEM")
    codec = compare_rfreg([f+"/codec.txt" for f in compare_folder_list], "Codec")
    lpm = compare_lpm(compare_folder_list)
    return bb, rf, modem, codec, lpm
