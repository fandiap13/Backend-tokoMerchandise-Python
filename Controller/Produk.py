from datetime import datetime
import os
from flask import make_response, request
from app import app
from Model.ProdukModel import ProdukModel
from Middleware.Middleware import jwt_token

Produk = ProdukModel()


@app.route('/produk', methods=['GET'])
@jwt_token
def daftar_produk(current_user):
    return Produk.daftar_produk_model()


@app.route('/produk/limit/<limit>/page/<page>', methods=['GET'])
@jwt_token
def pagination_produk(current_user, limit="5", page="1"):
    return Produk.pagination_produk(limit, page)


@app.route('/produk/<id>', methods=['get'])
@jwt_token
def detail_produk(current_user, id):
    return Produk.detail_produk(id=id)


@app.route('/cari-produk', methods=['post'])
@jwt_token
def cari_produk(current_user):
    try:
        keyword = request.form['keyword']
    except:
        return make_response({
            "code": 400,
            "status": "BAD_REQUEST",
            "error": "Field yang anda masukkan tidak sesuai !"}, 400)

    return Produk.cari_produk(keyword=keyword)


@app.route('/produk', methods=['post'])
@jwt_token
def tambah_produk(current_user):
    try:
        nama_produk = request.form['nama_produk']
        id_kategori = request.form['id_kategori']
        id_satuan = request.form['id_satuan']
        harga_produk = request.form['harga_produk']
        harga_jual = request.form['harga_jual']
        berat_produk = request.form['berat_produk']
        stok = request.form['stok']
        deskripsi_produk = request.form['deskripsi_produk']
    except:
        return make_response({
            "code": 400,
            "status": "BAD_REQUEST",
            "error": "Field yang anda masukkan tidak sesuai !"}, 400)

    return Produk.tambah_produk(nama_produk, id_kategori, id_satuan, harga_produk, harga_jual, berat_produk, stok, deskripsi_produk)


@app.route('/produk/<id>', methods=['put'])
@jwt_token
def ubah_produk(current_user, id):
    try:
        nama_produk = request.form['nama_produk']
        id_kategori = request.form['id_kategori']
        id_satuan = request.form['id_satuan']
        harga_produk = request.form['harga_produk']
        harga_jual = request.form['harga_jual']
        berat_produk = request.form['berat_produk']
        stok = request.form['stok']
        deskripsi_produk = request.form['deskripsi_produk']
    except:
        return make_response({
            "code": 400,
            "status": "BAD_REQUEST",
            "error": "Field yang anda masukkan tidak sesuai !"}, 400)

    return Produk.ubah_produk(nama_produk, id_kategori, id_satuan, harga_produk, harga_jual, berat_produk, stok, deskripsi_produk, id)


@app.route('/produk/<id>', methods=['delete'])
@jwt_token
def hapus_produk(current_user, id):
    return Produk.hapus_produk(id)


@app.route('/produk/<id>', methods=['patch'])
@jwt_token
def ubah_produk_2(current_user, id):
    return Produk.ubah_produk_2(id, request.form)


@app.route('/produk/upload/<id>', methods=['PUT'])
@jwt_token
def upload_gambar(current_user, id):
    if not Produk.cek_produk(id):
        return make_response({
            "code": 404,
            "status": "NOT_FOUND",
            'error': f'Produk dengan ID {id} tidak ditemukan'}, 404)

    try:
        file = request.files['gambar_produk']
    except:
        return make_response({
            "code": 400,
            "status": "BAD_REQUEST",
            "error": "Field yang anda masukkan tidak sesuai !"}, 400)

    # jika gambar kosong
    if not file:
        return make_response({
            "code": 400,
            "status": "BAD_REQUEST",
            "error": "Gambar tidak boleh kosong"}, 400)

    # replace = mengganti . menjadi spasi
    uniqueFileName = str(datetime.now().timestamp()).replace(".", "")
    # fungsi split macam explode di php
    fileNameSplit = file.filename.split(".")
    # mengambil ekstensi gambar
    extensi = fileNameSplit[len(fileNameSplit)-1]
    extensi = str(extensi.lower())

    if (extensi not in ["png", "jpeg", "jpg"]):
        return make_response({
            "code": 400,
            "status": "BAD_REQUEST",
            "error": "Gambar harus png/jpg/jpeg"}, 400)

    cek_gambar = Produk.cek_produk(id)
    if cek_gambar and cek_gambar['gambar_produk'] is not None and cek_gambar['gambar_produk'] != "":
        file_path = cek_gambar['gambar_produk']
        try:
            os.unlink(os.path.join(file_path))
        except:
            return make_response({
                "code": 500,
                "status": "INTERNAL_SERVER_ERROR",
                "error": "Error removing file"}, 500)

    # upload gambar ke database
    fileImageUpload = f"Uploads/Images/{uniqueFileName}.{extensi}"
    if (Produk.upload_gambar(id, fileImageUpload)):
        # save images ke repository
        file.save(fileImageUpload)
        return make_response({
            "code": 201,
            "status": "CREATED",
            "message": "Upload gambar produk berhasil"}, 201)
    else:
        return make_response({
            "code": 500,
            "status": "INTERNAL_SERVER_ERROR",
            "message": "Terdapat kesalahan sistem saat mengupload gambar"}, 500)
