from functools import wraps
import jwt
from flask import make_response, request
import mariadb
from app import app
from Config.config import dbconfig


def jwt_token(func):
    @wraps(func)
    def after(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return make_response({
                "code": 404,
                "status": "NOT_FOUND",
                'error': 'Token tidak ditemukan'}, 404)

        try:
            data = jwt.decode(
                token, app.config['SECRET_KEY'], algorithms=["HS256"])
            conn = mariadb.connect(
                user=dbconfig['user'],
                password=dbconfig['password'],
                host=dbconfig['host'],
                port=dbconfig['port'],
                database=dbconfig['database']
            )
            conn.autocommit = True
            cur = conn.cursor(dictionary=True)
            cur.execute(
                f"SELECT * FROM tbl_user WHERE id = '{data['public_id']}'")
            current_user = cur.fetchone()
            conn.commit()

            if not current_user:
                return make_response({
                    "code": 404,
                    "status": "NOT_FOUND",
                    'error': 'User tidak ditemukan'}, 404)

        except:
            return make_response({
                "code": 403,
                "status": "FORBIDDEN",
                'error': 'Token tidak valid'}, 403)

        return func(current_user, *args, **kwargs)

    # after.__name__ = func.__name__
    return after
