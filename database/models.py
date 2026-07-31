from __future__ import annotations

from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)


class Base(DeclarativeBase):
    """
    Base class untuk seluruh model SQLAlchemy.
    """
 
    pass


class MenuDB(Base):
    """
    Model database untuk tabel menu.
    """
    __tablename__ = "menu"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    nama: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    harga: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    stok: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    kategori: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )
    
    porsi: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    suhu: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    # Relasi satu menu dapat memiliki banyak transaksi.
    transaksi_list: Mapped[list["TransaksiDB"]] = relationship(
        back_populates="menu",
    )

    def __repr__(self) -> str:
        return (
            f"MenuDB("
            f"id={self.id}, "
            f"nama='{self.nama}', "
            f"harga={self.harga}, "
            f"stok={self.stok}, "
            f"kategori='{self.kategori}'"
            f")"
        )


class TransaksiDB(Base):
    """
    Model database untuk tabel transaksi.
    """

    __tablename__ = "transaksi"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    menu_id: Mapped[int] = mapped_column(
        ForeignKey("menu.id"),
        nullable=False,
    )

    nomor_meja: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )

    jumlah: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    subtotal: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    waktu: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    # Relasi balik menuju MenuDB.
    menu: Mapped["MenuDB"] = relationship(
        back_populates="transaksi_list",
    )

    def __repr__(self) -> str:
        return (
            f"TransaksiDB("
            f"id={self.id}, "
            f"menu_id={self.menu_id}, "
            f"nomor_meja='{self.nomor_meja}', "
            f"jumlah={self.jumlah}, "
            f"subtotal={self.subtotal}, "
            f"waktu='{self.waktu}'"
            f")"
        )