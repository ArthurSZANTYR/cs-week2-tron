import socket
from _thread import *
import threading
import time

print_lock = threading.Lock()
connected_clients = []  # Une liste pour stocker les clients connectés

# Fonction de gestion de thread
def threaded(c):
    global connected_clients  # Utilisez la liste globale des clients connectés

    while True:
        data = c.recv(1024)
        if not data:
            print('Client déconnecté')
            connected_clients.remove(c)  # Retirez le client de la liste lorsqu'il se déconnecte
            print_lock.release()
            break

        data = data[::-1]
        c.send(data)

def Main():
    host = ""
    port = 12345
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("Socket lié au port", port)
    s.listen(5)
    print("Socket en écoute")

    while True:
        c, addr = s.accept()
        print_lock.acquire()
        print('Connecté à :', addr[0], ':', addr[1])
        connected_clients.append(c)  # Ajoutez le client à la liste des clients connectés
        start_new_thread(threaded, (c,))
    
    s.close()
    

class Player:
    def __init__(self, x, y, d, id):
        """
        init method for class
        """
        self.x = x  # player x coord
        self.y = y  # player y coord
        self.speed = 1  # player speed
        self.bearing = d  # player direction
        self.colour = id
        self.boost = False  # is boost active
        self.start_boost = time.time()  # used to control boost length
        self.boosts = 3
        
    def __move__(self):
        """
        method for moving the player
        """
        if not self.boost:  # player isn't currently boosting
            self.x += self.bearing[0]
            self.y += self.bearing[1]
        else:
            self.x += self.bearing[0] * 2
            self.y += self.bearing[1] * 2

    def __boost__(self):
        """
        starts the player boost
        """
        if self.boosts > 0:
            self.boosts -= 1
            self.boost = True
            self.start_boost = time.time()


def new_game():
    # Instanciez un nouveau joueur pour chaque client connecté
    new_players = []
    idd =0
    for c in connected_clients:
                new_players.append(Player(width/len(new_players), 0, "h", idd))
                idd+=1
                
    width, height = 300*len(new_players), 330*len(new_players)  # window dimensions
	

    return new_players,width,height

offset = height - width #vertical space at top of window


check_time = time.time()  # used to check collisions with rects


wall_rects = [pygame.Rect([0, offset, 15, height]) , pygame.Rect([0, offset, width, 15]),\
              pygame.Rect([width - 15, offset, 15, height]),\
              pygame.Rect([0, height - 15, width, 15])]  # outer walls of window

done = False
new = False

while not done:
    for event in pygame.event.get():  # gets all event in last tick
        if event.type == pygame.QUIT:  # close button pressed
            done = True
        elif event.type == pygame.KEYDOWN:  # keyboard key pressed
            # === Player 1 === #
            if event.key == pygame.K_w:
                objects[0].bearing = (0, -2)
            elif event.key == pygame.K_s:
                objects[0].bearing = (0, 2)
            elif event.key == pygame.K_a:
                objects[0].bearing = (-2, 0)
            elif event.key == pygame.K_d:
                objects[0].bearing = (2, 0)
            elif event.key == pygame.K_TAB:
                objects[0].__boost__()
            # === Player 2 === #
            if event.key == pygame.K_UP:
                objects[1].bearing = (0, -2)
            elif event.key == pygame.K_DOWN:
                objects[1].bearing = (0, 2)
            elif event.key == pygame.K_LEFT:
                objects[1].bearing = (-2, 0)
            elif event.key == pygame.K_RIGHT:
                objects[1].bearing = (2, 0)
            elif event.key == pygame.K_RSHIFT:
                objects[1].__boost__()

    screen.fill(BLACK)  # clears the screen

    for r in wall_rects: pygame.draw.rect(screen, (42, 42, 42), r, 0)  # draws the walls

    for o in objects:
        if time.time() - o.start_boost >= 0.5:  # limits boost to 0.5s
            o.boost = False

        if (o.rect, '1') in path or (o.rect, '2') in path \
           or o.rect.collidelist(wall_rects) > -1:  # collided with path or wall
            # prevent player from hitting the path they just made
            if (time.time() - check_time) >= 0.1:
                check_time = time.time()

                if o.colour == P1_COLOUR:
                    player_score[1] += 1
                else: player_score[0] += 1

                new = True
                new_p1, new_p2 = new_game()
                objects = [new_p1, new_p2]
                path = [(p1.rect, '1'), (p2.rect, '2')]
                break
        else:  # not yet traversed
            path.append((o.rect, '1')) if o.colour == P1_COLOUR else path.append((o.rect, '2'))

        o.__draw__()
        o.__move__()

    for r in path:
        if new is True:
            path = []
            new = False
            break
        if r[1] == '1': pygame.draw.rect(screen, P1_COLOUR, r[0], 0)
        else: pygame.draw.rect(screen, P2_COLOUR, r[0], 0)

    
    pygame.display.flip()  # flips display
    clock.tick(60)  # regulates FPS

pygame.quit()	

if __name__ == '__main__':
    Main()
