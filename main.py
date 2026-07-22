from datetime import datetime

from sqlalchemy.exc import IntegrityError

from database.db_handler import (
    init_db,
    simpan_menu,
    ambil_semua_menu,
    update_stok_menu,
    simpan_transaksi,
    ambil_semua_transaksi,
)
from services.warung import Warung
from models.menu import MenuMakanan, MenuMinuman


# =========================================================
# DATA AWAL DAN PEMUATAN DATABASE
# =========================================================

def buat_menu_awal() -> None:
    """
    Membuat data menu awal hanya jika database masih kosong.
    """

    simpan_menu(
        nama="Nasi Rames",
        harga=15000,
        stok=20,
        kategori="makanan",
    )

    simpan_menu(
        nama="Es Teh",
        harga=5000,
        stok=30,
        kategori="minuman",
    )


def muat_menu_dari_database(warung: Warung) -> None:
    """
    Memuat seluruh data menu SQLite ke objek Warung.

    Database hanya menyimpan kategori, bukan porsi atau suhu.
    Karena itu digunakan nilai bawaan:
    - makanan: porsi Normal
    - minuman: suhu Dingin
    """

    daftar_menu_db = ambil_semua_menu()

    if not daftar_menu_db:
        buat_menu_awal()
        daftar_menu_db = ambil_semua_menu()

    for menu_db in daftar_menu_db:
        kategori = menu_db.kategori.lower()

        if kategori == "makanan":
            menu = MenuMakanan(
                menu_db.nama,
                menu_db.harga,
                menu_db.stok,
                "Normal",
            )

        elif kategori == "minuman":
            menu = MenuMinuman(
                menu_db.nama,
                menu_db.harga,
                menu_db.stok,
                "Dingin",
            )

        else:
            # Lewati data dengan kategori yang tidak dikenali.
            continue

        warung.tambah_menu(menu)


# =========================================================
# TAMPILAN DATABASE
# =========================================================

def tampilkan_menu_database() -> None:
    """
    Menampilkan seluruh menu yang tersimpan di SQLite.
    """

    daftar_menu = ambil_semua_menu()

    print("\n===== MENU DARI DATABASE =====")

    if not daftar_menu:
        print("Belum ada menu di database.")
        return

    for nomor, menu in enumerate(daftar_menu, start=1):
        print(
            f"{nomor}. {menu.nama} | "
            f"Rp{menu.harga:,.0f} | "
            f"Stok: {menu.stok} | "
            f"Kategori: {menu.kategori}"
        )


def tampilkan_transaksi_database() -> None:
    """
    Menampilkan seluruh transaksi yang tersimpan di SQLite.
    """

    daftar_transaksi = ambil_semua_transaksi()

    print("\n===== TRANSAKSI DARI DATABASE =====")

    if not daftar_transaksi:
        print("Belum ada transaksi di database.")
        return

    for nomor, transaksi in enumerate(
        daftar_transaksi,
        start=1,
    ):
        print(
            f"{nomor}. "
            f"Menu ID: {transaksi.menu_id} | "
            f"Meja: {transaksi.nomor_meja} | "
            f"Jumlah: {transaksi.jumlah} | "
            f"Subtotal: Rp{transaksi.subtotal:,.0f} | "
            f"Waktu: {transaksi.waktu}"
        )


# =========================================================
# TAMBAH MENU
# =========================================================

def tambah_menu_cli(warung: Warung) -> None:
    """
    Menambahkan menu ke objek Warung dan database.
    """

    print("\n===== TAMBAH MENU =====")
    print("m. Makanan")
    print("n. Minuman")

    jenis = input("Jenis menu (m/n): ").strip().lower()

    if jenis not in ("m", "n"):
        print("Jenis menu tidak valid.")
        return

    nama = input("Nama menu: ").strip()
    harga = float(input("Harga: "))
    stok = int(input("Stok: "))

    if not nama:
        print("Nama menu tidak boleh kosong.")
        return

    if harga < 0:
        print("Harga tidak boleh negatif.")
        return

    if stok < 0:
        print("Stok tidak boleh negatif.")
        return

    if jenis == "m":
        porsi = input("Porsi: ").strip()

        menu = MenuMakanan(
            nama,
            harga,
            stok,
            porsi,
        )

        kategori = "makanan"

    else:
        suhu = input("Suhu: ").strip()

        menu = MenuMinuman(
            nama,
            harga,
            stok,
            suhu,
        )

        kategori = "minuman"

    try:
        # Simpan ke database terlebih dahulu.
        simpan_menu(
            nama=menu.nama,
            harga=menu.harga,
            stok=menu.stok,
            kategori=kategori,
        )

        # Jika database berhasil, masukkan ke objek Warung.
        warung.tambah_menu(menu)

        print(
            f"Menu '{menu.nama}' berhasil ditambahkan "
            "dan disimpan ke database."
        )

    except IntegrityError:
        print(
            f"Menu dengan nama '{nama}' sudah ada "
            "di database."
        )


# =========================================================
# PEMESANAN
# =========================================================

def pesan_cli(warung: Warung) -> None:
    """
    Menambahkan pesanan dan memperbarui stok database.
    """

    print("\n===== BUAT PESANAN =====")

    nomor_meja = input("Nomor meja: ").strip()
    nama_menu = input("Nama menu: ").strip()
    jumlah = int(input("Jumlah: "))

    if jumlah <= 0:
        print("Jumlah pesanan harus lebih dari nol.")
        return

    # Method pesan() melakukan:
    # - pemeriksaan meja;
    # - pencarian menu;
    # - pengurangan stok;
    # - penambahan item pesanan.
    warung.pesan(
        nomor_meja,
        nama_menu,
        jumlah,
    )

    # Ambil objek menu setelah stoknya berkurang.
    menu = warung.cari_menu(nama_menu)

    # Simpan stok terbaru ke database.
    update_stok_menu(
        menu.nama,
        menu.stok,
    )

    print(
        f"Stok '{menu.nama}' di database "
        f"diperbarui menjadi {menu.stok}."
    )


# =========================================================
# PENYIMPANAN TRANSAKSI
# =========================================================

def ambil_daftar_item(pesanan) -> list:
    """
    Mengambil list item dari objek Pesanan.

    Beberapa kemungkinan nama atribut didukung agar
    kompatibel dengan struktur class Pesanan yang digunakan.
    """

    kemungkinan_atribut = (
        "_daftar_item",
        "_daftar_items",
        "_items",
        "daftar_item",
        "items",
    )

    for nama_atribut in kemungkinan_atribut:
        daftar_item = getattr(
            pesanan,
            nama_atribut,
            None,
        )

        if isinstance(daftar_item, list):
            return daftar_item

    raise AttributeError(
        "Daftar item tidak ditemukan pada class Pesanan. "
        "Periksa nama atribut item di models/pesanan.py."
    )


def hitung_subtotal_item(item) -> float:
    """
    Mengambil subtotal dari satu ItemPesanan.
    """

    if hasattr(item, "hitung_subtotal"):
        return float(item.hitung_subtotal())

    if hasattr(item, "subtotal"):
        subtotal = item.subtotal

        if callable(subtotal):
            return float(subtotal())

        return float(subtotal)

    menu = getattr(item, "menu", None)
    jumlah = getattr(item, "jumlah", None)

    if menu is None or jumlah is None:
        raise AttributeError(
            "Item pesanan tidak memiliki menu atau jumlah."
        )

    return float(menu.harga * jumlah)


def simpan_detail_transaksi(pesanan) -> None:
    """
    Menyimpan seluruh item pada satu pesanan ke database.
    """

    daftar_item = ambil_daftar_item(pesanan)
    daftar_menu_db = ambil_semua_menu()

    menu_db_berdasarkan_nama = {
        menu.nama.lower(): menu
        for menu in daftar_menu_db
    }

    waktu_transaksi = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    for item in daftar_item:
        menu = getattr(item, "menu", None)
        jumlah = getattr(item, "jumlah", None)

        if menu is None or jumlah is None:
            raise AttributeError(
                "Item pesanan tidak memiliki atribut "
                "'menu' atau 'jumlah'."
            )

        menu_db = menu_db_berdasarkan_nama.get(
            menu.nama.lower()
        )

        if menu_db is None:
            raise ValueError(
                f"Menu '{menu.nama}' tidak ditemukan "
                "di database."
            )

        subtotal = hitung_subtotal_item(item)

        simpan_transaksi(
            menu_id=menu_db.id,
            nomor_meja=str(pesanan.nomor_meja),
            jumlah=jumlah,
            subtotal=subtotal,
            waktu=waktu_transaksi,
        )


def bayar_cli(warung: Warung) -> None:
    """
    Memproses pembayaran dan menyimpan detail transaksi.
    """

    print("\n===== PEMBAYARAN =====")

    nomor_meja = input("Nomor meja: ").strip()

    pesanan = warung._pesanan_aktif.get(nomor_meja)

    if pesanan is None:
        print(f"Meja {nomor_meja} belum dibuka.")
        return

    total = pesanan.hitung_total()

    print(f"Total tagihan: Rp{total:,.0f}")

    uang = float(input("Uang bayar: "))

    if uang < total:
        kekurangan = total - uang

        print(
            f"Uang tidak cukup. "
            f"Kurang Rp{kekurangan:,.0f}."
        )
        return

    # Proses pembayaran melalui logika Warung.
    warung.bayar(
        nomor_meja,
        uang,
    )

    # Pesanan sudah berhasil dibayar,
    # selanjutnya disimpan secara permanen.
    simpan_detail_transaksi(pesanan)

    print("Transaksi berhasil disimpan ke database.")


# =========================================================
# MENU UTAMA
# =========================================================

def menu_utama(warung: Warung) -> None:
    """
    Menjalankan menu utama aplikasi.
    """

    while True:
        print("\n=== WARUNG MAKAN BU TUTI ===")
        print("1. Tambah Menu")
        print("2. Tampilkan Menu")
        print("3. Buka Meja")
        print("4. Pesan")
        print("5. Bayar")
        print("6. Riwayat")
        print("7. Tampilkan Menu dari Database")
        print("8. Tampilkan Transaksi dari Database")
        print("0. Keluar")

        pilih = input("Pilih: ").strip()

        try:
            if pilih == "1":
                tambah_menu_cli(warung)

            elif pilih == "2":
                warung.tampilkan_menu()

            elif pilih == "3":
                nomor = input("Nomor meja: ").strip()
                warung.buka_meja(nomor)

            elif pilih == "4":
                pesan_cli(warung)

            elif pilih == "5":
                bayar_cli(warung)

            elif pilih == "6":
                warung.tampilkan_riwayat()

            elif pilih == "7":
                tampilkan_menu_database()

            elif pilih == "8":
                tampilkan_transaksi_database()

            elif pilih == "0":
                print("Program selesai.")
                break

            else:
                print("Pilihan tidak valid.")

        except ValueError as error:
            print(f"Input tidak valid: {error}")

        except IntegrityError:
            print(
                "Data gagal disimpan karena terdapat "
                "data yang sama."
            )

        except Exception as error:
            print(f"Error: {error}")


# =========================================================
# PROGRAM UTAMA
# =========================================================

if __name__ == "__main__":
    # Buat tabel jika belum tersedia.
    init_db()

    # Buat controller utama.
    warung = Warung()

    # Masukkan menu SQLite ke dalam objek Warung.
    muat_menu_dari_database(warung)

    # Jalankan aplikasi.
    menu_utama(warung)