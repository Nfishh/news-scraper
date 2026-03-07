# ==========================================
# File: scraper/content_scraper.py
# Tugas: Membuka 1 URL, mengambil teks, dan membersihkannya
# ==========================================

from selenium.webdriver.common.by import By
import time

# 1. KITA IMPORT MODUL PEMBERSIH BUATANMU!
from utils.data_processor import clean_text, parse_date, validate_article

def scrape_single_article(driver, url):
    """
    Fungsi ini menerima driver Selenium dan 1 URL artikel.
    Tugasnya: Buka web -> Ekstrak Teks -> Bersihkan -> Validasi.
    """
    print(f"\nMencoba membuka: {url}")
    
    try:
        driver.get(url)
        # Delay secukupnya sesuai instruksi dosen agar server tidak down
        time.sleep(3) 
        
        # --- TEBAKAN 1: MENCARI JUDUL (Biasanya h1) ---
        try:
            judul_mentah = driver.find_element(By.TAG_NAME, 'h1').text
        except:
            judul_mentah = "" # Kalau gagal, kosongin aja
            
        # --- TEBAKAN 2: MENCARI TANGGAL YANG LEBIH PINTAR ---
        tanggal_mentah = ""
        
        # Cara 1: Coba cari pakai standar umum (tag time)
        try:
            tanggal_mentah = driver.find_element(By.TAG_NAME, 'time').text
        except:
            pass
            
        # Cara 2: Kalau gagal, coba cari class khusus punya Kompas.com
        if not tanggal_mentah:
            try:
                tanggal_mentah = driver.find_element(By.CLASS_NAME, 'read__time').text
            except:
                pass

        # Cara 3: Kalau masih gagal juga, coba cari class khusus punya Detik.com
        if not tanggal_mentah:
            try:
                tanggal_mentah = driver.find_element(By.CLASS_NAME, 'detail__date').text
            except:
                pass
            
        # --- TEBAKAN 3: MENCARI ISI (Kumpulan tag p) ---
        try:
            # Ambil semua tag <p> yang ada di halaman
            paragraf_elements = driver.find_elements(By.TAG_NAME, 'p')
            
            # Gabungkan teks dari semua paragraf menjadi satu teks panjang
            isi_kumpulan = []
            for p in paragraf_elements:
                isi_kumpulan.append(p.text)
            
            isi_mentah = " ".join(isi_kumpulan)
        except:
            isi_mentah = ""

    # (Selipkan kode ini sebelum artikel_jadi)
        print(f"--- INFO DEBUGGING ---")
        print(f"Judul Mentah  : '{judul_mentah}'")
        print(f"Tanggal Mentah: '{tanggal_mentah}'")
        print(f"Isi Mentah    : '{isi_mentah[:100]}...'") # Cuma nampilin 100 huruf awal biar terminal gak penuh
        print(f"----------------------")

        # ==========================================
        # SAATNYA MESIN CUCI IQBAL BEKERJA!
        # ==========================================
        artikel_jadi = {
            "title": clean_text(judul_mentah),
            "date": parse_date(tanggal_mentah),
            "content": clean_text(isi_mentah)
        }
        
        # Masukkan ke Satpam Kualitas
        if validate_article(artikel_jadi):
            print("✅ Artikel Valid!")
            return artikel_jadi
        else:
            print("❌ Artikel Cacat (Ada bagian yang kosong)!")
            return None

    except Exception as e:
        print(f"Gagal memproses URL karena error: {e}")
        return None

def scrape_multiple_articles(driver, url_list):
    """
    Mesin Ban Berjalan: Menerima banyak URL, memprosesnya satu per satu,
    lalu mengumpulkan semua artikel yang valid ke dalam satu koper (List).
    """
    kumpulan_artikel_valid = []
    
    print(f"Mulai memproses {len(url_list)} URL artikel...")
    
    for url in url_list:
        # 1. Panggil fungsi koki kita yang udah jago tadi
        hasil = scrape_single_article(driver, url)
        
        # 2. Kalau hasilnya valid (nggak None), masukin ke koper!
        if hasil:
            # WAJIB DITAMBAHIN: Biar tabel GUI Fidella bisa nampilin link-nya
            hasil["link"] = url 
            kumpulan_artikel_valid.append(hasil)
            
    print(f"\nSelesai! Berhasil mengumpulkan {len(kumpulan_artikel_valid)} artikel valid.")
    return kumpulan_artikel_valid

# ========================================== !! Hanya Simulasi !! - Iqbal
# AREA TESTING (Hanya dijalankan jika file ini di-run langsung)
# ========================================== !! Hanya simulasi !! - Iqbal
if __name__ == "__main__":
    from selenium import webdriver
    
    print("Membuka browser untuk testing...")
    driver = webdriver.Chrome() 
    
    # Simulasi data dari Orang 2 (List berisi banyak URL)
    list_url_dari_temen = [
        "https://internasional.kompas.com/read/2026/03/07/073642570/rusia-disebut-diam-diam-bantu-iran-hadapi-as-israel",
        "https://nasional.kompas.com/read/2026/03/06/123456789/contoh-link-berita-kedua-biar-error-buat-tes-satpam" # Sengaja disalahin biar dites satpamnya
    ]
    
    # Jalankan mesin pabriknya!
    hasil_akhir = scrape_multiple_articles(driver, list_url_dari_temen)
    
    print("\n=== HASIL AKHIR PABRIK BERITA ===")
    for artikel in hasil_akhir:
        print(f"Judul: {artikel['title']}")
        print(f"Tanggal: {artikel['date']}")
        print(f"Link: {artikel['link']}\n")
        print(f"Isi: {artikel['content'][:150]}...\n") # Cuma print 150 huruf awal
    
    driver.quit()