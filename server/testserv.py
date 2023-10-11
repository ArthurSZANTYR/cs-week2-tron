import socket
from _thread import *
import threading
import time
import numpy as np
import json

# Paramètres du jeu

FPS = 3 # Fréquence de vérification (25 fois par seconde)

# Temps entre chaque vérification
delta_time = 1 / FPS

print_lock = threading.Lock()
connected_clients = []  # Une liste pour stocker les clients connectés

class Player:
    def __init__(self, x, y, d, id): 
        self.x = x  # player x coord
        self.y = y  # player y coord
        self.d = d  # player direction
        self.id = id
    
    def update_direction(self, new_direction):
        self.d = new_direction

class Game:
    def __init__(self):
        self.width = 0
        self.height = 0
        self.players : list[Player] = []
        self.plateau = []

    def send_game_state_to_clients(self):
        all_players_data = []

        for player in self.players:
            player_data = f"{player.id},{player.x},{player.y},{player.d}"
            all_players_data.append(player_data)

        players_data = ";".join(all_players_data)  # Joindre les données de tous les joueurs avec des points-virgules

        for client in connected_clients:
            try:
                client.send((players_data + "!").encode("utf-8"))
            except Exception as e:
                print(e)
                connected_clients.remove(client)







    def new_game(self):
        # Définissez le nombre de lignes et de colonnes en fonction du nombre de joueurs
        num_players = len(connected_clients)
        # Créez une matrice remplie de zéros pour représenter le plateau
        self.width = 30 * num_players
        self.height = 30 * num_players
        self.plateau = np.zeros((self.width, self.height))
        off = self.width // (num_players + 1)
        for i, c in enumerate(connected_clients):
            x = 1 + i * off  # Répartissez les joueurs équitablement
        # Obtenez le nom du socket pour utiliser comme ID du joueur
            #player_id = c.getpeername()
            client_ip, client_port = c.getpeername()
            self.players.append(Player(x=x, y=0, d="U", id=client_port))
            print(c.getpeername())
            print(client_port)



    def deplacement(self, player):
        x, y, d, id = player.x, player.y, player.d, player.id
        new_x, new_y = x, y
    
        if d == "U":
            new_y = y - 1
        elif d == "D":
            new_y = y + 1
        elif d == "L":
            new_x = x - 1
        elif d == "R":
            new_x = x + 1
    
        if new_x < 0 or new_x >= self.width or new_y < 0 or new_y >= self.height:
            return True  # Collision avec les bords du plateau
    
        # Vérifiez si le joueur entre en collision avec d'autres joueurs ou des obstacles
        if self.plateau[new_y][new_x] != 0:
            return True  # Collision avec un autre joueur ou un obstacle
    
        # Mettez à jour les positions sur le plateau
        self.plateau[y][x] = 0  # Ancienne position
        self.plateau[new_y][new_x] = id  # Nouvelle position
    
        player.x, player.y = new_x, new_y  # Mettez à jour les coordonnées du joueur
    
        return False




    def Jeu(self):
        while True:
            # Heure de départ de la boucle
            start_time = time.time()
           # print("dans le jeu")
            # Votre logique de jeu ici
            for player in self.players:
                self.deplacement(player)
               # print("eplacement ?")
               # if not self.deplacement(player):
               #     # Le joueur n'a pas rencontré de collision, continuez le mouvement
               #     pass
               # else:
               #     # Collision, le joueur est éliminé ou doit être géré
               #     pass

            # Appelez send_game_state_to_clients pour envoyer les nouvelles positions des joueurs
            self.send_game_state_to_clients()

            # Heure de fin de la boucle
            end_time = time.time()

            # Calcul du temps d'attente pour atteindre la fréquence souhaitée
            elapsed_time = end_time - start_time
            sleep_time = max(0, delta_time - elapsed_time)
            time.sleep(sleep_time)


socket_to_player_id = {}

def threaded(c, game : Game):
    global connected_clients, socket_to_player_id

    try:
        client_name = c.getpeername()
        client_id = socket_to_player_id.get(client_name, None)

        while True:
            data = c.recv(1024).decode("utf-8")
            if len(data) == 0:
                print(f"Client {client_name} disconnected")
                connected_clients.remove(c)
                break

            # Supposons que les données reçues ont la forme "socket_id, direction"
            parts = data.split(",")
            if len(parts) == 2:
                socket_id, new_direction = parts  # Séparez les deux parties
                print(socket_id+new_direction)
                
                # Recherchez le joueur correspondant à l'ID du socket
                for player in game.players:
                    print(f"Socket id {socket_id} ")
                    print(f"Client id {player.id} ")
                    if int(player.id) == int(socket_id):
                        print("Im in")
                        player.update_direction(new_direction)
                        # break

    except ConnectionResetError:
        print(f"Client {client_name} disconnected")
        connected_clients.remove(c)


def Main():
    host = "0.0.0.0"
    port = 7778
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    print("Socket lié au port", port)
    s.listen(5)
    print("Socket en écoute")

    print("Clients connectés :", connected_clients)  # Afficher la liste des clients connectés

    # Créez une instance de la classe Game
    game = Game()

    def Complet():
        if len(connected_clients) == 2:
            return False
        return True
    

    i = True
    while i:
        c, addr = s.accept()
        print_lock.acquire()
        print('Connected to:', addr[0], ':', addr[1])
        connected_clients.append(c)

        # Utilisez l'adresse du socket comme ID unique
        player_id = addr[1]  # Utilisez l'adresse du socket comme ID unique

        game.players.append(Player(x=0, y=0, d="h", id=player_id))
        socket_to_player_id[c.getpeername()] = player_id

        # Pass the 'game' instance to the 'threaded' function
        start_new_thread(threaded, (c, game))
        print_lock.release()
        i = Complet()

    print("Exit")

    # Créez un nouveau jeu lorsque tous les clients sont connectés
    game.new_game()

    # Lancez le jeu dans un thread séparé
    game_thread = threading.Thread(target=game.Jeu)
    game_thread.daemon = True
    game_thread.start()
    #print("caca")
    #game.Jeu()
    #jeuencours = True
    #while jeuencours:
    #    for player22 in game.players :
    #        new_x, new_y = receive_player_movement_info(player22)  # Remplacez cette ligne par la façon dont vous recevez les coordonnées
    #        player22.deplacement(new_x, new_y)
       


    game_thread.join()

if __name__ == '__main__':
    Main()



