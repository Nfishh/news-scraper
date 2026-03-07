# ==========================================
# File: gui/main_window.py
# ==========================================

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLineEdit,
    QTableWidget, QTableWidgetItem, QLabel,
    QSpinBox, QMessageBox, QProgressBar
)
from PyQt5.QtCore import Qt

from export.export_csv import export_to_csv

# Worker buatan Orang 5
from utils.worker import ScraperWorker


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("News Scraper")
        self.resize(900, 600)

        self.data   = []
        self.worker = None   # Disimpan sebagai atribut agar tidak di-GC sebelum selesai

        layout = QVBoxLayout()

        # INPUT URL WEBSITE
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(
            "Masukkan URL halaman berita (contoh: https://nasional.kompas.com)"
        )
        layout.addWidget(QLabel("URL Website Berita"))
        layout.addWidget(self.search_input)

        # LIMIT ARTIKEL
        layout.addWidget(QLabel("Jumlah Artikel"))
        self.limit_spin = QSpinBox()
        self.limit_spin.setMinimum(1)
        self.limit_spin.setMaximum(20)
        self.limit_spin.setValue(5)
        layout.addWidget(self.limit_spin)

        # BUTTON SCRAPE
        self.scrape_button = QPushButton("Scrape Berita")
        self.scrape_button.clicked.connect(self.scrape_data)
        layout.addWidget(self.scrape_button)

        # PROGRESS BAR — hanya muncul saat scraping berjalan
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)        # mode indeterminate (animasi terus)
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        # LABEL STATUS
        self.status_label = QLabel("Siap.")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)

        # TABLE HASIL
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Judul", "Tanggal", "Link"])
        layout.addWidget(self.table)

        # BUTTON EXPORT
        self.export_button = QPushButton("Export ke CSV")
        self.export_button.clicked.connect(self.export_data)
        layout.addWidget(self.export_button)

        self.setLayout(layout)

    # ==========================================
    # SCRAPE DATA — sekarang pakai QThread
    # ==========================================

    def scrape_data(self):
        """
        Memulai ScraperWorker di background thread.
        GUI tetap responsif selama scraping berjalan.
        """
        url   = self.search_input.text().strip()
        limit = self.limit_spin.value()

        if not url:
            QMessageBox.warning(self, "Error", "Masukkan URL berita dulu")
            return

        # Reset tabel dan data lama
        self.table.setRowCount(0)
        self.data = []

        # Disable UI agar user tidak klik dua kali
        self._set_ui_busy(True)

        # Buat worker baru, sambungkan sinyal, lalu jalankan
        self.worker = ScraperWorker(url=url, limit=limit)

        # progress_update → update teks status_label
        self.worker.progress_update.connect(self.status_label.setText)

        # result_ready → isi tabel dengan data artikel
        self.worker.result_ready.connect(self._tampilkan_hasil)

        # error_occurred → tampilkan dialog error
        self.worker.error_occurred.connect(
            lambda msg: QMessageBox.warning(self, "Error", msg)
        )

        # finished_scraping → kembalikan UI ke mode normal
        self.worker.finished_scraping.connect(lambda: self._set_ui_busy(False))

        self.worker.start()

    # ==========================================
    # SLOT: ISI TABEL SETELAH DATA SIAP
    # ==========================================

    def _tampilkan_hasil(self, articles: list):
        """
        Dipanggil oleh sinyal result_ready dari worker.
        Mengisi QTableWidget dengan data yang diterima.
        """
        self.data = articles
        self.table.setRowCount(len(articles))

        for row, item in enumerate(articles):
            self.table.setItem(row, 0, QTableWidgetItem(item.get("title", "-")))
            self.table.setItem(row, 1, QTableWidgetItem(item.get("date",  "-")))
            self.table.setItem(row, 2, QTableWidgetItem(item.get("link",  "-")))

    # ==========================================
    # EXPORT DATA — tidak berubah dari Orang 4
    # ==========================================

    def export_data(self):
        if not self.data:
            QMessageBox.warning(self, "Error", "Belum ada data untuk disimpan")
            return

        export_to_csv(self.data)
        QMessageBox.information(self, "Sukses", "Data berhasil diexport ke CSV")

    # ==========================================
    # HELPER: TOGGLE MODE BUSY / IDLE
    # ==========================================

    def _set_ui_busy(self, busy: bool):
        """
        busy=True  → disable input & tombol, tampilkan progress bar
        busy=False → enable kembali, sembunyikan progress bar
        """
        self.scrape_button.setEnabled(not busy)
        self.export_button.setEnabled(not busy)
        self.search_input.setEnabled(not busy)
        self.limit_spin.setEnabled(not busy)
        self.progress_bar.setVisible(busy)

        if busy:
            self.status_label.setText("⏳ Sedang scraping, harap tunggu...")