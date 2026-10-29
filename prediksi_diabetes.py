import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os

folder = os.path.dirname(os.path.abspath(__file__))
lokasi_db = os.path.join(folder, "prediksi_diabetes.db")

db = sqlite3.connect(lokasi_db)
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS pasien (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama_pasien TEXT,
    usia INTEGER,
    gula_darah REAL,
    bmi REAL,
    riwayat_ortu TEXT,
    hasil_prediksi TEXT
)
""")

db.commit()


def prediksi():
    nama = entry_nama.get().strip()
    riwayat = combo_riwayat.get()

    try:
        usia = int(entry_usia.get())
        gula = float(entry_gula.get())
        bmi = float(entry_bmi.get())

        if not nama or usia <= 0 or gula <= 0 or bmi <= 0:
            raise ValueError

        if riwayat not in ["Ya", "Tidak"]:
            messagebox.showwarning("Peringatan", "Pilih riwayat orang tua.")
            return

    except ValueError:
        messagebox.showerror("Error", "Masukkan data dengan benar.")
        return

    if gula >= 200:
        hasil = "Sangat Tinggi" if bmi >= 30 or riwayat == "Ya" else "Tinggi"
    elif gula >= 140:
        hasil = "Tinggi" if bmi >= 30 or riwayat == "Ya" else "Sedang"
    elif bmi >= 30:
        hasil = "Sedang" if riwayat == "Ya" else "Waspada"
    elif riwayat == "Ya":
        hasil = "Waspada"
    else:
        hasil = "Rendah"

    warna = {
        "Rendah": "green",
        "Waspada": "orange",
        "Sedang": "darkorange",
        "Tinggi": "red",
        "Sangat Tinggi": "purple"
    }

    label_hasil.config(
        text=f"Hasil Prediksi: {hasil}",
        fg=warna[hasil]
    )

    cursor.execute("""
        INSERT INTO pasien
        (nama_pasien, usia, gula_darah, bmi, riwayat_ortu, hasil_prediksi)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (nama, usia, gula, bmi, riwayat, hasil))

    db.commit()
    messagebox.showinfo("Berhasil", "Data berhasil disimpan.")


def lihat_data():
    window = tk.Toplevel(root)
    window.title("Data Pasien")
    window.geometry("850x400")

    kolom = (
        "id", "nama", "usia", "gula",
        "bmi", "riwayat", "hasil"
    )

    tabel = ttk.Treeview(window, columns=kolom, show="headings")

    judul = [
        "ID", "Nama Pasien", "Usia", "Gula Darah",
        "BMI", "Riwayat Ortu", "Hasil"
    ]

    for nama_kolom, teks in zip(kolom, judul):
        tabel.heading(nama_kolom, text=teks)
        tabel.column(nama_kolom, width=110, anchor="center")

    cursor.execute("SELECT * FROM pasien")

    for data in cursor.fetchall():
        tabel.insert("", tk.END, values=data)

    tabel.pack(fill="both", expand=True, padx=10, pady=10)


root = tk.Tk()
root.title("Prediksi Risiko Diabetes")
root.geometry("450x470")

tk.Label(
    root,
    text="PREDIKSI RISIKO DIABETES",
    font=("Montserrat Bold", 16, "bold")
).pack(pady=15)

form = tk.Frame(root)
form.pack(pady=10)

tk.Label(form, text="Nama Pasien").grid(row=0, column=0, sticky="w", pady=7)
entry_nama = tk.Entry(form, width=25)
entry_nama.grid(row=0, column=1, padx=10)

tk.Label(form, text="Usia").grid(row=1, column=0, sticky="w", pady=7)
entry_usia = tk.Entry(form, width=25)
entry_usia.grid(row=1, column=1, padx=10)

tk.Label(form, text="Gula Darah").grid(row=2, column=0, sticky="w", pady=7)
entry_gula = tk.Entry(form, width=25)
entry_gula.grid(row=2, column=1, padx=10)

tk.Label(form, text="BMI").grid(row=3, column=0, sticky="w", pady=7)
entry_bmi = tk.Entry(form, width=25)
entry_bmi.grid(row=3, column=1, padx=10)

tk.Label(form, text="Apakah ada riwayat diabetes di keluarga?").grid(
    row=4, column=0, sticky="w", pady=7
)

combo_riwayat = ttk.Combobox(
    form,
    values=["Ya", "Tidak"],
    state="readonly",
    width=22
)
combo_riwayat.grid(row=4, column=1, padx=10)
combo_riwayat.set("Pilih")

tk.Button(
    root,
    text="Prediksi dan Simpan",
    command=prediksi,
    width=20
).pack(pady=10)

label_hasil = tk.Label(
    root,
    text="Hasil Prediksi: -",
    font=("Montserrat Bold", 13, "bold")
)
label_hasil.pack(pady=10)

tk.Button(
    root,
    text="Lihat Data",
    command=lihat_data,
    width=20
).pack(pady=10)

root.mainloop()