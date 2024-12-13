import pickle
import socket
import threading

from PyQt6.QtCore import pyqtSignal, QObject, pyqtSlot
from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton

from client_gui import Ui_MainWindow


class CityGameClient(QObject):
    message_received = pyqtSignal(str)

    def __init__(self, host="127.0.0.1", port=5555):
        super().__init__()
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))
        self.running = True

    def start(self):
        threading.Thread(target=self.listen_to_server).start()

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
                self.main_thread.join()
                break

    def send_msg(self, msg):
        self.client_socket.send(pickle.dumps(msg))


class Communication(QObject):
    chat_signal = pyqtSignal(str)


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, client: CityGameClient):
        super().__init__()
        self.client = client

        self.setupUi(self)

        self.setWindowTitle('чат')

        self.client.message_received.connect(self.add_msg)
        self.input.editingFinished.connect(self.send_message)
        self.send_button.clicked.connect(self.send_message)

        buttons = [self.first, self.second, self.third]

        for i, button in enumerate(buttons, start=1):  # type: int, QPushButton
            button.clicked.connect(lambda clicked, MSG=i: self.click_buttons(str(MSG)))

    def add_msg(self, msg):
        if msg == 'exit':
            self.self_close()
        self.output.append(msg)

    def send_message(self):
        message = self.input.text()
        self.client.send_msg(message)
        self.input.clear()

    def click_buttons(self, msg: str):
        self.client.send_msg(msg)


ex_client = CityGameClient()
ex_client.start()

app = QApplication([])
window = MainWindow(ex_client)
window.show()
app.exec()
