from flask import make_response
import mariadb
from Config.config import dbconfig


class UserModel:
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
            print("Terdapat error saat mengkoneksikan database")

    def data_user(self):
        try:
            self.cur.execute('SELECT * FROM tbl_user ORDER BY email ASC')
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
                    "code": 204,
                    "status": "NO_CONTENT",
                    'message': 'Data user kosong'}, 204)
        except mariadb.Error as e:
            return make_response({
                "code": 500,
                "status": "INTERNAL_SERVER_ERROR",
                'error': "Terdapat kesalahan sistem saat mengambil data"}, 500)

    def detail_user(self, id):
        try:
            self.cur.execute(f"SELECT * FROM tbl_user WHERE id='{id}'")
            result = self.cur.fetchone()
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
                    'error': f"User dengan id {id} tidak ditemukan"}, 404)
        except mariadb.Error as e:
            return make_response({
                "code": 500,
                "status": "INTERNAL_SERVER_ERROR",
                "error": "Terdapat kesalahan sistem saat mengambil data"}, 500)

    def cek_email(self, email):
        self.cur.execute(f"SELECT * FROM tbl_user WHERE email='{email}'")
        return self.cur.fetchone()

    def cek_user(self, id):
        self.cur.execute(f"SELECT * FROM tbl_user WHERE id='{id}'")
        return self.cur.fetchone()

    def tambah_user(self, email, nama, password):
        cek_email = self.cek_email(email)
        if cek_email:
            errorEmail = f"Email {email} sudah digunakan"

        if email is None or email == "":
            errorEmail = "Email user tidak boleh kosong"

        if nama is None or nama == "":
            errorNama = "Nama user tidak boleh kosong"
        if password is None or password == "":
            errorPassword = "Password user tidak boleh kosong"

        if 'errorEmail' in locals() or 'errorNama' in locals() or 'errorPassword' in locals():
            return make_response({
                "code": 400,
                "status": "BAD_REQUEST",
                'errors': {
                    'email': errorEmail if 'errorEmail' in locals() else "",
                    'nama': errorNama if 'errorNama' in locals() else "",
                    'password': errorPassword if 'errorPassword' in locals() else "",
                }}, 400)
        else:
            try:
                self.cur.execute(
                    f"INSERT INTO `tbl_user` (`email`, `password`, `nama`) VALUES ('{email}', '{password}', '{nama}')")
                self.conn.commit()
                return make_response({
                    "code": 201,
                    "status": "CREATED",
                    'message': 'Tambah user berhasil'}, 201)
            except:
                return make_response({
                    "code": 500,
                    "status": "INTERNAL_SERVER_ERROR",
                    'error': 'Terdapat kesalahan sistem saat menambahkan data'}, 500)

    def ubah_user(self, email, nama, password, id):
        cek_user = self.cek_user(id)
        if not cek_user:
            return make_response({
                "code": 404,
                "status": "NOT_FOUND",
                'message': f'User dengan ID {id} tidak ditemukan'}, 404)

        if password is None or password == "":
            password = cek_user['password']

        if email is None or email == "":
            errorEmail = "Email user tidak boleh kosong"

        if email != cek_user['email']:
            cek_email = self.cek_email(email)
            if cek_email:
                errorEmail = f"Email {email} sudah digunakan"

        if nama is None or nama == "":
            errorNama = "Nama user tidak boleh kosong"

        if 'errorEmail' in locals() or 'errorNama' in locals():
            return make_response({
                "code": 400,
                "status": "BAD_REQUEST",
                'errors': {
                    'email': errorEmail if 'errorEmail' in locals() else "",
                    'nama': errorNama if 'errorNama' in locals() else "",
                }}, 400)
        else:
            try:
                self.cur.execute(
                    f"UPDATE tbl_user SET email='{email}', nama='{nama}', `password`='{password}' WHERE id='{id}'")
                self.conn.commit()
                return make_response({
                    "code": 202,
                    "status": "ACCEPTED",
                    'message': 'Update user berhasil'}, 202)
            except:
                return make_response({
                    "code": 500,
                    "status": "INTERNAL_SERVER_ERROR",
                    'error': 'Terdapat kesalahan sistem saat mengubah data'}, 500)

    def hapus_user(self, id):
        cek_user = self.cek_user(id)
        if not cek_user:
            return make_response({
                "code": 404,
                "status": "NOT_FOUND",
                'error': f'User dengan ID {id} tidak ditemukan'}, 404)

        try:
            self.cur.execute(f"DELETE FROM tbl_user WHERE id='{id}'")
            self.conn.commit()
            return make_response({
                "code": 200,
                "status": "OK",
                'message': f"User dengan email {cek_user['email']} berhasil dihapus"}, 200)
        except mariadb.Error as e:
            return make_response({
                "code": 409,
                "status": "CONFLICT",
                "error": f"User dengan email {cek_user['email']} tidak dapat dihapus"}, 409)

    def cek_login(self, email, password):
        self.cur.execute(
            f"SELECT * FROM tbl_user WHERE email='{email}' and password='{password}'")
        result = self.cur.fetchone()
        return result
