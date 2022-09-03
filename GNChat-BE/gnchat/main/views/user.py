import json

from gnchat.utils.gnexcept import GNException
from gnchat.main.blueprint import main_blueprint
from gnchat.orm.main import UserModel

from flask import request

from gnchat.utils.response import CODENAME
from gnchat.utils.wrapper import response_wraps
from gnchat.utils.uuid_utils import get_uuid


@main_blueprint.route('/register', methods=['POST'])
@response_wraps
def register_user():
    data = json.loads(request.data.decode('utf-8'))
    username = data.get('username', None)
    password = data.get('password', None)
    if not username or not password:
        raise GNException(CODENAME.BAD_REQUEST)

    res = UserModel.query.filter_by(username=username).first()
    if res is not None:
        raise GNException(CODENAME.USERNAME_EXISTS)

    user_uuid = get_uuid()

    UserModel.insert_item(
        UserModel(
            user_uuid=user_uuid,
            username=username,
            password=password,
        )
    )

    return {"user_uuid": user_uuid}


@main_blueprint.route('/login', methods=['POST'])
@response_wraps
def login_user():
    data = json.loads(request.data.decode('utf-8'))
    username = data.get('username', None)
    password = data.get('password', None)
    if not username:
        raise GNException(CODENAME.BAD_REQUEST)
    res = UserModel.query.filter_by(username=username).first()

    # TODO make a register&login check
    if res is None:
        res = UserModel(
            user_uuid=get_uuid(),
            username=username,
            password="123456",
        )
        UserModel.insert_item(res)
    return res
