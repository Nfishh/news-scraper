from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLineEdit,
    QTableWidget, QTableWidgetItem, QLabel,
    QSpinBox, QMessageBox
)

# Import mesin milik Julfi dan Iqbal/Orang 2
from utils.worker import ScraperWorker
from export.export_csv import export_to_csv

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("News Scraper (Anti-Freeze Edition)")
        self.resize(900, 600)

        layout = QVBoxLayout()

        # INPUT URL WEBSITE
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Masukkan URL (contoh: https://indeks.kompas.com/news)")
        layout.addWidget(QLabel("URL Website Berita"))
        layout.addWidget(self.search_input)

        # LIMIT ARTIKEL
        layout.addWidget(QLabel("Jumlah Artikel"))
        self.limit_spin = QSpinBox()
        self.limit_spin.setMinimum(1)
        self.limit_spin.setMaximum(50)
        self.limit_spin.setValue(5)
        layout.addWidget(self.limit_spin)

        # TOMBOL SCRAPE
        self.scrape_button = QPushButton("Scrape Berita")
        self.scrape_button.clicked.connect(self.mulai_scraping)
        layout.addWidget(self.scrape_button)

        # LABEL STATUS (Dapat sinyal dari mesin Julfi)
        self.status_label = QLabel("Status: Menunggu perintah...")
        self.status_label.setStyleSheet("color: blue; font-weight: bold;")
        layout.addWidget(self.status_label)

        # TABLE HASIL (4 Kolom buatan Iqbal)
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Judul", "Tanggal", "Link", "Isi Berita"])
        layout.addWidget(self.table)

        # TOMBOL EXPORT
        self.export_button = QPushButton("Export ke CSV")
        self.export_button.clicked.connect(self.export_data)
        layout.addWidget(self.export_button)

        self.setLayout(layout)
        self.data = []

    # --- FUNGSI MENGHUBUNGKAN UI DENGAN THREAD JULFI ---
    def mulai_scraping(self):
        url = self.search_input.text()
        limit = self.limit_spin.value()

        if url == "":
            QMessageBox.warning(self, "Error", "Masukkan URL berita dulu!")
            return

        # 1. Matikan tombol biar user gak spam klik
        self.scrape_button.setEnabled(False)
        self.table.setRowCount(0) # Bersihkan tabel
        self.data = []

        # 2. Nyalakan mesin Thread Julfi
        self.worker = ScraperWorker(url, limit)
        
        # 3. Sambungkan sinyal-sinyal Julfi ke fungsi di UI ini
        self.worker.progress_update.connect(self.update_status)
        self.worker.result_ready.connect(self.tampilkan_data)
        self.worker.error_occurred.connect(self.tampilkan_error)
        self.worker.finished_scraping.connect(self.scraping_selesai)

        # 4. GAS JALANKAN DI BACKGROUND!
        self.worker.start()

    # --- FUNGSI PENERIMA SINYAL DARI JULFI ---
    def update_status(self, pesan):
        self.status_label.setText(f"Status: {pesan}")

    def tampilkan_data(self, articles):
        self.data = articles
        self.table.setRowCount(len(self.data))

        for row, item in enumerate(self.data):
            self.table.setItem(row, 0, QTableWidgetItem(item.get("title", "-")))
            self.table.setItem(row, 1, QTableWidgetItem(item.get("date", "-")))
            self.table.setItem(row, 2, QTableWidgetItem(item.get("link", "-")))
            self.table.setItem(row, 3, QTableWidgetItem(item.get("content", "-")))

    def tampilkan_error(self, pesan_error):
        QMessageBox.warning(self, "Error", pesan_error)

    def scraping_selesai(self):
        # Nyalakan tombol scrape lagi setelah beres
        self.scrape_button.setEnabled(True)

    # --- FUNGSI EXPORT IQBAL ---
    def export_data(self):
        if not self.data:
            QMessageBox.warning(self, "Error", "Belum ada data untuk disimpan!")
            return
        
        export_to_csv(self.data)
        QMessageBox.information(self, "Sukses", "Data berhasil diexport ke file CSV di folder projek!")