# Praktikum Tkinter Sesi 11 - Pendaftaran Kegiatan Mahasiswa

Praktikum Python Tkinter: Advanced Widgets dan Event Handling.

## Tujuan
Membangun aplikasi GUI dengan Python Tkinter yang memakai berbagai widget, event handling, validasi input, menu, dan dialog.

## Fitur
- **Entry** untuk nama, **Combobox** untuk program studi, **Radiobutton** untuk jenis kelamin, **Checkbutton** untuk kegiatan, **Text** untuk alasan.
- Tombol **Submit** dan **Reset**.
- **Ringkasan pendaftaran** tampil di area informasi.
- **Listbox** menampilkan kegiatan yang dipilih (update otomatis saat checkbox diklik).
- **Validasi**: nama, program studi, jenis kelamin, minimal satu kegiatan, dan alasan wajib diisi.
- **Messagebox** untuk notifikasi (peringatan validasi, sukses, konfirmasi keluar).
- **Menu File** (Reset Form, Keluar) dan **menu Bantuan** (About).
- Jendela **About** memakai `Toplevel`.
- **Event keyboard**: `Enter` = Submit (tidak aktif saat mengetik di kolom alasan), `Ctrl+R` = Reset, `Ctrl+Q` = Keluar, `F1` = About.
- Tata letak memakai `Frame`, `LabelFrame`, dan `grid`/`pack`.

## Cara Menjalankan
Syarat: Python 3.8+ dengan Tkinter (bawaan Python di Windows/macOS; di Ubuntu/Debian: `sudo apt install python3-tk`).

```bash
python main.py
```

## Screenshot
| Form terisi + ringkasan | Jendela About |
| --- | --- |
| ![Form](screenshot_form.png) | ![About](screenshot_about.png) |

## Struktur Berkas
```
praktikum-tkinter-sesi-11/
├── main.py
├── README.md
├── screenshot_form.png
└── screenshot_about.png
```
