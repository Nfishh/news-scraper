# ==========================================
# File: utils/data_processor.py
# Tugas: Membersihkan dan memvalidasi data berita
# ==========================================

import re
# !!Hanya Simulasi - Iqbal
# Bikin Data Dummy (Simulasi data kotor dari Scraper)
dummy_article = {
    "title": "   \n\n  BREAKING NEWS: Pasar Saham Anjlok Hari Ini!!! \t  ",
    "date": "06 Maret 2026",
    "content": "Jakarta - Harga saham turun drastis. \n\n Baca berita selengkapnya di www.beritapalsu.com. \n\n Klik subscribe ya!"
}

# Fungsi Pembersih Teks 
def clean_text(text):# <- Modul (1) yang wajib dipanggil kalo mau bersihin teks scrapingnya - Iqbal
    """
    Fungsi ini bertugas membersihkan teks dari spasi berlebih
    dan karakter-karakter aneh (seperti \n atau \t).
    """
    # Cek apakah teksnya kosong (None), kalau kosong kembaliin string kosong
    if not text:
        return ""
    
    # Menghapus spasi di awal dan akhir, serta menghapus \n dan \t
    teks_bersih = text.strip()
    
    return teks_bersih

# [Taruh di bawah fungsi clean_text]

def parse_date(date_text):
    """
    Mengubah teks tanggal menjadi format YYYY-MM-DD menggunakan pelacak pola (Regex).
    """
    if not date_text:
        return ""
        
    bulan_indo = {
        "januari": "01", "februari": "02", "maret": "03", "april": "04",
        "mei": "05", "juni": "06", "juli": "07", "agustus": "08",
        "september": "09", "oktober": "10", "november": "11", "desember": "12"
    }
    
    date_text = date_text.lower()
    
    try:
        # Senjata rahasia Regex: Cari pola "angka(1-2 digit) spasi huruf spasi angka(4 digit)"
        # Contoh yang bakal ketangkap: "7 maret 2026" atau "07 maret 2026"
        match = re.search(r'(\d{1,2})\s+([a-z]+)\s+(\d{4})', date_text)
        
        if match:
            hari = match.group(1).zfill(2)
            bulan_teks = match.group(2)
            tahun = match.group(3)
            
            bulan_angka = bulan_indo.get(bulan_teks, "01") 
            
            return f"{tahun}-{bulan_angka}-{hari}"
            
    except Exception as e:
        print(f"Ups, ada error pas nerjemahin tanggal: {e}")
        
    # Kalau gagal ngelacak pola, kembalikan teks aslinya (tapi udah dibersihin spasinya)
    return clean_text(date_text)
        
    # Kalau gagal atau formatnya aneh banget, kembaliin teks aslinya aja
    return date_text 

def validate_article(article_data): # <- Modul (3) yang wajib dipanggil kalo mau bersihin teks scrapingnya - Iqbal
    """
    Satpam Kualitas: Memastikan artikel punya judul, tanggal, dan isi yang tidak kosong.
    """
    # 1. Kalau datanya bener-bener kosong/nggak ada, langsung tolak
    if not article_data:
        return False
        
    # 2. Kita ambil datanya, dan bersihin sekalian buat ngecek 
    # (Pake .get() biar kodenya gak error kalau misalnya si Scraper lupa masukin kata kunci "title")
    judul = clean_text(article_data.get("title", ""))
    tanggal = article_data.get("date", "")
    isi = clean_text(article_data.get("content", ""))
    
    # 3. Cek kelengkapan: Kalau judul KOSONG, ATAU tanggal KOSONG, ATAU isi KOSONG -> Tolak!
    if not judul or not tanggal or not isi:
        return False
        
    # 4. Kalau semua cek lolos, berarti datanya bagus!
    return True

# ==========================================
# UPDATE AREA TESTING DI PALING BAWAH (!!!Hanya Simulai!!!), hanya pengetesan apakah kode bekerja - Iqbal
# ==========================================
if __name__ == "__main__":
    print("=== MENGUJI FUNGSI DATA PROCESSOR ===")
    
    # Tes Judul
    judul_kotor = dummy_article["title"]
    print(f"Judul Asli   : '{judul_kotor}'")
    print(f"Judul Bersih : '{clean_text(judul_kotor)}'\n")
    
    # Tes Tanggal
    tanggal_kotor = dummy_article["date"]
    print(f"Tanggal Asli : '{tanggal_kotor}'")
    print(f"Tanggal Rapih: '{parse_date(tanggal_kotor)}'")

    # Tes Satpam Kualitas (validate_article)
    print("\n--- Tes Validasi Artikel ---")
    
    # Kasus 1: Artikel Bagus (Lengkap)
    artikel_bagus = {
        "title": "Harga Emas Naik",
        "date": "06 Maret 2026",
        "content": "Ini adalah isi berita yang panjang dan jelas."
    }
    
    # Kasus 2: Artikel Cacat (Isinya kosong)
    artikel_cacat = {
        "title": "Harga Emas Turun",
        "date": "06 Maret 2026",
        "content": "    " # Ceritanya scrapernya ngambil teks kosong/spasi doang
    }
    
    print(f"Apakah Artikel Bagus valid? {validate_article(artikel_bagus)}")
    print(f"Apakah Artikel Cacat valid? {validate_article(artikel_cacat)}")