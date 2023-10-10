import socket
from _thread import *
import threading
import time
import numpy as np
import time
import json

# Paramètres du jeu
FPS = 25  # Fréquence de vérification (25 fois par seconde)

# Temps entre chaque vérification
delta_time = 1 / FPS



print_lock = threading.Lock()
connected_clients = []  # Une liste pour stocker les clients connectés

# Fonction de gestion de thread
def threaded(c : socket):
    global connected_clients  # Utilisez la liste globale des clients connectés
#s.getsockname
    try: 
        while True:
            data = c.recv(1024)
            if(len(data) == 0): 
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

    def Complet():
        if len(connected_clients) == 3:
            return False
        return True
    
    i = True
    while  i == True:
        c, addr = s.accept()
        print_lock.acquire()
        print('Connecté à :', addr[0], ':', addr[1])
        connected_clients.append(c)  # Ajoutez le client à la liste des clients connectés
        start_new_thread(threaded, (c,))
        print_lock.release()
        i = Complet()
    
    
    print("sortie")
    
    #s.close()



if __name__ == '__main__':
    Main()


class Player:
    def __init__(self, x, y, d, id): 
        self.x = x  # player x coord
        self.y = y  # player y coord
        self.b = d  # player direction
        self.id = id


class Game:
    def new_game():
        global width, height
        new_players = []
        # Définissez le nombre de lignes et de colonnes en fonction du nombre de joueurs
        num_players = len(connected_clients)
        # Créez une matrice remplie de zéros pour représenter le plateau
        width = 330*num_players
        height = 300*num_players
        plateau = np.zeros((width, height))
        off = width// (num_players + 1)
        for i in range(1, len(connected_clients) + 1):
            for j in range(20,width-20 ,off):
                new_players.append(Player(x=j, y=0, direction="h", id=i))

        return plateau,new_players

    # Assurez-vous que connected_clients et Player sont correctement définis dans votre code.
    #offset = height - width #vertical space at top of window


    check_time = time.time()  # used to check collisions with rects

    def broadcast_game_state(self):
        game_state = {
            "matrix": self.plateau.tolist(),
            "players": [
                {"id": player.id, "x": player.x, "y": player.y, "d": player.d}
                for player in self.players
            ],
        }
        game_state_json = json.dumps(game_state)

        for client in connected_clients:
            try:
                client.send(game_state_json.encode("utf-8"))
            except Exception as e:
                print(e)
                connected_clients.remove(client)

    def  deplacement(plateau, x, y, d, id):

        if d == "h":
            new_x, new_y = x, y - 1
        elif d == "b":
            new_x, new_y = x, y + 1
        elif d == "g":
            new_x, new_y = x - 1, y
        elif d == "d":
            new_x, new_y = x + 1, y

        if new_x < 0 or new_x >= width or new_y < 0 or new_y >= height:
            return True  # Collision avec les bords du plateau

        # Vérifie si le joueur entre en collision avec d'autres joueurs ou des obstacle
        if (new_x,new_y) != 0:
            return True 
        
        plateau[y][x] = id
        plateau[new_y][new_x] = id
        
        x, y = new_x, new_y

        return False  

    def Jeu(plateau,player ):
        while True:
            # Heure de départ de la boucle
            start_time = time.time()
            #ici chatgpt faire les verif etc stp
            # Heure de fin de la boucle
            end_time = time.time()

            # Calcul du temps d'attente pour atteindre la fréquence souhaitée
            elapsed_time = end_time - start_time
            sleep_time = max(0, delta_time - elapsed_time)
            time.sleep(sleep_time)
