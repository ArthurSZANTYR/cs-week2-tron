# Import socket module
import socket
import pygame
import sys
import time

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

class Fenetre:
    def __init__(self, largeur=400, hauteur=400) -> None:
        self.largeur = largeur
        self.hauteur = hauteur
        self.fenetre = pygame.display.set_mode((self.largeur, self.hauteur))
        self.matrice = [[0, 0, 0],
                        [0, 1, 0],
                        [0, 0, 0]]

    def render_matrix(self):
        # Boucle pour parcourir la matrice et dessiner les cellules
        for i in range(len(self.matrice)):
            for j in range(len(self.matrice[i])):
                cellule = self.matrice[i][j]
                couleur = (255, 0, 0) if cellule == 1 else (255, 255, 255)  # Par exemple, 1 pour blanc et 0 pour noir
                pygame.draw.rect(self.fenetre, couleur, (j * 100, i * 100, 100, 100))
        pygame.display.flip()

f = Fenetre()
while True:
    f.render_matrix()
    time.sleep(1/25)


			
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



