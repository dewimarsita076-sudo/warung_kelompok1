from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from database.models import Base, MenuDB, TransaksiDB


# Koneksi ke database SQLite.
# File warung.db akan dibuat di folder utama proyek.
engine = create_engine(
    "sqlite:///warung.db",
    echo=False,
)

# Factory untuk membuat session database.
SessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
)


def init_db() -> None:
    """
    Membuat seluruh tabel database jika tabel belum tersedia.
    """
    Base.metadata.create_all(engine)


def simpan_menu(
    nama: str,
    harga: float,
    stok: int,
    kategori: str,
) -> MenuDB:
    """
    Menyimpan menu baru ke tabel menu.

    Args:
        nama: Nama menu.
        harga: Harga menu dalam rupiah.
        stok: Jumlah stok menu.
        kategori: Kategori makanan atau minuman.

    Returns:
        Objek MenuDB yang sudah disimpan.
    """
    menu_baru = MenuDB(
        nama=nama,
        harga=harga,
        stok=stok,
        kategori=kategori,
    )

    with SessionLocal() as session:
        session.add(menu_baru)
        session.commit()
        session.refresh(menu_baru)

    return menu_baru


def ambil_semua_menu() -> list[MenuDB]:
    """
    Mengambil seluruh data menu dari database.

    Returns:
        List seluruh objek MenuDB.
    """
    with SessionLocal() as session:
        statement = select(MenuDB).order_by(MenuDB.id)
        daftar_menu = session.scalars(statement).all()

    return list(daftar_menu)


def update_stok_menu(
    nama: str,
    stok_baru: int,
) -> None:
    """
    Memperbarui stok menu berdasarkan nama.

    Args:
        nama: Nama menu yang akan diperbarui.
        stok_baru: Nilai stok terbaru.

    Raises:
        ValueError: Jika menu tidak ditemukan di database.
    """
    with SessionLocal() as session:
        statement = select(MenuDB).where(
            MenuDB.nama == nama
        )

        menu = session.scalar(statement)

        if menu is None:
            raise ValueError(
                f"Menu '{nama}' tidak ditemukan di database."
            )

        menu.stok = stok_baru
        session.commit()


def simpan_transaksi(
    menu_id: int,
    nomor_meja: str,
    jumlah: int,
    subtotal: float,
    waktu: str,
) -> TransaksiDB:
    """
    Menyimpan transaksi baru ke tabel transaksi.

    Args:
        menu_id: ID menu yang dibeli.
        nomor_meja: Nomor meja pelanggan.
        jumlah: Jumlah menu yang dibeli.
        subtotal: Total harga item.
        waktu: Waktu transaksi.

    Returns:
        Objek TransaksiDB yang sudah disimpan.
    """
    transaksi_baru = TransaksiDB(
        menu_id=menu_id,
        nomor_meja=nomor_meja,
        jumlah=jumlah,
        subtotal=subtotal,
        waktu=waktu,
    )

    with SessionLocal() as session:
        session.add(transaksi_baru)
        session.commit()
        session.refresh(transaksi_baru)

    return transaksi_baru


def ambil_semua_transaksi() -> list[TransaksiDB]:
    """
    Mengambil seluruh riwayat transaksi dari database.

    Returns:
        List seluruh objek TransaksiDB.
    """
    with SessionLocal() as session:
        statement = select(TransaksiDB).order_by(
            TransaksiDB.id
        )
        daftar_transaksi = session.scalars(statement).all()

    return list(daftar_transaksi)