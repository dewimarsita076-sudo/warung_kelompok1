from exceptions.custom_exceptions import MenuHabisError

class Menu:
    """Representasi satu item menu warung."""
    def __init__(self, nama: str, harga: float, stok: int) -> None:
        self.nama   = nama
        self._harga = 0.0
        self._stok  = 0
        self.harga  = harga
        self.stok   = stok


    @property
    def harga(self) -> float: return self._harga
    @harga.setter
    def harga(self, v: float) -> None:
        if v < 0: raise ValueError('Harga tidak boleh negatif.')
        self._harga = v


    @property
    def stok(self) -> int: return self._stok
    @stok.setter
    def stok(self, v: int) -> None:
        if v < 0: raise ValueError('Stok tidak boleh negatif.')
        self._stok = v


    def kurangi_stok(self, jumlah: int) -> None:
        """Raise MenuHabisError jika stok tidak mencukupi."""
        if jumlah > self._stok:
            raise MenuHabisError(f'{self.nama} hanya tersisa {self._stok} porsi.')
        self._stok -= jumlah


    def __str__(self) -> str:
        return f'{self.nama} | Rp{self.harga:,.0f} | Stok: {self.stok}'

