class Item_Pesanan:
    def __init__(self, nama_item, jumlah):
        self.nama_item = nama_item
        self.jumlah = jumlah

class Pesanan:
    def __init__(self, id_pesanan, nama_pelanggan, alamat_pelanggan, daftar_item):
        self.id_pesanan = id_pesanan
        self.nama_pelanggan = nama_pelanggan
        self.alamat_pelanggan = alamat_pelanggan
        self.daftar_item = daftar_item  # List of Item_Pesanan objects
    def total_item(self): 
        return sum(item.jumlah for item in self.daftar_item)
    def __str__(self):
        item_str = "\n".join([f"{item.nama_item} x {item.jumlah}" for item in self.daftar_item])
        return f"Pesanan ID: {self.id_pesanan}\nNama Pelanggan: {self.nama_pelanggan}\nAlamat Pelanggan: {self.alamat_pelanggan}\nDaftar Item:\n{item_str}\nTotal Item: {self.total_item()}"
# Contoh penggunaan
if __name__ == "__main__": 
    item1 = Item_Pesanan("Nasi Goreng", 2)
    item2 = Item_Pesanan("Mie Ayam", 1)
    pesanan = Pesanan(1, "Budi", "Jl. Merdeka No. 10", [item1, item2])
    print(pesanan)