# Import socket module
import socket
import pygame
import sys
import time
import random
import numpy as np 

###################

#'stan ip' : 172.21.72.136
host_ip = '172.21.72.136'
port = 7778

###################
class Client:
    def __init__(self) -> None:
        
        #creation d'un socket par client a chaque instanciation 
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #connexion au serveur du socket 
        self.client_socket.connect((host_ip, port))

        #recuperation de l'ip du client et du port client
        self.client_ip, self.client_port = self.client_socket.getsockname()
		

def send_to_server(client_socket: "socket", data: str) -> bool:
    """
    Fonction permettant de d'envoyer un paquet au serveur - avec le socket crée 

    Args:
        client_socket: "socket"  ->  socket du client pour communiquer avec le serveur
        data: str -> data a envoyée 

    Returns:
        bool ->  return true quand le message a correctement été envoyé
    """
    client_socket.send(str.encode(data))
    return True

def get_new_direction() -> str:
    """
    Fonction permettant de recuperer la nouvelle direction souhaité par le joueur - en fonction d'evenement sur le clavier ou non

    Args:

    Returns:
        str ->  retourne la direction souhaité - si aucun evenement clavier return None

    """
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                return "L"
            elif event.key == pygame.K_RIGHT:
                return "R"
            elif event.key == pygame.K_UP:
                return "U"
            elif event.key == pygame.K_DOWN:
                return "D"
    return None

# Créez un dictionnaire associant des nombres de 1 à 20 à des couleurs aléatoires
#color_dict = {i: (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for i in range(1, 21)}

class Fenetre:
    def __init__(self, n=3, largeur_fenetre=300, hauteur_fenetre=300) -> None:
        self.largeur = largeur_fenetre
        self.hauteur = hauteur_fenetre
        self.fenetre = pygame.display.set_mode((self.largeur, self.hauteur))
        self.matrice = np.zeros((30, 30), dtype=int)  # Créez une matrice de dimensions n x n remplie de zéros de type entier


    def render_matrix(self, player_data: dict, color_dict: dict) -> None:
        """
    Fonction permettant de mettre a jour la matrice courante du jeu et la fenetre pygame

    Args:
        player_data: dict ->  dictionnaire contenant les nouvelles positions de tous les joueurs envoyés par le serveur
        color_dict: dict -> dictionnaire généré en debut de partie qui atribue une couleur a chaque joueur

    Returns:

    """
        # Remplir l'écran avec une couleur blanche
        self.fenetre.fill((255, 255, 255))

        # Update de la matrice courante du jeu
        for player_id, (x, y, d) in player_data.items():
            self.matrice[int(y)][int(x)] = player_id
            
        # Boucle pour parcourir la matrice et dessiner les cellules
        for y in range(len(self.matrice)):
            for x in range(len(self.matrice[y])):
                position = self.matrice[y][x]
                if position != 0:
                    pygame.draw.rect(self.fenetre, color_dict[position], (y*5 , x*5 , 5, 5))  #probleme sur le facteur *10 ammene des hors cadres
        pygame.display.flip()

def decrypt_data(data_brut: str)-> dict:
    """
    Fonction permettant de convertir le paquet recu par le serveur en dictionnaire

    Args:
        data: str -> data recu par le serveur sous forme de string

    Returns:
        dict ->  return un dictionnaire avec key: client_port et value: la nouvelle position
    """

    data_brut = data_brut.split('!')
    data_brut = data_brut[0]

    data_players = data_brut.split(';')
    positions = {}

    for data_player in data_players:
        elements = data_player.split(',')
        key = int(elements[0])   #selectionne le port client identifié par le serveur
        position = tuple(elements[1:])  #selectionne la position pour la mettre en value
        positions[key] = position

    return positions

def generate_colors(player_data: dict)-> dict:
    """
    Fonction permettant de generer un dictionaire qui attribue une couleur aléatoire a chaque player

    Args:
        player_data: dict -> data recu par le serveur qui identifie les joueurs par leur port client

    Returns:
        dict ->  return un dictionnaire avec key: client_port et value: couleur
    """
    
    color_dict = {}
    for player_id, (x, y, d) in player_data.items():
        color_dict[player_id] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    return color_dict 


def run()-> None:
    """
    Fonction qui gere les différentes etapes de jeu

    Args:

    Returns:
    
    """

    c = Client()
    f = Fenetre()

    i=0 #pour identifier le premier tour de jeu

    #boucle de jeu
    while True:
        data = c.client_socket.recv(1024)  # 1024 est la taille max du message
        if not data:
            break

        player_data = decrypt_data(data.decode())

        if i == 0:  #au premier tour de jeu - generation du dictionnaire de couleur
          color_dict = generate_colors(player_data)
          i+=1

        print(player_data)
        f.render_matrix(player_data, color_dict)

        new_d = get_new_direction()   #verifie les evenements clavier si pas de retour pas d'envoi au serveur
        if new_d != None:   
            send_to_server(c.client_socket, f"{c.client_port},{new_d}")

run()

    
