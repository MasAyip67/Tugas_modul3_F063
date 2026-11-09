# Sistem Manajemen Perpustakaan

Aplikasi desktop manajemen perpustakaan yang dibangun dengan Python menggunakan pola arsitektur **MVC (Model-View-Controller)**, antarmuka **CustomTkinter**, dan basis data **MySQL**.

Dibuat sebagai tugas praktikum Rekayasa Perangkat Lunak oleh **Moh Arif Sigit (F5212520063)**.

## 1. Deskripsi Singkat Aplikasi

Aplikasi ini membantu petugas perpustakaan mengelola koleksi buku dan data anggota. Fitur utama:

- **Autentikasi login**: kata sandi disimpan sebagai hash SHA-256, dan verifikasi memakai parameterized query untuk mencegah SQL Injection.
- **Otorisasi berbasis peran (RBAC)**:
  - `admin` (petugas): dapat menambah, memperbarui, dan menghapus data buku.
  - `anggota`: hanya dapat melihat daftar buku. Form input serta tombol Simpan, Update, dan Hapus dikunci.
- **CRUD data buku** (Create, Read, Update, Delete).
- **Manajemen data anggota**.
- **Logout** yang mengembalikan pengguna ke halaman login.
- **CI/CD**: pengujian otomatis (pytest) dan pengecekan kode (flake8) lewat GitHub Actions.

## 2. Struktur Direktori MVC

```
MODUL 3 RPL/
├── .github/workflows/
│   └── ci_pipeline.yml      # GitHub Actions (flake8 + pytest)
├── config/
│   └── database.py          # Koneksi ke MySQL
├── controllers/             # CONTROLLER: logika alur aplikasi
│   ├── anggota_controller.py
│   ├── auth_controller.py
│   └── buku_controller.py
├── models/                  # MODEL: akses data ke MySQL
│   ├── anggota_model.py
│   ├── buku_model.py
│   └── user_model.py
├── views/                   # VIEW: antarmuka pengguna
│   ├── anggota_view.py
│   ├── buku_view.py
│   └── login_view.py
├── tests/                   # Unit test (pytest)
│   ├── test_anggota.py
│   ├── test_auth.py
│   ├── test_buku.py
│   └── test_model.py
├── main.py                  # Titik masuk aplikasi
├── pytest.ini
├── requirements.txt
└── .gitignore
```

| Komponen | Tanggung jawab |
|---|---|
| **Model** | Berkomunikasi dengan MySQL dan mengembalikan data, termasuk role pengguna. |
| **View** | Menampilkan antarmuka dan menyesuaikannya dengan role (misalnya menonaktifkan tombol). |
| **Controller** | Menghubungkan Model dan View serta mengatur logika autentikasi dan otorisasi. |

## 3. Panduan Instalasi dan Konfigurasi Database MySQL

### Prasyarat
Python 3.11+, Laragon (MySQL), Git, dan Visual Studio Code.

### Instalasi

```bash
git clone https://github.com/MasAyip67/Tugas_modul3_F063.git
cd Tugas_modul3_F063
python -m venv env
./env/Scripts/activate
python -m pip install -r requirements.txt
```

### Konfigurasi database

1. Jalankan Laragon, klik **Start All** sampai MySQL berjalan.
2. Buka Terminal Laragon, lalu masuk ke MySQL:

   ```bash
   mysql -u root -p
   ```

3. Buat database dan tabel:

   ```sql
   CREATE DATABASE IF NOT EXISTS perpustakaan;
   USE perpustakaan;

   CREATE TABLE IF NOT EXISTS buku (
       id_buku INT PRIMARY KEY AUTO_INCREMENT,
       judul VARCHAR(255) NOT NULL,
       penulis VARCHAR(255) NOT NULL,
       tahun_terbit INT NOT NULL
   );

   CREATE TABLE IF NOT EXISTS anggota (
       id_anggota INT PRIMARY KEY AUTO_INCREMENT,
       nama VARCHAR(255) NOT NULL,
       alamat VARCHAR(255) NOT NULL
   );

   CREATE TABLE IF NOT EXISTS users (
       id_user INT PRIMARY KEY AUTO_INCREMENT,
       username VARCHAR(50) NOT NULL UNIQUE,
       password VARCHAR(255) NOT NULL,
       role ENUM('admin', 'anggota') NOT NULL DEFAULT 'anggota'
   );
   ```

4. Tambahkan akun uji coba:

   ```sql
   INSERT INTO users (username, password, role) VALUES
   ('petugas', SHA2('admin123', 256), 'admin'),
   ('mahasiswa', SHA2('user123', 256), 'anggota');
   ```

5. Pengaturan koneksi ada di `config/database.py` (bawaan Laragon):

   ```python
   self.host = "localhost"
   self.db_name = "perpustakaan"
   self.username = "root"
   self.password = ""
   ```

## 4. Cara Menjalankan Aplikasi

1. Pastikan MySQL di Laragon sudah menyala.
2. Aktifkan virtual environment, lalu jalankan:

   ```bash
   python main.py
   ```

3. Login dengan akun uji coba:

   | Username | Password | Role | Hak akses |
   |---|---|---|---|
   | `petugas` | `admin123` | admin | Tambah, ubah, dan hapus buku |
   | `mahasiswa` | `user123` | anggota | Hanya melihat daftar buku |

**Menjalankan unit test:**

```bash
python -m pytest tests/ -v
```

**Membuat berkas .exe:**

```bash
python -m PyInstaller --noconfirm --onefile --windowed --name "AplikasiPerpustakaan" main.py
```

Versi siap unduh ada di halaman [Releases](https://github.com/MasAyip67/Tugas_modul3_F063/releases) (v1.0.0).