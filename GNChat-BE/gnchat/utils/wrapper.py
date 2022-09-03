from functools import wraps

from gnchat.utils.formatter import data_formatter
from gnchat.utils.gnexcept import GNException
from gnchat.utils.response import make_data_response, CODENAME


def response_wraps(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            ret = func(*args, **kwargs)
            ret = data_formatter(ret)
            response_data = make_data_response(CODENAME.OK, ret)
        except GNException as exc:
            response_data = make_data_response(exc.code, exc.message)
        print("response: {}".format(response_data.response))
        return response_data

    return wrapper
