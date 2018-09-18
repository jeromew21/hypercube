def flip1(bit):
    if bit == 1:
        return 0
    elif bit == 0:
        return 1
    else:
        raise Exception("Not a bit")
    
def flip2(bit):
    return 0 if bit == 1 else 1

flip3 = lambda bit: abs(bit - 1)