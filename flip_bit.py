def flip1(bit):
    if bit == 1:
        return 0
    if bit == 0:
        return 1
    else:
        raise Exception("Not a bit")
    
def flip2(bit):
    return abs(bit - 1)

flip3 = lambda bit: 1 if bit == 0 else 0