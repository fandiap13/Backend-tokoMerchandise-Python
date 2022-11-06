from flask import make_response, request
from app import app
from Model.KategoriModel import KategoriModel
from Middleware.Middleware import jwt_token

Kategori = KategoriModel()


@app.route('/kategori', methods=['get'])
@jwt_token
def data_kategori(current_user):
    return Kategori.data_kategori()


@app.route('/kategori', methods=['post'])
@jwt_token
def tambah_kategori(current_user):
    try:
        kategori = request.form['kategori']
    except:
        return make_response({
            "code": 400,
            "status": "BAD_REQUEST",
            'error': 'Kategori tidak boleh kosong'
        }, 400)

    if kategori:
        return Kategori.tambah_kategori(request.form)
    else:
        return make_response({
            "code": 400,
            "status": "BAD_REQUEST",
            "error": "Kategori tidak boleh kosong"
        }, 400)


@app.route('/kategori/<id>', methods=['put'])
@jwt_token
def ubah_kategori(current_user, id):
    try:
        kategori = request.form['kategori']
    except:
        return make_response({
            "code": 400,
            "status": "BAD_REQUEST",
            'error': 'Kategori tidak boleh kosong'}, 400)

    if kategori:
        return Kategori.ubah_kategori(id, request.form)
    else:
        return make_response({
            "code": 400,
            "status": "BAD_REQUEST",
            'error': 'Kategori tidak boleh kosong'}, 400)


@app.route('/kategori/<id>', methods=['delete'])
@jwt_token
def hapus_kategori(current_user, id):
    return Kategori.hapus_kategori(id)
