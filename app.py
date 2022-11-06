from datetime import timedelta
from flask import *
from flask_cors import CORS, cross_origin
# from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, get_jwt_identity, jwt_required, set_access_cookies, unset_jwt_cookies

app = Flask(__name__)

# CROS
cors = CORS(app)
app.config['CORS_HEADERS'] = 'application/json'  # Content-Type

# session
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
# app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=60)
# agar output json tidak auto urut
app.config['JSON_SORT_KEYS'] = False
app.config['DEBUG'] = True

# JWT
# app.config["JWT_COOKIE_SECURE"] = False
# app.config["JWT_TOKEN_LOCATION"] = ["cookies"]

# app.config["JWT_SECRET_KEY"] = "super-secret"
# app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
# app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
# jwt = JWTManager(app)

@app.route('/', methods=['GET'])
# @cross_origin()
def home():
    return make_response({
        "code": 200,
        "status": "OK",
        'message': 'Selamat datang di api api'}, 200)

# menagkap file gambar menggunakan url
@app.route('/Uploads/Images/<filename>', methods=['get'])
def ambil_gambar(filename):
    return send_file(f"Uploads/Images/{filename}")

# @app.route('/testing-token', methods=['get'])
# def testing():
#     access_token = create_access_token(identity="john")
#     refresh_token = create_refresh_token(identity="john")
#     return {
#             'access_token': access_token,
#             'refresh_token': refresh_token
#     }, 200    
    
# @app.route('/refresh-token/', methods=['get'])
# @jwt_required(refresh=True)
# def testing_refresh():
#     identity = get_jwt_identity()
#     # access_token = create_access_token(identity=identity, fresh=True)
#     access_token = create_access_token(identity=identity)
#     return jsonify(access_token=access_token)

# @app.route("/protected", methods=['get'])
# @jwt_required()
# def protected():
#     return jsonify(foo="bar")

# @app.route('/remove', methods=['get'])
# @jwt_required()
# def remove():
#     resp = jsonify({'logout': True})
#     unset_jwt_cookies(resp)
#     return resp, 200

try:
    from Controller import *
except Exception as e:
    print(e)
