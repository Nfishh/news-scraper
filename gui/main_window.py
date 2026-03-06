from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QProgressBar, QLabel, QSpinBox, QDateEdit, QHeaderView
)
from PyQt5.QtCore import QDate, QTimer, Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("News Scraper App")
        self.setGeometry(100, 100, 900, 600)

        self.current_count = 0
        self.total_limit = 0

        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        form_layout = QHBoxLayout()

        # ===== Judul Aplikasi =====
        title = QLabel("News Scraper Application")
        title.setStyleSheet("font-size:20px; font-weight:bold;")
        title.setAlignment(Qt.AlignCenter)

        # ===== Input URL =====
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Masukkan URL website berita")

        # ===== Limit berita =====
        self.limit_spin = QSpinBox()
        self.limit_spin.setRange(1, 100)
        self.limit_spin.setValue(15)

        # ===== Tanggal =====
        self.start_date = QDateEdit()
        self.start_date.setCalendarPopup(True)
        self.start_date.setDate(QDate.currentDate())

        self.end_date = QDateEdit()
        self.end_date.setCalendarPopup(True)
        self.end_date.setDate(QDate.currentDate())

        # ===== Tombol =====
        self.start_button = QPushButton("Start Scraping")
        self.export_button = QPushButton("Export")

        # Style Tombol
        self.start_button.setStyleSheet(
            "background-color: #4CAF50; color: white; padding:6px;"
        )

        self.export_button.setStyleSheet(
            "background-color: #2196F3; color: white; padding:6px;"
        )

        self.start_button.clicked.connect(self.start_scraping)

        # ===== Tambahkan ke Form Layout =====
        form_layout.addWidget(QLabel("URL:"))
        form_layout.addWidget(self.url_input)

        form_layout.addWidget(QLabel("Limit:"))
        form_layout.addWidget(self.limit_spin)

        form_layout.addWidget(QLabel("Start Date:"))
        form_layout.addWidget(self.start_date)

        form_layout.addWidget(QLabel("End Date:"))
        form_layout.addWidget(self.end_date)

        form_layout.addWidget(self.start_button)
        form_layout.addWidget(self.export_button)

        # ===== Table =====
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["No", "Judul", "Tanggal", "Link"])

        # Auto resize tabel
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # ===== Progress Bar =====
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setFixedHeight(20)

        # ===== Status Label =====
        self.status_label = QLabel("Status: Ready")

        # ===== Tambahkan ke Layout =====
        main_layout.addWidget(title)
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.table)
        main_layout.addWidget(self.progress_bar)
        main_layout.addWidget(self.status_label)

        # Padding layout
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)

        central_widget.setLayout(main_layout)

    def start_scraping(self):

        # Reset tabel dan progress
        self.table.setRowCount(0)
        self.progress_bar.setValue(0)

        # Ambil limit
        self.total_limit = self.limit_spin.value()
        self.current_count = 0

        # Disable tombol
        self.start_button.setEnabled(False)

        self.status_label.setText("Status: Scraping dimulai...")

        # Timer simulasi scraping
        self.timer = QTimer()
        self.timer.timeout.connect(self.simulate_scraping)
        self.timer.start(500)

    def simulate_scraping(self):

        if self.current_count < self.total_limit:
            self.current_count += 1

            # Data dummy
            dummy_data = {
                "title": f"Berita Ke-{self.current_count}",
                "date": QDate.currentDate().toString("dd-MM-yyyy"),
                "link": "https://example.com"
            }

            self.add_to_table(dummy_data)

            # Update progress
            progress = int((self.current_count / self.total_limit) * 100)
            self.progress_bar.setValue(progress)

            self.status_label.setText(
                f"Status: Mengambil berita {self.current_count} dari {self.total_limit}"
            )

        else:
            # Stop timer
            self.timer.stop()
            self.start_button.setEnabled(True)

            self.status_label.setText("Status: Scraping selesai")

    def add_to_table(self, data):

        row_position = self.table.rowCount()
        self.table.insertRow(row_position)

        self.table.setItem(row_position, 0, QTableWidgetItem(str(row_position + 1)))
        self.table.setItem(row_position, 1, QTableWidgetItem(data.get("title", "")))
        self.table.setItem(row_position, 2, QTableWidgetItem(data.get("date", "")))
        self.table.setItem(row_position, 3, QTableWidgetItem(data.get("link", "")))