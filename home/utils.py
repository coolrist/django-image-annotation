def is_number(n):
    try:
        int(n)
        return True
    except ValueError:
        return False