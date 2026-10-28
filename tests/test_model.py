from models.buku_model import BukuModel

model = BukuModel()

print("=== 1. Menampilkan Semua Buku Awal ===")
daftar_buku = model.get_all_buku()
for buku in daftar_buku:
    print(f"[{buku['id_buku']}] {buku['judul']} - {buku['penulis']} ({buku['tahun_terbit']})")

# Gunakan ID 3 karena ID 3 ada di daftar terminal Anda
print("\n=== 2. Menguji Fungsi Update Buku ===")
model.update_buku(3, "Laskar Pelangi (Edisi Revisi)", "Andrea Hirata", 2008)

print("\n=== 3. Menampilkan Buku Setelah Update ===")
daftar_buku = model.get_all_buku()
for buku in daftar_buku:
    print(f"[{buku['id_buku']}] {buku['judul']} - {buku['penulis']} ({buku['tahun_terbit']})")

# Gunakan ID 3 untuk diuji hapus
print("\n=== 4. Menguji Fungsi Delete Buku ===")
model.delete_buku(3)

print("\n=== 5. Menampilkan Buku Setelah Delete ===")
daftar_buku = model.get_all_buku()
for buku in daftar_buku:
    print(f"[{buku['id_buku']}] {buku['judul']} - {buku['penulis']} ({buku['tahun_terbit']})")