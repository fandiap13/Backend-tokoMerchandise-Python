import datetime
from flask import make_response, request, session
import jwt
from app import app
from Model.UserModel import UserModel
from Middleware.Middleware import jwt_token

User = UserModel()


@app.route('/cek_login', methods=['POST'])
def login():
    try:
        email = request.form['email']
        password = request.form['password']
    except:
        return make_response({
            "code": 400,
            "status": "BAD_REQUEST",
            "error": "Field yang anda masukkan tidak sesuai (field = email, password) !"
        }, 400)

    cek_data = User.cek_login(email, password)
    if (cek_data):
        token = jwt.encode({'public_id': cek_data['id'], 'exp': datetime.datetime.utcnow(
        ) + datetime.timedelta(minutes=60)}, app.config['SECRET_KEY'], "HS256")
        return make_response({
            "code": 200,
            "status": "Ok",
            "message": "Login berhasil", "token": token
        }, 200)
    else:
        return make_response({
            "code": 403,
            "status": "FORBIDDEN",
            "error": "Email / password anda salah"
        }, 403)


@app.route('/data_user', methods=['get'])
@jwt_token
def data_user(current_user):
    return User.data_user()


@app.route('/detail_user/<id>', methods=['get'])
@jwt_token
def detail_user(current_user, id):
    return User.detail_user(id)


@app.route('/tambah_user', methods=['post'])
@jwt_token
def tambah_user(current_user):
    try:
        email = request.form['email']
        nama = request.form['nama']
        password = request.form['password']
    except:
        return make_response({"code": 400,
                              "status": "BAD_REQUEST",
                              "error": "Field yang anda masukkan tidak sesuai (field = email, password) !"
                              }, 400)

    return User.tambah_user(email, nama, password)


@app.route('/ubah_user/<id>', methods=['put'])
@jwt_token
def ubah_user(current_user, id):
    try:
        email = request.form['email']
        nama = request.form['nama']
        password = request.form['password']
    except:
        return make_response({
            "code": 400,
            "status": "BAD_REQUEST",
            "error": "Field yang anda masukkan tidak sesuai (field = email, password) !"}, 400)

    return User.ubah_user(email, nama, password, id)


@app.route('/hapus_user/<id>', methods=['delete'])
@jwt_token
def hapus_user(current_user, id):
    return User.hapus_user(id)

# @app.route('/logout', methods=['get'])
# def logout():
#   session.pop('auth', None)
#   return make_response({"message": "Logout berhasil"}, 200)
