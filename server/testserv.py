import socket
from _thread import *
import threading
import time
import numpy as np
import json

# Paramètres du jeu
FPS = 30 # Fréquence de vérification (25 fois par seconde)

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

class Game:
    def __init__(self):
        self.width = 0
        self.height = 0
        self.players = []
        self.plateau = []

    def send_game_state_to_clients(self):
        players_data = {
            player.id: (player.x, player.y, player.d)
            for player in self.players
        }

        players_data_json = json.dumps(players_data)  # Convertir en JSON

        for client in connected_clients:
            try:
                client.send(players_data_json.encode("utf-8"))
            except Exception as e:
                print(e)
                connected_clients.remove(client)







    def new_game(self):
        # Définissez le nombre de lignes et de colonnes en fonction du nombre de joueurs
        num_players = len(connected_clients)
        # Créez une matrice remplie de zéros pour représenter le plateau
        self.width = 330 * num_players
        self.height = 300 * num_players
        self.plateau = np.zeros((self.width, self.height))
        off = self.width // (num_players + 1)
        for i, c in enumerate(connected_clients):
            x = 20 + i * off  # Répartissez les joueurs équitablement
            self.players.append(Player(x=x, y=0, d="h", id=i + 1))

    def send_game_state_to_clients(self):
        players_data = ";".join(
            f"{player.id},{player.x},{player.y},{player.d}"
            for player in self.players
        )
        players_data += "!"

        for client in connected_clients:
            try:
                client.send(players_data.encode("utf-8"))
            except Exception as e:
                print(e)
                connected_clients.remove(client)



    def deplacement(self, player):
        x, y, d, id = player.x, player.y, player.d, player.id
        new_x, new_y = x, y

        if d == "h":
            new_y = y - 1
        elif d == "b":
            new_y = y + 1
        elif d == "g":
            new_x = x - 1
        elif d == "d":
            new_x = x + 1

        if new_x < 0 or new_x >= self.width or new_y < 0 or new_y >= self.height:
            return True  # Collision avec les bords du plateau

        # Vérifie si le joueur entre en collision avec d'autres joueurs ou des obstacles
        if self.plateau[new_y][new_x] != 0:
            return True 
        
        self.plateau[y][x] = id
        self.plateau[new_y][new_x] = id
        player.x, player.y = new_x, new_y

        return False




    def Jeu(self):
        while True:
            # Heure de départ de la boucle
            start_time = time.time()
            # Votre logique de jeu ici
            for player in self.players:
                if not self.deplacement(player):
                    # Le joueur n'a pas rencontré de collision, continuez le mouvement
                    pass
                else:
                    # Collision, le joueur est éliminé ou doit être géré
                    pass
            # Envoi des informations du jeu à tous les clients
            self.send_game_state_to_clients()
            # Heure de fin de la boucle
            end_time = time.time()

            # Calcul du temps d'attente pour atteindre la fréquence souhaitée
            elapsed_time = end_time - start_time
            sleep_time = max(0, delta_time - elapsed_time)
            time.sleep(sleep_time)



def threaded(c):
    global connected_clients  # Utilisez la liste globale des clients connectés

    try: 
        while True:
            data = c.recv(1024)
            if len(data) == 0: 
                print("client disconnected")
                connected_clients.remove(c)
                break

            print(data.decode())            

    except ConnectionResetError:
        print("client disconnected")
        connected_clients.remove(c)

def Main():
    host = "172.21.72.136"
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
        if len(connected_clients) == 1:
            return False
        return True
    
    i = True
    while i == True:
        c, addr = s.accept()
        print_lock.acquire()
        print('Connecté à :', addr[0], ':', addr[1])
        connected_clients.append(c)  # Ajoutez le client à la liste des clients connectés
        start_new_thread(threaded, (c,))
        print_lock.release()
        i = Complet()

    print("sortie")

    # Créez un nouveau jeu lorsque tous les clients sont connectés
    game.new_game()

    # Lancez le jeu dans un thread séparé
    game_thread = threading.Thread(target=game.Jeu)
    game_thread.daemon = True
    game_thread.start()

    # Laissez le jeu s'exécuter indéfiniment
    game_thread.join()

if __name__ == '__main__':
    Main()



