# Import socket module
import socket
import pygame
import sys
import time
import random
import numpy as np 
import threading

import sys
sys.path.append("..")  #répertoire racine pour avoir accés au dossier network
from network import network


###################

#'stan ip' : 172.21.72.136
# art ip : 172.21.72.105
host_ip = network.host_ip
port = network.port
#nombre_joueur = 3 #pour la taille matrice

###################

pygame.init()

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

        self.font36 = pygame.font.Font("../font/ethnocentric.otf", 36)
        self.font22 = pygame.font.Font("../font/ethnocentric.otf", 22)
        self.font_classic22 = pygame.font.Font("../font/Cocogoose.ttf", 22)
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

        
        text = self.font36.render("Voici ta couleur", True, (255, 255, 255))

        text_rect = text.get_rect()
        text_rect.center = (self.largeur_window // 2, self.hauteur_window // 2)

        self.fenetre.blit(text, text_rect.topleft)

        pygame.display.flip()


    def render_endgame(self, classement_joueurs: list, color_dict: dict, c: "Client"):
        self.fenetre.fill((255, 255, 255))

        y = 100  # Position verticale de départ

        # Affiche "Classement final de la partie" en utilisant une police plus grande (font48)
        title_text = self.font22.render("Classement final de la partie", True, (0, 0, 0))
        title_rect = title_text.get_rect(center=(self.largeur_window // 2, y))
        self.fenetre.blit(title_text, title_rect.topleft)
        y += title_rect.height + 20  # Augmente la position verticale pour le classement

        i = 1
        for player in classement_joueurs:
            print(f" player : {player}")
            # Crée un objet de texte
            player_text = self.font22.render(str(f"{i} - {player}"), True, color_dict[player])
            i += 1

            # Afficher le texte à l'écran
            self.fenetre.blit(player_text, (50, y))

            y += 50  # Augmenter la position verticale pour le joueur suivant

        message = self.font_classic22.render("Appuyez sur 'a' pour refaire une partie ou 'q' pour quitter le jeu", True, (0, 0, 0))
        self.fenetre.blit(message, (50, y + 100))  # Augmentez la position verticale pour le message

        pygame.display.flip()

    def render_waiting():
        fenetre = pygame.display.set_mode((800, 800))
        fenetre.fill((255, 255, 255))
        pygame.display.flip()

        



    #def render_waiting():
    #    pygame.init()
    #    largeur_window = 800
    #    hauteur_window = 800
    #    fenetre = pygame.display.set_mode((largeur_window, hauteur_window))
#
    #    # Dimensions du rectangle de chargement
    #    rect_width = 400
    #    rect_height = 20
#
    #    # Position du rectangle de chargement
    #    rect_x = (largeur_window - rect_width) // 2
    #    rect_y = (hauteur_window - rect_height) // 2
#
    #    # Couleurs du rectangle de chargement
    #    rect_color = (0, 128, 255)  # Couleur bleue
    #    background_color = (200, 200, 200)  # Couleur de l'arrière-plan
#
    #    # Avancement du rectangle de chargement (de 0 à rect_width)
    #    progress = 0
#
    #    clock = pygame.time.Clock()
#
    #    running = True
    #    while running:
    #        for event in pygame.event.get():
    #            if event.type == pygame.QUIT:
    #                running = False
#
    #        # Dessiner l'arrière-plan
    #        fenetre.fill(background_color)
#
    #        # Dessiner le rectangle de chargement
    #        pygame.draw.rect(fenetre, rect_color, (rect_x, rect_y, progress, rect_height))
#
    #        # Mettre à jour l'affichage
    #        pygame.display.flip()
#
    #        # Simuler un chargement (remplacez cette partie par votre logique de chargement réelle)
    #        if progress < rect_width:
    #            progress += 2  # Augmentez la valeur de progression (ajustez selon vos besoins)
    #        else:
    #            progress = 0  # Réinitialisez la barre de chargement
#
    #        clock.tick(60)  # Limitez la fréquence de rafraîchissement (60 FPS)
#




        
            


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

    data_str = data_brut.decode('utf-8')
    data_str = data_str[1:]
    data = data_str.split('!')[0]
    classement = data.split(',')
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
    # Vérifie si data_brut commence par un certain caractère "?"
    return data_brut.startswith("?")


def run() -> None:
    while True:
        c = Client()

        #thread waiting window
        #render_thread = threading.Thread(target=Fenetre.render_waiting)
        #render_thread.start()
#
        #Fenetre.render_waiting()

        waiting_for_players = True  # Initialisation du drapeau d'attente

        while waiting_for_players:
            # Attendre de recevoir le nombre de joueurs du serveur
            nombre_joueur = c.client_socket.recv(1024).decode('utf-8')
            print(nombre_joueur)
            if nombre_joueur:
                waiting_for_players = False  # La condition a été satisfaite, sortez de la boucle

        #pygame.quit() 
        f = Fenetre(int(nombre_joueur))

        #1er message server et attribution des couleurs
        while True:
            data = c.client_socket.recv(1024) 
            player_data = decrypt_data(data.decode())
            color_dict = generate_colors(player_data)
            if data:
                break
            
        f.render_intro(color_dict, c)

        #boucle de jeu
        i=0 #test pour tour de jeu - a supprimer
        while True:
            data_brut = c.client_socket.recv(1024)  # 1024 est la taille max du message
            data = data_brut.decode() 
            if end_game(data):  #pour le dernier tour de jeu - le serveur femre donc plus de data - je sort de la boucle
                break 
            #print("herre")


            player_data = decrypt_data(data) #pour le dernier tour de jeu - le dernier message du serveur sera le classement que je garde en mémoire

            #if end_game(player_data):
            #   print("this is the end ")
            #    break
            i+=1
            f.render_matrix(player_data, color_dict)

            new_d = get_new_direction()   #verifie les evenements clavier si pas de retour pas d'envoi au serveur
            if new_d != None:   
                send_to_server(c.client_socket, f"{c.client_port},{new_d}")

        end_data = decrypt_end_data(data_brut) #la derniere donnée envoyé est le classement

        f.render_endgame(end_data, color_dict, c)


        restart = False
        while restart == False:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        exit()                       # Quitte le programme
                    elif event.key == pygame.K_a:
                        restart = True             # Sort de la boucle de fin de jeu pour rejouer

        
                    

run()

    