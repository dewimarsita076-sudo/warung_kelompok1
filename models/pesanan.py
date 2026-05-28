from datetime import datetime
from models.menu import Menu


# HELPER CLASS : ITEM PESANAN
class ItemPesanan:
    """
    Class kecil sebagai pasangan menu + jumlah
    """

    def __init__(self, menu, jumlah):
        self.menu = menu
        self.jumlah = jumlah

    def subtotal(self):
        """
        Menghitung subtotal item
        """
        return self.menu.harga * self.jumlah

    def __str__(self):
        return (
            f"{self.menu.nama:<20} "
            f"x {self.jumlah:<3} "
            f"= Rp{self.subtotal():,}"
        )


# CLASS STATUS MEJA
class StatusMeja:
    KOSONG = "Kosong"
    TERISI = "Terisi"
    SELESAI = "Selesai"


# CLASS PESANAN
class Pesanan:
    """
    Mengelola seluruh item pesanan dalam satu meja
    """

    pajak = 0.10  # 10%

    def __init__(self, nomor_meja):
        self.nomor_meja = nomor_meja
        self._items = []
        self.status = StatusMeja.TERISI
        self.waktu_pesan = datetime.now()

    # METHOD TAMBAH ITEM
    def tambah_item(self, menu, jumlah):
        """
        Menambahkan item pesanan
        """

        # Validasi jumlah
        if jumlah <= 0:
            print("Jumlah harus lebih dari 0")
            return

        # Cek apakah menu sudah ada
        for item in self._items:
            if item.menu.kode == menu.kode:
                item.jumlah += jumlah
                return

        # Jika belum ada
        item_baru = ItemPesanan(menu, jumlah)
        self._items.append(item_baru)

    # METHOD HAPUS ITEM
    def hapus_item(self, kode_menu):
        """
        Menghapus item berdasarkan kode menu
        """

        for item in self._items:
            if item.menu.kode == kode_menu:
                self._items.remove(item)
                print(f"Menu {item.menu.nama} berhasil dihapus")
                return

        print("Menu tidak ditemukan")

    # METHOD HITUNG TOTAL
    def hitung_total(self):
        """
        Menghitung total seluruh subtotal item
        """
        return sum(item.subtotal() for item in self._items)

    # METHOD HITUNG PAJAK
    def hitung_pajak(self):
        return self.hitung_total() * Pesanan.pajak

    # METHOD TOTAL BAYAR
    def total_bayar(self):
        return self.hitung_total() + self.hitung_pajak()

    # METHOD TAMPILKAN STRUK
    def tampilkan_struk(self):

        garis = "=" * 50

        daftar_item = "\n".join(
            [str(item) for item in self._items]
        )

        return (
            f"{garis}\n"
            f"          RESTORAN SEDERHANA\n"
            f"{garis}\n"
            f"Nomor Meja : {self.nomor_meja}\n"
            f"Waktu      : {self.waktu_pesan.strftime('%d-%m-%Y %H:%M:%S')}\n"
            f"Status     : {self.status}\n"
            f"{garis}\n"
            f"DAFTAR PESANAN\n"
            f"{garis}\n"
            f"{daftar_item}\n"
            f"{garis}\n"
            f"Subtotal   : Rp{self.hitung_total():,}\n"
            f"Pajak 10%  : Rp{self.hitung_pajak():,}\n"
            f"Total Bayar: Rp{self.total_bayar():,}\n"
            f"{garis}"
        )

    # METHOD SELESAI
    def selesai(self):
        """
        Menyelesaikan transaksi
        """

        self.status = StatusMeja.SELESAI

        print("\nTRANSAKSI BERHASIL DISELESAIKAN")
        print(f"Total Pembayaran : Rp{self.total_bayar():,}")

    # METHOD STR
    def __str__(self):
        return self.tampilkan_struk()


# PROGRAM UTAMA
if __name__ == "__main__":

    # DATA MENU
    menu1 = Menu("M01", "Nasi Goreng", 18000, "Makanan")
    menu2 = Menu("M02", "Mie Ayam", 15000, "Makanan")
    menu3 = Menu("M03", "Ayam Geprek", 20000, "Makanan")
    menu4 = Menu("D01", "Es Teh", 5000, "Minuman")
    menu5 = Menu("D02", "Jus Alpukat", 12000, "Minuman")

    # TAMPILKAN MENU
    print("=" * 50)
    print("              DAFTAR MENU")
    print("=" * 50)

    daftar_menu = [menu1, menu2, menu3, menu4, menu5]

    for menu in daftar_menu:
        print(menu)

    print("=" * 50)

    # MEMBUAT PESANAN
    pesanan1 = Pesanan("A01")

    # Tambah item
    pesanan1.tambah_item(menu1, 2)
    pesanan1.tambah_item(menu4, 3)
    pesanan1.tambah_item(menu5, 1)

    # Tambah menu yang sama
    pesanan1.tambah_item(menu1, 1)

    # Hapus item
    pesanan1.hapus_item("D02")

    # TAMPILKAN STRUK
    print("\n")
    print(pesanan1)

    # SELESAIKAN TRANSAKSI
    pesanan1.selesai()
    print(f"Status Meja Sekarang : {pesanan1.status}")