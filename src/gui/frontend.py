import random
import random
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QGridLayout,
    QWidget,
    QPushButton,
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QStackedWidget,
    QRadioButton,
    QButtonGroup,
    QMessageBox,
    QMessageBox
)
from game.logic import is_valid_move, won
from IA.tree_search import best_move
from game.logic import is_valid_move, won
from IA.tree_search import best_move


class VLine(QFrame):
    """Linha vertical para separar visualmente os botões do tabuleiro."""

    def __init__(self):
        """Inicializa a linha vertical."""
        super().__init__()
        self.setFrameShape(QFrame.VLine)
        self.setFrameShadow(QFrame.Sunken)


class HLine(QFrame):
    """Linha horizontal para separar visualmente os botões do tabuleiro."""

    def __init__(self):
        """Inicializa a linha horizontal."""
        super().__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)


class MainWindow(QMainWindow):
    """
    Janela principal do jogo da velha com interface PyQt5.

    Responsável por gerenciar a interface gráfica, o estado do jogo,
    a interação do usuário e a lógica de quem começa e quem joga.
    """

    def __init__(self):
        """
        Inicializa a janela principal, configura o layout, widgets e estado inicial do jogo.
        """
        super().__init__()
        self.setWindowTitle("PyQt5 Application")
        self.setGeometry(100, 100, 800, 600)

        self.player_symbol = "X"
        self.player_role = None  # +1 ou -1
        self.pc_symbol = "O"
        self.pc_role = None  # +1 ou -1

        self.game_state = [
            ["", "", ""],
            ["", "", ""],
            ["", "", ""]
        ]

        self.free_slots = [
            [0, 0], [0, 1], [0, 2],
            [1, 0], [1, 1], [1, 2],
            [2, 0], [2, 1], [2, 2],
        ]

        self.buttons = []
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        menu_page = self.create_menu_ui()
        board_page = self.create_board_ui()

        self.stacked_widget.addWidget(menu_page)
        self.stacked_widget.addWidget(board_page)

    def create_menu_ui(self):
        """
        Cria a interface do menu inicial, permitindo ao usuário escolher símbolo e quem começa.

        Returns:
            QWidget: Widget do menu inicial.
        """
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

        self.button_x.toggled.connect(lambda: self.update_symbol("X"))
        self.button_o.toggled.connect(lambda: self.update_symbol("O"))

        start_label = QLabel("Quem começa?")
        self.start_group = QButtonGroup(menu_widget)
        self.start_player = QRadioButton("Você")
        self.start_pc = QRadioButton("Computador")
        self.start_player.setChecked(True)

        start_layout = QHBoxLayout()
        start_layout.addStretch()
        start_layout.addWidget(self.start_player)
        start_layout.addWidget(self.start_pc)
        start_layout.addStretch()

        self.start_group.addButton(self.start_player)
        self.start_group.addButton(self.start_pc)

        start_button = QPushButton("Start Game")
        start_button.clicked.connect(self.start_game)

        main_layout.addStretch()
        main_layout.addWidget(title_label, alignment=Qt.AlignCenter)
        main_layout.addSpacing(30)
        main_layout.addWidget(symbol_label, alignment=Qt.AlignCenter)
        main_layout.addLayout(symbol_layout)
        main_layout.addSpacing(20)
        main_layout.addWidget(start_label, alignment=Qt.AlignCenter)
        main_layout.addLayout(start_layout)
        main_layout.addSpacing(40)
        main_layout.addWidget(start_button, alignment=Qt.AlignCenter)
        main_layout.addStretch()

        return menu_widget

    def update_symbol(self, symbol):
        """
        Atualiza o símbolo do jogador conforme a seleção no menu.

        Args:
            symbol (str): Símbolo escolhido ('X' ou 'O').
        """
        self.player_symbol = symbol

    def create_board_ui(self):
        """
        Cria a interface do tabuleiro do jogo da velha.

        Returns:
            QWidget: Widget do tabuleiro.
        """
        board_widget = QWidget()
        board_layout = QGridLayout(board_widget)
        board_layout.setAlignment(Qt.AlignCenter)
        board_layout.setSpacing(10)

        temp_buttons_grid = []
        buttons_indx = []
        for i in range(5):
            if i % 2 == 1:
                board_layout.addWidget(HLine(), i, 0, 1, 3)
                board_layout.addWidget(HLine(), i, 2, 1, 3)
                board_layout.addWidget(HLine(), i, 4, 1, 3)
                continue

            buttons_row = []
            for j in range(5):
                if j % 2 == 1:
                    board_layout.addWidget(VLine(), i, j, 3, 1)
                    continue

                button = QPushButton("")
                button.setStyleSheet("font-size: 24px;")
                buttons_indx.append((i // 2, j // 2))
                button.setFixedSize(100, 100)
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
        """
        Inicia o jogo, define quem é +1 e -1, limpa o tabuleiro e faz a primeira jogada se necessário.
        """
        if self.start_player.isChecked():
            self.player_role = +1
            self.pc_role = -1
            self.pc_symbol = "O" if self.player_symbol == "X" else "X"
        else:
            self.player_role = -1
            self.pc_role = +1
            self.pc_symbol = "O" if self.player_symbol == "X" else "X"
        self.reset_game(clear_menu=False)
        self.stacked_widget.setCurrentIndex(1)
        if self.pc_role == +1:
            self.pc_move()

    def player_move(self, row, col):
        """
        Realiza a jogada do jogador humano.

        Args:
            row (int): Linha do tabuleiro.
            col (int): Coluna do tabuleiro.
        """
        if [row, col] not in self.free_slots:
            print("Célula já ocupada!")
            return

        self.game_state[row][col] = self.player_role
        self.buttons[row][col].setText(self.player_symbol)
        self.free_slots.remove([row, col])

        if won(self.game_state, self.player_role):
            self.show_game_over("Vitória!", "Parabéns, você venceu!")
            return

        if not self.free_slots:
            self.show_game_over("Empate!", "O jogo terminou em empate.")
            return

        self.pc_move()

    def pc_move(self):
        """
        Realiza a jogada do computador. Se for a primeira jogada, escolhe uma quina aleatória.
        Nas demais, utiliza a função de melhor jogada.
        """
        if self.free_slots:
            if len(self.free_slots) == 9:
                # Primeira jogada: sorteia uma das quinas
                corners = [[0, 0], [0, 2], [2, 0], [2, 2]]
                move = random.choice(
                    [corner for corner in corners if corner in self.free_slots]
                )
                row, col = move
            else:
                row, col, _ = best_move(self.pc_role, self.game_state, self.free_slots)
            self.game_state[row][col] = self.pc_role
            self.buttons[row][col].setText(self.pc_symbol)
            self.free_slots.remove([row, col])

        if won(self.game_state, self.pc_role):
            self.show_game_over("Derrota!", "O computador venceu.")
            return

        if not self.free_slots:
            self.show_game_over("Empate!", "O jogo terminou em empate.")
            return

    def show_game_over(self, title, message):
        """
        Exibe uma mensagem de fim de jogo e pergunta se o usuário deseja jogar novamente.

        Args:
            title (str): Título da janela.
            message (str): Mensagem a ser exibida.
        """
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

    def reset_game(self, clear_menu=True):
        """
        Reinicia o estado do jogo e limpa o tabuleiro.

        Args:
            clear_menu (bool, optional): Se True, retorna ao menu inicial. Default é True.
        """
        self.game_state = [
            ["", "", ""],
            ["", "", ""],
            ["", "", ""]
        ]
        self.free_slots = [
            [0, 0], [0, 1], [0, 2],
            [1, 0], [1, 1], [1, 2],
            [2, 0], [2, 1], [2, 2],
        ]
        for row in self.buttons:
            for button in row:
                button.setText("")
                button.setEnabled(True)
        if clear_menu:
            self.stacked_widget.setCurrentIndex(0)
