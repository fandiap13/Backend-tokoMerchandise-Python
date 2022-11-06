# __all__ = ['Produk', 'Kategori']

import glob
import os

# pada folder controller, cari file didalam folder controller
# hapus 3 huruf paling akhir pada semua file didalam controller, contoh : fandi.py menjadi fandi
# kemudian disimpan di variabel untuk digunakan di app

__all__=[os.path.basename(f)[:-3] for f in glob.glob(os.path.dirname(__file__) + "/*.py")] 
