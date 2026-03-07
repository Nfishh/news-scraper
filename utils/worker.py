# ==========================================
# File: utils/worker.py
# Tugas (Orang 5): Background thread untuk scraping
# ==========================================

from PyQt5.QtCore import QThread, pyqtSignal


class ScraperWorker(QThread):
    """
    Menjalankan run_full_scraper() di background thread
    agar GUI tidak freeze saat scraping berlangsung.

    SINYAL:
        progress_update(str)  → pesan status ke QLabel
        result_ready(list)    → data artikel ke QTableWidget
        error_occurred(str)   → pesan error ke QMessageBox
        finished_scraping()   → reset UI setelah selesai
    """

    progress_update   = pyqtSignal(str)
    result_ready      = pyqtSignal(list)
    error_occurred    = pyqtSignal(str)
    finished_scraping = pyqtSignal()

    def __init__(self, url: str, limit: int = 5):
        super().__init__()
        self.url   = url
        self.limit = limit

    def run(self):
        
        try:
            from scraper.link_scraper import run_full_scraper

            self.progress_update.emit("🔍 Membuka halaman dan mencari link artikel...")

            articles = run_full_scraper(self.url, self.limit)

            if articles:
                self.progress_update.emit(
                    f"✅ Selesai! Berhasil mengambil {len(articles)} artikel."
                )
            else:
                self.progress_update.emit("⚠️ Tidak ada artikel yang berhasil diambil.")

            self.result_ready.emit(articles or [])

        except Exception as e:
            self.error_occurred.emit(f"Error saat scraping:\n{str(e)}")
            self.progress_update.emit("❌ Scraping gagal.")

        finally:
            self.finished_scraping.emit()