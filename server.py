import socket
import threading
import pickle
import time


class Room:
    def __init__(self, name):
        self.name: str = name
        self.clients: list = []
        self.names: list = []
        self.city_history: list = []
        self.semaphore: threading.Semaphore = threading.Semaphore(2)

    def remove_all(self):
        self.clients = []
        self.names = []
        self.city_history = []
        self.semaphore.release()
        self.semaphore.release()

    def add_client(self, client_socket: socket.socket, player_name: str):
        self.clients.append(client_socket)
        self.names.append(player_name)
        self.semaphore.acquire()

    def remove_client(self, client_socket: socket.socket, player_name: str):
        self.clients.remove(client_socket)
        self.names.remove(player_name)
        self.semaphore.release()

    def is_full(self):
        return len(self.clients) == 2

    def broadcast(self, sender, message):
        for client in self.clients:
            if client != sender:
                client.send(pickle.dumps(message))


class CityGameServer:
    def __init__(self, host="0.0.0.0", port=5555):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        self.rooms = {}
        self.lock = threading.Lock()
        self.time_limit = 20
        self.banned_players: list = []

    def start(self):
        print("Сервер запущен и ожидает подключений...")
        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"Подключен клиент: {addr}")
            threading.Thread(target=self.handle_client, args=(client_socket, False)).start()

    def handle_client(self, client_socket: socket.socket, name):
        player_name = name

        if not name:
            time.sleep(0.5)
            client_socket.send(pickle.dumps("Введите совё имя: "))
            player_name = pickle.loads(client_socket.recv(1024)).strip()
            print(player_name)
            client_socket.send(pickle.dumps(f"close"))
            time.sleep(0.5)
            client_socket.send(pickle.dumps(f"Здравствуйте {player_name} :)"))
        time.sleep(0.5)
        client_socket.send(pickle.dumps('1. создать комнату \n2. вступить в комнату \n3. покинуть игру'))

        while True:
            command = pickle.loads(client_socket.recv(1024)).strip()

            if command == '1':
                self.create(client_socket, player_name)
                break

            elif command == '2':
                self.join(client_socket, player_name)
                break

            elif command == '3':
                client_socket.send(pickle.dumps('exit'))
                break

            else:
                client_socket.send(pickle.dumps('неизвестная команда, выберете из [1 2 3]'))

    def create(self, client_socket, player_name):
        client_socket.send(pickle.dumps('введите название для комнаты:'))
        room_name = pickle.loads(client_socket.recv(1024)).strip()

        with self.lock:
            self.rooms[room_name] = Room(room_name)
            room = self.rooms[room_name]
            room.add_client(client_socket, player_name)

        client_socket.send(pickle.dumps(f'комната {room_name} создаётся'))

        time.sleep(0.5)
        client_socket.send(pickle.dumps(f'комната {room_name} создана'))
        client_socket.send(pickle.dumps('ждём второго игрока...'))

        threading.Thread(target=self.play_game, args=(room,)).start()

    def join(self, client_socket: socket.socket, player_name: str):
        if client_socket not in self.banned_players:
            client_socket.send(pickle.dumps('введите название для комнаты:'))
            room_name = pickle.loads(client_socket.recv(1024)).strip()

            with self.lock:
                if room_name in self.rooms:
                    room = self.rooms[room_name]
                    client_socket.send(pickle.dumps(f'комната {room_name} создаётся'))
                    room.add_client(client_socket, player_name)
                    return True
                else:
                    client_socket.send(pickle.dumps('такой комнаты нет'))
                    return False
        else:
            client_socket.send(pickle.dumps('вы забанены'))
            client_socket.send(pickle.dumps('exit'))

    def play_game(self, room: Room):
        current_letter = None
        game_over = False
        turn_index = 0

        while not room.is_full():
            continue

        for client in room.clients:
            time.sleep(0.5)
            client.send(pickle.dumps(f"Игра началась! {room.names[0]} вводит первый город."))

        while not game_over:
            player: socket.socket = room.clients[turn_index]
            name: str = room.names[turn_index]
            player.send(pickle.dumps(f"1 - покинуть игру \n2 - поменять комнату \n3 - забанить игрока \nВаш ход, {name}. Введите название города: "))

            while True:
                command = pickle.loads(player.recv(1024)).strip()

                if command == '1':
                    # player.send(pickle.dumps('end'))
                    self.delete_player(room=room, player=player, name=name, turn_index=turn_index)
                    game_over = True
                    threading.Thread(target=self.handle_client, args=(player, name)).start()
                    break

                elif command == '2':
                    if self.join(player, name):
                        self.delete_player(room=room, player=player, name=name, turn_index=turn_index)
                        game_over = True
                        break

                    else:
                        player.send(pickle.dumps(f"Придётся играть тут {name}. Введите название города: "))
                        command = pickle.loads(player.recv(1024)).strip()

                elif command == '3':
                    player.send(pickle.dumps(f"назовите причину: "))
                    reason = pickle.loads(player.recv(1024)).strip()
                    print(f'{name} запрашивает бан игроку {room.names[(turn_index + 1) % 2]} \n причина: {reason}')
                    answer = input('ok or not:')
                    if answer == 'ok':
                        threading.Thread(target=self.handle_client, args=(player, name)).start()
                        player.send(pickle.dumps(f'игрок {room.names[(turn_index + 1) % 2]} забанен'))

                        turn_index = (turn_index + 1) % 2
                        player: socket.socket = room.clients[turn_index]
                        name: str = room.names[turn_index]

                        self.banned_players.append(player)
                        player.send(pickle.dumps('exit'))
                        game_over = True
                        room.remove_all()

                        break

                    else:
                        player.send(pickle.dumps('запрос отклонён. вводите город'))

                else:
                    city = command

                    if self.is_valid_city(city, current_letter, room):
                        room.city_history.append(city)

                        room.broadcast(player, f"{name} назвал город  --- {city} ---")
                        current_letter = city[-1]

                        turn_index = (turn_index + 1) % 2

                        if current_letter in 'ъьйы':
                            current_letter = city[-2]

                        break

                    else:
                        player.send(pickle.dumps("Неправильный город! Попробуйте снова: "))

    def delete_player(self, room: Room, player: socket.socket, name: str, turn_index: int):
        room.broadcast(player, f'игрок {name} вышел')
        turn_index = (turn_index + 1) % 2
        player: socket.socket = room.clients[turn_index]
        name: str = room.names[turn_index]
        room.remove_all()
        threading.Thread(target=self.handle_client, args=(player, name)).start()

    @staticmethod
    def is_valid_city(city, current_letter, room: Room):
        if city in room.city_history:
            return False
        if current_letter and city[0].lower() != current_letter:
            return False
        return True


if __name__ == "__main__":
    server = CityGameServer()
    server.start()