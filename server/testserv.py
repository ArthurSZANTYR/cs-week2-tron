import socket
from _thread import *
import threading
import time
import numpy as np
import json
import queue
import argparse

import sys
sys.path.append("..")  # répertoire racine pour acceder au dossier network
from network import network

# arguments en ligne de commande - nombre de clients sur le serveur
parser = argparse.ArgumentParser(description='Serveur de jeu Tron')
parser.add_argument('nombre_clients', type=int, help='Nombre de clients souhaités pour le serveur')
args = parser.parse_args()

###############################################"
host = network.host_ip
port = network.port
###############################################


FPS = 20# Fréquence de vérification (25 fois par seconde)
delta_time = 1 / FPS # Temps entre chaque vérification

print_lock = threading.Lock()
connected_clients = []  # Une liste pour stocker les clients connectés

class Player:
    def __init__(self, x, y, d, id): 
        self.x = x  # player x coord
        self.y = y  # player y coord
        self.d = d  # player direction
        self.id = id # player id (socket id)
    
    def update_direction(self, new_direction):
        self.d = new_direction

class Game:
    def __init__(self):
        self.width = 0
        self.height = 0
        self.players : list[Player] = []
        self.plateau = []

        self.game_state_queue = queue.Queue()

    def send_game_state_to_clients(self):
        all_players_data = []

        for player in self.players:
            player_data = f"{player.id},{player.x},{player.y},{player.d}"
            all_players_data.append(player_data)

        players_data = ";".join(all_players_data)  # Joindre les données de tous les joueurs avec des points-virgules
        self.game_state_queue.put(players_data + "!" )


    def send_game_state_worker(self):
        counter = 0
        while True:
            data = self.game_state_queue.get()
            # print(f'data to send : {data}')
            for client in connected_clients:
                try:

                    client.send((data + "!").encode("utf-8"))
                    counter+=1
                    print(f'couzaeiuiazteu : {data}')
                except Exception as e:
                   # print(e)
                    connected_clients.remove(client)



    def new_game(self):   
        num_players = len(connected_clients) #Nombre de lignes et de colonnes en fonction du nombre de joueurs
        gross = 40
        self.width =  gross * num_players
        self.height = gross * num_players
        self.plateau = np.zeros((self.width, self.height))  # Créez une matrice remplie de zéros pour représenter le plateau
        off = self.width // (num_players + 1)
        self.plateau[0, :] = -1  # Remplit la première ligne avec -1
        self.plateau[-1, :] = -1  # Remplit la dernière ligne avec -1
        self.plateau[:, 0] = -1  # Remplit la première colonne avec -1
        self.plateau[:, -1] = -1  # Remplit la dernière colonne avec -1

        for i, c in enumerate(connected_clients):
            k=0
            x = 10 + k*off # Répartissez les joueurs équitablement
            client_port = c.getpeername()[1] # Obtenez le nom du socket pour utiliser comme ID du joueur

            k = k+1
            print(i)

            if num_players <= 4:
                if i == 0:
                    self.players.append(Player(x=1 , y= self.height//2, d="R", id=client_port))
                elif i == 1:
                    self.players.append(Player(x=self.width -1 , y=self.height//2, d="L", id=client_port))
                elif i == 2:
                    self.players.append(Player(x=self.width//2, y=1, d="D", id=client_port))
                elif i == 3:
                    self.players.append(Player(x=self.width//2, y=self.height -1 , d="U", id=client_port))

            elif num_players >= 5 :
                self.players.append(Player(x=x, y=0, d="D", id=client_port))
            
            

        

                

    def MortClient(self, player):
        x, y, d, id = player.x, player.y, player.d, player.id
        new_x, new_y = player.x, player.y
        self.plateau[new_y][new_x] = player.id  # Nouvelle position à jour les positions sur le plateau
        player.x, player.y = new_x, new_y  # Mettez à jour les coordonnées du joueur
        player.id = -1
        return False

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
    
        if new_x <0 or new_x >= self.width or new_y <0 or new_y >= self.height:  # Vérifie collision avec les bords
           # print("Colision Bord")
            return True  # Collision avec les bords du plateau
    
 
        if self.plateau[new_y][new_x] != 0:    # Vérifie collision avec d'autres joueurs
            #print("Colosion avec lui meme ou autre joueur")
            return True  # Collision avec un autre joueur ou un obstacle
        
        self.plateau[new_y][new_x] = id  # Nouvelle position à jour les positions sur le plateau
    
        player.x, player.y = new_x, new_y  # Mettez à jour les coordonnées du joueur
    
        return False


    def TousMort(self, player):
        liste = []
        for player in self.players:
            x, y, d, id = player.x, player.y, player.d, player.id
            liste.append(player.id)


        bla = False

        if all(ele == -1 for ele in liste):
            tableau = self.plateau
            occurrences = {}

            for ligne in tableau:
                for valeur in ligne:
                    if valeur not in [0, -1]:
                        occurrences[valeur] = occurrences.get(valeur, 0) + 1

            # Trier le dictionnaire par ID dans l'ordre croissant
            classement = sorted(occurrences.items(), key=lambda x: x[0])

            for client in connected_clients:
                # Créer une liste des IDs triés et les joindre en une seule chaîne
                ids_tries = [str(int(item[0])) for item in classement]
                message = ("?"+','.join(ids_tries) +"!").encode("utf-8")
                client.send(message)
                print("envoie classement")
                print(message)

            bla = True

        return bla



    
    def Jeu(self):
        stop = True
        Fingame = False
       
        send_game_state_thread = threading.Thread(target=self.send_game_state_worker, daemon=True)
        send_game_state_thread.start()
        k=0
        while stop == True:            


            for player in self.players:
                if not self.deplacement(player): # Le joueur n'a pas rencontré de collision, continuez le mouvement
                    pass 
                elif self.TousMort(player) == True :
                    stop = False
                    pass
                else:
                    self.MortClient(player)
                   # print("COLISION !)")
                    pass
            
            self.send_game_state_to_clients()
            if k ==0:
                time.sleep(4)
                k+=1
            

            start_time = time.time()


            end_time = time.time() # Heure de fin de la boucle       
            elapsed_time = end_time - start_time # Calcul du temps d'attente pour atteindre la fréquence souhaitée
            sleep_time = max(0, delta_time - elapsed_time)
            time.sleep(sleep_time)
            

        print("Fin du Jeu !")

    


socket_to_player_id = {}

def threaded(c, game : Game):
    global connected_clients, socket_to_player_id

    try:
        client_name = c.getpeername()

        while True:
            data = c.recv(1024).decode("utf-8")
            if len(data) == 0:
              
                break

            parts = data.split(",")
            if len(parts) == 2:
                socket_id, new_direction = parts  # Séparez les deux parties
                print(socket_id+new_direction)
                
                
                for player in game.players: # Recherchez le joueur correspondant à l'ID du socket

                    if int(player.id) == int(socket_id):
                        player.update_direction(new_direction)
           
        c.close             # break

    except ConnectionResetError:
        print(f"Client {client_name} disconnected")
    #    
    #    


def Main():
    #host = host
    #port = port
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    print("Socket lié au port", port)
    s.listen()

    def Complet():
            if len(connected_clients) == args.nombre_clients:
                return False
            return True

    while True :
        
        game = Game()

        i = True
        while i:
            c, addr = s.accept()
            print_lock.acquire()
            print('Connected to:', addr[0], ':', addr[1])
            connected_clients.append(c)


            # Pass the 'game' instance to the 'threaded' function
            start_new_thread(threaded, (c, game))
            print_lock.release()
            i = Complet()
        print("Exit")
        print(f'Nbr Connexion client : {len(connected_clients)}')
        game.new_game() # Créez un nouveau jeu lorsque tous les clients sont connectés
        for client in connected_clients:
            message = str(len(connected_clients)).encode("utf-8")
            client.send(message)
        #time.sleep(0.2)
        
        game.send_game_state_to_clients()


        game_thread = threading.Thread(target=game.Jeu)  # Lancez le jeu dans un thread séparé
        game_thread.daemon = True
        
        game_thread.start()
        #time.sleep(4)
        game_thread.join()
        print("fin jeu")
        time.sleep(1)
        connected_clients.clear()

        



if __name__ == '__main__':
    Main()