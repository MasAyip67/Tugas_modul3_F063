from tkinter import messagebox
from models.anggota_model import AnggotaModel
from views.anggota_view import AnggotaView

class AnggotaController:
    def __init__(self):
        self.model = AnggotaModel()
        self.view = AnggotaView()

        # Binding tombol-tombol di View
        self.view.btn_simpan.configure(command=self.simpan_data)
        self.view.btn_hapus.configure(command=self.hapus_data)
        self.view.btn_update.configure(command=self.perbarui_data)
        self.view.tabel.bind("<ButtonRelease-1>", self.select_tabel)

        # Muat data tabel saat pertama kali dibuka
        self.muat_data_tabel()

    def muat_data_tabel(self):
        for item in self.view.tabel.get_children():
            self.view.tabel.delete(item)
        
        data_anggota = self.model.get_all_anggota()
        for anggota in data_anggota:
            self.view.tabel.insert("", "end", values=(anggota['id_anggota'], anggota['nama'], anggota['email'], anggota['telepon']))

    def select_tabel(self, event):
        selected_item = self.view.tabel.selection()
        if selected_item:
            row = self.view.tabel.item(selected_item)
            values = row['values']
            if values:
                self.selected_id = values[0]
                self.view.entry_nama.delete(0, 'end')
                self.view.entry_nama.insert(0, values[1])
                self.view.entry_email.delete(0, 'end')
                self.view.entry_email.insert(0, values[2])
                self.view.entry_telepon.delete(0, 'end')
                self.view.entry_telepon.insert(0, values[3])

    def simpan_data(self):
        nama = self.view.entry_nama.get()
        email = self.view.entry_email.get()
        telepon = self.view.entry_telepon.get()

        if not nama or not email or not telepon:
            messagebox.showwarning("Peringatan", "Semua kolom form harus diisi!")
            return

        berhasil = self.model.create_anggota(nama, email, telepon)
        if berhasil:
            messagebox.showinfo("Sukses", "Data anggota berhasil disimpan!")
            self.view.entry_nama.delete(0, 'end')
            self.view.entry_email.delete(0, 'end')
            self.view.entry_telepon.delete(0, 'end')
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Terjadi kesalahan saat menyimpan data.")

    def perbarui_data(self):
        if not hasattr(self, 'selected_id'):
            messagebox.showwarning("Peringatan", "Pilih data anggota dari tabel yang ingin diperbarui!")
            return

        nama = self.view.entry_nama.get()
        email = self.view.entry_email.get()
        telepon = self.view.entry_telepon.get()

        if not nama or not email or not telepon:
            messagebox.showwarning("Peringatan", "Semua kolom form harus diisi!")
            return

        berhasil = self.model.update_anggota(self.selected_id, nama, email, telepon)
        if berhasil:
            messagebox.showinfo("Sukses", "Data anggota berhasil diperbarui!")
            self.muat_data_tabel()
            self.selected_id = None
        else:
            messagebox.showerror("Error", "Terjadi kesalahan saat memperbarui data.")

    def hapus_data(self):
        if not hasattr(self, 'selected_id'):
            messagebox.showwarning("Peringatan", "Pilih data anggota dari tabel yang ingin dihapus!")
            return

        konfirmasi = messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus data anggota ini?")
        if konfirmasi:
            berhasil = self.model.delete_anggota(self.selected_id)
            if berhasil:
                messagebox.showinfo("Sukses", "Data anggota berhasil dihapus!")
                self.muat_data_tabel()
                self.selected_id = None
            else:
                messagebox.showerror("Error", "Terjadi kesalahan saat menghapus data.")

    def run(self):
        self.view.mainloop()