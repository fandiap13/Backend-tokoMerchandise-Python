-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 05 Nov 2022 pada 04.30
-- Versi server: 10.4.21-MariaDB
-- Versi PHP: 8.0.11

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `toko_online_api`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `tbl_detail_transaksi`
--

CREATE TABLE `tbl_detail_transaksi` (
  `id` int(11) NOT NULL,
  `transaksiid` char(13) NOT NULL,
  `produkid` int(11) NOT NULL,
  `jml` int(11) NOT NULL,
  `harga_jual` int(11) NOT NULL,
  `biaya_tambahan` int(11) NOT NULL,
  `catatan` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data untuk tabel `tbl_detail_transaksi`
--

INSERT INTO `tbl_detail_transaksi` (`id`, `transaksiid`, `produkid`, `jml`, `harga_jual`, `biaya_tambahan`, `catatan`) VALUES
(1, '0411220001', 2, 3, 120000, 0, ''),
(2, '0411220001', 6, 1, 30000, 1000, 'Warna hitam');

-- --------------------------------------------------------

--
-- Struktur dari tabel `tbl_kategori`
--

CREATE TABLE `tbl_kategori` (
  `id` int(11) NOT NULL,
  `kategori` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data untuk tabel `tbl_kategori`
--

INSERT INTO `tbl_kategori` (`id`, `kategori`) VALUES
(1, 'PDH'),
(2, 'Stiker'),
(5, 'Celana'),
(6, 'Baju'),
(8, 'Kaus'),
(10, 'Minuman'),
(11, 'Pakaian'),
(12, 'Topi');

-- --------------------------------------------------------

--
-- Struktur dari tabel `tbl_pelanggan`
--

CREATE TABLE `tbl_pelanggan` (
  `id` int(11) NOT NULL,
  `nama_pelanggan` varchar(150) NOT NULL,
  `alamat` text DEFAULT NULL,
  `no_telp` varchar(20) DEFAULT NULL,
  `email` varchar(150) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data untuk tabel `tbl_pelanggan`
--

INSERT INTO `tbl_pelanggan` (`id`, `nama_pelanggan`, `alamat`, `no_telp`, `email`) VALUES
(1, 'fandi', 'bandardawung', '0895391525544', 'andiazizp123@gmail.com'),
(7, 'fandi p', NULL, NULL, NULL),
(11, 'Wihan ', '-', NULL, NULL),
(12, 'Jofan', '-', NULL, NULL);

-- --------------------------------------------------------

--
-- Struktur dari tabel `tbl_produk`
--

CREATE TABLE `tbl_produk` (
  `id` int(11) NOT NULL,
  `nama_produk` varchar(200) NOT NULL,
  `id_kategori` int(11) NOT NULL,
  `id_satuan` int(11) NOT NULL,
  `deskripsi_produk` text DEFAULT NULL,
  `berat_produk` int(11) NOT NULL,
  `harga_produk` int(11) NOT NULL,
  `harga_jual` int(11) NOT NULL,
  `gambar_produk` varchar(150) DEFAULT NULL,
  `stok` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data untuk tabel `tbl_produk`
--

INSERT INTO `tbl_produk` (`id`, `nama_produk`, `id_kategori`, `id_satuan`, `deskripsi_produk`, `berat_produk`, `harga_produk`, `harga_jual`, `gambar_produk`, `stok`) VALUES
(2, 'PDH HMPTI', 1, 1, 'Ini adalah produk HMPTI', 1000, 100000, 120000, 'Uploads/Images/1667553616203954.png', 97),
(3, 'Stiker HMPTI baru', 1, 2, 'Ini adalah produk HMPTI', 1, 1000, 1500, NULL, 1000),
(4, 'Pakaian santai', 11, 2, 'Ini adalah produk HMPTI', 100, 100000, 150000, NULL, 1000),
(5, 'PDH TEKNIK INFORMATIKA', 1, 2, 'Ini adalah produk HMPTI', 100, 120000, 150000, NULL, 1000),
(6, 'Topi HMPTI', 12, 2, 'Ini adalah produk HMPTI', 100, 20000, 30000, NULL, 999);

-- --------------------------------------------------------

--
-- Struktur dari tabel `tbl_satuan`
--

CREATE TABLE `tbl_satuan` (
  `id` int(11) NOT NULL,
  `satuan` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data untuk tabel `tbl_satuan`
--

INSERT INTO `tbl_satuan` (`id`, `satuan`) VALUES
(1, 'PCS'),
(2, 'Pack'),
(3, 'Cm'),
(4, 'Setel');

-- --------------------------------------------------------

--
-- Struktur dari tabel `tbl_temp_transaksi`
--

CREATE TABLE `tbl_temp_transaksi` (
  `id` int(11) NOT NULL,
  `transaksiid` char(13) NOT NULL,
  `produkid` int(11) NOT NULL,
  `jml` int(11) NOT NULL,
  `harga_jual` int(11) NOT NULL,
  `biaya_tambahan` int(11) NOT NULL,
  `catatan` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Struktur dari tabel `tbl_transaksi`
--

CREATE TABLE `tbl_transaksi` (
  `id` char(13) NOT NULL,
  `userid` int(11) NOT NULL,
  `tgl_transaksi` datetime NOT NULL,
  `pelangganid` int(11) NOT NULL,
  `total_bayar` int(11) NOT NULL,
  `dibayar` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data untuk tabel `tbl_transaksi`
--

INSERT INTO `tbl_transaksi` (`id`, `userid`, `tgl_transaksi`, `pelangganid`, `total_bayar`, `dibayar`) VALUES
('0411220001', 1, '2022-11-04 16:23:38', 1, 391000, 400000);

-- --------------------------------------------------------

--
-- Struktur dari tabel `tbl_user`
--

CREATE TABLE `tbl_user` (
  `id` int(11) NOT NULL,
  `email` varchar(150) NOT NULL,
  `password` varchar(150) NOT NULL,
  `nama` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data untuk tabel `tbl_user`
--

INSERT INTO `tbl_user` (`id`, `email`, `password`, `nama`) VALUES
(1, 'andiazizp123@gmail.com', 'fandi', 'Fandi AP'),
(11, 'wihan@gmail.com', 'wihan', 'wihan'),
(12, 'jofan@gmail.com', 'jofan', 'jofan');

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `tbl_detail_transaksi`
--
ALTER TABLE `tbl_detail_transaksi`
  ADD PRIMARY KEY (`id`),
  ADD KEY `produkid` (`produkid`),
  ADD KEY `transaksiid` (`transaksiid`);

--
-- Indeks untuk tabel `tbl_kategori`
--
ALTER TABLE `tbl_kategori`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `tbl_pelanggan`
--
ALTER TABLE `tbl_pelanggan`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `tbl_produk`
--
ALTER TABLE `tbl_produk`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_kategori` (`id_kategori`),
  ADD KEY `id_satuan` (`id_satuan`);

--
-- Indeks untuk tabel `tbl_satuan`
--
ALTER TABLE `tbl_satuan`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `tbl_temp_transaksi`
--
ALTER TABLE `tbl_temp_transaksi`
  ADD PRIMARY KEY (`id`),
  ADD KEY `produkid` (`produkid`),
  ADD KEY `transaksiid` (`transaksiid`);

--
-- Indeks untuk tabel `tbl_transaksi`
--
ALTER TABLE `tbl_transaksi`
  ADD PRIMARY KEY (`id`),
  ADD KEY `userid` (`userid`);

--
-- Indeks untuk tabel `tbl_user`
--
ALTER TABLE `tbl_user`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `tbl_detail_transaksi`
--
ALTER TABLE `tbl_detail_transaksi`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT untuk tabel `tbl_kategori`
--
ALTER TABLE `tbl_kategori`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT untuk tabel `tbl_pelanggan`
--
ALTER TABLE `tbl_pelanggan`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT untuk tabel `tbl_produk`
--
ALTER TABLE `tbl_produk`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT untuk tabel `tbl_satuan`
--
ALTER TABLE `tbl_satuan`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT untuk tabel `tbl_temp_transaksi`
--
ALTER TABLE `tbl_temp_transaksi`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT untuk tabel `tbl_user`
--
ALTER TABLE `tbl_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- Ketidakleluasaan untuk tabel pelimpahan (Dumped Tables)
--

--
-- Ketidakleluasaan untuk tabel `tbl_detail_transaksi`
--
ALTER TABLE `tbl_detail_transaksi`
  ADD CONSTRAINT `tbl_detail_transaksi_ibfk_1` FOREIGN KEY (`produkid`) REFERENCES `tbl_produk` (`id`);

--
-- Ketidakleluasaan untuk tabel `tbl_produk`
--
ALTER TABLE `tbl_produk`
  ADD CONSTRAINT `tbl_produk_ibfk_1` FOREIGN KEY (`id_kategori`) REFERENCES `tbl_kategori` (`id`),
  ADD CONSTRAINT `tbl_produk_ibfk_2` FOREIGN KEY (`id_satuan`) REFERENCES `tbl_satuan` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
