"""Program utama Sistem Manajemen Warung Makan Bu Tuti."""

from __future__ import annotations

import inspect
from datetime import datetime
from typing import Any

from sqlalchemy.exc import IntegrityError

from database.db_handler import (
    ambil_semua_menu,
    ambil_semua_transaksi,
    init_db,
    simpan_menu,
    simpan_transaksi,
    update_stok_menu,
)
from exceptions.custom_exceptions import (
    MejaSudahTerisiError,
    MejaTidakDitemukanError,
    MenuHabisError,
    MenuTidakDitemukanError,
)
from models.menu import MenuMakanan, MenuMinuman
from services.api_client import harga_dalam_mata_uang
from services.laporan import (
    menu_tersedia,
    pendapatan_per_kategori,
    ringkasan_transaksi,
    riwayat_diurutkan_total,
)
from services.warung import Warung


# =========================================================
# HELPER MENU
# =========================================================

def ambil_detail_menu(
    menu: Any,
    nama_atribut: str,
    nilai_default: str,
) -> str:
    """
    Mengambil atribut porsi atau suhu dari objek menu.

    Mendukung nama atribut biasa dan atribut private.
    """
    nilai = getattr(
        menu,
        nama_atribut,
        None,
    )

    if nilai is None:
        nilai = getattr(
            menu,
            f"_{nama_atribut}",
            None,
        )

    return str(nilai or nilai_default)


def simpan_menu_kompatibel(
    menu: Any,
    kategori: str,
) -> None:
    """
    Menyimpan menu ke database.

    Fungsi dibuat kompatibel dengan db_handler.py yang
    hanya memiliki parameter kategori maupun versi yang
    memiliki tambahan parameter porsi dan suhu.
    """
    parameter_fungsi = inspect.signature(
        simpan_menu
    ).parameters

    data_menu: dict[str, Any] = {
        "nama": menu.nama,
        "harga": menu.harga,
        "stok": menu.stok,
        "kategori": kategori,
    }

    if "porsi" in parameter_fungsi:
        data_menu["porsi"] = (
            ambil_detail_menu(
                menu,
                "porsi",
                "Normal",
            )
            if kategori == "makanan"
            else None
        )

    if "suhu" in parameter_fungsi:
        data_menu["suhu"] = (
            ambil_detail_menu(
                menu,
                "suhu",
                "Dingin",
            )
            if kategori == "minuman"
            else None
        )

    simpan_menu(**data_menu)


def muat_menu_dari_database(
    warung: Warung,
) -> None:
    """
    Mengambil seluruh menu dari database dan
    memasukkannya kembali ke dalam objek Warung.
    """
    daftar_menu_database = ambil_semua_menu()

    for menu_db in daftar_menu_database:
        kategori = str(
            menu_db.kategori
        ).strip().lower()

        if kategori == "makanan":
            porsi = getattr(
                menu_db,
                "porsi",
                None,
            ) or "Normal"

            menu = MenuMakanan(
                menu_db.nama,
                menu_db.harga,
                menu_db.stok,
                porsi,
            )

        elif kategori == "minuman":
            suhu = getattr(
                menu_db,
                "suhu",
                None,
            ) or "Dingin"

            menu = MenuMinuman(
                menu_db.nama,
                menu_db.harga,
                menu_db.stok,
                suhu,
            )

        else:
            print(
                f"Kategori menu '{menu_db.nama}' "
                "tidak dikenali."
            )
            continue

        warung.tambah_menu(menu)


def buat_menu_awal(
    warung: Warung,
) -> None:
    """
    Membuat menu awal jika database masih kosong.
    """
    nasi_rames = MenuMakanan(
        "Nasi Rames",
        15000,
        20,
        "Normal",
    )

    es_teh = MenuMinuman(
        "Es Teh",
        5000,
        30,
        "Dingin",
    )

    simpan_menu_kompatibel(
        nasi_rames,
        "makanan",
    )

    simpan_menu_kompatibel(
        es_teh,
        "minuman",
    )

    warung.tambah_menu(nasi_rames)
    warung.tambah_menu(es_teh)

    print(
        "Menu awal berhasil dibuat "
        "dan disimpan ke database."
    )


# =========================================================
# TAMPILKAN MENU
# =========================================================

def tampilkan_menu_dengan_konversi(
    warung: Warung,
) -> None:
    """
    Menampilkan menu beserta pilihan konversi
    harga ke mata uang asing.
    """
    print("\n===== DAFTAR MENU =====")

    if not warung._daftar_menu:
        print("Belum ada menu.")
        return

    mata_uang = input(
        "Tampilkan harga dalam mata uang asing "
        "(USD/JPY/EUR/SGD, kosongkan untuk melewati): "
    ).strip().upper()

    if not mata_uang:
        for nomor, menu in enumerate(
            warung._daftar_menu,
            start=1,
        ):
            kategori = (
                "Makanan"
                if isinstance(menu, MenuMakanan)
                else "Minuman"
            )

            print(
                f"{nomor}. {menu.nama} | "
                f"Rp{menu.harga:,.0f} | "
                f"Kategori: {kategori} | "
                f"Stok: {menu.stok}"
            )

        return

    try:
        for nomor, menu in enumerate(
            warung._daftar_menu,
            start=1,
        ):
            kategori = (
                "Makanan"
                if isinstance(menu, MenuMakanan)
                else "Minuman"
            )

            harga_asing = harga_dalam_mata_uang(
                menu.harga,
                mata_uang,
            )

            print(
                f"{nomor}. {menu.nama} | "
                f"Rp{menu.harga:,.0f} "
                f"(≈ {harga_asing}) | "
                f"Kategori: {kategori} | "
                f"Stok: {menu.stok}"
            )

    except ValueError as error:
        print(
            f"Mata uang tidak valid: {error}"
        )

    except ConnectionError as error:
        print(
            f"Gagal mengambil kurs: {error}"
        )


def tampilkan_menu_database() -> None:
    """
    Menampilkan menu yang tersimpan permanen
    di dalam database.
    """
    print("\n===== MENU DARI DATABASE =====")

    daftar_menu = ambil_semua_menu()

    if not daftar_menu:
        print("Database menu masih kosong.")
        return

    for nomor, menu in enumerate(
        daftar_menu,
        start=1,
    ):
        print(
            f"{nomor}. ID: {menu.id} | "
            f"{menu.nama} | "
            f"Rp{menu.harga:,.0f} | "
            f"Stok: {menu.stok} | "
            f"Kategori: {menu.kategori}"
        )


# =========================================================
# TAMBAH MENU
# =========================================================

def tambah_menu_cli(
    warung: Warung,
) -> None:
    """
    Menambahkan menu baru ke Warung dan database.
    """
    print("\n===== TAMBAH MENU =====")
    print("m. Makanan")
    print("n. Minuman")

    jenis = input(
        "Jenis menu (m/n): "
    ).strip().lower()

    if jenis not in ("m", "n"):
        print("Jenis menu tidak valid.")
        return

    nama = input(
        "Nama menu: "
    ).strip()

    if not nama:
        print("Nama menu tidak boleh kosong.")
        return

    menu_sudah_ada = any(
        menu.nama.strip().lower()
        == nama.lower()
        for menu in warung._daftar_menu
    )

    if menu_sudah_ada:
        print(
            f"Menu '{nama}' sudah tersedia."
        )
        return

    harga = float(
        input("Harga: ")
    )

    stok = int(
        input("Stok: ")
    )

    if harga < 0:
        print("Harga tidak boleh negatif.")
        return

    if stok < 0:
        print("Stok tidak boleh negatif.")
        return

    if jenis == "m":
        porsi = input(
            "Porsi: "
        ).strip() or "Normal"

        menu_baru = MenuMakanan(
            nama,
            harga,
            stok,
            porsi,
        )

        kategori = "makanan"

    else:
        suhu = input(
            "Suhu: "
        ).strip() or "Dingin"

        menu_baru = MenuMinuman(
            nama,
            harga,
            stok,
            suhu,
        )

        kategori = "minuman"

    try:
        # Simpan permanen ke database.
        simpan_menu_kompatibel(
            menu_baru,
            kategori,
        )

        # Masukkan ke objek Warung setelah database berhasil.
        warung.tambah_menu(
            menu_baru
        )

        print(
            f"Menu '{menu_baru.nama}' berhasil "
            "ditambahkan dan disimpan ke database."
        )

    except IntegrityError:
        print(
            f"Menu dengan nama '{nama}' "
            "sudah terdapat di database."
        )


# =========================================================
# PENGELOLAAN MEJA DAN PESANAN
# =========================================================

def buka_meja_cli(
    warung: Warung,
) -> None:
    """Membuka meja baru."""
    print("\n===== BUKA MEJA =====")

    nomor_meja = input(
        "Nomor meja: "
    ).strip()

    warung.buka_meja(
        nomor_meja
    )


def pesan_cli(
    warung: Warung,
) -> None:
    """
    Menambahkan pesanan dan menyimpan perubahan
    stok ke database.
    """
    print("\n===== BUAT PESANAN =====")

    nomor_meja = input(
        "Nomor meja: "
    ).strip()

    nama_menu = input(
        "Nama menu: "
    ).strip()

    jumlah = int(
        input("Jumlah: ")
    )

    if jumlah <= 0:
        print(
            "Jumlah pesanan harus lebih dari nol."
        )
        return

    warung.pesan(
        nomor_meja,
        nama_menu,
        jumlah,
    )

    menu = warung.cari_menu(
        nama_menu
    )

    update_stok_menu(
        menu.nama,
        menu.stok,
    )

    print(
        f"Stok '{menu.nama}' di database "
        f"diperbarui menjadi {menu.stok}."
    )


# =========================================================
# HELPER TRANSAKSI
# =========================================================

def ambil_daftar_item(
    pesanan: Any,
) -> list[Any]:
    """
    Mengambil seluruh ItemPesanan dari objek Pesanan.
    """
    kemungkinan_atribut = (
        "_items",
        "items",
        "_daftar_item",
        "daftar_item",
        "_daftar_items",
    )

    for nama_atribut in kemungkinan_atribut:
        nilai = getattr(
            pesanan,
            nama_atribut,
            None,
        )

        if isinstance(nilai, list):
            return nilai

    return []


def ambil_menu_item(
    item: Any,
) -> Any:
    """Mengambil objek menu dari ItemPesanan."""
    menu = getattr(
        item,
        "menu",
        None,
    )

    if menu is None:
        menu = getattr(
            item,
            "_menu",
            None,
        )

    return menu


def ambil_jumlah_item(
    item: Any,
) -> int:
    """Mengambil jumlah pesanan dari ItemPesanan."""
    jumlah = getattr(
        item,
        "jumlah",
        None,
    )

    if jumlah is None:
        jumlah = getattr(
            item,
            "_jumlah",
            0,
        )

    return int(jumlah)


def hitung_subtotal_item(
    item: Any,
) -> float:
    """Menghitung subtotal satu item pesanan."""
    method_subtotal = getattr(
        item,
        "subtotal",
        None,
    )

    if callable(method_subtotal):
        return float(
            method_subtotal()
        )

    menu = ambil_menu_item(item)
    jumlah = ambil_jumlah_item(item)

    if menu is None:
        return 0.0

    return float(
        menu.harga * jumlah
    )


def simpan_detail_transaksi(
    pesanan: Any,
) -> None:
    """
    Menyimpan setiap item transaksi ke database.
    """
    daftar_menu_database = ambil_semua_menu()

    menu_db_berdasarkan_nama = {
        menu.nama.strip().lower(): menu
        for menu in daftar_menu_database
    }

    waktu_transaksi = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    for item in ambil_daftar_item(pesanan):
        menu = ambil_menu_item(item)
        jumlah = ambil_jumlah_item(item)

        if menu is None:
            continue

        menu_db = menu_db_berdasarkan_nama.get(
            menu.nama.strip().lower()
        )

        if menu_db is None:
            raise ValueError(
                f"Menu '{menu.nama}' tidak ditemukan "
                "di database."
            )

        simpan_transaksi(
            menu_id=menu_db.id,
            nomor_meja=str(
                pesanan.nomor_meja
            ),
            jumlah=jumlah,
            subtotal=hitung_subtotal_item(item),
            waktu=waktu_transaksi,
        )


# =========================================================
# PEMBAYARAN
# =========================================================

def bayar_cli(
    warung: Warung,
) -> None:
    """
    Memproses pembayaran dan menyimpan transaksi
    secara permanen.
    """
    print("\n===== PEMBAYARAN =====")

    nomor_meja = input(
        "Nomor meja: "
    ).strip()

    pesanan = warung._pesanan_aktif.get(
        nomor_meja
    )

    if pesanan is None:
        raise MejaTidakDitemukanError(
            f"Meja {nomor_meja} belum dibuka."
        )

    total = pesanan.hitung_total()

    print(
        f"Total tagihan: Rp{total:,.0f}"
    )

    uang_bayar = float(
        input("Uang bayar: ")
    )

    if uang_bayar < total:
        kekurangan = total - uang_bayar

        print(
            f"Uang tidak cukup. "
            f"Kurang Rp{kekurangan:,.0f}."
        )
        return

    kembalian = warung.bayar(
        nomor_meja,
        uang_bayar,
    )

    simpan_detail_transaksi(
        pesanan
    )

    print(
        "Transaksi berhasil disimpan "
        "ke database."
    )

    print(
        f"Kembalian: Rp{kembalian:,.0f}"
    )


def tampilkan_transaksi_database() -> None:
    """
    Menampilkan seluruh transaksi yang tersimpan
    di database.
    """
    print("\n===== TRANSAKSI DARI DATABASE =====")

    daftar_transaksi = ambil_semua_transaksi()

    if not daftar_transaksi:
        print(
            "Belum ada transaksi di database."
        )
        return

    daftar_menu = ambil_semua_menu()

    nama_menu_berdasarkan_id = {
        menu.id: menu.nama
        for menu in daftar_menu
    }

    for nomor, transaksi in enumerate(
        daftar_transaksi,
        start=1,
    ):
        nama_menu = nama_menu_berdasarkan_id.get(
            transaksi.menu_id,
            f"Menu ID {transaksi.menu_id}",
        )

        print(
            f"{nomor}. Meja {transaksi.nomor_meja} | "
            f"{nama_menu} | "
            f"Jumlah: {transaksi.jumlah} | "
            f"Subtotal: Rp{transaksi.subtotal:,.0f} | "
            f"Waktu: {transaksi.waktu}"
        )


# =========================================================
# LAPORAN FUNCTIONAL PROGRAMMING
# =========================================================

def tampilkan_laporan_menu_tersedia(
    warung: Warung,
) -> None:
    """Menampilkan menu dengan stok lebih dari nol."""
    print("\n===== MENU TERSEDIA =====")

    hasil = menu_tersedia(
        warung._daftar_menu
    )

    if not hasil:
        print("Tidak ada menu yang tersedia.")
        return

    for nomor, menu in enumerate(
        hasil,
        start=1,
    ):
        print(
            f"{nomor}. {menu.nama} | "
            f"Rp{menu.harga:,.0f} | "
            f"Stok: {menu.stok}"
        )


def tampilkan_laporan_pendapatan(
    warung: Warung,
) -> None:
    """Menampilkan pendapatan berdasarkan kategori."""
    print("\n===== PENDAPATAN PER KATEGORI =====")

    hasil = pendapatan_per_kategori(
        warung._riwayat
    )

    print(
        "Pendapatan Makanan : "
        f"Rp{hasil.get('MenuMakanan', 0):,.0f}"
    )

    print(
        "Pendapatan Minuman : "
        f"Rp{hasil.get('MenuMinuman', 0):,.0f}"
    )

    total = (
        hasil.get("MenuMakanan", 0)
        + hasil.get("MenuMinuman", 0)
    )

    print(
        f"Total Pendapatan    : Rp{total:,.0f}"
    )


def tampilkan_laporan_riwayat(
    warung: Warung,
) -> None:
    """
    Menampilkan riwayat berdasarkan total terbesar.
    """
    print("\n===== RIWAYAT URUT TOTAL =====")

    hasil = riwayat_diurutkan_total(
        warung._riwayat
    )

    if not hasil:
        print("Belum ada riwayat transaksi.")
        return

    for nomor, pesanan in enumerate(
        hasil,
        start=1,
    ):
        print(
            f"{nomor}. Meja {pesanan.nomor_meja} | "
            f"Total: Rp{pesanan.hitung_total():,.0f}"
        )


def tampilkan_laporan_ringkasan(
    warung: Warung,
) -> None:
    """Menampilkan ringkasan setiap transaksi."""
    print("\n===== RINGKASAN TRANSAKSI =====")

    hasil = ringkasan_transaksi(
        warung._riwayat
    )

    if not hasil:
        print("Belum ada riwayat transaksi.")
        return

    for nomor, ringkasan in enumerate(
        hasil,
        start=1,
    ):
        print(
            f"{nomor}. {ringkasan}"
        )


def menu_laporan(
    warung: Warung,
) -> None:
    """Menampilkan empat submenu laporan."""
    while True:
        print("\n===== MENU LAPORAN =====")
        print("1. Menu Tersedia")
        print("2. Pendapatan per Kategori")
        print("3. Riwayat Diurutkan Berdasarkan Total")
        print("4. Ringkasan Transaksi")
        print("0. Kembali")

        pilihan = input(
            "Pilih laporan: "
        ).strip()

        if pilihan == "1":
            tampilkan_laporan_menu_tersedia(
                warung
            )

        elif pilihan == "2":
            tampilkan_laporan_pendapatan(
                warung
            )

        elif pilihan == "3":
            tampilkan_laporan_riwayat(
                warung
            )

        elif pilihan == "4":
            tampilkan_laporan_ringkasan(
                warung
            )

        elif pilihan == "0":
            return

        else:
            print("Pilihan laporan tidak valid.")


# =========================================================
# MENU UTAMA
# =========================================================

def menu_utama(
    warung: Warung,
) -> None:
    """Menjalankan menu utama aplikasi."""
    while True:
        print("\n=== WARUNG MAKAN BU TUTI ===")
        print("1. Tambah Menu")
        print("2. Tampilkan Menu")
        print("3. Buka Meja")
        print("4. Pesan")
        print("5. Bayar")
        print("6. Riwayat Transaksi Sesi")
        print("7. Tampilkan Menu dari Database")
        print("8. Tampilkan Transaksi dari Database")
        print("9. Laporan")
        print("0. Keluar")

        pilihan = input(
            "Pilih: "
        ).strip()

        try:
            if pilihan == "1":
                tambah_menu_cli(
                    warung
                )

            elif pilihan == "2":
                tampilkan_menu_dengan_konversi(
                    warung
                )

            elif pilihan == "3":
                buka_meja_cli(
                    warung
                )

            elif pilihan == "4":
                pesan_cli(
                    warung
                )

            elif pilihan == "5":
                bayar_cli(
                    warung
                )

            elif pilihan == "6":
                warung.tampilkan_riwayat()

            elif pilihan == "7":
                tampilkan_menu_database()

            elif pilihan == "8":
                tampilkan_transaksi_database()

            elif pilihan == "9":
                menu_laporan(
                    warung
                )

            elif pilihan == "0":
                print(
                    "Program selesai. "
                    "Data telah tersimpan di database."
                )
                return

            else:
                print("Pilihan tidak valid.")

        except (
            MejaSudahTerisiError,
            MejaTidakDitemukanError,
            MenuHabisError,
            MenuTidakDitemukanError,
            ValueError,
            TypeError,
        ) as error:
            print(
                f"Error: {error}"
            )

        except IntegrityError:
            print(
                "Error database: data dengan nilai "
                "yang sama sudah tersimpan."
            )

        except Exception as error:
            print(
                f"Terjadi kesalahan: {error}"
            )


# =========================================================
# PROGRAM UTAMA
# =========================================================

if __name__ == "__main__":
    # Membuat tabel database jika belum tersedia.
    init_db()

    warung = Warung()

    # Memuat seluruh menu lama dari database.
    muat_menu_dari_database(
        warung
    )

    # Menu awal hanya dibuat jika database benar-benar kosong.
    if not warung._daftar_menu:
        buat_menu_awal(
            warung
        )

    menu_utama(
        warung
    )