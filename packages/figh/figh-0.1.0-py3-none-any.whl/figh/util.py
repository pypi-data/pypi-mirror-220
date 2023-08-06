from figh.errors import DupKeyException


def nested_set(dic, keys, value):
    for key in keys[:-1]:
        dic = dic.setdefault(key, {})
    if keys[-1] in dic and dic[keys[-1]]:
        raise DupKeyException(f"key {keys[-1]} duplicated")
    dic[keys[-1]] = value
