def safe_division(a, b):
    if a == 0 or b == 0:
        return 0.0
    return round(a / float(b), 4)
