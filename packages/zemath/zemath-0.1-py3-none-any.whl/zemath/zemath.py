def add(x=0, *args):
    result = x
    for a in args:
        result = result + a
    return result

def sub(x=0, *args):
    result = x
    for a in args:
        result = result - a
    return result

def mul(x=0, *args):
    result = x
    for a in args:
        result = result * a
    return result

def div(x=0, *args):
    result = x
    for a in args:
        result = result / a
    return result