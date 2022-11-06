from flask import make_response
import mariadb
from Config.config import dbconfig


class KategoriModel:
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

    def data_kategori(self):
        try:
            self.cur.execute(
                'SELECT * FROM tbl_kategori ORDER BY kategori ASC')
            result = self.cur.fetchall()
            if result:
                response = make_response({
                    'code': 200,
                    'status': 'OK',
                    'data': result
                }, 200)
                return response
            else:
                return make_response({
                    'code': 404,
                    'status': 'NOT_FOUND',
                    'message': 'Data kategori kosong'}, 404)
        except:
            return make_response({
                "code": 500,
                "status": "INTERNAL_SERVER_ERROR",
                "error": "Terdapat kesalahan sistem saat mengambil data"}, 500)

    def cek_kategori(self, id):
        self.cur.execute(f"SELECT * FROM tbl_kategori WHERE id='{id}'")
        result = self.cur.fetchone()
        return result

    def tambah_kategori(self, data):
        try:
            self.cur.execute(
                f"INSERT INTO tbl_kategori (`kategori`) VALUES ('{data['kategori']}')")
            if self.cur.rowcount > 0:
                self.conn.commit()
                return make_response({
                    "code": 201,
                    "status": "CREATED",
                    "message": "Tambah kategori berhasil"}, 201)
            else:
                return make_response({
                    "code": 202,
                    "status": "ACCEPTED",
                    "message": "Tidak ada data yang ditambahkan"}, 202)
        except mariadb.Error as e:
            return make_response({
                "code": 500,
                "status": "INTERNAL_SERVER_ERROR",
                "error": "Terdapat kesalahan sistem saat menambahkan data"}, 500)

    def ubah_kategori(self, id, data):
        cek_kategori = self.cek_kategori(id)
        if not cek_kategori:
            return make_response({
                "code": 404,
                "status": "NOT_FOUND",
                'error': f'Data kategori dengan ID {id} tidak ditemukan'}, 404)

        try:
            self.cur.execute(
                f"UPDATE tbl_kategori SET kategori='{data['kategori']}' WHERE id='{id}'")
            if self.cur.rowcount > 0:
                self.conn.commit()
                return make_response({
                    "code": 202,
                    "status": "ACCEPTED",
                    "message": "Ubah kategori berhasil"}, 202)
            else:
                return make_response({
                    "code": 202,
                    "status": "ACCEPTED",
                    "message": "Tidak ada yang diubah"}, 202)
        except mariadb.Error as e:
            return make_response({
                "code": 500,
                "status": "INTERNAL_SERVER_ERROR",
                "error": "Data kategori gagal diubah"}, 500)

    def hapus_kategori(self, id):
        cek_kategori = self.cek_kategori(id)
        if not cek_kategori:
            return make_response({
                "code": 404,
                "status": "NOT_FOUND",
                'error': f'Data kategori dengan ID {id} tidak ditemukan'}, 404)

        try:
            self.cur.execute(f"DELETE FROM tbl_kategori WHERE id='{id}'")
            self.conn.commit()
            return make_response({
                "code": 200,
                "status": "OK",
                'message': f'Kategori dengan id {id} berhasil dihapus'}, 200)
        except mariadb.Error as e:
            return make_response({
                "code": 409,
                "status": "CONFLICT",
                "error": f"Kategori dengan id {id} tidak dapat dihapus"}, 409)
