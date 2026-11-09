import tkinter.messagebox as messagebox
from models.buku_model import BukuModel
from views.buku_view import BukuView


class BukuController:
    def __init__(self, user_role="anggota"):
        self.user_role = user_role
        self.selected_id = None
        self.model = BukuModel()
        self.view = BukuView(current_role=self.user_role)  # kirim role ke View

        # Binding tombol dan tabel
        self.view.btn_simpan.configure(command=self.simpan_data)
        self.view.btn_update.configure(command=self.perbarui_data)
        self.view.btn_delete.configure(command=self.hapus_data)
        self.view.tabel.bind("<ButtonRelease-1>", self.select_tabel)

        # Otorisasi: batasi akses jika role adalah anggota
        if self.user_role == "anggota":
            self.view.btn_simpan.configure(state="disabled", text="Akses Terkunci (Khusus Admin)")
            self.view.entry_judul.configure(state="disabled")
            self.view.entry_penulis.configure(state="disabled")
            self.view.entry_tahun.configure(state="disabled")

        self.muat_data_tabel()

    def muat_data_tabel(self):
        for item in self.view.tabel.get_children():
            self.view.tabel.delete(item)
        for buku in self.model.get_all_buku():
            self.view.tabel.insert("", "end", values=(
                buku["id_buku"], buku["judul"], buku["penulis"], buku["tahun_terbit"]))

    def simpan_data(self):
        # Proteksi ganda di level controller
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

    def select_tabel(self, event=None):
        selected_item = self.view.tabel.selection()
        if selected_item:
            values = self.view.tabel.item(selected_item)["values"]
            if values:
                self.selected_id = values[0]
                # Form hanya diisi jika bukan anggota (form anggota terkunci)
                if self.user_role != "anggota":
                    self.view.entry_judul.delete(0, "end")
                    self.view.entry_judul.insert(0, values[1])
                    self.view.entry_penulis.delete(0, "end")
                    self.view.entry_penulis.insert(0, values[2])
                    self.view.entry_tahun.delete(0, "end")
                    self.view.entry_tahun.insert(0, values[3])

    def perbarui_data(self):
        if self.user_role == "anggota":
            messagebox.showerror("Akses Ditolak", "Anda tidak memiliki izin untuk mengubah data!")
            return

        if self.selected_id is None:
            messagebox.showwarning("Peringatan", "Pilih data buku dari tabel yang ingin diperbarui!")
            return

        judul = self.view.entry_judul.get()
        penulis = self.view.entry_penulis.get()
        tahun = self.view.entry_tahun.get()

        if not judul or not penulis or not tahun:
            messagebox.showwarning("Peringatan", "Semua kolom form harus diisi!")
            return

        if self.model.update_buku(self.selected_id, judul, penulis, tahun):
            messagebox.showinfo("Sukses", "Data buku berhasil diperbarui!")
            self.muat_data_tabel()
            self.selected_id = None
        else:
            messagebox.showerror("Error", "Terjadi kesalahan saat memperbarui data.")

    def hapus_data(self):
        if self.user_role == "anggota":
            messagebox.showerror("Akses Ditolak", "Anda tidak memiliki izin untuk menghapus data!")
            return

        if self.selected_id is None:
            messagebox.showwarning("Peringatan", "Pilih data buku dari tabel yang ingin dihapus!")
            return

        if messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus data buku ini?"):
            if self.model.delete_buku(self.selected_id):
                messagebox.showinfo("Sukses", "Data buku berhasil dihapus!")
                self.muat_data_tabel()
                self.selected_id = None
            else:
                messagebox.showerror("Error", "Terjadi kesalahan saat menghapus data.")

    def run(self):
        self.view.mainloop()