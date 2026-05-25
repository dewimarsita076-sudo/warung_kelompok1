from models.pesanan import (
    Menu,
    Pesanan,
    StatusMeja
)


# CUSTOM ERROR
class MenuTidakDitemukanError(Exception):
    pass


class MejaSudahTerisiError(Exception):
    pass


# CLASS WARUNG
class Warung:
    """
    Controller utama sistem warung makan
    Mengelola:
    - daftar menu
    - pesanan aktif
    - riwayat transaksi
    """

    def __init__(self):

        # List semua menu
        self._daftar_menu = []

        # Dict nomor meja -> pesanan aktif
        self._pesanan_aktif = {}

        # Riwayat transaksi selesai
        self._riwayat = []

    # METHOD TAMBAH MENU
    def tambah_menu(self, menu):
        """
        Menambahkan menu ke daftar menu
        """

        self._daftar_menu.append(menu)

    # METHOD CARI MENU
    def cari_menu(self, nama):
        """
        Mencari menu berdasarkan nama
        """

        for menu in self._daftar_menu:
            if menu.nama.lower() == nama.lower():
                return menu

        raise MenuTidakDitemukanError(
            f"Menu '{nama}' tidak ditemukan"
        )

    # METHOD TAMPILKAN MENU
    def tampilkan_menu(self):

        print("\n" + "=" * 50)
        print("              DAFTAR MENU")
        print("=" * 50)

        for menu in self._daftar_menu:
            print(menu)

        print("=" * 50)

    # METHOD BUKA MEJA
    def buka_meja(self, nomor):
        """
        Membuka meja baru
        """

        if nomor in self._pesanan_aktif:
            raise MejaSudahTerisiError(
                f"Meja {nomor} sedang digunakan"
            )

        pesanan_baru = Pesanan(nomor)

        self._pesanan_aktif[nomor] = pesanan_baru

        print(f"\nMeja {nomor} berhasil dibuka")

    # METHOD PESAN
    def pesan(self, nomor_meja, nama_menu, jumlah):
        """
        Menambahkan pesanan ke meja tertentu
        """

        # Cari pesanan aktif
        if nomor_meja not in self._pesanan_aktif:
            print("Meja belum dibuka")
            return

        # Cari menu
        try:
            menu = self.cari_menu(nama_menu)

        except MenuTidakDitemukanError as e:
            print(e)
            return

        # Tambahkan item
        pesanan = self._pesanan_aktif[nomor_meja]

        pesanan.tambah_item(menu, jumlah)

        print(
            f"{menu.nama} sebanyak {jumlah} berhasil ditambahkan"
        )

    # METHOD BAYAR
    def bayar(self, nomor_meja, uang):
        """
        Menyelesaikan pembayaran
        """

        # Cek meja
        if nomor_meja not in self._pesanan_aktif:
            print("Pesanan meja tidak ditemukan")
            return

        pesanan = self._pesanan_aktif[nomor_meja]

        total = pesanan.total_bayar()

        print("\n" + pesanan.tampilkan_struk())

        print(f"\nUang Bayar : Rp{uang:,}")

        # Validasi uang
        if uang < total:
            print("Uang tidak cukup")
            return

        kembalian = uang - total

        print(f"Kembalian : Rp{kembalian:,}")

        # Selesaikan transaksi
        pesanan.selesai()

        # Pindahkan ke riwayat
        self._riwayat.append(pesanan)

        # Hapus dari pesanan aktif
        del self._pesanan_aktif[nomor_meja]

    # METHOD TAMPILKAN RIWAYAT
    def tampilkan_riwayat(self):

        print("\n" + "=" * 50)
        print("           RIWAYAT TRANSAKSI")
        print("=" * 50)

        if len(self._riwayat) == 0:
            print("Belum ada transaksi")
            return

        for i, pesanan in enumerate(self._riwayat, start=1):

            print(f"\nTRANSAKSI #{i}")
            print(pesanan)
            print("-" * 50)


# PROGRAM UTAMA
if __name__ == "__main__":

    # MEMBUAT OBJECT WARUNG
    warung = Warung()

    # TAMBAH MENU
    warung.tambah_menu(
        Menu("M01", "Nasi Goreng", 18000, "Makanan")
    )

    warung.tambah_menu(
        Menu("M02", "Mie Ayam", 15000, "Makanan")
    )

    warung.tambah_menu(
        Menu("M03", "Ayam Geprek", 20000, "Makanan")
    )

    warung.tambah_menu(
        Menu("D01", "Es Teh", 5000, "Minuman")
    )

    warung.tambah_menu(
        Menu("D02", "Jus Alpukat", 12000, "Minuman")
    )

    # TAMPILKAN MENU
    warung.tampilkan_menu()

    # BUKA MEJA
    warung.buka_meja("A01")

    # PESAN MAKANAN
    warung.pesan("A01", "Nasi Goreng", 2)
    warung.pesan("A01", "Es Teh", 3)
    warung.pesan("A01", "Jus Alpukat", 1)

    # BAYAR
    warung.bayar("A01", 100000)

    # TAMPILKAN RIWAYAT
    warung.tampilkan_riwayat()