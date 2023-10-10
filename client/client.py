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

def connect_to_server():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host_ip, port))
    return True

def send_to_server(client_socket: "socket", data: str):
    client_socket.send(str.encode(data))
    return True

def get_new_direction():
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
color_dict = {i: (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for i in range(1, 21)}

class Fenetre:
    def __init__(self, n=3, largeur=400, hauteur=400) -> None:
        self.largeur = largeur
        self.hauteur = hauteur
        self.fenetre = pygame.display.set_mode((self.largeur, self.hauteur))
        self.matrice = np.zeros((40, 40), dtype=int)  # Créez une matrice de dimensions n x n remplie de zéros de type entier


    def render_matrix(self):
        # Remplir l'écran avec une couleur blanche
        self.fenetre.fill((255, 255, 255))

        # Mettre id des joueurs sur la matrice
        for player_id, (x, y) in player_data.items():
            self.matrice[y][x] = player_id

        # Boucle pour parcourir la matrice et dessiner les cellules
        for i in range(len(self.matrice)):
            for j in range(len(self.matrice[i])):
                position = self.matrice[i][j]
                if position != 0:
                    pygame.draw.rect(self.fenetre, color_dict[position], (j * 10, i * 10, 10, 10))
        pygame.display.flip()

f = Fenetre()
while True:
    # Supposer que vous recevez les nouvelles positions des joueurs du serveur sous forme de dictionnaire
    player_data = {1: (random.randrange(0,40), random.randrange(0,40)), 2: (random.randrange(0,40), random.randrange(0+1,40-1))}  # Exemple de nouvelles données de joueurs
    print(player_data)
    f.render_matrix()
    time.sleep(1)


    


			
"""
class Player():
    
	def __init__(self,id, x, y, direction, color=(255,0,0)) -> None:

		#self.id = id

		self.x = x
		self.y = y
		self.direction = direction #haut, bas, gauche, droite

		self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		
		self.socket.connect((host_ip, port))
		print("c'est moiu")
		#self.socket.recv(2048).decode() #reste ne écoute sur le serveur sinon deco direct
		print("je suis ici")

	def send_to_server(self, data):
		print("la")
		self.socket.send(str.encode(data))
		print("amdoulad")

	def move(self): #return new direction
		keys = pygame.key.get_pressed()

		if keys[pygame.K_RIGHT]:
			self.direction = "R"
			self.x += 1

		if keys[pygame.K_LEFT]:
			self.direction = "L"
			self.x -=1
		
		if keys[pygame.K_UP]:
			self.direction = "U"
			self.y += 1

		if keys[pygame.K_DOWN]:
			self.direction = "D"
			self.y -=1

	def data_network_format(self):
		return f"{self.x},{self.y},{self.direction},{self.socket.getsockname()[1]}"
	
p1 = Player(1,0,2,"R")


while True:
	p1.send_to_server(p1.data_network_format())

p1.send_to_server(p1.data_network_format())
p1.send_to_server(p1.data_network_format())

#while True:
#	p1.send_to_server("mama")
#p1.send_to_server(p1.data_network_format())
#p1.send_to_server(p1.data_network_format())
#p1.send_to_server(p1.data_network_format())


"""		



