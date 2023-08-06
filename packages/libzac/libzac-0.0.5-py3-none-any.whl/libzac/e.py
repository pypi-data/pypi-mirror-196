from . import _sys
from . import _re
from . import _np
from . import _plt
from . import _pd
from .io import byte2int as _byte2int
import subprocess as _subprocess

def eread(addr, length=1, dtype="u1", ch=0):
    raw = _subprocess.run(f"e {addr}l{length}", capture_output=True, env={"ch":f"{ch}"}).stdout.decode("utf8")
    return eraw2int(raw, dtype=dtype)[0]

def ewrite(addr, value, ch=0):
    _subprocess.run(f"e {addr} {value}", env={"ch":f"{ch}"})

def ewrite_block(addr, u1_data):
    data_length = len(u1_data)
    addr = addr if isinstance(addr, int) else int(addr,16)
    
    for i in range(0,data_length,8):
        block = u1_data[i:min(i+8,data_length)]
        data = "".join([f"{b:02x}" if isinstance(b,(int,_np.integer)) else b for b in block][::-1])
        start_address = f"{addr + i:x}"
        ewrite(start_address, data)

def eraw2byte(raw, skip_row=1):
    raw = raw.split("\n")[skip_row:]
    data = []
    addr = []
    start_addr = int(_re.search("[0-9a-f]+(?= : )",raw[0]).group(),16)
    start_addr += (_re.search(" [0-9a-f]{2} ",raw[0]).span()[0]-8)//3
    for r in raw:
        row = _re.split("(\\W*[0-9a-f]+ : )",r)
        if len(row) > 2:
            for d in row[2].split(" "):
                if (len(d)==2):
                    data.append(int(d,16))
                    addr.append(f"{start_addr:x}")
                    start_addr += 1
    byte = _np.asarray(data,dtype=_np.uint8).tobytes()
    addr = _np.asarray(addr)
    return byte, addr

def eraw2int(raw, dtype="<i4", skip_row=1):
    byte, addr = eraw2byte(raw, skip_row=skip_row)
    return _byte2int(byte,  dtype=dtype), addr

def eraw2plt(raw, dtype="<i4", skip_row=1):
    _plt.figure()
    data, addr = eraw2int(raw, dtype=dtype, skip_row=skip_row)
    _plt.plot(addr, data)
    _plt.show()

def efile2byte(filename,skip_row=1):
    with open(filename,"r") as f:
        raw = f.read()
    return eraw2byte(raw, skip_row=skip_row)

def efile2int(filename, dtype="<i4", skip_row=1):
    with open(filename,"r") as f:
        raw = f.read()
    return eraw2int(raw, dtype=dtype, skip_row=skip_row)

def efile2plt(filename, dtype="<i4", skip_row=1):
    with open(filename,"r") as f:
        raw = f.read()
    return eraw2plt(raw, dtype=dtype, skip_row=skip_row)

def efilewrite_block(filename, skip_row=1):
    u1_data,addr = efile2int(filename, "u1", skip_row=skip_row)
    ewrite_block(addr[0], u1_data)

