from functools import wraps


def cccc(func):
    # @wraps
    def wrapper(*args, **kwargs):
        nargs, nkwargs = args2kwargs(func, *args, **kwargs)
        print(nargs, nkwargs)
        return func(*nargs, **nkwargs)

    return wrapper


@cccc
def hello2(d, /, c, b, *args, word=10, **kwargs):
    return locals()


# def hello2(a, *args, word=10, **kwargs):
#     return locals()


def args2kwargs(func, *args, **kwargs):
    args = list(args)
    params = list(func.__code__.co_varnames)
    kwargs_new_dict = {}
    args_new_list = []

    for _ in range(func.__code__.co_posonlyargcount):
        kwargs_new_dict[params.pop(0)] = args.pop(0)

    for _ in range(func.__code__.co_argcount - 1):
        kwargs_new_dict[params.pop(0)] = args.pop(0)

    for _ in range(func.__code__.co_kwonlyargcount):
        params.pop(0)
    args_new_list = tuple(args_new_list)
    kwargs_new_dict[params.pop(0)] = tuple(args)
    kwargs_new_dict.update(kwargs)
    return kwargs_new_dict


if __name__ == '__main__':
    print(hello2.__code__.co_varnames)
    print(hello2.__code__.co_nlocals)
    print("co_posonlyargcount", hello2.__code__.co_posonlyargcount)
    print("co_argcount", hello2.__code__.co_argcount)
    print("co_kwonlyargcount", hello2.__code__.co_kwonlyargcount)
    print(hello2.__code__.co_stacksize)

    print(hello2(16, 3, 4, 5, 6, 7, 15, ccccc=15))
