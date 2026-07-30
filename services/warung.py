"""Service utama Sistem Manajemen Warung Makan."""

from __future__ import annotations

from typing import Any

from exceptions.custom_exceptions import (
    MejaSudahTerisiError,
    MejaTidakDitemukanError,
    MenuTidakDitemukanError,
)
from models.pesanan import Pesanan


class Warung:
    """
    Mengelola menu, meja, pesanan, pembayaran,
    dan riwayat transaksi di dalam memori.

    Penyimpanan ke database dilakukan melalui main.py,
    bukan langsung dari class Warung.
    """

    def __init__(self) -> None:
        """Membuat objek Warung dengan data awal kosong."""
        self._daftar_menu: list[Any] = []
        self._pesanan_aktif: dict[str, Pesanan] = {}
        self._riwayat: list[Pesanan] = []

    # =====================================================
    # PENGELOLAAN MENU
    # =====================================================

    def tambah_menu(self, menu: Any) -> None:
        """
        Menambahkan objek menu ke daftar menu di memori.

        Method ini tidak menyimpan menu ke database.
        Penyimpanan database dilakukan melalui main.py.
        """
        nama_menu = str(menu.nama).strip()

        if not nama_menu:
            raise ValueError(
                "Nama menu tidak boleh kosong."
            )

        menu_sama = any(
            str(menu_lama.nama).strip().lower()
            == nama_menu.lower()
            for menu_lama in self._daftar_menu
        )

        if menu_sama:
            raise ValueError(
                f"Menu '{nama_menu}' sudah tersedia."
            )

        self._daftar_menu.append(menu)

    def cari_menu(self, nama_menu: str) -> Any:
        """
        Mencari menu berdasarkan nama.

        Pencarian tidak membedakan huruf besar dan kecil.

        Raises:
            MenuTidakDitemukanError:
                Jika menu tidak ditemukan.
        """
        nama_dicari = str(nama_menu).strip().lower()

        for menu in self._daftar_menu:
            if str(menu.nama).strip().lower() == nama_dicari:
                return menu

        raise MenuTidakDitemukanError(
            f"Menu '{nama_menu}' tidak ditemukan."
        )

    def tampilkan_menu(self) -> None:
        """Menampilkan seluruh menu yang tersedia."""
        print("\n===== DAFTAR MENU =====")

        if not self._daftar_menu:
            print("Belum ada menu.")
            return

        for nomor, menu in enumerate(
            self._daftar_menu,
            start=1,
        ):
            print(
                f"{nomor}. {menu.nama} | "
                f"Rp{menu.harga:,.0f} | "
                f"Stok: {menu.stok}"
            )

    # =====================================================
    # PENGELOLAAN MEJA
    # =====================================================

    def buka_meja(self, nomor_meja: str) -> None:
        """
        Membuka meja dan membuat pesanan aktif baru.

        Raises:
            MejaSudahTerisiError:
                Jika meja sudah mempunyai pesanan aktif.
        """
        nomor_meja = str(nomor_meja).strip()

        if not nomor_meja:
            raise ValueError(
                "Nomor meja tidak boleh kosong."
            )

        if nomor_meja in self._pesanan_aktif:
            raise MejaSudahTerisiError(
                f"Meja {nomor_meja} sudah terisi."
            )

        self._pesanan_aktif[nomor_meja] = Pesanan(
            nomor_meja
        )

        print(
            f"Meja {nomor_meja} berhasil dibuka."
        )

    def tampilkan_pesanan_aktif(self) -> None:
        """Menampilkan seluruh pesanan yang masih aktif."""
        print("\n===== PESANAN AKTIF =====")

        if not self._pesanan_aktif:
            print("Tidak ada pesanan aktif.")
            return

        for nomor_meja, pesanan in (
            self._pesanan_aktif.items()
        ):
            print(
                f"\nMeja {nomor_meja}"
            )
            print(pesanan)

    # =====================================================
    # PEMESANAN
    # =====================================================

    def pesan(
        self,
        nomor_meja: str,
        nama_menu: str,
        jumlah: int,
    ) -> None:
        """
        Menambahkan menu ke pesanan pada meja aktif.

        Method ini mengurangi stok objek menu di memori.
        Penyimpanan perubahan stok ke database dilakukan
        oleh main.py.

        Raises:
            MejaTidakDitemukanError:
                Jika meja belum dibuka.
            MenuTidakDitemukanError:
                Jika menu tidak ditemukan.
            ValueError:
                Jika jumlah pesanan tidak valid.
        """
        nomor_meja = str(nomor_meja).strip()

        if nomor_meja not in self._pesanan_aktif:
            raise MejaTidakDitemukanError(
                f"Meja {nomor_meja} belum dibuka."
            )

        if not isinstance(jumlah, int):
            raise TypeError(
                "Jumlah pesanan harus berupa bilangan bulat."
            )

        if jumlah <= 0:
            raise ValueError(
                "Jumlah pesanan harus lebih dari nol."
            )

        menu = self.cari_menu(nama_menu)

        # Method kurangi_stok() melakukan validasi stok.
        menu.kurangi_stok(jumlah)

        pesanan = self._pesanan_aktif[nomor_meja]

        pesanan.tambah_item(
            menu,
            jumlah,
        )

        print(
            f"{jumlah} x {menu.nama} berhasil "
            f"ditambahkan ke meja {nomor_meja}."
        )

    # =====================================================
    # PEMBAYARAN
    # =====================================================

    def bayar(
        self,
        nomor_meja: str,
        uang_bayar: float,
    ) -> float:
        """
        Memproses pembayaran pesanan.

        Pesanan yang selesai dipindahkan dari
        _pesanan_aktif ke _riwayat.

        Returns:
            Nilai kembalian pelanggan.

        Raises:
            MejaTidakDitemukanError:
                Jika meja belum dibuka.
            ValueError:
                Jika uang pembayaran tidak mencukupi.
        """
        nomor_meja = str(nomor_meja).strip()

        if nomor_meja not in self._pesanan_aktif:
            raise MejaTidakDitemukanError(
                f"Meja {nomor_meja} belum dibuka."
            )

        pesanan = self._pesanan_aktif[nomor_meja]
        total = pesanan.hitung_total()

        if uang_bayar < total:
            kekurangan = total - uang_bayar

            raise ValueError(
                f"Uang pembayaran kurang "
                f"Rp{kekurangan:,.0f}."
            )

        kembalian = uang_bayar - total

        # Simpan ke riwayat di dalam memori.
        self._riwayat.append(pesanan)

        # Meja kembali kosong setelah pembayaran.
        del self._pesanan_aktif[nomor_meja]

        print("\n===== PEMBAYARAN BERHASIL =====")
        print(f"Meja       : {nomor_meja}")
        print(f"Total      : Rp{total:,.0f}")
        print(f"Uang bayar : Rp{uang_bayar:,.0f}")
        print(f"Kembalian  : Rp{kembalian:,.0f}")

        return kembalian

    # =====================================================
    # RIWAYAT TRANSAKSI
    # =====================================================

    def tampilkan_riwayat(self) -> None:
        """Menampilkan riwayat transaksi yang selesai."""
        print("\n===== RIWAYAT TRANSAKSI =====")

        if not self._riwayat:
            print("Belum ada riwayat transaksi.")
            return

        for nomor, pesanan in enumerate(
            self._riwayat,
            start=1,
        ):
            print(
                f"\nTransaksi {nomor}"
            )
            print(pesanan)