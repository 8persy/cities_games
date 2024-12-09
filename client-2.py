import pickle
import socket
import threading


class CityGameClient:
    def __init__(self, host="127.0.0.1", port=5555):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))
        self.running = True

    def start(self):
        threading.Thread(target=self.listen_to_server).start()
        self.send_messages()

    def listen_to_server(self):
        while self.running:
            try:
                message = pickle.loads(self.client_socket.recv(1024))
                if message:
                    if message == 'exit':
                        self.client_socket.close()
                    else:
                        print(message)
                else:
                    break
            except:
                print("Соединение с сервером потеряно.")
                self.running = False
                self.client_socket.close()
                break

    def send_messages(self):
        while self.running:
            try:
                message = input()
                self.client_socket.send(pickle.dumps(message))
            except:
                print("Соединение закрыто.")
                self.running = False
                self.client_socket.close()
                break


if __name__ == "__main__":
    client = CityGameClient()
    client.start()

