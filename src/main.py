from PyQt5.QtWidgets import QApplication
from gui.frontend import MainWindow

def main():
    """
    Inicializa e executa a aplicação do jogo da velha.

    Esta função cria a aplicação Qt, instancia a janela principal e inicia o loop de eventos da interface gráfica.
    """
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()