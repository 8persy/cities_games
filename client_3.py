import pickle
import socket
import threading

from PyQt6.QtCore import pyqtSignal, QObject
from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QVBoxLayout, QLineEdit, QGridLayout, QTextEdit

from client_gui import Ui_MainWindow


class CityGameClient(QObject):
    message_received = pyqtSignal(str)

    def __init__(self, host="127.0.0.1", port=5555):
        super().__init__()
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))
        self.running = True

    def start(self):
        threading.Thread(target=self.listen_to_server, daemon=True).start()

    def listen_to_server(self):
        while self.running:
            try:
                message = pickle.loads(self.client_socket.recv(1024))
                if message:
                    if message == 'exit':
                        self.message_received.emit('вы покинули игру')
                        self.client_socket.close()
                        break

                    self.message_received.emit(message)
                else:
                    break
            except:
                print("Соединение с сервером потеряно.")
                self.running = False
                self.client_socket.close()
                break

    def send_msg(self, msg):
        self.client_socket.send(pickle.dumps(msg))


class RegistrationWindow(QWidget):
    def __init__(self, client: CityGameClient):
        super().__init__()
        self.client = client
        self.client.message_received.connect(self.handle_server_message)

        self.main_window = None

        self.setWindowTitle('registration')
        self.setGeometry(300, 300, 250, 120)
        layout = QVBoxLayout()
        self.input_name = QLineEdit()
        self.input_name.setPlaceholderText('enter your name')

        send = QPushButton('send')
        layout.addWidget(self.input_name)
        layout.addWidget(send)

        self.setLayout(layout)

        send.clicked.connect(self.send)

        self.show()

    def send(self):
        name = self.input_name.text()
        if name:
            self.client.send_msg(name)

    def handle_server_message(self, message):
        if message == "close":
            self.hide()
            self.client.name = self.input_name.text()
            self.main_window = MainWindow(self.client)


# class Communication(QObject):
#     chat_signal = pyqtSignal(str)


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, client: CityGameClient):
        super().__init__()
        self.client = client
        self.hidden = None
        self.current_room = None

        self.setupUi(self)

        self.setWindowTitle('чат')

        self.client.message_received.connect(self.add_msg)
        self.input.editingFinished.connect(self.send_message)
        self.send_button.clicked.connect(self.send_message)

        buttons = [self.first, self.second, self.third]

        for i, button in enumerate(buttons, start=1):  # type: int, QPushButton
            button.clicked.connect(lambda clicked, MSG=i: self.click_buttons(str(MSG)))

        self.show()

    def add_msg(self, msg: str):
        if not self.hidden:
            if 'комната' in msg and 'создаётся' in msg:
                self.current_room = msg.split()[1]
                self.hide()
                RoomWindow(client=self.client, room=self.current_room, main_window=self)
                self.hidden = True
            else:
                self.output.append(msg)

    def send_message(self):
        message = self.input.text()
        self.client.send_msg(message)
        self.input.clear()

    def click_buttons(self, msg: str):
        self.client.send_msg(msg)


class RoomWindow(QWidget):
    def __init__(self, client: CityGameClient, room, main_window:MainWindow):
        super().__init__()
        self.client = client

        # self.setupUi(self)
        self.main_window = main_window
        self.setWindowTitle(f'{room}')
        layout = QVBoxLayout()

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(self.output)

        self.client.message_received.connect(self.add_msg)
        self.input = QLineEdit()
        self.input.editingFinished.connect(self.send_message)
        layout.addWidget(self.input)

        self.send_button = QPushButton()
        self.send_button.clicked.connect(self.send_message)
        self.send_button.setText('send')
        layout.addWidget(self.send_button)

        grid = QGridLayout()
        self.second = QPushButton()
        self.first = QPushButton()
        self.third = QPushButton()

        buttons = [self.first, self.second, self.third]

        for i, button in enumerate(buttons, start=1):  # type: int, QPushButton
            button.clicked.connect(lambda clicked, MSG=i: self.click_buttons(str(MSG)))
            button.setText(f'{i}')
            grid.addWidget(button, 3, i-1, 1, 1)
        layout.addLayout(grid)

        self.setLayout(layout)
        self.show()

    def add_msg(self, msg):
        self.output.append(msg)

    def send_message(self):
        message = self.input.text()
        self.client.send_msg(message)
        self.input.clear()

    def click_buttons(self, msg: str):
        self.client.send_msg(msg)
        if msg == '2':
            self.hide()
            self.main_window.hidden = False
            self.main_window.show()
        # if msg == '3':
        #     self.hide()
        #     self.main_window.hidden = False
        #     self.main_window.show()


ex_client = CityGameClient()
ex_client.start()

app = QApplication([])
window = RegistrationWindow(ex_client)
window.show()
app.exec()
