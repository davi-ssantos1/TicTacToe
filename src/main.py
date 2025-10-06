from gui.frontend import MainWindow
from PyQt5.QtWidgets import QApplication


app = QApplication([])
window = MainWindow()
window.show()
app.exec()