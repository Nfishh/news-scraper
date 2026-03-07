# ==========================================
# File: export_CSV.py
# Tugas: Menyimpan hasil scraping ke file CSV 
# ==========================================
import csv
import os

def export_to_csv(data, filename="hasil_scraping_berita.csv"):
    """
    Versi Final: Kompatibel dengan GUI asli, 
    lebih aman terhadap error folder dan karakter Excel.
    """
    if not data:
        print("Data kosong, tidak ada yang disimpan.")
        return

    try:
        # Menangani pembuatan folder jika path mengandung folder
        directory = os.path.dirname(filename)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        # 'utf-8-sig' agar Excel menampilkan teks Indonesia dengan sempurna
        with open(filename, mode="w", newline="", encoding="utf-8-sig") as file:
            # IQBAL NGE-FIX INI: Nambahin "content" biar isi berita ikut kesimpen!
            fieldnames = ["title", "date", "link", "content"] 
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            writer.writeheader()
            for item in data:
                # Mengambil data berdasarkan key, default ke string kosong jika tidak ada
                row = {
                    "title": item.get("title", ""),
                    "date": item.get("date", ""),
                    "link": item.get("link", ""),
                    "content": item.get("content", "") # <--- Tambahan dari Iqbal
                }
                writer.writerow(row)

        print(f"✅ Sukses! Data tersimpan di: {filename}")

    except Exception as e:
        print(f"❌ Terjadi kesalahan: {e}")