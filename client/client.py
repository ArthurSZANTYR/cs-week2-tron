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
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host_ip, port))

        self.client_ip, self.client_port = self.client_socket.getsockname()
		
#def connect_to_server():
#    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    client_socket.connect((host_ip, port))
#    return True

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
#color_dict = {i: (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for i in range(1, 21)}

class Fenetre:
    def __init__(self, n=3, largeur_fenetre=300, hauteur_fenetre=300) -> None:
        self.largeur = largeur_fenetre
        self.hauteur = hauteur_fenetre
        self.fenetre = pygame.display.set_mode((self.largeur, self.hauteur))
        self.matrice = np.zeros((30, 30), dtype=int)  # Créez une matrice de dimensions n x n remplie de zéros de type entier


    def render_matrix(self, player_data, color_dict):
        # Remplir l'écran avec une couleur blanche
        self.fenetre.fill((255, 255, 255))

        # Mettre id des joueurs sur la matrice
        for player_id, (x, y, d) in player_data.items():
            print(player_id)
            print(y+" , "+x)
            self.matrice[int(y)][int(x)] = player_id
            #self.matrice[3][9] = 1
            #self.matrice[3][6] = 2
            print(f"{player_id}  ->   {self.matrice[int(y)][int(x)]}")
            

        # Boucle pour parcourir la matrice et dessiner les cellules
        for y in range(len(self.matrice)):
            for x in range(len(self.matrice[y])):
                position = self.matrice[y][x]
                if position != 0:
                    print(f"position : {position}")
                    #pygame.draw.rect(self.fenetre, color_dict[position], (y*10 , x*10 , 10, 10))  #probleme sur le *10 ammene des hors cadres
                    pygame.draw.rect(self.fenetre, color_dict[position], (y*10 , x*10 , 10, 10))  #probleme sur le *10 ammene des hors cadres
                    print(f" after draw : {y} et {x}")
        pygame.display.flip()

#f = Fenetre()
#while True:
#    # Supposer que vous recevez les nouvelles positions des joueurs du serveur sous forme de dictionnaire
#    player_data = {1: (random.randrange(0,40), random.randrange(0,40)), 2: (random.randrange(0,40), random.randrange(0+1,40-1))}  # Exemple de nouvelles données de joueurs
#    print(player_data)
#    f.render_matrix()
#    time.sleep(1)

def decrypt_data(data):

    data = data.split('!')
    data = data[0]

    lines = data.split(';')
    positions = {}

    for line in lines:
        elements = line.split(',')
        key = int(elements[0])
        values = tuple(elements[1:])
        positions[key] = values

    return positions

def generate_colors(player_data):
    color_dict = {}
    for player_id, (x, y, d) in player_data.items():
        color_dict[player_id] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    return color_dict 


def run():
    c = Client()
    f = Fenetre()
    #for i in range(10):
    #    send_to_server(c.client_socket, "hello stanos")
    #print("rayyy")
    i=0
    while True:
        #send_to_server(c.client_socket, "hello stanos")
        data = c.client_socket.recv(1024)  # 1024 est la taille du tampon, ajustez-la en fonction de vos besoins
        if not data:
            break
        #print("Message reçu du serveur :", data.decode()) 

        player_data = decrypt_data(data.decode())

        if i == 0:
          color_dict = generate_colors(player_data)
          i+=1

        print(player_data)
        f.render_matrix(player_data, color_dict)

        new_d = get_new_direction()
        if new_d != None:
            send_to_server(c.client_socket, f"{c.client_port},{new_d}")


        
    #wait "start" from server

    #while True:
    #    new_direction = get_new_direction()
    #    if new_direction != None:
    #        send_to_server(new_direction)


run()

    


			
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



