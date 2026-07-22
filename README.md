Sistem Manajemen Warung Makan

📖 Deskripsi Proyek

Sistem Manajemen Warung Makan adalah aplikasi berbasis Python yang digunakan untuk mengelola data menu, pesanan, dan transaksi pada sebuah warung makan. Program ini dibuat menggunakan konsep Object Oriented Programming (OOP) dan dilengkapi dengan unit testing menggunakan pytest untuk memastikan setiap fitur berjalan dengan baik.

👥 Anggota Kelompok dan Pembagian Tugas
Nama Anggota	            Tugas
Dewi Marsita	            Membuat branch feature/warung-main,services/warung.py + main.py + README.md + tests/test_warung.py
Livia Agistina Afrizal	    Membuat branch feature/models-meja, models/meja.py
Dhiha Hermalia Putri	    Membuat branch feature/models-meja, models/meja.py
Karuniansyah Daryawan P.L   Membuat branch feature/models-menu, Exception/custom_exceptions.py + models/menu.py
Alifianda Nur Mahardika 	Membuat branch feature/pesanan, models/pesanan.py

Cara Menjalankan main.py

Pastikan Python sudah terinstall di komputer.
Jalankan program dengan perintah:
python main.py
Perintah tersebut akan menjalankan file utama aplikasi yang berisi menu dan alur sistem warung makan.

🧪 Cara Menjalankan Unit Test

Untuk menjalankan pengujian program menggunakan pytest:

pytest tests/ -v
Penjelasan:
pytest → menjalankan pengujian otomatis
tests/ → folder tempat file testing
-v → menampilkan detail hasil test

Jika semua pengujian berhasil, maka akan muncul status:
PASSED

✅ Fitur yang Sudah Diimplementasikan
Menambahkan menu makanan
Menampilkan daftar menu
Membuat pesanan
Menghitung total pembayaran
Penyimpanan data menggunakan class
Pengujian otomatis menggunakan pytest
Struktur program berbasis OOP

# 📊 Class Diagram (Teks)

```text
+--------------------------------------------------+
|         exceptions/custom_exceptions.py          |
+--------------------------------------------------+
| MenuHabisError                                   |
| MejaTidakDitemukanError                          |
| MejaSudahTerisiError                             |
| MenuTidakDitemukanError                          |
+--------------------------------------------------+


+--------------------------------------------------+
|               models/menu.py                     |
+--------------------------------------------------+
|                  Menu (Base Class)               |
+--------------------------------------------------+
| - nama : str                                     |
| - harga : int                                    |
| - stok : int                                     |
+--------------------------------------------------+
| + kurangi_stok(jumlah:int)                       |
+--------------------------------------------------+
                 ▲
                 │
        ---------------------
        │                   │

+---------------------------+     +---------------------------+
|       MenuMakanan         |     |       MenuMinuman         |
+---------------------------+     +---------------------------+
| - porsi : str             |     | - suhu : str              |
+---------------------------+     +---------------------------+


+--------------------------------------------------+
|                models/meja.py                    |
+--------------------------------------------------+
|          StatusMeja (Abstract Class)             |
+--------------------------------------------------+
| + keterangan() : str                             |
| + bisa_pesan() : bool                            |
+--------------------------------------------------+
                 ▲
                 │
        ---------------------
        │                   │

+---------------------------+     +---------------------------+
|        MejaTerisi         |     |        MejaKosong         |
+---------------------------+     +---------------------------+
| - jam_masuk : datetime    |     |                           |
+---------------------------+     +---------------------------+
| + keterangan() : str      |     | + keterangan() : str      |
| + bisa_pesan() : bool     |     | + bisa_pesan() : bool     |
+---------------------------+     +---------------------------+


+--------------------------------------------------+
|               models/pesanan.py                  |
+--------------------------------------------------+
|                  ItemPesanan                     |
+--------------------------------------------------+
| - menu : Menu                                    |
| - jumlah : int                                   |
+--------------------------------------------------+
| + subtotal() : float                             |
+--------------------------------------------------+


+--------------------------------------------------+
|                  Pesanan                         |
+--------------------------------------------------+
| - list_item : List[ItemPesanan]                  |
| - total : float                                  |
+--------------------------------------------------+
| + hitung_total() : float                         |
| + selesai() : void                               |
+--------------------------------------------------+


+--------------------------------------------------+
|               services/warung.py                 |
+--------------------------------------------------+
|                    Warung                        |
+--------------------------------------------------+
| - menu_list : List[Menu]                         |
| - meja_list : List[StatusMeja]                   |
| - pesanan_aktif : List[Pesanan]                  |
+--------------------------------------------------+
| + kelola_menu()                                  |
| + buat_pesanan()                                 |
| + histori_pesanan()                              |
+--------------------------------------------------+


+--------------------------------------------------+
|               tests/test_warung.py               |
+--------------------------------------------------+
|                  Unit Test                       |
+--------------------------------------------------+
| - test_harga_negatif()                           |
| - test_menu_habis()                              |
| - test_kurangi_stok()                            |
| - test_meja_terisi_bisa_pesan()                  |
| - test_subtotal_benar()                          |
+--------------------------------------------------+


+--------------------------------------------------+
|                     main.py                      |
+--------------------------------------------------+
| + menu_utama(warung)                             |
| + if __name__ == "__main__"                      |
+--------------------------------------------------+
```
🏗️ Keputusan Desain

Program ini menggunakan pendekatan Object Oriented Programming (OOP) karena lebih mudah dalam mengelola data dan fitur aplikasi.
Setiap class memiliki tanggung jawab masing-masing sehingga kode menjadi lebih rapi, terstruktur, dan mudah dikembangkan.

Class Menu digunakan untuk menyimpan data menu makanan, class Pesanan digunakan untuk mengelola transaksi pemesanan, sedangkan class Warung digunakan untuk mengatur keseluruhan sistem aplikasi.

Dengan pemisahan class tersebut:
1. kode lebih mudah dibaca
2. proses debugging lebih mudah
3. fitur baru dapat ditambahkan tanpa mengubah keseluruhan program
4. dan unit testing menjadi lebih terstruktur