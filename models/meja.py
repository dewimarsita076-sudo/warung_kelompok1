from abc import ABC, abstractmethod
from datetime import datetime

jam_sekarang = datetime.now().strftime("%H:%M")

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
        return (f"Jam masuk disimpan: {self.jam_masuk}")

    def keterangan(self):
        return "Terisi"

    def bisa_pesan(self):
        return (f"Meja terisi sejak: {self.jam_masuk}")


# Subclass Meja Kosong
class MejaKosong(StatusMeja):

    def keterangan(self):
        return "Kosong"

    def bisa_pesan(self):
        return (f"Meja kosong")

# from models.meja import MejaTerisi, MejaKosong

print("=== STATUS MEJA WARUNG ===\n")

# meja terisi
meja1 = MejaTerisi(jam_sekarang)

print(f"Meja 1           : {meja1.keterangan()}")          
print(f"Meja 1 bisa pesan: {meja1.bisa_pesan()}")          
print(f"Meja 1           : {meja1.simpan_jam_masuk()}")   

print("\n")

# meja kosong
meja2 = MejaKosong()

print(f"Meja 2           : {meja2.keterangan()}")         
print(f"Meja 2 bisa pesan: {meja2.bisa_pesan()}")         

