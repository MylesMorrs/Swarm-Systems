import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtWebEngineWidgets import QWebEngineView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HTML Viewer")

        self.browser = QWebEngineView()
        # Ensure the HTML file is in the same directory as your Python script
        # or provide the full path to the HTML file.
        with open("/home/mcuser/Mother/scripts/map.html", "r") as f: # Use 'index.html' or your actual file name.
            html_content = f.read()
        self.browser.setHtml(html_content)

        self.setCentralWidget(self.browser)
        self.setGeometry(100, 100, 800, 600) # Optional: Set initial window size and position.

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
