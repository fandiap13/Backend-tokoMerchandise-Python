from flask import make_response, request
from app import app
from Middleware.Middleware import jwt_token
from Model.PelangganModel import PelangganModel

Pelanggan = PelangganModel()


@app.route('/daftar-pelanggan', methods=['get'])
@jwt_token
def daftar_pelanggan(current_user):
    return Pelanggan.daftar_pelanggan()


@app.route('/detail-pelanggan/<id>', methods=['get'])
@jwt_token
def detail_pelanggan(current_user, id):
    return Pelanggan.detail_pelanggan(id)


@app.route('/tambah-pelanggan', methods=['post'])
@jwt_token
def tambah_pelanggan(current_user):
    try:
        nama_pelanggan = request.form['nama_pelanggan']
        alamat = request.form['alamat']
        notelp = request.form['notelp']
        email = request.form['email']

    except:
        return make_response({
            "code": 400,
            "status": "BAD_REQUEST",
            "error": "Field yang anda masukkan tidak sesuai (field = nama_pelanggan, alamat, notelp, email) !"}, 400)

    return Pelanggan.tambah_pelanggan(nama_pelanggan, alamat, notelp, email)


@app.route('/ubah-pelanggan/<id>', methods=['put'])
@jwt_token
def ubah_pelanggan(current_user, id):
    try:
        nama_pelanggan = request.form['nama_pelanggan']
        alamat = request.form['alamat']
        notelp = request.form['notelp']
        email = request.form['email']

    except:
        return make_response({
            "code": 400,
            "status": "BAD_REQUEST",
            "error": "Field yang anda masukkan tidak sesuai (field = nama_pelanggan, alamat, notelp, email) !"}, 400)

    return Pelanggan.ubah_pelanggan(id, nama_pelanggan, alamat, notelp, email)


@app.route('/hapus-pelanggan/<id>', methods=['delete'])
@jwt_token
def hapus_pelanggan(current_user, id):
    return Pelanggan.hapus_pelanggan(id)
