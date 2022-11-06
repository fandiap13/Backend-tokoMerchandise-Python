import re
from flask import make_response
import mariadb
from Config.config import dbconfig


class PelangganModel:
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

    def daftar_pelanggan(self):
        try:
            self.cur.execute(f"SELECT * FROM tbl_pelanggan")
            result = self.cur.fetchall()
            if result:
                return make_response({
                    "code": 200,
                    "status": "OK",
                    'data': result
                }, 200)
            else:
                return make_response({
                    "code": 204,
                    "status": "NO_CONTENT",
                    "message": "Data pelanggan kosong"}, 204)
        except:
            return make_response({
                "code": 500,
                "status": "INTERNAL_SERVER_ERROR",
                'error': 'Terdapat kesalahan sistem saaat mengambil data'}, 500)

    def detail_pelanggan(self, id):
        try:
            self.cur.execute(f"SELECT * FROM tbl_pelanggan WHERE id='{id}'")
            result = self.cur.fetchone()
            if result:
                return make_response({
                    "code": 200,
                    "status": "OK",
                    'data': result
                }, 200)
            else:
                return make_response({
                    "code": 404,
                    "status": "NOT_FOUND",
                    "error": f"Pelanggan dengan ID {id} tidak ditemukan"}, 404)
        except:
            return make_response({
                "code": 500,
                "status": "INTERNAL_SERVER_EROR",
                'error': 'Terdapat kesalahan sistem saat mengambil data'}, 500)

    def tambah_pelanggan(self, nama_pelanggan, alamat, no_telp, email):
        if email or email != "":
            if not re.match(f"[^@]+@[^@]+\.[^@]+", email):
                errorEmail = "Email yang anda masukkan tidak valid"
        else:
            email = None

        if nama_pelanggan is None or nama_pelanggan == "":
            errorNama = "Nama pelanggan user tidak boleh kosong"
        else:
            self.cur.execute(
                f"SELECT * FROM tbl_pelanggan WHERE nama_pelanggan = '{nama_pelanggan}'")
            cek_pelanggan = self.cur.fetchone()
            if cek_pelanggan:
                errorNama = f"Nama {nama_pelanggan} sudah digunakan"

        if alamat is None or alamat == "":
            alamat = None

        if no_telp or no_telp != "":
            if not no_telp.isnumeric():
                errorNoTelp = "No telp harus angka"
        else:
            no_telp = None

        if 'errorEmail' in locals() or 'errorNama' in locals() or 'errorNoTelp' in locals():
            return make_response({
                "code": 400,
                "status": "BAD_REQUEST",
                'errors': {
                    'email': errorEmail if 'errorEmail' in locals() else "",
                    'no_telp': errorNoTelp if 'errorNoTelp' in locals() else "",
                    'nama_pelanggan': errorNama if 'errorNama' in locals() else "",
                }}, 400)
        else:
            try:
                self.cur.execute(f"INSERT INTO `tbl_pelanggan` (`nama_pelanggan`, `alamat`, `no_telp`, `email`) VALUES (%s, %s, %s, %s)",
                                 (nama_pelanggan, alamat, no_telp, email))
                return make_response({
                    "code": 201,
                    "status": "CREATED",
                    'message': 'Tambah pelanggan berhasil'}, 201)
            except mariadb.Error as e:
                return make_response({
                    "code": 500,
                    "status": "INTERNAL_SERVER_ERROR",
                    'error': f'Terdapat kesalahan sistem saat menambahkan data'}, 500)

    def ubah_pelanggan(self, id, nama_pelanggan, alamat, no_telp, email):
        self.cur.execute(f"SELECT * FROM tbl_pelanggan WHERE id='{id}'")
        cek_pelanggan = self.cur.fetchone()
        if not cek_pelanggan:
            return make_response({
                "code": 404,
                "status": "NOT_FOUND",
                "error": f"Pelanggan dengan ID {id} tidak ditemukan"}, 404)

        if email or email != "":
            if not re.match(f"[^@]+@[^@]+\.[^@]+", email):
                errorEmail = "Email yang anda masukkan tidak valid"
        else:
            email = None

        if nama_pelanggan is None or nama_pelanggan == "":
            errorNama = "Nama pelanggan user tidak boleh kosong"
        else:
            if cek_pelanggan['nama_pelanggan'] != nama_pelanggan:
                self.cur.execute(
                    f"SELECT * FROM tbl_pelanggan WHERE nama_pelanggan = '{nama_pelanggan}'")
                cek_pelanggan = self.cur.fetchone()
                if cek_pelanggan:
                    errorNama = f"Nama {nama_pelanggan} sudah digunakan"

        if alamat is None or alamat == "":
            alamat = None

        if no_telp or no_telp != "":
            if not no_telp.isnumeric():
                errorNoTelp = "No telp harus angka"
        else:
            no_telp = None

        if 'errorEmail' in locals() or 'errorNama' in locals() or 'errorNoTelp' in locals():
            return make_response({
                "code": 400,
                "status": "BAD_REQUEST",
                'errors': {
                    'email': errorEmail if 'errorEmail' in locals() else "",
                    'no_telp': errorNoTelp if 'errorNoTelp' in locals() else "",
                    'nama_pelanggan': errorNama if 'errorNama' in locals() else "",
                }}, 400)
        else:
            try:
                self.cur.execute(f"UPDATE tbl_pelanggan SET nama_pelanggan=?,  alamat=?, no_telp=?, email=? WHERE id='{id}'",
                                 (nama_pelanggan, alamat, no_telp, email))
                return make_response({
                    "code": 202,
                    "status": "ACCEPTED",
                    'message': 'Update pelanggan berhasil'}, 202)
            except mariadb.Error as e:
                return make_response({
                    "code": 500,
                    "status": "INTERNAL_SERVER_ERROR",
                    'error': f'Terdapat kesalahan sistem saat mengubah data'}, 500)

    def hapus_pelanggan(self, id):
        self.cur.execute(f"SELECT * FROM tbl_pelanggan WHERE id = '{id}'")
        cek_pelanggan = self.cur.fetchone()
        if not cek_pelanggan:
            return make_response({
                "code": 404,
                "status": "NOT_FOUND",
                'error': 'Data pelanggan tidak ditemukan'}, 404)

        try:
            self.cur.execute(f"DELETE FROM tbl_pelanggan WHERE id='{id}'")
            self.conn.commit()
            return make_response({
                "code": 200,
                "status": "OK",
                'message': f"Pelanggan dengan ID {id} berhasil dihapus"})
        except mariadb.Error as e:
            return make_response({
                "code": 409,
                "status": "CONFLICT",
                "error": f"Pelanggan dengan ID {id} tidak dapat dihapus"}, 409)
