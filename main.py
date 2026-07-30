from services.warung import Warung
from services import api_client
from services import laporan
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
        print("7. Konversi Mata Uang")
        print("8. Laporan")
        print("0. Keluar")

        try:
            pilih = input("Pilih: ")

            if pilih == "1":
                jenis = input(
                    "Makanan/Minuman (m/n): "
                )

                nama = input("Nama Menu: ")
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

            elif pilih == "7":
                kode = input(
                    "Kode mata uang tujuan (mis. USD, JPY, EUR): "
                )

                try:
                    kurs = api_client.get_kurs(kode)
                    kode_tampil = kode.strip().upper()

                    print(
                        f"\n===== KONVERSI MATA UANG "
                        f"({kode_tampil}) ====="
                    )
                    print(f"Kurs 1 IDR = {kurs:.6f} {kode_tampil}\n")

                    if not warung._daftar_menu:
                        print("Belum ada menu.")
                    else:
                        for menu in warung._daftar_menu:
                            hasil = menu.harga * kurs
                            print(
                                f"{menu.nama:<15} : "
                                f"Rp {menu.harga:,.0f}"
                                f"  =  {hasil:,.2f} {kode_tampil}"
                            )

                except ValueError as error:
                    print(f"Mata uang tidak valid: {error}")

                except ConnectionError as error:
                    print(f"Gagal mengambil kurs: {error}")

            elif pilih == "8":
                print("\n----- MENU LAPORAN -----")
                print("1. Menu Tersedia (urut harga termurah)")
                print("2. Pendapatan per Kategori")
                print("3. Riwayat Diurutkan (total tertinggi)")
                print("4. Ringkasan Transaksi")
                sub = input("Pilih laporan: ")

                if sub == "1":
                    hasil = laporan.menu_tersedia(
                        warung._daftar_menu
                    )

                    print("\n===== MENU TERSEDIA =====")

                    if not hasil:
                        print("Tidak ada menu dengan stok tersedia.")
                    else:
                        for menu in hasil:
                            print(
                                f"{menu.nama:<15} : "
                                f"Rp {menu.harga:,.0f}  "
                                f"(stok: {menu.stok})"
                            )

                elif sub == "2":
                    hasil = laporan.pendapatan_per_kategori(
                        warung._riwayat
                    )

                    print("\n===== PENDAPATAN PER KATEGORI =====")
                    print(
                        f"Makanan : Rp "
                        f"{hasil['MenuMakanan']:,.0f}"
                    )
                    print(
                        f"Minuman : Rp "
                        f"{hasil['MenuMinuman']:,.0f}"
                    )

                elif sub == "3":
                    hasil = laporan.riwayat_diurutkan_total(
                        warung._riwayat
                    )

                    print(
                        "\n===== RIWAYAT (Total Tertinggi -> "
                        "Terendah) ====="
                    )

                    if not hasil:
                        print("Belum ada riwayat.")
                    else:
                        for pesanan in hasil:
                            print(pesanan)

                elif sub == "4":
                    hasil = laporan.ringkasan_transaksi(
                        warung._riwayat
                    )

                    print("\n===== RINGKASAN TRANSAKSI =====")

                    if not hasil:
                        print("Belum ada transaksi.")
                    else:
                        for baris in hasil:
                            print(baris)

                else:
                    print("Pilihan laporan tidak valid.")

            elif pilih == "0":
                break

            else:
                print("Pilihan tidak valid.")

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":

    warung = Warung()

    # Seed menu awal hanya jika database masih kosong,
    # supaya tidak bentrok dengan constraint unique nama menu
    # setiap kali program dijalankan ulang.
    if not warung._daftar_menu:
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