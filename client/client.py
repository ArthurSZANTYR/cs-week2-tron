# Import socket module
import socket

###################

#'stan ip' : 172.21.72.136
host_ip = '172.21.72.136'
port = 12345

###################

class Player():
    
	def __init__(self, x, y, direction, color=(255,0,0)) -> None:
		self.x = x
		self.y = y
		self.direction = direction #haut, bas, gauche, droite
		self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

		self.s.connect((host_ip, port))

	def input(self): #return new direction
		new_dir = 

"""
def Main():
	# local host IP '127.0.0.1'
    # stan ip : 172.21.72.136
	host = '172.21.72.136'

	# Define the port on which you want to connect
	port = 8080

	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

	# connect to server on local computer
	s.connect((host,port))

	# message you send to server
	message = "shaurya says geeksforgeeks"
	while True:

		# message sent to server
		s.send(message.encode('ascii'))

		# message received from server
		data = s.recv(1024)

		# print the received message
		# here it would be a reverse of sent message
		print('Received from the server :',str(data.decode('ascii')))

		# ask the client whether he wants to continue
		ans = input('\nDo you want to continue(y/n) :')
		if ans == 'y':
			continue
		else:
			break
	# close the connection
	s.close()

	#test123

if __name__ == '__main__':
	Main()
"""