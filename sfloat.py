def twos_complement(value, bitWidth):
    if value >= 2**bitWidth:
        raise ValueError(
            "Value: {} out of range of {}-bit value.".    format(value, bitWidth))
    else:
        return value - int((value << 1) & 2**bitWidth)


def getExponent(value):
    exponent = twos_complement(((value >> 12) & 0xF), 4)
    return int(exponent)


def getMantissa(value):
    mantissa = twos_complement((value & 0x0FFF), 12)
    return int(mantissa)


def to_int(value):
    # NaN
    if (value == 0x07FF):
        return float('nan')
    # NRes (not at this resolution)
    elif (value == 0x0800):
        return float('nan')
    # Positive infinity
    elif (value == 0x07FE):
        return float("inf")
    # Negative infinity
    elif (value == 0x0802):
        return float("-inf")
    # Reserved
    elif (value == 0x0801):
        return float("nan")
    else:
        return float(getMantissa(value) * pow(10, getExponent(value)))

