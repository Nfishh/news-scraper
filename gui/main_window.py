from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLineEdit,
    QTableWidget, QTableWidgetItem, QLabel,
    QSpinBox, QMessageBox
)

# Import sesuai struktur folder
from scraper.link_scraper import run_full_scraper
from export.export_csv import export_to_csv


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("News Scraper")
        self.resize(900, 600)

        layout = QVBoxLayout()

        # INPUT URL WEBSITE
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Masukkan URL halaman berita (contoh: https://nasional.kompas.com)")
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

        self.data = []

    def scrape_data(self):

        url = self.search_input.text()
        limit = self.limit_spin.value()

        if url == "":
            QMessageBox.warning(self, "Error", "Masukkan URL berita dulu")
            return

        try:
            # Jalankan scraper lengkap
            self.data = run_full_scraper(url, limit)

        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))
            return

        # tampilkan ke tabel
        self.table.setRowCount(len(self.data))

        for row, item in enumerate(self.data):

            self.table.setItem(
                row, 0, QTableWidgetItem(item.get("title", "-"))
            )

            self.table.setItem(
                row, 1, QTableWidgetItem(item.get("date", "-"))
            )

            self.table.setItem(
                row, 2, QTableWidgetItem(item.get("link", "-"))
            )

    def export_data(self):

        if not self.data:
            QMessageBox.warning(self, "Error", "Belum ada data untuk disimpan")
            return

        export_to_csv(self.data)

        QMessageBox.information(self, "Sukses", "Data berhasil diexport ke CSV")