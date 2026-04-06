def is_valid(value, base):
    try:
        int(value, base)
        return True
    except:
        return False