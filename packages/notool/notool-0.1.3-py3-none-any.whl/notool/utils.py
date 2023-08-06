import re
import inspect
import linecache
import typing as t
import functools

C = t.TypeVar('C')


def wraps_hint(decorator: C) -> C:
    return decorator


@wraps_hint
def functools_cache(func):
    return functools.cache(func)


@wraps_hint
def start_generator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        generator = func(*args, **kwargs)
        next(generator)
        return generator
    return wrapper


def get_var_name(var):
    # f'{var=}' slow down if data grows, and you must call f'' inline
    result = inspect.currentframe().f_back
    result = linecache.getline(result.f_code.co_filename, result.f_lineno)
    result = re.match(rf'.*?get_var_name\((.*?)\).*?', result).groups()
    return result[0] if result else ''
