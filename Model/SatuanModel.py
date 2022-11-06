from flask import make_response
import mariadb
from Config.config import dbconfig


class SatuanModel:
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

    def data_satuan(self):
        self.cur.execute('SELECT * FROM tbl_satuan ORDER BY satuan ASC')
        result = self.cur.fetchall()
        if result:
            response = make_response({
                "code": 200,
                "status": "OK",
                'data': result
            }, 200)
            return response
        else:
            return make_response({
                "code": 404,
                "status": "NOT_FOUND",
                'message': 'Data satuan kosong'}, 404)

    def cek_satuan(self, id):
        self.cur.execute(f"SELECT * FROM tbl_satuan WHERE id='{id}'")
        result = self.cur.fetchone()
        return result

    def tambah_satuan(self, data):
        try:
            self.cur.execute(
                f"INSERT INTO tbl_satuan (`satuan`) VALUES ('{data['satuan']}')")
            if self.cur.rowcount > 0:
                self.conn.commit()
                return make_response({
                    "code": 201,
                    "status": "CREATED",
                    "message": "Tambah satuan berhasil"}, 201)
            else:
                return make_response({
                    "code": 202,
                    "status": "ACCEPTED",
                    "message": "Nothing To Add"}, 202)
        except mariadb.Error as e:
            return make_response({
                "code": 500,
                "status": "INTERNAL_SERVER_ERROR",
                "message": "Terdapat kesalahan sistem saat menambahkan data"}, 500)

    def ubah_satuan(self, id, data):
        cek_satuan = self.cek_satuan(id)
        if not cek_satuan:
            return make_response({
                "code": 404,
                "status": "NOT_FOUND",
                'error': 'Data tidak ditemukan'}, 404)

        try:
            self.cur.execute(
                f"UPDATE tbl_satuan SET satuan='{data['satuan']}' WHERE id='{id}'")
            if self.cur.rowcount > 0:
                self.conn.commit()
                return make_response({
                    "code": 202,
                    "status": "ACCEPTED",
                    "message": "Ubah satuan berhasil"}, 202)
            else:
                return make_response({
                    "code": 202,
                    "status": "ACCEPTED",
                    "message": "Nothing To Update"}, 202)
        except mariadb.Error as e:
            return make_response({
                "code": 500,
                "status": "INTERNAL SERVER ERROR",
                "message": "Terdapat kesalahan sistem saat mengubah data"}, 500)

    def hapus_satuan(self, id):
        cek_satuan = self.cek_satuan(id)
        if not cek_satuan:
            return make_response({
                "code": 404,
                "status": "NOT_FOUND",
                'error': 'Data tidak ditemukan'}, 404)

        try:
            self.cur.execute(f"DELETE FROM tbl_satuan WHERE id='{id}'")
            self.conn.commit()
            return make_response({'message': f'satuan dengan id {id} berhasil dihapus'})
        except mariadb.Error as e:
            return make_response(
                {
                    "code": 409,
                    "status": "CONFLICT",
                    "error": f"satuan dengan id {id} tidak dapat dihapus"}, 409)
