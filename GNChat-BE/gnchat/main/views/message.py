import json
import logging
from copy import copy

from flask import request
from datetime import datetime

from sqlalchemy import text

from gnchat.utils.encrypt import decrypt, encrypt
from gnchat.utils.formatter import data_formatter
from gnchat.utils.gnexcept import GNException
from gnchat.utils.wrapper import response_wraps
from gnchat.main.blueprint import main_blueprint
from gnchat.orm.main import MessageModel, UserModel
from gnchat.utils.response import CODENAME
from gnchat.utils.uuid_utils import get_uuid


@main_blueprint.route("/pmsg", methods=['POST'])
@response_wraps
def send_message():
    data = decrypt(request.data)
    user_uuid = data.get('user_uuid', None)
    is_picture = data.get('is_picture', False)
    content = data.get('content', None)

    if UserModel.get_item(user_uuid=user_uuid) is None:
        raise GNException(CODENAME.MSG_USER_NOT_EXISTS)

    message_uuid = get_uuid()

    MessageModel.insert_item(
        MessageModel(
            message_uuid=message_uuid,
            owner_uuid=user_uuid,
            is_picture=is_picture,
            content=content,
            group_id=0,  # default group
            send_time=datetime.utcnow()
        )
    )
    return encrypt({"message_uuid": message_uuid})


@main_blueprint.route("/gmsg", methods=['POST'])
@response_wraps
def get_message():
    data = decrypt(request.data)
    # print("Request data is: {}".format(data))
    user_uuid = data.get('user_uuid', None)

    if not user_uuid:
        raise GNException(CODENAME.BAD_REQUEST)

    user = UserModel.get_user(user_uuid)
    if user is None:
        raise GNException(CODENAME.MSG_USER_NOT_EXISTS)

    count = data.get('count')
    if not count:
        latest_read = copy(user.latest_read)

        message_list = MessageModel.query.filter_by(group_id=0).filter(
            latest_read < MessageModel.send_time,
        ).order_by(text("-send_time")).limit(20).all()
        message_list = [msg.to_dict() for msg in message_list]
        if len(message_list) != 0:
            user.update_item(latest_read=datetime.utcnow())
    else:
        earliest_msg_time = data.get('msg_time')
        if not earliest_msg_time:
            raise GNException(CODENAME.MSG_TIME_NOT_SPECIFIED)

        message_list = MessageModel.query.filter_by(group_id=0).filter(
            MessageModel.send_time < datetime.fromtimestamp(earliest_msg_time)
        ).order_by(text("-send_time")).limit(count).all()

    print("Message list length: {}".format(len(message_list)))
    return encrypt(message_list)
