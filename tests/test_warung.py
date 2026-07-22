"""Unit test untuk Sistem Manajemen Warung Makan."""

import sys
from pathlib import Path

import pytest

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from exceptions.custom_exceptions import (
    MejaSudahTerisiError,
    MejaTidakDitemukanError,
    MenuHabisError,
    MenuTidakDitemukanError,
)
from models.meja import MejaKosong, MejaTerisi
from models.menu import Menu, MenuMakanan, MenuMinuman
from models.pesanan import ItemPesanan
from services.warung import Warung


@pytest.fixture
def menu_makanan() -> MenuMakanan:
    """Menyediakan objek menu makanan untuk pengujian."""
    return MenuMakanan("Nasi Rames", 15000, 10, "Porsi normal")


@pytest.fixture
def menu_minuman() -> MenuMinuman:
    """Menyediakan objek menu minuman untuk pengujian."""
    return MenuMinuman("Es Teh", 5000, 20, "Dingin")


@pytest.fixture
def warung_dengan_menu() -> Warung:
    """Menyediakan objek warung yang sudah memiliki beberapa menu."""
    warung = Warung()
    warung.tambah_menu(MenuMakanan("Nasi Rames", 15000, 10, "Porsi normal"))
    warung.tambah_menu(MenuMinuman("Es Teh", 5000, 20, "Dingin"))
    return warung


def test_harga_negatif_raise_error() -> None:
    """Harga negatif harus menghasilkan ValueError."""
    with pytest.raises(ValueError):
        MenuMakanan("Nasi Goreng", -1000, 5, "Porsi normal")


def test_stok_negatif_raise_error() -> None:
    """Stok negatif harus menghasilkan ValueError."""
    with pytest.raises(ValueError):
        MenuMinuman("Kopi", 7000, -2, "Panas")


def test_kurangi_stok_berhasil(menu_makanan: MenuMakanan) -> None:
    """Stok harus berkurang sesuai jumlah yang dipesan."""
    menu_makanan.kurangi_stok(3)

    assert menu_makanan.stok == 7


def test_menu_habis_raise_error(menu_makanan: MenuMakanan) -> None:
    """Pesanan yang melebihi stok harus menghasilkan MenuHabisError."""
    with pytest.raises(MenuHabisError):
        menu_makanan.kurangi_stok(20)


def test_menu_makanan_adalah_menu(menu_makanan: MenuMakanan) -> None:
    """MenuMakanan harus menjadi turunan dari Menu."""
    assert isinstance(menu_makanan, Menu)


def test_menu_minuman_adalah_menu(menu_minuman: MenuMinuman) -> None:
    """MenuMinuman harus menjadi turunan dari Menu."""
    assert isinstance(menu_minuman, Menu)


def test_meja_terisi_bisa_pesan() -> None:
    """MejaTerisi harus dapat menerima pesanan."""
    meja = MejaTerisi("12:00")

    assert meja.keterangan() == "Terisi"
    assert meja.bisa_pesan() is True


def test_meja_kosong_tidak_bisa_pesan() -> None:
    """MejaKosong tidak boleh menerima pesanan."""
    meja = MejaKosong()

    assert meja.keterangan() == "Kosong"
    assert meja.bisa_pesan() is False


def test_subtotal_benar(menu_makanan: MenuMakanan) -> None:
    """Subtotal item pesanan harus sesuai harga dikali jumlah."""
    item = ItemPesanan(menu_makanan, 2)

    assert item.subtotal() == 30000


def test_cari_menu_berhasil(warung_dengan_menu: Warung) -> None:
    """Warung harus dapat mencari menu berdasarkan nama."""
    menu = warung_dengan_menu.cari_menu("Nasi Rames")

    assert menu.nama == "Nasi Rames"
    assert menu.harga == 15000


def test_cari_menu_tidak_ada_raise_error(warung_dengan_menu: Warung) -> None:
    """Menu yang tidak tersedia harus menghasilkan MenuTidakDitemukanError."""
    with pytest.raises(MenuTidakDitemukanError):
        warung_dengan_menu.cari_menu("Sate Ayam")


def test_buka_meja_berhasil(warung_dengan_menu: Warung) -> None:
    """Meja baru harus masuk ke daftar pesanan aktif."""
    warung_dengan_menu.buka_meja("1")

    assert "1" in warung_dengan_menu._pesanan_aktif


def test_buka_meja_yang_sama_raise_error(warung_dengan_menu: Warung) -> None:
    """Meja yang sudah terisi tidak boleh dibuka ulang."""
    warung_dengan_menu.buka_meja("1")

    with pytest.raises(MejaSudahTerisiError):
        warung_dengan_menu.buka_meja("1")


def test_pesan_meja_tidak_ada_raise_error(warung_dengan_menu: Warung) -> None:
    """Pesanan pada meja yang belum dibuka harus menghasilkan error."""
    with pytest.raises(MejaTidakDitemukanError):
        warung_dengan_menu.pesan("99", "Nasi Rames", 1)


def test_warung_pesan_mengurangi_stok_dan_menghitung_total(
    warung_dengan_menu: Warung,
) -> None:
    """Pesanan melalui Warung harus mengurangi stok dan menghitung total."""
    warung_dengan_menu.buka_meja("1")
    warung_dengan_menu.pesan("1", "Nasi Rames", 2)

    menu = warung_dengan_menu.cari_menu("Nasi Rames")
    pesanan = warung_dengan_menu._pesanan_aktif["1"]

    assert menu.stok == 8
    assert pesanan.hitung_total() == 30000


def test_bayar_memindahkan_pesanan_ke_riwayat(
    warung_dengan_menu: Warung,
) -> None:
    """Pembayaran harus menghapus pesanan aktif dan menyimpan riwayat."""
    warung_dengan_menu.buka_meja("2")
    warung_dengan_menu.pesan("2", "Es Teh", 3)

    warung_dengan_menu.bayar("2", 20000)

    assert "2" not in warung_dengan_menu._pesanan_aktif
    assert len(warung_dengan_menu._riwayat) == 1
    assert warung_dengan_menu._riwayat[0].hitung_total() == 15000