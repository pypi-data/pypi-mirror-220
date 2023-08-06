from itertools import product


def product_dict(srcdict)->list:
    """
    Args:
        srcdict (dict): key:str, value: list(元素为可能的值),

    Returns:
        list: 拆分后的参数字典
    """
    paras = []
    comb = product(*[srcdict[key] for key in srcdict])
    for para in comb:
        t = {}
        for idx, key in enumerate(srcdict):
            t[key] = para[idx]
        paras.append(t)
    return paras
