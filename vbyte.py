# vbyte.py

def vbyte_encode(numbers):
    encoded = []
    for number in numbers:
        while number >= 128:
            encoded.append((number & 0x7F) | 0x80)
            number >>= 7
        encoded.append(number & 0x7F)
    return encoded

def vbyte_decode(encoded):
    numbers = []
    current_number = 0
    shift = 0
    for byte in encoded:
        if byte & 0x80:
            current_number |= (byte & 0x7F) << shift
            shift += 7
        else:
            current_number |= byte << shift
            numbers.append(current_number)
            current_number = 0
            shift = 0
    return numbers

