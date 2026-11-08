"""
Praktikum Sesi 11 - Advanced Widgets dan Event Handling
Aplikasi Pendaftaran Kegiatan Mahasiswa (Python Tkinter)
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

PRODI = [
    "Teknik Informatika",
    "Sistem Informasi",
    "Teknik Industri",
    "Manajemen",
    "Akuntansi",
    "Pendidikan Matematika",
]

KEGIATAN = [
    "Seminar Teknologi",
    "Lomba Coding",
    "Workshop Desain",
    "Bakti Sosial",
    "Turnamen Futsal",
]

PLACEHOLDER_INFO = " "


class AplikasiPendaftaran:
    def __init__(self, root):
        self.root = root
        self.about_window = None
        self.jumlah_daftar = 0

        root.title("Pendaftaran Kegiatan Mahasiswa")
        root.geometry("820x600")
        root.minsize(760, 560)
        ttk.Style().theme_use("clam")

        # Variabel kontrol widget
        self.var_nama = tk.StringVar()
        self.var_prodi = tk.StringVar()
        self.var_gender = tk.StringVar()
        self.var_kegiatan = {k: tk.BooleanVar() for k in KEGIATAN}

        self._buat_menu()
        self._buat_form()
        self._buat_panel_hasil()
        self._pasang_event()

        self.ent_nama.focus_set()

    # ------------------------------------------------------------------ UI
    def _buat_menu(self):
        menubar = tk.Menu(self.root)

        menu_file = tk.Menu(menubar, tearoff=0)
        menu_file.add_command(label="Reset Form", command=self.reset,
                              accelerator="Ctrl+R")
        menu_file.add_separator()
        menu_file.add_command(label="Keluar", command=self.keluar,
                              accelerator="Ctrl+Q")
        menubar.add_cascade(label="File", menu=menu_file)

        menu_bantuan = tk.Menu(menubar, tearoff=0)
        menu_bantuan.add_command(label="Tentang Aplikasi (About)",
                                 command=self.tampilkan_about, accelerator="F1")
        menubar.add_cascade(label="Bantuan", menu=menu_bantuan)

        self.root.config(menu=menubar)

    def _buat_form(self):
        self.frame_form = ttk.LabelFrame(self.root, text=" Formulir Pendaftaran ",
                                         padding=12)
        self.frame_form.grid(row=0, column=0, sticky="nsew", padx=(12, 6), pady=12)
        self.frame_form.columnconfigure(1, weight=1)
        f = self.frame_form

        # Nama - Entry
        ttk.Label(f, text="Nama").grid(row=0, column=0, sticky="w", pady=4)
        self.ent_nama = ttk.Entry(f, textvariable=self.var_nama)
        self.ent_nama.grid(row=0, column=1, sticky="ew", pady=4)

        # Program studi - Combobox
        ttk.Label(f, text="Program Studi").grid(row=1, column=0, sticky="w", pady=4)
        self.cmb_prodi = ttk.Combobox(f, textvariable=self.var_prodi,
                                      values=PRODI, state="readonly")
        self.cmb_prodi.grid(row=1, column=1, sticky="ew", pady=4)

        # Jenis kelamin - Radiobutton
        ttk.Label(f, text="Jenis Kelamin").grid(row=2, column=0, sticky="w", pady=4)
        frame_gender = ttk.Frame(f)
        frame_gender.grid(row=2, column=1, sticky="w", pady=4)
        for teks in ("Laki-laki", "Perempuan"):
            ttk.Radiobutton(frame_gender, text=teks, value=teks,
                            variable=self.var_gender).pack(side="left", padx=(0, 12))

        # Kegiatan - Checkbutton
        ttk.Label(f, text="Kegiatan").grid(row=3, column=0, sticky="nw", pady=4)
        frame_kegiatan = ttk.Frame(f)
        frame_kegiatan.grid(row=3, column=1, sticky="w", pady=4)
        for k in KEGIATAN:
            ttk.Checkbutton(frame_kegiatan, text=k, variable=self.var_kegiatan[k],
                            command=self.perbarui_listbox).pack(anchor="w")

        # Alasan - Text
        ttk.Label(f, text="Alasan Mengikuti").grid(row=4, column=0, sticky="nw", pady=4)
        self.txt_alasan = tk.Text(f, height=5, width=30, wrap="word")
        self.txt_alasan.grid(row=4, column=1, sticky="ew", pady=4)

        # Tombol
        frame_tombol = ttk.Frame(f)
        frame_tombol.grid(row=5, column=0, columnspan=2, sticky="e", pady=(12, 0))
        ttk.Button(frame_tombol, text="Submit",
                   command=self.submit).pack(side="left", padx=4)
        ttk.Button(frame_tombol, text="Reset",
                   command=self.reset).pack(side="left", padx=4)

    def _buat_panel_hasil(self):
        frame_kanan = ttk.Frame(self.root)
        frame_kanan.grid(row=0, column=1, sticky="nsew", padx=(6, 12), pady=12)
        frame_kanan.rowconfigure(1, weight=1)
        frame_kanan.columnconfigure(0, weight=1)

        # Listbox pilihan kegiatan
        frame_list = ttk.LabelFrame(frame_kanan, text=" Kegiatan Dipilih ",
                                    padding=8)
        frame_list.grid(row=0, column=0, sticky="ew")
        frame_list.columnconfigure(0, weight=1)
        self.lst_kegiatan = tk.Listbox(frame_list, height=5, activestyle="none")
        self.lst_kegiatan.grid(row=0, column=0, sticky="ew")

        # Area informasi ringkasan
        frame_info = ttk.LabelFrame(frame_kanan, text=" Ringkasan Pendaftaran ",
                                    padding=8)
        frame_info.grid(row=1, column=0, sticky="nsew", pady=(12, 0))
        frame_info.rowconfigure(0, weight=1)
        frame_info.columnconfigure(0, weight=1)
        self.txt_info = tk.Text(frame_info, width=34, height=12, wrap="word",
                                state="disabled", background="#f5f5f5")
        self.txt_info.grid(row=0, column=0, sticky="nsew")
        self._set_info(PLACEHOLDER_INFO)

        self.root.columnconfigure(0, weight=3)
        self.root.columnconfigure(1, weight=2)
        self.root.rowconfigure(0, weight=1)

    def _pasang_event(self):
        # Enter menjalankan Submit (kecuali saat mengetik di kolom alasan,
        # karena Enter di sana dipakai untuk baris baru)
        self.root.bind("<Return>", self._on_enter)
        self.root.bind("<KP_Enter>", self._on_enter)
        self.root.bind("<Control-r>", lambda e: self.reset())
        self.root.bind("<Control-q>", lambda e: self.keluar())
        self.root.bind("<F1>", lambda e: self.tampilkan_about())
        self.root.protocol("WM_DELETE_WINDOW", self.keluar)

    # ------------------------------------------------------------- Helper
    def _set_info(self, teks):
        self.txt_info.config(state="normal")
        self.txt_info.delete("1.0", "end")
        self.txt_info.insert("1.0", teks)
        self.txt_info.config(state="disabled")

    def _kegiatan_terpilih(self):
        return [k for k, v in self.var_kegiatan.items() if v.get()]

    def perbarui_listbox(self):
        self.lst_kegiatan.delete(0, "end")
        for k in self._kegiatan_terpilih():
            self.lst_kegiatan.insert("end", k)

    # -------------------------------------------------------------- Event
    def _on_enter(self, event):
        if event.widget is self.txt_alasan:
            return
        self.submit()

    def validasi(self):
        """Mengembalikan True jika semua input valid; jika tidak, tampilkan pesan."""
        nama = self.var_nama.get().strip()
        if not nama:
            messagebox.showwarning("Validasi", "Nama tidak boleh kosong.")
            self.ent_nama.focus_set()
            return False
        if not self.var_prodi.get():
            messagebox.showwarning("Validasi", "Program studi belum dipilih.")
            self.cmb_prodi.focus_set()
            return False
        if not self.var_gender.get():
            messagebox.showwarning("Validasi", "Jenis kelamin belum dipilih.")
            return False
        if not self._kegiatan_terpilih():
            messagebox.showwarning("Validasi", "Pilih minimal satu kegiatan.")
            return False
        if not self.txt_alasan.get("1.0", "end").strip():
            messagebox.showwarning("Validasi", "Alasan mengikuti kegiatan wajib diisi.")
            self.txt_alasan.focus_set()
            return False
        return True

    def submit(self):
        if not self.validasi():
            return

        self.jumlah_daftar += 1
        kegiatan = "\n".join(f"  - {k}" for k in self._kegiatan_terpilih())
        ringkasan = (
            f"Pendaftaran ke-{self.jumlah_daftar}\n"
            f"Waktu     : {datetime.now():%d-%m-%Y %H:%M}\n"
            f"Nama      : {self.var_nama.get().strip()}\n"
            f"Prodi     : {self.var_prodi.get()}\n"
            f"Gender    : {self.var_gender.get()}\n"
            f"Kegiatan  :\n{kegiatan}\n"
            f"Alasan    :\n{self.txt_alasan.get('1.0', 'end').strip()}"
        )
        self._set_info(ringkasan)
        messagebox.showinfo("Berhasil",
                            f"Pendaftaran atas nama {self.var_nama.get().strip()} "
                            "berhasil disimpan.")

    def reset(self):
        self.var_nama.set("")
        self.var_prodi.set("")
        self.var_gender.set("")
        for v in self.var_kegiatan.values():
            v.set(False)
        self.txt_alasan.delete("1.0", "end")
        self.perbarui_listbox()
        self._set_info(PLACEHOLDER_INFO)
        self.ent_nama.focus_set()

    def keluar(self):
        if messagebox.askokcancel("Keluar", "Yakin ingin keluar dari aplikasi?"):
            self.root.destroy()

    def tampilkan_about(self):
        # Cegah jendela About terbuka ganda
        if self.about_window is not None and self.about_window.winfo_exists():
            self.about_window.lift()
            self.about_window.focus_set()
            return

        win = tk.Toplevel(self.root)
        self.about_window = win
        win.title("Tentang Aplikasi")
        win.resizable(False, False)
        win.transient(self.root)

        frame = ttk.Frame(win, padding=20)
        frame.pack()
        ttk.Label(frame, text="Pendaftaran Kegiatan Mahasiswa",
                  font=("TkDefaultFont", 12, "bold")).pack(pady=(0, 8))
        ttk.Label(frame, justify="center",
                  text="Praktikum Python Tkinter - Sesi 11\n"
                       "Advanced Widgets dan Event Handling\n\n"
                       "Versi 1.0\n"
                       "Dibuat oleh: Achmad Lutfi Ubaidhillah (NIM 2595114037)"
                  ).pack()
        ttk.Button(frame, text="Tutup", command=win.destroy).pack(pady=(16, 0))
        win.bind("<Escape>", lambda e: win.destroy())

        # Posisikan di tengah jendela utama
        win.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - win.winfo_width()) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - win.winfo_height()) // 2
        win.geometry(f"+{max(x, 0)}+{max(y, 0)}")


if __name__ == "__main__":
    root = tk.Tk()
    AplikasiPendaftaran(root)
    root.mainloop()