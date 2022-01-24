from fractions import Fraction

def number_str_to_float(amount_str):
    success = False
    number_as_float = amount_str
    try:
        number_as_float = float(sum(Fraction(s) for s in f'{amount_str}'.split()))
    except:
        pass
    if isinstance(number_as_float, float):
        success = True
    return number_as_float, success
