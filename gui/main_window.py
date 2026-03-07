from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLineEdit,
    QTableWidget, QTableWidgetItem, QLabel,
    QSpinBox, QMessageBox
)

from scraper_cnn import scrape_cnn
from exporter import export_to_excel


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("CNN News Scraper")
        self.resize(800, 600)

        layout = QVBoxLayout()

        # SEARCH KEYWORD
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Masukkan kata kunci berita...")
        layout.addWidget(QLabel("Search Keyword"))
        layout.addWidget(self.search_input)

        # LIMIT ARTIKEL
        layout.addWidget(QLabel("Jumlah Artikel"))

        self.limit_spin = QSpinBox()
        self.limit_spin.setMinimum(1)
        self.limit_spin.setMaximum(100)
        self.limit_spin.setValue(15)   # default jumlah artikel
        layout.addWidget(self.limit_spin)

        # BUTTON SCRAPE
        self.scrape_button = QPushButton("Scrape Berita")
        self.scrape_button.clicked.connect(self.scrape_data)
        layout.addWidget(self.scrape_button)

        # TABLE HASIL
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Judul", "Link"])
        layout.addWidget(self.table)

        # BUTTON EXPORT
        self.export_button = QPushButton("Export ke Excel")
        self.export_button.clicked.connect(self.export_data)
        layout.addWidget(self.export_button)

        self.setLayout(layout)

        self.data = []

    def scrape_data(self):

        keyword = self.search_input.text()
        limit = self.limit_spin.value()

        if keyword == "":
            QMessageBox.warning(self, "Error", "Masukkan kata kunci dulu")
            return

        self.data = scrape_cnn(keyword, limit)

        self.table.setRowCount(len(self.data))

        for row, item in enumerate(self.data):

            self.table.setItem(
                row, 0, QTableWidgetItem(item["title"])
            )

            self.table.setItem(
                row, 1, QTableWidgetItem(item["link"])
            )

    def export_data(self):

        if not self.data:
            QMessageBox.warning(self, "Error", "Belum ada data untuk disimpan")
            return

        export_to_excel(self.data, "hasil_scraping_cnn.xlsx")

        QMessageBox.information(self, "Sukses", "Data berhasil disimpan ke Excel")