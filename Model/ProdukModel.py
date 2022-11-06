import json
import math
import os
from flask import make_response
import mariadb
from Config.config import dbconfig


class ProdukModel():
    conn = ""
    cur = ""

    def __init__(self):
        try:
            self.conn = mariadb.connect(
                user=dbconfig['user'],
                password=dbconfig['password'],
                host=dbconfig['host'],
                port=dbconfig['port'],
                database=dbconfig['database']
            )
            self.conn.autocommit = True
            self.cur = self.conn.cursor(dictionary=True)
        except:
            print("Terdapat error saat mengkoneksikan ke database")

    def daftar_produk_model(self):
        try:
            self.cur.execute('SELECT * FROM tbl_produk')
            result = self.cur.fetchall()
            # return f"{len(result)}"

            # self.cur.execute('SELECT * FROM tbl_produk')
            # self.cur.fetchall()
            # print(self.cur.rowcount)

            # return result[0]
            if len(result) > 0:
                response = make_response({
                    "code": 200,
                    "status": "OK",
                    "data": result
                }, 200)
                # return json.dumps(result)
                return response
            else:
                return make_response({
                    "code": 404,
                    "status": "NOT_FOUND",
                    'message': 'Data produk kosong'}, 404)
        except mariadb.Error as e:
            return make_response({
                "code": 500,
                "status": "INTERNAL_SERVER_ERROR",
                'error': "Terdapat kesalahan sistem saat mengambil data"}, 500)

    def cari_produk(self, keyword):
        self.cur.execute(
            f"SELECT * FROM tbl_produk INNER JOIN tbl_kategori ON tbl_produk.id_kategori = tbl_kategori.id WHERE nama_produk LIKE '%{keyword}%' OR kategori LIKE '%{keyword}%'")
        result = self.cur.fetchall()
        if result:
            response = make_response({
                "code": 200,
                "status": "OK",
                "data": result
            }, 200)
            return response
        else:
            return make_response({'message': 'Data produk kosong'}, 204)

    def pagination_produk(self, limit, page):
        self.cur.execute("SELECT count(*) as total FROM tbl_produk")
        size = self.cur.fetchone()['total']

        star = (int(page) * int(limit)) - int(limit)
        self.cur.execute(f'SELECT * FROM tbl_produk LIMIT {star}, {limit}')
        result = self.cur.fetchall()
        if result:
            response = make_response({
                "code": 200,
                "status": "OK",
                "data": result,
                "page": {
                    "size": size,
                    'totalElements': int(limit),
                    'totalPages': math.ceil(int(size) / int(limit)),
                    'current': int(page),
                }
            }, 200)
            return response
        else:
            return make_response({'error': 'Data tidak ditemukan'}, 404)

    def detail_produk(self, id):
        self.cur.execute(
            f'SELECT tbl_produk.id, id_kategori, id_satuan, nama_produk,kategori, satuan,deskripsi_produk, harga_produk, harga_jual, berat_produk, gambar_produk, stok FROM `tbl_produk` INNER JOIN tbl_kategori ON tbl_produk.id_kategori=tbl_kategori.id INNER JOIN tbl_satuan ON tbl_produk.id_satuan=tbl_satuan.id WHERE tbl_produk.id="{id}"')
        result = self.cur.fetchone()
        if result:
            response = make_response({
                "code": 200,
                "status": "OK",
                "data": result
            }, 200)
            return response
        else:
            return make_response({
                'code': 404,
                'status': 'NOT_FOUND',
                'error': f'Data produk dengan ID {id} tidak ditemukan'}, 404)

    def tambah_produk(self, nama_produk, id_kategori, id_satuan, harga_produk, harga_jual, berat_produk, stok, deskripsi_produk):
        if nama_produk is None or nama_produk == "":
            errorProduk = "Nama produk tidak boleh kosong"

        if id_kategori is None or id_kategori == "":
            errorKategori = "Kategori tidak boleh kosong"
        elif (not id_kategori.isnumeric()):
            errorKategori = "Kategori harus angka"

        if id_satuan is None or id_satuan == "":
            errorSatuan = "Satuan tidak boleh kosong"
        elif (not id_satuan.isnumeric()):
            errorSatuan = "Satuan harus angka"

        if harga_produk is None or harga_produk == "":
            errorHarga = "Harga produk tidak boleh kosong"
        elif (not harga_produk.isnumeric()):
            errorHarga = "Harga harus angka"

        if harga_jual is None or harga_jual == "":
            errorHargaJual = "Harga jual tidak boleh kosong"
        elif (not harga_jual.isnumeric()):
            errorHargaJual = "Harga jual harus angka"

        if berat_produk is None or berat_produk == "":
            errorBerat = "Berat produk tidak boleh kosong"
        elif (not berat_produk.isnumeric()):
            errorBerat = "Berat produk harus angka"

        if stok is None or stok == "":
            errorStok = "Stok produk tidak boleh kosong"
        elif (not stok.isnumeric()):
            errorStok = "Stok harus angka"

        if deskripsi_produk == "" or deskripsi_produk is None:
            deskripsi_produk = None

        if 'errorProduk' in locals() or 'errorKategori' in locals() or 'errorSatuan' in locals() or 'errorHarga' in locals() or 'errorHargaJual' in locals() or 'errorBerat' in locals() or 'errorStok' in locals():
            return make_response({
                "code": 400,
                "status": "BAD_REQUEST",
                'errors': {
                    'nama_produk': errorProduk if 'errorProduk' in locals() else "",
                    'id_kategori': errorKategori if 'errorKategori' in locals() else "",
                    'id_satuan': errorSatuan if 'errorSatuan' in locals() else "",
                    'harga_produk': errorHarga if 'errorHarga' in locals() else "",
                    'harga_jual': errorHargaJual if 'errorHargaJual' in locals() else "",
                    'berat_produk': errorBerat if 'errorBerat' in locals() else "",
                    'stok': errorStok if 'errorStok' in locals() else "",
                }}, 400)
        else:
            try:
                self.cur.execute(f"INSERT INTO `tbl_produk` (`nama_produk`, `id_kategori`, `id_satuan`, `deskripsi_produk`, `berat_produk`, `harga_produk`, `harga_jual`, `stok`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                                 (nama_produk, id_kategori, id_satuan, deskripsi_produk, berat_produk, harga_produk, harga_jual, stok))
                if self.cur.rowcount > 0:
                    self.conn.commit()
                    return make_response({
                        "code": 201,
                        "status": "CREATED",
                        "message": "Produk berhasil ditambahkan"}, 201)
                else:
                    return make_response({
                        "code": 202,
                        "status": "ACCEPTED",
                        "message": "Nothing To Add"}, 202)
            except mariadb.Error as e:
                return make_response({
                    "code": 500,
                    "status": "INTERNAL_SERVER_ERROR",
                    'error': 'Terdapat kesalahan sistem saat menambahkan data'
                }, 500)

    def ubah_produk(self, nama_produk, id_kategori, id_satuan, harga_produk, harga_jual, berat_produk, stok, deskripsi_produk, id):
        if not self.cek_produk(id):
            return make_response({
                "code": 404,
                "status": "NOT_FOUND",
                'error': f'Data produk dengan ID {id} tidak ditemukan'}, 404)

        if nama_produk is None or nama_produk == "":
            errorProduk = "Nama produk tidak boleh kosong"

        if id_kategori is None or id_kategori == "":
            errorKategori = "Kategori tidak boleh kosong"
        elif (not id_kategori.isnumeric()):
            errorKategori = "Kategori harus angka"

        if id_satuan is None or id_satuan == "":
            errorSatuan = "Satuan tidak boleh kosong"
        elif (not id_satuan.isnumeric()):
            errorSatuan = "Satuan harus angka"

        if harga_produk is None or harga_produk == "":
            errorHarga = "Harga produk tidak boleh kosong"
        elif (not harga_produk.isnumeric()):
            errorHarga = "Harga harus angka"

        if harga_jual is None or harga_jual == "":
            errorHargaJual = "Harga jual tidak boleh kosong"
        elif (not harga_jual.isnumeric()):
            errorHargaJual = "Harga jual harus angka"

        if berat_produk is None or berat_produk == "":
            errorBerat = "Berat produk tidak boleh kosong"
        elif (not berat_produk.isnumeric()):
            errorBerat = "Berat produk harus angka"

        if stok is None or stok == "":
            errorStok = "Stok produk tidak boleh kosong"
        elif (not stok.isnumeric()):
            errorStok = "Stok harus angka"

        if deskripsi_produk == "" or deskripsi_produk is None:
            deskripsi_produk = None

        if 'errorProduk' in locals() or 'errorKategori' in locals() or 'errorSatuan' in locals() or 'errorHarga' in locals() or 'errorHargaJual' in locals() or 'errorBerat' in locals() or 'errorStok' in locals():
            return make_response({
                "code": 400,
                "status": "BAD_REQUEST",
                'errors': {
                    'nama_produk': errorProduk if 'errorProduk' in locals() else "",
                    'id_kategori': errorKategori if 'errorKategori' in locals() else "",
                    'id_satuan': errorSatuan if 'errorSatuan' in locals() else "",
                    'harga_produk': errorHarga if 'errorHarga' in locals() else "",
                    'harga_jual': errorHargaJual if 'errorHargaJual' in locals() else "",
                    'berat_produk': errorBerat if 'errorBerat' in locals() else "",
                    'stok': errorStok if 'errorStok' in locals() else "",
                }}, 400)
        else:
            try:
                self.cur.execute(f"UPDATE `tbl_produk` SET `nama_produk` = ?, `id_kategori` = ?, `id_satuan` = ?, `deskripsi_produk` = ?, `berat_produk` = ?, `harga_produk` = ?, `harga_jual` = ?, `stok` = ? WHERE `tbl_produk`.`id` = ?",
                                 (nama_produk, id_kategori, id_satuan, deskripsi_produk, berat_produk, harga_produk, harga_jual, stok, id))
                if self.cur.rowcount > 0:
                    self.conn.commit()
                    return make_response({
                        "code": 202,
                        "status": "ACCEPTED",
                        "message": "Produk berhasil diubah"}, 202)
                else:
                    return make_response({
                        "code": 202,
                        "status": "ACCEPTED",
                        "message": "Nothing To Update"}, 202)
            except mariadb.Error as e:
                print(f"Error: {e}")

    def ubah_produk_2(self, id, data):
        if not self.cek_produk(id):
            return make_response({
                "code": 404,
                "status": "NOT_FOUND",
                'message': f'Produk dengan ID {id} tidak ditemukan'}, 404)

        query = 'UPDATE tbl_produk SET '
        for key in data:
            query += f"{key}='{data[key]}',"

        # query = query[:-1]  # meghilangkan karakter terakhir
        query = query[:-1] + f" WHERE id={id}"
        try:
            self.cur.execute(query)
            self.conn.commit()
            return make_response({
                "code": 202,
                "status": "ACCEPTED",
                "message": "Produk berhasil diubah"}, 202)
        except mariadb.Error as e:
            return make_response({
                "code": 500,
                "status": "INTERNAL_SERVER_ERROR",
                'error': 'Terdapat kesalahan sistem saat mengubah data'
            }, 500)

    def hapus_produk(self, id):
        try:
            cek_gambar = self.cek_produk(id)
            if not cek_gambar:
                return make_response({
                    "code": 404,
                    "status": "NOT_FOUND",
                    'message': f'Produk dengan ID {id} tidak ditemukan'}, 404)

            if cek_gambar and cek_gambar['gambar_produk'] is not None and cek_gambar['gambar_produk'] != "":
                file_path = cek_gambar['gambar_produk']
                os.unlink(os.path.join(file_path))

            self.cur.execute(f"DELETE FROM tbl_produk WHERE id={id}")
            self.conn.commit()
            return make_response({
                "code": 200,
                "status": "OK",
                "message": f"Produk dengan ID {id} berhasil dihapus"}, 200)
        except mariadb.Error as e:
            return make_response({
                "code": 409,
                "status": "CONFLICT",
                "error": f"Produk dengan ID {id} tidak dapat dihapus"}, 409)

    def cek_produk(self, id):
        self.cur.execute(f"SELECT * FROM tbl_produk WHERE id={id}")
        return self.cur.fetchone()

    def upload_gambar(self, id, fileImageUpload):
        try:
            self.cur.execute(
                f"UPDATE tbl_produk SET gambar_produk='{fileImageUpload}' WHERE id={id}")
            self.conn.commit()
            return True
        except mariadb.Error as e:
            return False

    def cek_stok(self, produkid, jml):
        self.cur.execute(
            f"SELECT * FROM tbl_produk WHERE id='{produkid}' AND stok >= '{jml}'")
        return self.cur.fetchone()
