import datetime

from gnchat.orm.main import MessageModel, UserModel


def data_formatter(data):
    if isinstance(data, MessageModel):
        data = data.to_dict()
    elif isinstance(data, list):
        data = [data_formatter(i) for i in data]
    elif isinstance(data, UserModel):
        data = data.to_dict()
    # elif isinstance(data, dict):
    #     data = {
    #         key: data_formatter(value)
    #         for key, value in data.items()
    #     }
    return data
