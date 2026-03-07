# ==========================================
# File: export/export_csv.py
# Tugas: Menyimpan hasil scraping ke file CSV
# ==========================================

import csv


def export_to_csv(data, filename="hasil_scraping_berita.csv"):
    """
    Menyimpan data artikel ke file CSV.
    Data berupa list of dictionary.
    """

    if not data:
        print("Tidak ada data untuk disimpan.")
        return

    try:
        with open(filename, mode="w", newline="", encoding="utf-8") as file:

            writer = csv.writer(file)

            # Header kolom
            writer.writerow(["Judul", "Tanggal", "Link"])

            # Isi data
            for item in data:
                writer.writerow([
                    item.get("title", ""),
                    item.get("date", ""),
                    item.get("link", "")
                ])

        print(f"Data berhasil disimpan ke {filename}")

    except Exception as e:
        print("Gagal menyimpan file:", e)