import sys
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QListWidget, QMessageBox
import sqlite3
import datetime

DB_FILE = "data/prices.db"
RETAILERS = ["Amazon", "Walmart"]

def init_db():
    conn = sqlite3.connect(DB_FILE)
    conn.execute('''CREATE TABLE IF NOT EXISTS prices
                   (id INTEGER PRIMARY KEY, retailer TEXT, name TEXT, price REAL, date TEXT)''')
    conn.commit()
    conn.close()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Super Deals Canada")
        self.setGeometry(200, 200, 600, 400)

        layout = QVBoxLayout()
        self.btn_update = QPushButton("Actualizar precios")
        self.btn_update.clicked.connect(self.update_prices)
        layout.addWidget(self.btn_update)

        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        self.setLayout(layout)
        init_db()

    def update_prices(self):
        # Este es un ejemplo, en producción se debería insertar scraping real
        conn = sqlite3.connect(DB_FILE)
        conn.execute("INSERT INTO prices (retailer, name, price, date) VALUES (?, ?, ?, ?)",
                     ("Amazon", "Ejemplo Producto", 123.45, str(datetime.datetime.now())))
        conn.commit()
        conn.close()
        self.load_prices()

    def load_prices(self):
        self.list_widget.clear()
        conn = sqlite3.connect(DB_FILE)
        for row in conn.execute("SELECT retailer, name, price, date FROM prices"):
            self.list_widget.addItem(f"{row[0]} - {row[1]} = ${row[2]:.2f} ({row[3]})")
        conn.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
