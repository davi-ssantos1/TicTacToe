from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon,QKeySequence
from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QCheckBox,
    QLabel,
    QMainWindow,
    QStatusBar,
    QToolBar,
    QGridLayout,
    QWidget,
    QPushButton,
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
)

class VLine(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.VLine)
        self.setFrameShadow(QFrame.Sunken)
        
class HLine(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)

class MainWindow(QMainWindow):
    def __init__(self): 
        super().__init__()
        self.setWindowTitle("PyQt5 Application")
        self.setGeometry(100, 100, 800, 600)
        
        self.board_UI()
                
    def board_UI(self):
        
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        board_widget = QWidget()
        
        board_layout = QGridLayout(board_widget)
        board_layout.setSpacing(10)
        
       
        
        for i in range(5):
            if i % 2 == 1:
                board_layout.addWidget(HLine(), i,0, 1,3)
                board_layout.addWidget(HLine(), i,2, 1,3)
                board_layout.addWidget(HLine(), i,4, 1,3)
                continue
            for j in range(5):
                
                if j % 2 == 1:
                    board_layout.addWidget(VLine(), i, j,3,1)
                    continue
                
                button = QPushButton(f"Button {i},{j}")
                button.setFixedSize(100,100)
                board_layout.addWidget(button, i, j)
           
        main_layout = QVBoxLayout(central_widget)
           
        main_layout.addWidget(board_widget,0, Qt.AlignCenter)
   
        
        
       
        
        
        
        
app = QApplication([])
window = MainWindow()
window.show()
app.exec()