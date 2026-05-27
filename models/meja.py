from abc import ABC, abstractmethod


class StatusMeja(ABC):

    @abstractmethod
    def keterangan(self):
        pass

    @abstractmethod
    def bisa_pesan(self):
        pass


class MejaTerisi(StatusMeja):

    def __init__(self, jam_masuk):
        self.jam_masuk = jam_masuk

    def keterangan(self):
        return "Terisi"

    def bisa_pesan(self):
        return True


class MejaKosong(StatusMeja):

    def keterangan(self):
        return "Kosong"

    def bisa_pesan(self):
        return False