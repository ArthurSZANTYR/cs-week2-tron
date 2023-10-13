 $${\color{red}CS-WEEK2-TRON}$$
 
Createch - computer science project week2 - Tron light cycle game in network
## Contributors
##### -Arthur SZANTYR
##### -Stanislas GADECEAU
We realized this project as part of a week of computer science courses, we had to make a network game in the format of "*Tron light racer*".

> Light Cycles is a video game created by Kevin Flynn. The game is played by driving a vehicle known as a light cycle, which leaves an impenetrable barrier called a Jetwall. The object of the game is to make all of the other opponents drive into the jetwall, effectively derezzing the cycle. The last person still on their cycle is the winner.

The instructions were to use sockets and multi threading to make this game work

--------

## Installation and Usage
To use the game follow these steps :


__Installation__
* Open the file "Server.py" 
  * Choose the number of players in the "Hand"
  * Put the right ip that will host the server the time of the part "host = "x.x.x.x""
  * Put a chosen port "port = xxxx"
* Open a "Client.py" file by desired players
  * Put the right ip that host the server "host = "x.x.x.x""
  * Put the right port "port = xxxx"

__Usage__
* Make sure that the file "Server.py" is launched
* Launch each one "Client.py" file per player
  * When the right number of players are connected, the game will start
 *  At the time of the launch of the game you will see your color highlighted on the screen remember the good it is important !
* You will appear in different places of the map, use the arrow keys to orient yourself
* At the end of the game the ranking is displayed, you can either quit the game or want to replay (follow the instructions)

__Rules__
* You advance at a constant speed on the map, you leave behind a continuous trace of your color
* If you run into a wall (map limit), you lose
* If you run in a track you lose (even yours) so a half turn makes you lose also 😉
* The winner is the last survivor, the one with the longest trace

 ___Good Game___

![alt text](https://github.com/ArthurSZANTYR/cs-week2-tron/blob/main/image/ScreenGameTron.jpeg?raw=true)

## Project Structure

The project is organized as follows:

- `Server.py` file containing the server, calculations of positions, colisions, creations of players and others...
- `Client.py` file containing the client part, therefore only the display and sending of data (change of direction)

## Thank you and conclusion
We would like to thank Gregor for offering us this exercise that we have fun doing despite the many problems encountered.
This type of exercise is pleasant to learn new knowledge in python, project management, management of Github and the fact that we are free of our time is more challenging.

Thanks also to  [https://github.com/matthieu-sgi] @matthieu-sgi for his help and for his time.
