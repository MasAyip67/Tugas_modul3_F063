import tkinter.messagebox as messagebox
from models.buku_model import BukuModel
from views.buku_view import BukuView

class BukuController:
    def __init__(self, user_role="anggota"):
        self.user_role = user_role
        self.model = BukuModel()
        self.view = BukuView()
        
        self.view.title(f"Sistem Manajemen Perpustakaan - Mode: {self.user_role.upper()}")
        self.view.btn_simpan.configure(command=self.simpan_data)

        # Otorisasi: Batasi akses jika role adalah anggota
        if self.user_role == "anggota":
            self.view.btn_simpan.configure(state="disabled", text="Akses Terkunci (Khusus Admin)")
            self.view.entry_judul.configure(state="disabled")
            self.view.entry_penulis.configure(state="disabled")
            self.view.entry_tahun.configure(state="disabled")

        self.muat_data_tabel()

    def muat_data_tabel(self):
        for item in self.view.tabel.get_children():
            self.view.tabel.delete(item)
        data_buku = self.model.get_all_buku()
        for buku in data_buku:
            self.view.tabel.insert("", "end", values=(buku["id_buku"], buku["judul"], buku["penulis"], buku["tahun_terbit"]))

    def simpan_data(self):
        # Proteksi tambahan controller
        if self.user_role == "anggota":
            messagebox.showerror("Akses Ditolak", "Anda tidak memiliki izin untuk menambah data!")
            return

        judul = self.view.entry_judul.get()
        penulis = self.view.entry_penulis.get()
        tahun = self.view.entry_tahun.get()

        if not judul or not penulis or not tahun:
            messagebox.showwarning("Peringatan", "Semua kolom form harus diisi!")
            return

        if self.model.create_buku(judul, penulis, tahun):
            messagebox.showinfo("Sukses", "Data buku berhasil disimpan!")
            self.view.entry_judul.delete(0, "end")
            self.view.entry_penulis.delete(0, "end")
            self.view.entry_tahun.delete(0, "end")
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Gagal menyimpan data.")

    def run(self):
        self.view.mainloop()
        
        def select_tabel(self, event):
            selected_item = self.view.tabel.selection()
            if selected_item:
                row = self.view.tabel.item(selected_item)
                values = row['values']
                if values:
                    self.selected_id = values[0]
                    self.view.entry_judul.delete(0, 'end')
                    self.view.entry_judul.insert(0, values[1])
                    self.view.entry_penulis.delete(0, 'end')
                    self.view.entry_penulis.insert(0, values[2])
                    self.view.entry_tahun.delete(0, 'end')  
                    self.view.entry_tahun.insert(0, values[3])

        def perbarui_data(self):
            if not hasattr(self, 'selected_id'):
                messagebox.showwarning("Peringatan", "Pilih data buku dari tabel yang ingin diperbarui!")
                return

            judul = self.view.entry_judul.get()
            penulis = self.view.entry_penulis.get()
            tahun = self.view.entry_tahun.get()

            if not judul or not penulis or not tahun:
                messagebox.showwarning("Peringatan", "Semua kolom form harus diisi!")
                return

            berhasil = self.model.update_buku(self.selected_id, judul, penulis, tahun)
            if berhasil:
                messagebox.showinfo("Sukses", "Data buku berhasil diperbarui!")
                self.muat_data_tabel()
                self.selected_id = None
            else:
                messagebox.showerror("Error", "Terjadi kesalahan saat memperbarui data.")

    def hapus_data(self):
        if not hasattr(self, 'selected_id'):
            messagebox.showwarning("Peringatan", "Pilih data buku dari tabel yang ingin dihapus!")
            return

        konfirmasi = messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus data buku ini?")
        if konfirmasi:
            berhasil = self.model.delete_buku(self.selected_id)
            if berhasil:
                messagebox.showinfo("Sukses", "Data buku berhasil dihapus!")
                self.muat_data_tabel()
                self.selected_id = None
            else:
                messagebox.showerror("Error", "Terjadi kesalahan saat menghapus data.")

    def simpan_data(self):
        # Mengambil teks dari kotak input di View
        judul = self.view.entry_judul.get()
        penulis = self.view.entry_penulis.get()
        tahun = self.view.entry_tahun.get()

        # Binding tombol dan tabel
        self.view.btn_update.configure(command=self.perbarui_data)
        self.view.btn_hapus.configure(command=self.hapus_data)
        self.view.tabel.bind("<ButtonRelease-1>", self.select_tabel)

        # Validasi Form Kosong
        if not judul or not penulis or not tahun:
            tkinter.messagebox.showwarning("Peringatan", "Semua kolom form harus diisi!")
            return

        # Mengirim data ke Model untuk disimpan
        berhasil = self.model.create_buku(judul, penulis, tahun)

        if berhasil:
            tkinter.messagebox.showinfo("Sukses", "Data buku berhasil disimpan!")
            # Bersihkan form input
            self.view.entry_judul.delete(0, 'end')
            self.view.entry_penulis.delete(0, 'end')
            self.view.entry_tahun.delete(0, 'end')
            # Muat ulang tabel agar data terbaru muncul
            self.muat_data_tabel()  
        else:
            tkinter.messagebox.messagebox.showerror("Error", "Terjadi kesalahan saat menyimpan data.")

    # Fungsi untuk menyalakan aplikasi
    def run(self):
        self.view.mainloop()

    def select_tabel(self, event):
        # Mengambil data dari baris tabel yang diklik untuk dimasukkan ke form
        selected_item = self.view.tabel.selection()
        if selected_item:
            row = self.view.tabel.item(selected_item)
            values = row['values']
            if values:
                # Asumsi urutan kolom tabel: [id_buku, judul, penulis, tahun]
                self.selected_id = values[0]
                self.view.entry_judul.delete(0, 'end')
                self.view.entry_judul.insert(0, values[1])
                self.view.entry_penulis.delete(0, 'end')
                self.view.entry_penulis.insert(0, values[2])
                self.view.entry_tahun.delete(0, 'end')
                self.view.entry_tahun.insert(0, values[3])

    def perbarui_data(self, event=None):
        if not hasattr(self, 'selected_id'):
            messagebox.showwarning("Peringatan", "Pilih data buku dari tabel yang ingin diperbarui!")
            return
        
        judul = self.view.entry_judul.get()
        penulis = self.view.entry_penulis.get()
        tahun = self.view.entry_tahun.get()

        if not judul or not penulis or not tahun:
            messagebox.showwarning("Peringatan", "Semua kolom form harus diisi!")
            return

        berhasil = self.model.update_buku(self.selected_id, judul, penulis, tahun)
        if berhasil:
            messagebox.showinfo("Sukses", "Data buku berhasil diperbarui!")
            self.muat_data_tabel()
            self.selected_id = None
        else:
            messagebox.showerror("Error", "Terjadi kesalahan saat memperbarui data.")

    def hapus_data(self, event=None):
        if not hasattr(self, 'selected_id'):
            messagebox.showwarning("Peringatan", "Pilih data buku dari tabel yang ingin dihapus!")
            return

        konfirmasi = messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus data buku ini?")
        if konfirmasi:
            berhasil = self.model.delete_buku(self.selected_id)
            if berhasil:
                messagebox.showinfo("Sukses", "Data buku berhasil dihapus!")
                self.muat_data_tabel()
                self.selected_id = None
            else:
                messagebox.showerror("Error", "Terjadi kesalahan saat menghapus data.")