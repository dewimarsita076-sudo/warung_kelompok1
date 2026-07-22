"""Class pesanan."""

from datetime import datetime

from models.meja import MejaTerisi, MejaKosong
from models.menu import Menu


class ItemPesanan:
    """Representasi item pesanan."""

    def __init__(self, menu: Menu, jumlah: int) -> None:
        self.menu = menu
        self.jumlah = jumlah

    def subtotal(self) -> float:
        return self.menu.harga * self.jumlah

    def __str__(self) -> str:
        return (
            f"{self.menu.nama} x {self.jumlah}"
            f" = Rp{self.subtotal():,.0f}"
        )


class Pesanan:
    """Pesanan satu meja."""

    def __init__(self, nomor_meja: str) -> None:
        self.nomor_meja = nomor_meja
        self._items = []

        self.status = MejaTerisi(
            datetime.now().strftime("%H:%M")
        )

    def tambah_item(
        self,
        menu: Menu,
        jumlah: int
    ) -> None:
        self._items.append(
            ItemPesanan(menu, jumlah)
        )

    def hitung_total(self) -> float:
        return sum(
            item.subtotal()
            for item in self._items
        )

    def selesai(self) -> float:
        total = self.hitung_total()
        self.status = MejaKosong()
        return total

    def __str__(self) -> str:
        teks = f"\nMeja {self.nomor_meja}\n"

        for item in self._items:
            teks += str(item) + "\n"

        teks += f"Total: Rp{self.hitung_total():,.0f}"

        return teks