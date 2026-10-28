import mysql.connector
from mysql.connector import Error
from config.database import Database

class AnggotaModel:
    def __init__(self):
        self.db = Database()

    # Operasi Create (Tambah Anggota)
    def create_anggota(self, nama, alamat):
        conn = self.db.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                query = "INSERT INTO anggota (nama, alamat) VALUES (%s, %s)"
                values = (nama, alamat)
                cursor.execute(query, values)
                conn.commit()
                cursor.close()
                conn.close()
                print(f"Anggota '{nama}' berhasil ditambahkan!")
            except Error as e:
                print(f"Error Create Anggota: {e}")

    # Operasi Read (Tampilkan Seluruh Anggota)
    def get_all_anggota(self):
        conn = self.db.get_connection()
        if conn:
            try:
                cursor = conn.cursor(dictionary=True)
                query = "SELECT * FROM anggota"
                cursor.execute(query)
                results = cursor.fetchall()
                cursor.close()
                conn.close()
                return results
            except Error as e:
                print(f"Error Read Anggota: {e}")
                return []