#server.py
#---------
#Mike Moniz - 0950795
#Adam Axtmann - 

import socket
import sys
import time
import string

#---------------------------------------------		
#dectEnd
#return x if the game is won by x
#return o if the game is won by o
#return c for cats game
#return p if the game is in play
def dectEnd():
	win = dectWin()
	if win == 'x' or win == 'o':
		return win
	full = dectFullBoard()
	if(full == 0):
		return 'c'
	else:
		return 'p'
		

#dectWin
#return o or x if there is a win
#return -1 if there is no winner
def dectWin():
	#detect if there is a diagonal win
	if(board[0] == board[4] == board[8]):
		return board[0]
	elif(board[2] == board[4] == board[6]):
		return board[2]
	
	#detect if there is a horizontal win
	for i in range(0, 6):
		if(board[i] == board[i+1] == board[i+2]):
			return board[i]
		i = i + 3
		
	#detect if there is a vertical win
	for i in range(0, 3):
		if(board[i] == board[i+3] == board[i+6]):
			return board[i]
		i = i + 1
	
#dectFullBoard
#return 0 if the board is not full
#return 1 if the board is full
def dectFullBoard():
	for item in board:
		if item != 'x' or item != 'o':
			return 0
	return 1
	
#------------------------------------

port = sys.argv[1] #obtain the port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
name = socket.gethostname()
board = ['0','1','2','3','4','5','6','7','8'] #initialize the board
players_connected = 0

s.bind((name,int(port)))
s.listen(1) #queues up to 5 requests

player1 = -1
player2 = -1
player_indication = 0

while 1:
	#reset board for continuous play
	board = ['0','1','2','3','4','5','6','7','8']
	(clientsocket1, address1) = s.accept()
	print "waiting for second player..."
        (clientsocket2, address2) = s.accept()
        print "second player connected"

        while 1:
			#-----player 1-------------
			#by default the first person to connect is x
			clientsocket1.send('1')

			data = clientsocket1.recv(1)
			ind = int(data)
			
			#if the move is valid and not out of bounds
			if((0 <= ind and ind < 9) and (board[ind] != 'x' or board[ind] != 'o')):
				board[ind] = 'x'
				clientsocket1.send('v')
			else:
				clientsocket1.send('i')
			#send the opponent the updated move
			clientsocket2.send('q')
			clientsocket2.send(data)

			winner = dectEnd()
			if (winner == "x" or winner == "o"):
				clientsocket1.send(winner)
				clientsocket2.send(winner)
				print winner, " wins!"
				break
                        
			#--------player 2----------------
			clientsocket2.send('2')
			
			data = clientsocket2.recv(1)
			ind = int(data)
			
			#if the move is valid and not out of bounds
			if((0 <= ind and ind < 9) and (board[ind] != 'x' or board[ind] != 'o')):
				board[ind] = 'o'
				clientsocket2.send('v')
			else:
				clientsocket1.send('i')
				
			#send the opponent the updated move
			clientsocket1.send('w')
			clientsocket1.send(data)
			
			winner = dectEnd()
			if (winner == "x" or winner == "o"):
				clientsocket1.send(winner)
				clientsocket2.send(winner)
				print winner, " wins!"
				break
                
        clientsocket1.send('t')
        clientsocket2.send('t')
        clientsocket1.close()
        clientsocket2.close()