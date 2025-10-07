import random
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
    QMessageBox
)
from game.logic import is_valid_move, won
from IA.tree_search import best_move

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
        self.game_state = [
            ['', '', ''],
            ['', '', ''],
            ['', '', '']
        ]
        
        self.free_slots = [
            [0,0], [0,1], [0,2],
            [1,0], [1,1], [1,2],
            [2,0], [2,1], [2,2],
        ]

        self.buttons = []
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
        
       
        temp_buttons_grid = []
        buttons_indx=[]
        for i in range(5):
            if i % 2 == 1:
                board_layout.addWidget(HLine(), i,0, 1,3)
                board_layout.addWidget(HLine(), i,2, 1,3)
                board_layout.addWidget(HLine(), i,4, 1,3)
                continue
                
            buttons_row = []
            for j in range(5):
                
                if j % 2 == 1:
                    board_layout.addWidget(VLine(), i, j,3,1)
                    continue
                
                button = QPushButton('')
                button.setStyleSheet("font-size: 24px;")
                
                buttons_indx.append((i//2,j//2))
                
                button.setFixedSize(100,100)
                
                buttons_row.append(button)
                
                board_layout.addWidget(button, i, j)
            temp_buttons_grid.append(buttons_row)
        
        cont = 0
        for button_row in temp_buttons_grid:
            for button in button_row:
                row, col = buttons_indx[cont]
                button.clicked.connect(lambda _, r=row, c=col: self.player_move(r, c))
                cont += 1 
                
        self.buttons = temp_buttons_grid
        
        return board_widget
    
    def start_game(self):
        
        print(f"Starting game with symbol {self.player_symbol} and difficulty {self.difficulty}")
        self.stacked_widget.setCurrentIndex(1)
        

    def player_move(self,row,col):
      
        if [row, col] not in self.free_slots:
            print("Célula já ocupada!")
            return # Simplesmente sai da função se o movimento for inválido

        # 1. Atualiza o estado lógico e a interface com a jogada do jogador
        self.game_state[row][col] = +1  # Jogador é sempre +1
        self.buttons[row][col].setText(self.player_symbol)
        self.free_slots.remove([row, col])

        # 2. Verifica se o jogador venceu
        if won(self.game_state, +1):
            self.show_game_over("Vitória!", "Parabéns, você venceu!")
            return # O jogo acabou, não chama o PC

        # 3. Verifica se deu empate
        if not self.free_slots:
            self.show_game_over("Empate!", "O jogo terminou em empate.")
            return # O jogo acabou, não chama o PC

        # 4. Se o jogo continua, é a vez do PC
        self.pc_move()

    def pc_move(self):
        if self.free_slots:
            row, col, _ = best_move(-1, self.game_state, self.free_slots)
            pc_symbol = 'O' if self.player_symbol == 'X' else 'X'
            self.game_state[row][col] = -1
            self.buttons[row][col].setText(pc_symbol)
            self.free_slots.remove([row,col])
            
        if won(self.game_state, -1):
            self.show_game_over("Derrota!", "O computador venceu.")
            return
        
        if self.free_slots == []:
            self.show_game_over("Empate!", "O jogo terminou em empate.")
            return

    def show_game_over(self, title,message):
        
        msgBox = QMessageBox(self)
        msgBox.setWindowTitle(title)
        msgBox.setText(message)
        msgBox.setIcon(QMessageBox.Information)
        
        msgBox.addButton("Sair", QMessageBox.RejectRole)
        play_again_button = msgBox.addButton("Jogar Novamente", QMessageBox.AcceptRole)
        msgBox.exec_()
        
        if msgBox.clickedButton() == play_again_button:
            self.reset_game()
        else:
            QApplication.quit()
            
    def reset_game(self):
        self.game_state = [
            ['', '', ''],
            ['', '', ''],
            ['', '', '']
        ]
        self.free_slots = [
            [0,0], [0,1], [0,2],
            [1,0], [1,1], [1,2],
            [2,0], [2,1], [2,2],
        ]
        
        for row in self.buttons:
            for button in row:
                button.setText('')
                button.setEnabled(True)
                
        self.stacked_widget.setCurrentIndex(0)
