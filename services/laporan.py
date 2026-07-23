"""
Fungsi laporan Sistem Manajemen Warung Makan.

Seluruh proses menggunakan functional programming:
- map
- filter
- sorted

Tidak menggunakan loop eksplisit.
"""

from models.menu import MenuMakanan, MenuMinuman


def _daftar_item(pesanan) -> list:
    """
    Mengambil daftar item dari objek Pesanan.

    Mendukung beberapa kemungkinan nama atribut agar
    kompatibel dengan struktur class Pesanan.
    """
    nama_atribut = (
        "_items",
        "items",
        "_daftar_item",
        "daftar_item",
        "_daftar_items",
    )

    kandidat = map(
        lambda nama: getattr(pesanan, nama, None),
        nama_atribut,
    )

    return next(
        filter(
            lambda nilai: isinstance(nilai, list),
            kandidat,
        ),
        [],
    )


def _menu_dari_item(item):
    """
    Mengambil objek menu dari ItemPesanan.
    """
    kandidat = map(
        lambda nama: getattr(item, nama, None),
        ("menu", "_menu"),
    )

    return next(
        filter(
            lambda nilai: nilai is not None,
            kandidat,
        ),
        None,
    )


def _jumlah_dari_item(item) -> int:
    """
    Mengambil jumlah pembelian dari ItemPesanan.
    """
    kandidat = map(
        lambda nama: getattr(item, nama, None),
        ("jumlah", "_jumlah"),
    )

    hasil = next(
        filter(
            lambda nilai: nilai is not None,
            kandidat,
        ),
        0,
    )

    return int(hasil)


def _subtotal_item(item) -> float:
    """
    Mengambil subtotal dari ItemPesanan.
    """
    kandidat_method = filter(
        callable,
        map(
            lambda nama: getattr(item, nama, None),
            ("subtotal", "hitung_subtotal"),
        ),
    )

    method_subtotal = next(
        kandidat_method,
        None,
    )

    if method_subtotal is not None:
        return float(method_subtotal())

    menu = _menu_dari_item(item)
    jumlah = _jumlah_dari_item(item)

    if menu is None:
        return 0.0

    return float(menu.harga * jumlah)


def menu_tersedia(daftar_menu: list) -> list:
    """
    Mengambil menu yang stoknya masih tersedia.

    Hasil diurutkan dari harga paling murah.
    """
    menu_stok_ada = filter(
        lambda menu: menu.stok > 0,
        daftar_menu,
    )

    return sorted(
        menu_stok_ada,
        key=lambda menu: menu.harga,
    )


def pendapatan_per_kategori(
    daftar_riwayat: list,
) -> dict:
    """
    Menghitung pendapatan berdasarkan kategori menu.

    Return:
        {
            "MenuMakanan": total,
            "MenuMinuman": total
        }
    """
    seluruh_daftar_item = map(
        _daftar_item,
        daftar_riwayat,
    )

    seluruh_item = list(
        map(
            lambda item: item,
            sum(seluruh_daftar_item, []),
        )
    )

    item_makanan = filter(
        lambda item: isinstance(
            _menu_dari_item(item),
            MenuMakanan,
        ),
        seluruh_item,
    )

    item_minuman = filter(
        lambda item: isinstance(
            _menu_dari_item(item),
            MenuMinuman,
        ),
        seluruh_item,
    )

    total_makanan = sum(
        map(
            _subtotal_item,
            item_makanan,
        )
    )

    total_minuman = sum(
        map(
            _subtotal_item,
            item_minuman,
        )
    )

    return {
        "MenuMakanan": total_makanan,
        "MenuMinuman": total_minuman,
    }


def riwayat_diurutkan_total(
    daftar_riwayat: list,
) -> list:
    """
    Mengurutkan riwayat dari total tagihan terbesar
    menuju total tagihan terkecil.
    """
    return sorted(
        daftar_riwayat,
        key=lambda pesanan: pesanan.hitung_total(),
        reverse=True,
    )


def ringkasan_transaksi(
    daftar_riwayat: list,
) -> list[str]:
    """
    Mengubah setiap pesanan menjadi ringkasan teks.
    """

    def buat_ringkasan(pesanan) -> str:
        daftar_item = _daftar_item(pesanan)

        jumlah_item = sum(
            map(
                _jumlah_dari_item,
                daftar_item,
            )
        )

        total = pesanan.hitung_total()

        return (
            f"Meja {pesanan.nomor_meja} — "
            f"Total: Rp{total:,.0f} — "
            f"{jumlah_item} item"
        )

    return list(
        map(
            buat_ringkasan,
            daftar_riwayat,
        )
    )