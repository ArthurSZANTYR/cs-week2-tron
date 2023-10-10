# Import socket module
import socket
import pygame

###################

#'stan ip' : 172.21.72.136
host_ip = '172.21.72.136'
port = 7778

###################

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


		



