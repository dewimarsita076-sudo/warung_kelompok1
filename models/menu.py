"""Modul model menu untuk sistem manajemen warung makan."""

from exceptions.custom_exceptions import MenuHabisError
from exceptions.custom_exceptions import MenuTidakDitemukanError

class Menu:
    """Representasi dasar untuk semua item menu warung."""

    def __init__(self, nama: str, harga: float, stok: int) -> None:
        """
        Membuat objek menu dengan nama, harga, dan stok.

        Args:
            nama: Nama menu.
            harga: Harga satuan menu.
            stok: Jumlah stok menu.
        """
        self.nama = nama
        self._harga = 0.0
        self._stok = 0
        self.harga = harga
        self.stok = stok

    @property
    def harga(self) -> float:
        """Mengambil nilai harga menu."""
        return self._harga

    @harga.setter
    def harga(self, nilai: float) -> None:
        """
        Mengatur harga menu.

        Raises:
            ValueError: Jika harga bernilai negatif.
        """
        if nilai < 0:
            raise ValueError("Harga tidak boleh negatif.")
        self._harga = nilai

    @property
    def stok(self) -> int:
        """Mengambil jumlah stok menu."""
        return self._stok

    @stok.setter
    def stok(self, nilai: int) -> None:
        """
        Mengatur stok menu.

        Raises:
            ValueError: Jika stok bernilai negatif.
        """
        if nilai < 0:
            raise ValueError("Stok tidak boleh negatif.")
        self._stok = nilai

    def kurangi_stok(self, jumlah: int) -> None:
        """
        Mengurangi stok menu sesuai jumlah pesanan.

        Args:
            jumlah: Jumlah menu yang dipesan.

        Raises:
            ValueError: Jika jumlah pesanan <= 0.
            MenuHabisError: Jika stok tidak mencukupi.
        """
        if jumlah <= 0:
            raise ValueError("Jumlah pesanan harus lebih dari 0.")

        if jumlah > self._stok:
            raise MenuHabisError(
                f"Stok {self.nama} tidak mencukupi. Sisa stok: {self._stok}."
            )

        self._stok -= jumlah

    def __str__(self) -> str:
        """Mengembalikan informasi menu dalam bentuk teks."""
        return f"{self.nama} | Rp{self.harga:,.0f} | Stok: {self.stok}"


class MenuMakanan(Menu):
    """Representasi menu makanan dengan tambahan informasi porsi."""

    def __init__(self, nama: str, harga: float, stok: int, porsi: str) -> None:
        """
        Membuat objek menu makanan.

        Args:
            nama: Nama makanan.
            harga: Harga makanan.
            stok: Jumlah stok makanan.
            porsi: Ukuran atau deskripsi porsi makanan.
        """
        super().__init__(nama, harga, stok)
        self.porsi = porsi

    def __str__(self) -> str:
        """Mengembalikan informasi menu makanan dalam bentuk teks."""
        return f"{super().__str__()} | Porsi: {self.porsi}"


class MenuMinuman(Menu):
    """Representasi menu minuman dengan tambahan informasi suhu."""

    def __init__(self, nama: str, harga: float, stok: int, suhu: str) -> None:
        """
        Membuat objek menu minuman.

        Args:
            nama: Nama minuman.
            harga: Harga minuman.
            stok: Jumlah stok minuman.
            suhu: Jenis suhu minuman, misalnya Panas, Dingin, atau Es.
        """
        super().__init__(nama, harga, stok)
        self.suhu = suhu

    def __str__(self) -> str:
        """Mengembalikan informasi menu minuman dalam bentuk teks."""
        return f"{super().__str__()} | Suhu: {self.suhu}"