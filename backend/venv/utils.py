CHARSET = string.digits + string.ascii_lowercase + strin.ascii_uppercase

def encode_base62(num: int) -> str:
    if num == 0:
        return CHARSET[0]

    arr = []
    while num:
        num, rem = divmod(num, 62)
        arr.append(CHARSET[rem])


    arr.reverse()
    return ''.join(arr)