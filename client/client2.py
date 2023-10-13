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
port = 1995
#nombre_joueur = 3 #pour la taille matrice

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
    def __init__(self, nombre_joueur: int) -> None:
        self.facteur_grossisment_pygame = 20/nombre_joueur  #densité d'affichage reduit avec le nombre de joueur
        self.nb_case_matrice_par_joueur = 40

        self.largeur_window = self.nb_case_matrice_par_joueur *nombre_joueur*self.facteur_grossisment_pygame
        self.hauteur_window = self.nb_case_matrice_par_joueur *nombre_joueur*self.facteur_grossisment_pygame
        self.fenetre = pygame.display.set_mode((self.largeur_window , self.hauteur_window ))
        self.matrice = np.zeros((self.nb_case_matrice_par_joueur *nombre_joueur, self.nb_case_matrice_par_joueur *nombre_joueur), dtype=int)  # Créez une matrice de dimensions n x n remplie de zéros de type entier

        ##################################################################################
        # Remplir le tour de la matrice avec -1 pour afficher les bords sur pygame 
        self.matrice[0, :] = -1  # Remplit la première ligne avec -1
        self.matrice[-1, :] = -1  # Remplit la dernière ligne avec -1
        self.matrice[:, 0] = -1  # Remplit la première colonne avec -1
        self.matrice[:, -1] = -1  # Remplit la dernière colonne avec -1
        
        
    def render_matrix(self, player_data: dict, color_dict: dict) -> None:
        """
    Fonction permettant de mettre a jour la matrice courante du jeu et la fenetre pygame

    Args:
        player_data: dict ->  dictionnaire contenant les nouvelles positions de tous les joueurs envoyés par le serveur
        color_dict: dict -> dictionnaire généré en debut de partie qui atribue une couleur a chaque joueur

    Returns:

    """
        pygame.init()

        # Remplir l'écran avec une couleur blanche
        self.fenetre.fill((255, 255, 255))

        # Update de la matrice courante du jeu
        for player_id, (x, y, d) in player_data.items():
            self.matrice[int(x)][int(y)] = player_id

            
        # Boucle pour parcourir la matrice et dessiner les cellules
        for y in range(len(self.matrice)):
            for x in range(len(self.matrice[y])):
                position = self.matrice[x][y]
                if position == -1:
                    pygame.draw.rect(self.fenetre, (255,0,0), (x*self.facteur_grossisment_pygame , y*self.facteur_grossisment_pygame , self.facteur_grossisment_pygame, self.facteur_grossisment_pygame))

                if position > 0:
                    pygame.draw.rect(self.fenetre, color_dict[position], (x*self.facteur_grossisment_pygame , y*self.facteur_grossisment_pygame , self.facteur_grossisment_pygame, self.facteur_grossisment_pygame))  #probleme sur le facteur *10 ammene des hors cadres
        pygame.display.flip()

    def render_intro(self, color_dict: dict, c: "Client")-> None:
        self.fenetre.fill(color_dict[c.client_port])
        pygame.display.flip()

    def render_endgame(self, classement_joueurs: list, color_dict: dict, c: "Client"):
        self.fenetre.fill((255, 255, 255))

        # Définir la police et la taille du texte
        font = pygame.font.Font(None, 36)

        y = 100  # Position verticale de départ
        for player in classement_joueurs:
            # Créer un objet de texte
            player_text = font.render(str(player), True, color_dict[player])

            # Afficher le texte à l'écran
            self.fenetre.blit(player_text, (50, y))

            y += 50  # Augmenter la position verticale pour le joueur suivant

        pygame.display.flip()
        
            


def decrypt_data(data_brut: str)-> dict:
    """
    Fonction permettant de convertir le paquet recu par le serveur en dictionnaire

    Args:F
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

def decrypt_end_data(data_brut: bytes) -> list:
    # Décoder les données brutes en une chaîne de caractères (str)
    data_str = data_brut.decode('utf-8')

    # Enlevez le premier caractère (par exemple, "?")
    data_str = data_str[1:]

    # Divisez la chaîne en fonction de '!' pour obtenir la liste
    data = data_str.split('!')[0]

    # Divisez la liste obtenue en fonction de ',' pour obtenir les éléments individuels
    classement = data.split(',')
    
    # Convertissez les éléments en entiers si nécessaire
    classement = [int(item) for item in classement]

    return classement




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

def end_game(data_brut: str) -> bool:
    # Vérifie si data_brut commence par un certain caractère (par exemple, "?")
    return data_brut.startswith("?")


def run()-> None:
    """
    Fonction qui gere les différentes etapes de jeu

    Args:

    Returns:
    
    """

    c = Client()

    while True: #att de recevoir un premier message du server - contenant le nombre de joueur pour modifier matrice - avant de continuer
        nombre_joueur = c.client_socket.recv(1024).decode('utf-8')
        print(f'nombre_joueur : {nombre_joueur}')
        if nombre_joueur:
            break

    f = Fenetre(int(nombre_joueur))

    #1er message server et attribution des couleurs
    while True:
        data = c.client_socket.recv(1024) 
        player_data = decrypt_data(data.decode())
        color_dict = generate_colors(player_data)
        print(f"premiere donnée {player_data}")
        if data:
            break

    f.render_intro(color_dict, c)

    #boucle de jeu
    while True:
        data_brut = c.client_socket.recv(1024)  # 1024 est la taille max du message
        data = data_brut.decode() 
        print(f"ici datatatata : {data}")
        if end_game(data):  #pour le dernier tour de jeu - le serveur femre donc plus de data - je sort de la boucle
            print("endddddddddddddd")
            break
        print("herre")
        
        
        player_data = decrypt_data(data) #pour le dernier tour de jeu - le dernier message du serveur sera le classement que je garde en mémoire

        #if end_game(player_data):
        #   print("this is the end ")
        #    break

        print(player_data)
        f.render_matrix(player_data, color_dict)

        new_d = get_new_direction()   #verifie les evenements clavier si pas de retour pas d'envoi au serveur
        if new_d != None:   
            send_to_server(c.client_socket, f"{c.client_port},{new_d}")

    
    print("fin de jeu")
    end_data = decrypt_end_data(data_brut) #la derniere donnée envoyé est le classement
    print(end_data)
    f.render_endgame(end_data, color_dict, c)
    time.sleep(10) #temp d'affichage du window de result

run()

    