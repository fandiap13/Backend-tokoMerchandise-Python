from flask import make_response, request
from app import app
from Model.SatuanModel import SatuanModel
from Middleware.Middleware import jwt_token

Satuan = SatuanModel()


@app.route('/satuan', methods=['get'])
@jwt_token
def data_satuan(current_user):
    return Satuan.data_satuan()


@app.route('/satuan', methods=['post'])
@jwt_token
def tambah_satuan(current_user):
    try:
        satuan = request.form['satuan']
    except:
        return make_response({
            "code": 400,
            "status": "BAD_REQUEST",
            'error': 'satuan tidak boleh kosong'}, 400)

    if satuan:
        return Satuan.tambah_satuan(request.form)
    else:
        return make_response({
            "code": 400,
            "status": "BAD_REQUEST",
            "error": "satuan tidak boleh kosong"}, 400)


@app.route('/satuan/<id>', methods=['put'])
@jwt_token
def ubah_satuan(current_user, id):
    try:
        satuan = request.form['satuan']
    except:
        return make_response({
            "code": 400,
            "status": "BAD_REQUEST",
            'error': 'satuan tidak boleh kosong'}, 400)

    if satuan:
        return Satuan.ubah_satuan(id, request.form)
    else:
        return make_response({
            "code": 400,
            "status": "BAD_REQUEST",
            'error': 'satuan tidak boleh kosong'}, 400)


@app.route('/satuan/<id>', methods=['delete'])
@jwt_token
def hapus_satuan(current_user, id):
    return Satuan.hapus_satuan(id)
