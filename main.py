# Program Biodata Kelompok - Tugas Modul 3

def tampilkan_header():
    print("=" * 60)
    print("           PROGRAM BIODATA ANGGOTA KELOMPOK         ")
    print("=" * 60)

def main():
    tampilkan_header()
    
    # Input Data Kelompok
    nama_kelompok = input("Masukkan Nama/Nomor Kelompok : ")
    
    while True:
        try:
            jumlah_anggota = int(input("Masukkan Jumlah Anggota     : "))
            if jumlah_anggota > 0:
                break
            print("Jumlah anggota harus lebih dari 0!")
        except ValueError:
            print("Harap masukkan angka yang valid!")

    print("-" * 60)
    
    daftar_anggota = []
    
    # Perulangan untuk input data setiap anggota
    for i in range(1, jumlah_anggota + 1):
        print(f"\n--- Input Data Anggota Ke-{i} ---")
        nama = input("Nama Lengkap : ")
        nim  = input("NIM          : ")
        peran = input("Peran/Tugas  : ")
        
        # Menyimpan data anggota ke dalam dictionary
        anggota = {
            "nama": nama,
            "nim": nim,
            "peran": peran
        }
        daftar_anggota.append(anggota)
        
    # Menampilkan Rincian Biodata
    print("\n" + "=" * 60)
    print(f"         RINCIAN BIODATA {nama_kelompok.upper()}         ")
    print("=" * 60)
    
    for idx, member in enumerate(daftar_anggota, 1):
        print(f"Anggota {idx}:")
        print(f"  • Nama  : {member['nama']}")
        print(f"  • NIM   : {member['nim']}")
        print(f"  • Peran : {member['peran']}")
        print("-" * 60)

    # Menampilkan Ringkasan Semua Anggota (Tabel / Rekap Akhir)
    print("\n" + "=" * 60)
    print(f"     REKAPITULASI SEMUA ANGGOTA {nama_kelompok.upper()}     ")
    print("=" * 60)
    print(f"{'NO':<4} | {'NAMA LENGKAP':<25} | {'NIM':<15} | {'PERAN':<15}")
    print("-" * 65)
    
    for idx, member in enumerate(daftar_anggota, 1):
        print(f"{idx:<4} | {member['nama']:<25} | {member['nim']:<15} | {member['peran']:<15}")
        
    print("=" * 60)
    print("Terima kasih! Program selesai.")
    print("=" * 60)

if __name__ == "__main__":
    main()