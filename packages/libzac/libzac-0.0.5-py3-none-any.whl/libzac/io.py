from . import _re
from . import _np
from . import _sys
_np.set_printoptions(threshold=999999)

def i4_to_i3u1(i4):
    i3u1 = _np.zeros(i4.size*3, dtype=_np.uint8)
    i4u1 = _np.frombuffer(i4.tobytes(), dtype=_np.uint8)
    if i4.dtype.byteorder == ">":
        i3u1[0::3] = i4u1[1::4]
        i3u1[1::3] = i4u1[2::4]
        i3u1[2::3] = i4u1[3::4]
    else:
        i3u1[0::3] = i4u1[0::4]
        i3u1[1::3] = i4u1[1::4]
        i3u1[2::3] = i4u1[2::4]
    return i3u1

def i3u1_to_i4(i3u1, endianness="<"):
    i4 = _np.zeros(i3u1.size//3, dtype=_np.int32)
    i4u1 = i4.view(_np.uint8)
    if endianness == ">":
        i4u1[1::4] = i3u1[0::3]
        i4u1[2::4] = i3u1[1::3]
        i4u1[3::4] = i3u1[2::3]
    else:
        i4u1[0::4] = i3u1[0::3]
        i4u1[1::4] = i3u1[1::3]
        i4u1[2::4] = i3u1[2::3]
    i4 = u2i(i4, 24)
    return i4

def u2i(x, width):
    upper = (1<<(width))-1
    lower = 0
    up = x > upper
    low = x < lower 

    if isinstance(x, (int, _np.integer)):
        if up:
            print("OVERFLOW")
            return upper
        if low:
            print("UNDERFLOW")
            return lower
        return x-(1<<width) if x & (1<<(width-1)) else x

    elif isinstance(x, _np.ndarray):
        dtype = f"=i{x.dtype.itemsize}"
        x = x.copy().astype("i8")
        if up.any():
            print("OVERFLOW")
            x[up] = upper
        if low.any():
            print("UNDERFLOW")
            x[low] = lower
        x[x >= (1<<(width-1))] -= (1<<width)
        return x.astype(dtype)

    else:
        print("NOT SUPPORT")
        return None

def i2u(x, width):
    upper = (1<<(width-1))-1
    lower = -(1<<(width-1))
    up = x > upper
    low = x < lower 

    if isinstance(x, (int, _np.integer)):
        if up:
            print("OVERFLOW")
            return upper
        if low:
            print("UNDERFLOW")
            return lower
        return x+(1<<width) if x < 0 else x

    elif isinstance(x, _np.ndarray):
        x = x.copy().astype("i8")
        if up.any():
            print("OVERFLOW")
            x[up] = upper
        if low.any():
            print("UNDERFLOW")
            x[low] = lower
        x[x < 0] += (1<<width)        
        return x

    else:
        print("NOT SUPPORT")
        return None

def c2np(filename):
    with open(filename,'r') as f:
        raw = f.read()
    dtype_dict = {
        'float':        _np.float32,
        'double':       _np.float64,
        'unsigned char':_np.uint8,
        'char':         _np.int8,
        'uint8_t':      _np.uint8,
        'int8_t':       _np.int8,
        'short':        _np.int16,
        'uint16_t':     _np.uint16,
        'int16_t':      _np.int16,
        'unsigned int': _np.uint32,
        'uint32_t':     _np.uint32,
        'int':          _np.int32,
        'int32_t':      _np.int32,
    }
    regex = "((?:"+")|(?:".join(list(dtype_dict.keys()))+"))" + r"\s*(\w*)(\[.*\])\s*=\s*(\{[\s\S]*?\});"
    match = _re.findall(regex, raw)
    array_dict = {}
    for group in match:
        dtype = dtype_dict[group[0]]
        array_name = group[1]
        data_str = group[3].replace("{","[").replace("}",']')   # change c array {} to python list []
        clean_str = _re.sub("\/\/[\S\s]*?\\n", '', data_str)    # remove comment //
        clean_str = _re.sub("\/\*[\S\s]*?\*\/",'', clean_str)   # remove comment /* */
        try:
            data = eval(clean_str) # this is not secure but i dont care
        except Exception as error:
            print(f"parse {group[1]} error: ",error)
        array = _np.array(data).astype(dtype)
        array_dict[array_name] = array
    return array_dict

def np2c(np_dict_array, filename, addition=[]):
    with open(filename, "w") as f:
        filename_no_ext = filename.split('.')[0]
        f.write(f"#ifndef __{filename_no_ext}__\n#define __{filename_no_ext}__\n#include <stdint.h>\n\n")
        
        for line in addition:
            f.write(line)
            f.write("\n")
        
        for array_name,array in np_dict_array.items():
            dtype = array.dtype
            if _np.issubdtype(dtype, _np.floating):
                dtype_name = "float" if dtype.itemsize == 4 else "double"
            elif _np.issubdtype(dtype, _np.integer):
                dtype_name = f"{_np.dtype(dtype).base.name}_t"
            f.write(f"const {dtype_name} {array_name}[{array.size}] = {{\n")
            array_str = _np.array2string(array, separator=",")[1:-1]
            f.write(array_str)
            f.write("\n};\n\n")

        f.write("\n#endif")           


def file2c(filename_in, filename_out, array_name, dtype=_np.uint8):
    with open(filename_in, "rb") as f:
        raw_byte = f.read()
    byte2c(raw_byte, filename_out, array_name, dtype)

def byte2c(byte, filename, array_name="byte_buf", dtype=_np.int8):
    dtype = _np.dtype(dtype)
    size = dtype.itemsize
    byte = byte[:len(byte)//size*size]
    array = _np.frombuffer(byte, dtype=dtype)
    np2c({array_name:array}, filename)

def byte2int(byte, dtype="<i4"):
    if isinstance(dtype, str) and dtype[-1]=='3':
        i3u1 = _np.frombuffer(byte,"u1").copy()
        endianness = ">" if dtype[0]==">" else "<"
        return i3u1_to_i4(i3u1, endianness)
    else:
        return _np.frombuffer(byte,dtype=dtype).copy()

