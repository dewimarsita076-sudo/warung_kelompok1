"""Berisi custom exception untuk sistem manajemen warung makan."""
class MenuHabisError(Exception):
    """Exception saat stok menu tidak mencukupi."""
    pass


class MejaTidakDitemukanError(Exception):
    """Exception saat nomor meja tidak ditemukan."""
    pass


class MejaSudahTerisiError(Exception):
    """Exception saat meja sudah terisi."""
    pass


class MenuTidakDitemukanError(Exception):
    """Exception saat menu tidak ditemukan."""
    pass