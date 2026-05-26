from models.menu import Menu
from models.pesanan import Pesanan
from exceptions.custom_exceptions import (
    MenuTidakDitemukanError,
    MejaSudahTerisiError
)


class Warung:
    """
    Controller utama aplikasi warung makan.
    Mengelola:
    - daftar menu
    - pesanan aktif
    - riwayat pesanan
    """

    def __init__(self):
        # List semua menu
        self._daftar_menu = []

        # Dict nomor_meja -> pesanan aktif
        self._pesanan_aktif = {}

        # List pesanan selesai
        self._riwayat = []

    # =========================
    # MENU
    # =========================

    def tambah_menu(self, menu):
        """
        Menambahkan menu ke daftar menu
        """
        self._daftar_menu.append(menu)

    def cari_menu(self, nama):
        """
        Mencari menu berdasarkan nama
        """
        for menu in self._daftar_menu:
            if menu.nama.lower() == nama.lower():
                return menu

        raise MenuTidakDitemukanError(
            f"Menu '{nama}' tidak ditemukan!"
        )

    def tampilkan_menu(self):
        """
        Menampilkan semua menu
        """
        print("\n===== DAFTAR MENU =====")

        if not self._daftar_menu:
            print("Belum ada menu.")
            return

        for i, menu in enumerate(self._daftar_menu, start=1):
            print(f"{i}. {menu}")

    # =========================
    # PESANAN
    # =========================

    def buka_meja(self, nomor):
        """
        Membuka meja baru
        """

        if nomor in self._pesanan_aktif:
            raise MejaSudahTerisiError(
                f"Meja {nomor} sedang digunakan!"
            )

        pesanan_baru = Pesanan(nomor)
        self._pesanan_aktif[nomor] = pesanan_baru

        print(f"Meja {nomor} berhasil dibuka.")

    def pesan(self, nomor_meja, nama_menu, jumlah):
        """
        Menambahkan pesanan ke meja
        """

        if nomor_meja not in self._pesanan_aktif:
            print(f"Meja {nomor_meja} belum dibuka!")
            return

        # Cari menu
        menu = self.cari_menu(nama_menu)

        # Kurangi stok
        menu.kurangi_stok(jumlah)

        # Tambahkan ke pesanan
        pesanan = self._pesanan_aktif[nomor_meja]
        pesanan.tambah_item(menu, jumlah)

        print(
            f"{jumlah}x {menu.nama} berhasil ditambahkan "
            f"ke meja {nomor_meja}"
        )

    def bayar(self, nomor_meja, uang):
        """
        Membayar pesanan
        """

        if nomor_meja not in self._pesanan_aktif:
            print(f"Meja {nomor_meja} tidak ditemukan!")
            return

        pesanan = self._pesanan_aktif[nomor_meja]

        total = pesanan.hitung_total()

        if uang < total:
            print("Uang tidak cukup!")
            return

        kembalian = uang - total

        # Pindahkan ke riwayat
        self._riwayat.append(pesanan)

        # Hapus dari pesanan aktif
        del self._pesanan_aktif[nomor_meja]

        print("\n===== PEMBAYARAN =====")
        print(f"Total      : Rp {total}")
        print(f"Bayar      : Rp {uang}")
        print(f"Kembalian  : Rp {kembalian}")
        print("Pembayaran berhasil!")

    # =========================
    # RIWAYAT
    # =========================

    def tampilkan_riwayat(self):
        """
        Menampilkan semua riwayat pesanan
        """

        print("\n===== RIWAYAT PESANAN =====")

        if not self._riwayat:
            print("Belum ada riwayat.")
            return

        for i, pesanan in enumerate(self._riwayat, start=1):
            print(f"\nRiwayat #{i}")
            print(pesanan)