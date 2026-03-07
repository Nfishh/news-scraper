# ==========================================
# File: utils/data_processor.py
# Tugas: Membersihkan dan memvalidasi data berita
# ==========================================

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

def parse_date(date_text): # <- Modul (2) yang wajib dipanggil kalo mau bersihin teks scrapingnya - Iqbal
    """
    Mengubah teks tanggal bahasa Indonesia menjadi format standar YYYY-MM-DD.
    Contoh input: "06 Maret 2026" -> Output: "2026-03-06"
    """
    if not date_text:
        return ""
        
    # 1. Kamus penerjemah bulan Indonesia ke angka
    bulan_indo = {
        "januari": "01", "februari": "02", "maret": "03", "april": "04",
        "mei": "05", "juni": "06", "juli": "07", "agustus": "08",
        "september": "09", "oktober": "10", "november": "11", "desember": "12"
    }
    
    # 2. Kita bersihin dulu teksnya pakai fungsi yang udah kita bikin sebelumnya, lalu kecilin semua hurufnya (lower)
    date_text = clean_text(date_text).lower() 
    
    try:
        # 3. Misahin teks berdasarkan spasi. "06 maret 2026" jadi daftar: ["06", "maret", "2026"]
        parts = date_text.split()
        
        if len(parts) >= 3:
            hari = parts[0].zfill(2) # zfill(2) ini trik biar kalau angkanya "6", otomatis ditambahin nol jadi "06"
            bulan_teks = parts[1]
            tahun = parts[2]
            
            # 4. Ambil angka bulan dari kamus. Kalau gak nemu, defaultnya "01"
            bulan_angka = bulan_indo.get(bulan_teks, "01") 
            
            # 5. Susun ulang formatnya jadi Tahun-Bulan-Hari
            return f"{tahun}-{bulan_angka}-{hari}"
            
    except Exception as e:
        print(f"Ups, ada error pas nerjemahin tanggal: {e}")
        
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