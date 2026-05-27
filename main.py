from services.warung import Warung
from models.menu import (
    MenuMakanan,
    MenuMinuman
)


def menu_utama(warung: Warung):

    while True:
        print("\n=== WARUNG MAKAN BU TUTI ===")
        print("1. Tambah Menu")
        print("2. Tampilkan Menu")
        print("3. Buka Meja")
        print("4. Pesan")
        print("5. Bayar")
        print("6. Riwayat")
        print("0. Keluar")

        try:
            pilih = input("Pilih: ")

            if pilih == "1":
                jenis = input(
                    "Makanan/Minuman (m/n): "
                )

                nama = input("Nama: ")
                harga = float(input("Harga: "))
                stok = int(input("Stok: "))

                if jenis.lower() == "m":
                    porsi = input("Porsi: ")

                    warung.tambah_menu(
                        MenuMakanan(
                            nama,
                            harga,
                            stok,
                            porsi
                        )
                    )

                else:
                    suhu = input("Suhu: ")

                    warung.tambah_menu(
                        MenuMinuman(
                            nama,
                            harga,
                            stok,
                            suhu
                        )
                    )

            elif pilih == "2":
                warung.tampilkan_menu()

            elif pilih == "3":
                nomor = input("Nomor meja: ")
                warung.buka_meja(nomor)

            elif pilih == "4":
                meja = input("Nomor meja: ")
                menu = input("Nama menu: ")
                jumlah = int(input("Jumlah: "))

                warung.pesan(
                    meja,
                    menu,
                    jumlah
                )

            elif pilih == "5":
                meja = input("Nomor meja: ")
                uang = float(
                    input("Uang bayar: ")
                )

                kembali = warung.bayar(
                    meja,
                    uang
                )

                print(
                    f"Kembalian: Rp{kembali:,.0f}"
                )

            elif pilih == "6":
                warung.tampilkan_riwayat()

            elif pilih == "0":
                break

            else:
                print("Pilihan tidak valid.")

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":

    warung = Warung()

    warung.tambah_menu(
        MenuMakanan(
            "Nasi Rames",
            15000,
            20,
            "Normal"
        )
    )

    warung.tambah_menu(
        MenuMinuman(
            "Es Teh",
            5000,
            30,
            "Dingin"
        )
    )

    menu_utama(warung)