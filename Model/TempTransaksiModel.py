from flask import make_response
import mariadb
from Config.config import dbconfig
import datetime


class TempTransaksiModel:
    cur = ""
    conn = ""

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

    def get_invoice(self, tanggal):
        if tanggal is None or tanggal == "":
            tanggal = datetime.datetime.now().strftime("%Y-%m-%d")
            tanggalBaru = datetime.datetime.now().strftime("%d%m%y")
        else:
            tanggalBaru = tanggal.split('-')
            y = tanggalBaru[0][2:]
            m = tanggalBaru[1]
            d = tanggalBaru[2]
            tanggalBaru = d+m+y

        self.cur.execute(
            f"SELECT id FROM tbl_transaksi WHERE DATE_FORMAT(tgl_transaksi, '%Y-%m-%d') = '{tanggal}' ORDER BY id DESC LIMIT 1")
        result = self.cur.fetchone()

        if result:
            data = result['id']
            lastNoUrut = data[-4:]
            nextNoUrut = int(lastNoUrut) + 1
            invoice = str(tanggalBaru) + str("%04d" % (nextNoUrut))
        else:
            invoice = str(tanggalBaru) + "0001"

        return invoice

    def tambah_temp(self, tanggal, produkid, jml, biaya_tambahan, catatan):
        self.cur.execute(f"SELECT * FROM tbl_produk WHERE id={produkid}")
        cek_produk = self.cur.fetchone()
        if cek_produk is None:
            return make_response({
                "code": 404,
                "status": "NOT_FOUND",
                'message': 'Produk tidak ditemukan'}, 404)

        harga_jual = cek_produk['harga_jual']

        if jml is None or jml == "":
            errorJml = "Qty / Jml tidak boleh kosong"
        elif (not jml.isnumeric()):
            errorJml = "Qty / Jml harus angka"

        if biaya_tambahan and not biaya_tambahan.isnumeric():
            errorBiayaTambahan = "Biaya tambahan harus angka"

        try:
            datetime.datetime.strptime(tanggal, '%Y-%m-%d')
            transaksiid = self.get_invoice(tanggal)
        except ValueError:
            errorTanggal = "Enter a date formatted as YYYY-MM-DD !"

        if 'errorJml' in locals() or 'errorTanggal' in locals() or 'errorBiayaTambahan' in locals():
            return make_response({
                "code": 400,
                "status": "BAD_REQUEST",
                'errors': {
                    'jml': errorJml if 'errorJml' in locals() else "",
                    'tanggal': errorTanggal if 'errorTanggal' in locals() else "",
                    'biayaTambahan': errorBiayaTambahan if 'errorBiayaTambahan' in locals() else "",
                }}, 400)

        else:
            try:
                self.cur.execute(
                    f'SELECT * FROM tbl_produk WHERE id={produkid}')
                data_produk = self.cur.fetchone()
                stok_terbaru = int(data_produk['stok']) - int(jml)

                if int(data_produk['stok']) < int(jml):
                    return make_response({"error": f"Stok dari {data_produk['nama_produk']} habis, sisa stok {data_produk['stok']}"}, 201)

                # tambah temp
                self.cur.execute(
                    f"INSERT INTO tbl_temp_transaksi (transaksiid, produkid, jml, harga_jual, biaya_tambahan, catatan) VALUES ('{transaksiid}', '{produkid}', '{jml}', '{harga_jual}', '{biaya_tambahan}', '{catatan}')")

                # ubah stok
                self.cur.execute(f"UPDATE tbl_produk SET stok=%s WHERE id=%d",
                                 (stok_terbaru, produkid))

                return make_response({
                    "code": 201,
                    "status": "CREATED",
                    "message": f"Produk berhasil ditambahkan ke temp"}, 201)

            except mariadb.Error as e:
                return make_response({
                    "code": 500,
                    "status": "INTERNAL_SERVER_ERROR",
                    "message": "Terdapat kesalahan sistem saat menambah data"}, 500)

    def hapus_semua_temp(self, transaksiid):
        self.cur.execute(
            f"SELECT stok, jml, produkid FROM tbl_temp_transaksi INNER JOIN tbl_produk ON tbl_temp_transaksi.produkid = tbl_produk.id WHERE transaksiid = '{transaksiid}'")
        cek_data = self.cur.fetchall()
        if len(cek_data) < 1:
            return make_response({
                "code": 404,
                "status": "NOT_FOUND",
                'error': f'Data temp dengan ID {transaksiid} tidak ditemukan'}, 404)

        try:
            # mengembalikan stok
            for i in cek_data:
                self.cur.execute(
                    f"SELECT stok FROM tbl_produk WHERE id='{i['produkid']}'")
                stokProduk = self.cur.fetchone()['stok']
                stokTerbaru = int(stokProduk) + int(i['jml'])
                self.cur.execute(
                    f"UPDATE tbl_produk SET stok = '{stokTerbaru}' WHERE id = '{i['produkid']}'")

            self.cur.execute(
                f"DELETE FROM tbl_temp_transaksi WHERE transaksiid={transaksiid}")
            return make_response({
                "code": 200,
                "status": "OK",
                'message': f"Temp dengan ID Transaksi {transaksiid} berhasil dihapus"}, 200)
        except mariadb.Error as e:
            return make_response({
                "code": 500,
                "status": "INTERNAL SERVER ERROR",
                "error": f"Terdapat kesalahan sistem saat menghapus data"}, 500)

    def hapus_temp(self, id):
        self.cur.execute(
            f"SELECT stok, jml, produkid FROM tbl_temp_transaksi INNER JOIN tbl_produk ON tbl_temp_transaksi.produkid = tbl_produk.id WHERE tbl_temp_transaksi.id = '{id}'")
        cek_data = self.cur.fetchone()
        if not cek_data:
            return make_response({
                "code": 404,
                "status": "NOT_FOUND",
                'error': f'Data temp dengan ID {id} tidak ditemukan'}, 404)

        try:
            stokTerbaru = int(cek_data['stok']) + int(cek_data['jml'])
            self.cur.execute(
                f"UPDATE tbl_produk SET stok = '{stokTerbaru}' WHERE id = '{cek_data['produkid']}'")
            self.cur.execute(f"DELETE FROM tbl_temp_transaksi WHERE id={id}")
            return make_response({
                "code": 200,
                "status": "OK",
                'message': f"Temp berhasil dihapus"})
        except mariadb.Error as e:
            return make_response({
                "code": 500,
                "status": "INTERNAL SERVER ERROR",
                "error": f"Terdapat kesalahan sistem saat menghapus data"}, 500)

    def daftar_temp(self, transaksiid):
        try:
            self.cur.execute(
                f"SELECT *, (jml * harga_jual)+biaya_tambahan as subtotal FROM tbl_temp_transaksi WHERE transaksiid = '{transaksiid}'")
            result = self.cur.fetchall()

            total_bayar = 0
            for i in result:
                total_bayar += i['subtotal']

            if result:
                response = make_response({
                    "code": 200,
                    "status": "OK",
                    "total_bayar": total_bayar,
                    "data": result,
                }, 200)
                return response
            else:
                return make_response({
                    "code": 404,
                    "status": "NOT_FOUND",
                    'error': f'Data temp dengan ID {transaksiid} tidak ditemukan'}, 404)
        except:
            return make_response({
                "code": 500,
                "status": "INTERNAL_SERVER_ERROR",
                'error': 'Terdapat kesalahan sistem saat mengambil data'}, 500)
