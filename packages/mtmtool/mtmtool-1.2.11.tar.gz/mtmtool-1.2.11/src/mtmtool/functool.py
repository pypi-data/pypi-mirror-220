def func_args2kwargs(func, *args, **kwargs):
    """
    将函数的参数转换为字典
    """
    args = list(args)
    params = list(func.__code__.co_varnames)
    kwargs_new_dict = {}

    # Python 3.8+ only
    try:
        for _ in range(func.__code__.co_posonlyargcount):
            kwargs_new_dict[params.pop(0)] = args.pop(0)
    except Exception:
        pass
    
    # Python 3
    for _ in range(func.__code__.co_argcount - 1):
        kwargs_new_dict[params.pop(0)] = args.pop(0)

    for _ in range(func.__code__.co_kwonlyargcount):
        params.pop(0)

    kwargs_new_dict[params.pop(0)] = tuple(args)
    kwargs_new_dict.update(kwargs)
    return kwargs_new_dict