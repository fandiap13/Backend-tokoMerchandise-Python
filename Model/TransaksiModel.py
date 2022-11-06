import datetime
from flask import make_response
from Config.config import dbconfig
import mariadb


class TransaksiModel:
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

    def cek_format_tanggal(self, tanggal):
        try:
            return bool(datetime.datetime.strptime(tanggal, '%Y-%m-%d'))
        except ValueError:
            return False

    def simpan_transaksi(self, userid, tgl_transaksi, pelangganid, dibayar):
        try:
            if tgl_transaksi is None or tgl_transaksi == "":
                errorTanggal = "Tanggal transaksi tidak boleh kosong"

            if self.cek_format_tanggal(tgl_transaksi) == False:
                errorTanggal = "Enter a date formatted as YYYY-MM-DD !"

            if pelangganid is None or pelangganid == "":
                errorPelanggan = "ID pelanggan tidak boleh kosong"
            else:
                self.cur.execute(
                    f"SELECT * FROM tbl_pelanggan WHERE id='{pelangganid}'")
                cek_pelanggan = self.cur.fetchone()
                if not cek_pelanggan:
                    errorPelanggan = f"Pelanggan dengan ID {pelangganid} tidak ditemukan"

            if dibayar is None or dibayar == "":
                errorDibayar = "Uang yang dibayarkan tidak boleh kosong"
            elif (not dibayar.isnumeric()):
                errorDibayar = "Uang yang dibayarkan harus angka"

            if 'errorPelanggan' in locals() or 'errorDibayar' in locals() or 'errorTanggal' in locals():
                return make_response({
                    "code": 400,
                    "status": "BAD_REQUEST",
                    'errors': {
                        'pelangganid': errorPelanggan if 'errorPelanggan' in locals() else "",
                        'dibayar': errorDibayar if 'errorDibayar' in locals() else "",
                        'tgl_transaksi': errorTanggal if 'errorTanggal' in locals() else "",
                    }}, 400)

            transaksiid = self.get_invoice(tgl_transaksi)
            tanggal = tgl_transaksi + " " + \
                str(datetime.datetime.now().strftime("%H:%M:%S"))

            self.cur.execute(
                f"SELECT *, (tbl_temp_transaksi.harga_jual * jml) + biaya_tambahan as subtotal FROM tbl_temp_transaksi INNER JOIN tbl_produk ON tbl_temp_transaksi.produkid = tbl_produk.id WHERE transaksiid = '{transaksiid}'")
            cek_temp = self.cur.fetchall()

            if len(cek_temp) > 0:
                total_bayar = 0
                for i in cek_temp:
                    total_bayar += i['subtotal']

                if int(total_bayar) > int(dibayar):
                    return make_response({
                        "code": 400,
                        "status": "BAD_REQUEST",
                        "error": f"Uang yang dibayarkan kurang!, total yang harus dibayar {total_bayar}"}, 400)

                # insert detail transaksi
                self.cur.execute(
                    f"SELECT * FROM tbl_temp_transaksi WHERE transaksiid='{transaksiid}'")
                data_temp = self.cur.fetchall()
                # return data_temp
                for i in data_temp:
                    self.cur.execute(
                        f"INSERT INTO tbl_detail_transaksi (transaksiid, produkid, jml, harga_jual, biaya_tambahan, catatan) VALUES ('{i['transaksiid']}', '{i['produkid']}', '{i['jml']}', '{i['harga_jual']}', '{i['biaya_tambahan']}', '{i['catatan']}')")
                    self.conn.commit()

                # hapus temp
                self.cur.execute(
                    f"DELETE FROM tbl_temp_transaksi WHERE transaksiid='{transaksiid}'")

                # insert transaksi
                self.cur.execute(
                    f"INSERT INTO `tbl_transaksi` (`id`, `userid`, `tgl_transaksi`, `pelangganid`, `total_bayar`, `dibayar`) VALUES ('{transaksiid}', '{userid}', '{tanggal}', '{pelangganid}', '{total_bayar}', '{dibayar}')")

                return make_response({
                    "code": 201,
                    "status": "CREATED",
                    'message': f'Transaksi {transaksiid} berhasil !'}, 201)
            else:
                return make_response({
                    "code": 404,
                    "status": "NOT_FOUND",
                    'error': 'Anda belum memesan produk, silahkan masukkan pesanan'}, 404)
        except mariadb.Error as e:
            return make_response({
                "code": 500,
                "status": "INTERNAL_SERVER_ERROR",
                'error': f'Terdapat kesalahan sistem saat menyimpan transaksi'}, 500)

    def daftar_transaksi(self):
        try:
            self.cur.execute(f"SELECT tbl_transaksi.id, tgl_transaksi, pelangganid, nama_pelanggan, total_bayar, dibayar, (dibayar - total_bayar) as kembalian, userid, tbl_user.nama as kasir FROM tbl_transaksi INNER JOIN tbl_user ON tbl_transaksi.userid = tbl_user.id INNER JOIN tbl_pelanggan ON tbl_transaksi.pelangganid = tbl_pelanggan.id ORDER BY tgl_transaksi ASC")
            result = self.cur.fetchall()
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
                    'message': 'Data transaksi kosong'}, 404)
        except mariadb.Error as e:
            return make_response({
                "code": 500,
                "status": "INTERNAL_SERVER_ERROR",
                'error': 'Terdapat kesalahan sistem saat mengambil data'}, 500)

    def detail_transaksi(self, transaksiid):
        try:
            self.cur.execute(
                f"SELECT tbl_transaksi.id, tgl_transaksi, pelangganid, nama_pelanggan, total_bayar, dibayar, (dibayar - total_bayar) as kembalian, userid, tbl_user.nama as kasir FROM tbl_transaksi INNER JOIN tbl_user ON tbl_transaksi.userid = tbl_user.id INNER JOIN tbl_pelanggan ON tbl_transaksi.pelangganid = tbl_pelanggan.id WHERE tbl_transaksi.id = '{transaksiid}'")
            result1 = self.cur.fetchone()
            self.cur.execute(
                f"SELECT dt.id, dt.transaksiid, dt.produkid, p.nama_produk, dt.jml, dt.harga_jual, dt.biaya_tambahan, (dt.jml * dt.harga_jual) + dt.biaya_tambahan as subtotal, dt.catatan FROM tbl_detail_transaksi as dt INNER JOIN tbl_produk as p ON dt.produkid=p.id WHERE transaksiid = '{transaksiid}'")
            result2 = self.cur.fetchall()
            if result1 and result2:
                return make_response({
                    "code": 200,
                    "status": "OK",
                    'data': {
                        'transaksi': result1,
                        'detail_transaksi': result2
                    }
                }, 200)
            else:
                return make_response({
                    "code": 404,
                    "status": "NOT_FOUND",
                    'error': f'Detail transaksi dengan ID transaksi {transaksiid} tidak ditemukan'}, 404)
        except mariadb.Error as e:
            return make_response({
                "code": 500,
                "status": "INTERNAL_SERVER_ERROR",
                'error': f"Terdapat kesalahan saat mengambil data"}, 500)
