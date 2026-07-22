from models.menu import Menu
from models.pesanan import Pesanan
from exceptions.custom_exceptions import (
    MejaTidakDitemukanError,
    MenuTidakDitemukanError,
    MejaSudahTerisiError,
)


class Warung:
    """
    Controller utama aplikasi warung makan.

    Mengelola:
    - daftar menu;
    - pesanan aktif berdasarkan nomor meja;
    - riwayat pesanan yang sudah dibayar.
    """

    def __init__(self) -> None:
        # Menyimpan semua objek menu.
        self._daftar_menu: list[Menu] = []

        # Menyimpan pesanan aktif.
        # Format: nomor_meja -> objek Pesanan.
        self._pesanan_aktif: dict[str, Pesanan] = {}

        # Menyimpan pesanan yang sudah selesai dibayar.
        self._riwayat: list[Pesanan] = []

    # =========================================================
    # MENU
    # =========================================================

    def tambah_menu(self, menu: Menu) -> None:
        """
        Menambahkan objek menu ke daftar menu.
        """
        self._daftar_menu.append(menu)

    def cari_menu(self, nama: str) -> Menu:
        """
        Mencari menu berdasarkan nama.

        Pencarian tidak membedakan huruf besar dan kecil.

        Raises:
            MenuTidakDitemukanError:
                Jika menu dengan nama tersebut tidak tersedia.
        """
        for menu in self._daftar_menu:
            if menu.nama.lower() == nama.lower():
                return menu

        raise MenuTidakDitemukanError(
            f"Menu '{nama}' tidak ditemukan!"
        )

    def tampilkan_menu(self) -> None:
        """
        Menampilkan seluruh menu yang tersedia.
        """
        print("\n===== DAFTAR MENU =====")

        if not self._daftar_menu:
            print("Belum ada menu.")
            return

        for nomor, menu in enumerate(
            self._daftar_menu,
            start=1
        ):
            print(f"{nomor}. {menu}")

    # =========================================================
    # MEJA DAN PESANAN
    # =========================================================

    def buka_meja(self, nomor: str) -> None:
        """
        Membuka meja dan membuat pesanan aktif baru.

        Raises:
            MejaSudahTerisiError:
                Jika nomor meja sudah memiliki pesanan aktif.
        """
        if nomor in self._pesanan_aktif:
            raise MejaSudahTerisiError(
                f"Meja {nomor} sedang digunakan!"
            )

        pesanan_baru = Pesanan(nomor)
        self._pesanan_aktif[nomor] = pesanan_baru

        print(f"Meja {nomor} berhasil dibuka.")

    def pesan(
        self,
        nomor_meja: str,
        nama_menu: str,
        jumlah: int,
    ) -> None:
        """
        Menambahkan menu ke pesanan pada meja aktif.

        Proses:
        1. Memeriksa apakah meja sudah dibuka.
        2. Mencari menu berdasarkan nama.
        3. Mengurangi stok menu.
        4. Menambahkan item ke pesanan.

        Raises:
            MejaTidakDitemukanError:
                Jika meja belum dibuka.
            MenuTidakDitemukanError:
                Jika menu tidak ditemukan.

        Error stok diteruskan dari method menu.kurangi_stok().
        """
        if nomor_meja not in self._pesanan_aktif:
            raise MejaTidakDitemukanError(
                f"Meja {nomor_meja} belum dibuka!"
            )

        menu = self.cari_menu(nama_menu)

        # Method ini juga akan melakukan validasi stok.
        menu.kurangi_stok(jumlah)

        pesanan = self._pesanan_aktif[nomor_meja]
        pesanan.tambah_item(menu, jumlah)

        print(
            f"{jumlah} x {menu.nama} berhasil ditambahkan "
            f"ke meja {nomor_meja}."
        )

    # =========================================================
    # PEMBAYARAN
    # =========================================================

    def bayar(
        self,
        nomor_meja: str,
        uang: float,
    ) -> None:
        """
        Memproses pembayaran pesanan.

        Pesanan yang berhasil dibayar akan:
        - dipindahkan ke riwayat;
        - dihapus dari daftar pesanan aktif.
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

        # Pindahkan pesanan ke riwayat.
        self._riwayat.append(pesanan)

        # Hapus pesanan dari daftar pesanan aktif.
        del self._pesanan_aktif[nomor_meja]

        print("\n===== PEMBAYARAN =====")
        print(f"Total      : Rp {total:,.0f}")
        print(f"Bayar      : Rp {uang:,.0f}")
        print(f"Kembalian  : Rp {kembalian:,.0f}")
        print("Pembayaran berhasil!")

    # =========================================================
    # RIWAYAT
    # =========================================================

    def tampilkan_riwayat(self) -> None:
        """
        Menampilkan seluruh pesanan yang telah dibayar.
        """
        print("\n===== RIWAYAT PESANAN =====")

        if not self._riwayat:
            print("Belum ada riwayat.")
            return

        for nomor, pesanan in enumerate(
            self._riwayat,
            start=1
        ):
            print(f"\nRiwayat #{nomor}")
            print(pesanan)