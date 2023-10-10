# Import socket module
import socket
import pygame

###################

#'stan ip' : 172.21.72.136
host_ip = '172.21.72.136'
port = 7777

###################

class Player():
    
	def __init__(self,id, x, y, direction, color=(255,0,0)) -> None:

		self.id = id

		self.x = x
		self.y = y
		self.direction = direction #haut, bas, gauche, droite

		self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		
		self.socket.connect((host_ip, port))
		self.socket.recv(2048).decode() #reste ne écoute sur le serveur sinon deco direct

	def send_to_server(self, data):
		self.socket.send(str.encode(data))

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
		return f"{self.x},{self.y},{self.direction},{self.id}"
	
p1 = Player(1,0,2,"R")
p1.send_to_server(p1.data_network_format())

		



