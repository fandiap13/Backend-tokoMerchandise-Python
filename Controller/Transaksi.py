from flask import make_response, request
from app import app
from Model.TransaksiModel import TransaksiModel
from Model.TempTransaksiModel import TempTransaksiModel
from Middleware.Middleware import jwt_token
import datetime

TempTransaksi = TempTransaksiModel()
Transaksi = TransaksiModel()


@app.route('/get_invoice/<tanggal>', methods=['get'])
@jwt_token
def get_no_invoice(current_user, tanggal):
    try:
        datetime.datetime.strptime(tanggal, '%Y-%m-%d')
    except ValueError:
        return make_response({
            "code": 400,
            "status": "BAD_REQUEST",
            'error': 'Enter a date formatted as YYYY-MM-DD !'}, 400)

    return make_response({
        "code": 200,
        "status": "OK",
        "no_invoice": Transaksi.get_invoice(tanggal)
    }, 200)


@app.route('/tambah_temp', methods=['post'])
@jwt_token
def tambah_temp(current_user):
    try:
        tanggal = request.form['tanggal']
        produkid = request.form['produkid']
        jml = request.form['jml']
        catatan = request.form['catatan']
        biaya_tambahan = request.form['biaya_tambahan']
    except:
        return make_response({
            "code": 400,
            "status": "BAD_REQUEST",
            "error": "Field yang anda masukkan tidak sesuai (tanggal, produkid, jml, catatan, biaya_tambahan) !"}, 400)

    return TempTransaksi.tambah_temp(tanggal, produkid, jml, biaya_tambahan, catatan)


@app.route('/daftar_temp/<transaksiid>', methods=['get'])
@jwt_token
def daftar_temp(current_user, transaksiid):
    return TempTransaksi.daftar_temp(transaksiid)


@app.route('/hapus_temp/<id>', methods=['delete'])
@jwt_token
def hapus_temp(current_user, id):
    return TempTransaksi.hapus_temp(id)


@app.route('/hapus_semua_temp/<transaksiid>', methods=['delete'])
@jwt_token
def hapus_semua_temp(current_user, transaksiid):
    return TempTransaksi.hapus_semua_temp(transaksiid)


@app.route('/simpan_transaksi', methods=['post'])
@jwt_token
def simpan_transaksi(current_user):
    try:
        userid = current_user['id']
        tgl_transaksi = request.form['tgl_transaksi']
        pelangganid = request.form['pelangganid']
        dibayar = request.form['dibayar']

    except:
        return make_response({
            "code": 400,
            "status": "BAD_REQUEST",
            "error": "Field yang anda masukkan tidak sesuai (tgl_transaksi, pelanggan, dibayar) !"}, 400)

    return Transaksi.simpan_transaksi(userid, tgl_transaksi, pelangganid, dibayar)


@app.route('/daftar-transaksi', methods=['get'])
@jwt_token
def daftar_transaksi(current_user):
    return Transaksi.daftar_transaksi()


@app.route('/detail-transaksi/<transaksiid>', methods=['get'])
@jwt_token
def detail_transaksi(current_user, transaksiid):
    return Transaksi.detail_transaksi(transaksiid)
