def convert_from_decimal(n):
    return {
        "DEC": str(n),
        "BIN": bin(n)[2:],
        "HEX": hex(n)[2:].upper(),
        "OCT": oct(n)[2:]
    }

def convert_to_decimal(value, base):
    return int(value, base)

def convert_any(value, base):
    dec = convert_to_decimal(value, base)
    return convert_from_decimal(dec)