from unittest.mock import MagicMock
from models.buku_model import BukuModel

def test_create_buku_berhasil():
    # Menginisialisasi Model
    model = BukuModel()
    
    # Memanipulasi (Mock) koneksi database agar tidak mengotori data asli
    model.conn = MagicMock()
    mock_cursor = MagicMock()
    model.conn.cursor.return_value = mock_cursor

    # Melakukan eksekusi fungsi
    hasil = model.create_buku("Buku Testing", "Penulis QA", 2026)
    
    # Memverifikasi apakah fungsi mengembalikan nilai True
    assert hasil is True
    # Memverifikasi apakah cursor.execute benar-benar dipanggil
    mock_cursor.execute.assert_called_once()
    # Memverifikasi apakah perintah commit (simpan) dipanggil
    model.conn.commit.assert_called_once()

# --- TAMBAHKAN FUNGSI INI DI BAGIAN BAWAHNYA ---
def test_get_all_buku():
    model = BukuModel()
    model.conn = MagicMock()
    mock_cursor = MagicMock()
    model.conn.cursor.return_value = mock_cursor

    # Simulasi data dummy yang dikembalikan database
    dummy_data = [
        (1, "Pemrograman Python", "Guido", 2023),
        (2, "Struktur Data", "Anonym", 2024)
    ]
    mock_cursor.fetchall.return_value = dummy_data

    # Melakukan eksekusi fungsi
    hasil = model.get_all_buku()

    # Memverifikasi hasil
    mock_cursor.execute.assert_called_once()
    assert isinstance(hasil, list)
    assert len(hasil) == 2