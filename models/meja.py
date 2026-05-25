cfrom abc import ABC, abstractmethod


# Abstract Class
class StatusMeja(ABC):

    @abstractmethod
    def keterangan(self):
        pass

    @abstractmethod
    def bisa_pesan(self):
        pass


# Subclass Meja Terisi
class MejaTerisi(StatusMeja):

    def __init__(self, jam_masuk):
        self.jam_masuk = jam_masuk

    def simpan_jam_masuk(self):
        return True

    def keterangan(self):
        return "terisi"

    def bisa_pesan(self):
        return True


# Subclass Meja Kosong
class MejaKosong(StatusMeja):

    def keterangan(self):
        return "kosong"

    def bisa_pesan(self):
        return False
    
from models.meja import MejaTerisi, MejaKosong

# meja terisi
meja1 = MejaTerisi("19:30")

print(meja1.keterangan())          # terisi
print(meja1.bisa_pesan())          # True
print(meja1.simpan_jam_masuk())   # True

# meja kosong
meja2 = MejaKosong()

print(meja2.keterangan())         # kosong
print(meja2.bisa_pesan())         # False

