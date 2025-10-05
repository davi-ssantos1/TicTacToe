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
    QStackedWidget,
    QRadioButton,
    QButtonGroup,
    QComboBox,
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
        
        self.player_symbol = 'X'
        self.difficulty = 'Easy'
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        menu_page = self.create_menu_ui()
        board_page = self.create_board_ui()
        
        self.stacked_widget.addWidget(menu_page)
        self.stacked_widget.addWidget(board_page)
        
    def create_menu_ui(self):
        menu_widget = QWidget()
        main_layout = QVBoxLayout(menu_widget)
        
        title_label = QLabel("Game Menu")
        title_label.setAlignment(Qt.AlignCenter)
    
        symbol_label = QLabel("Choose your symbol:")
        
        self.buttom_group = QButtonGroup(menu_widget)
        self.button_x = QRadioButton("X")
        self.button_o = QRadioButton("O")
        
        symbol_layout = QHBoxLayout()
        symbol_layout.addStretch()
        symbol_layout.addWidget(self.button_x)
        symbol_layout.addWidget(self.button_o)
        symbol_layout.addStretch()
        
        self.buttom_group.addButton(self.button_x)
        self.buttom_group.addButton(self.button_o)
        
        
        
        self.button_x.toggled.connect(lambda: self.update_symbol('X'))
        self.button_o.toggled.connect(lambda :self.update_symbol('O')) 
        
        
        difficulty_label = QLabel("Select Difficulty:")
        self.combo_difficulty = QComboBox()
        self.combo_difficulty.addItems(["Easy", "Medium", "Hard"])
        
        self.combo_difficulty.currentTextChanged.connect(self.set_difficulty)
        
        start_button = QPushButton("Start Game")
        start_button.clicked.connect(self.start_game)        
        
        main_layout.addStretch()
        main_layout.addWidget(title_label, alignment=Qt.AlignCenter)
        main_layout.addSpacing(30)
        main_layout.addWidget(symbol_label, alignment=Qt.AlignCenter)
        main_layout.addLayout(symbol_layout)
        main_layout.addSpacing(20)
        main_layout.addWidget(difficulty_label, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.combo_difficulty, alignment=Qt.AlignCenter)
        main_layout.addSpacing(40)
        main_layout.addWidget(start_button, alignment=Qt.AlignCenter)
        main_layout.addStretch()
        
        return menu_widget
        
        
    def update_symbol(self, symbol):
        self.player_symbol = symbol   
        
    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
        
    def create_board_ui(self):
        
        
        board_widget = QWidget()
        
        board_layout = QGridLayout(board_widget)
        board_layout.setAlignment(Qt.AlignCenter)
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
           
        
        return board_widget
    def start_game(self):
        
        print(f"Starting game with symbol {self.player_symbol} and difficulty {self.difficulty}")
        self.stacked_widget.setCurrentIndex(1)
        
        
       
        
        
        
        
app = QApplication([])
window = MainWindow()
window.show()
app.exec()