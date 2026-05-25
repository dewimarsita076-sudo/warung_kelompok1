from abc import ABC, abstractmethod
from datetime import datetime

jam_sekarang = datetime.now().strftime("%H:%M")

# Abstract Class
class StatusMeja(ABC):

    abstractmethod
    def keterangan(self):
        pass

    abstractmethod
    def bisa_pesan(self):
        pass


# Subclass Meja Terisi
class MejaTerisi(StatusMeja):

    def __init__(self, jam_masuk):
        self.jam_masuk = jam_masuk

    def simpan_jam_masuk(self):
        return True

    def keterangan(self):
        return "Terisi"

    def bisa_pesan(self):
        return True


# Subclass Meja Kosong
class MejaKosong(StatusMeja):

    def keterangan(self):
        return "Kosong"

    def bisa_pesan(self):
        return False
    
# from models.meja import MejaTerisi, MejaKosong

print("=== STATUS MEJA WARUNG ===\n")

# meja terisi
meja1 = MejaTerisi(jam_sekarang)

print("meja 1")
print("Status        :", meja1.keterangan())
print("Bisa Pesan    :", meja1.bisa_pesan())
print("Jam Masuk     :", meja1.simpan_jam_masuk())

# meja kosong
meja2 = MejaKosong()

print("Meja 2")
print("Status        :", meja2.keterangan())
print("Bisa Pesan    :", meja2.bisa_pesan())