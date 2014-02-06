#client.py
#---------
#Mike Moniz - 0950795
#Adam Axtmann - 

import socket
import sys
import time
import string

#printBoard
#prints to the screen the current version of the board
def printBoard():
	i = 0;
	line = ""
	
	for item in board:
		line = line + (item).rjust(1) 
		if (i + 1)% 3 == 0 and i < 6:
			line = line + "\n---------\n"
		elif i < 8:
			line = line + " | "
		i= i + 1
	print line

	
board = ['0','1','2','3','4','5','6','7','8'] #initialize the board

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip = sys.argv[1]
port = sys.argv[2]

#connect to the server
try:
	s.connect((ip,int(port)))
    
	# Receive data from the server and shut down
	while 1:			
		state = s.recv(1)
		
		#This state is to allow player 1 to make their move (ignoring invalid moves)
		if (state == '1'):
			printBoard()
			data = raw_input('your turn: ')
			s.send(data)
			
			valid = s.recv(1)
			
			#once valid, mark the board
			if(valid == 'v'):
				board[int(data)] = 'x'
			printBoard()
		
		#This state is to allow player 2 to make their move (ignoring invalid moves)
		elif (state == '2'):
			printBoard()
			data = raw_input('your turn: ')
			s.send(data)
			
			valid = s.recv(1)
			
			#once valid, mark the board
			if(valid == 'v'):
				board[int(data)] = 'o'
			printBoard()
			
		#This state is to update player 1's board with player 2's move
		elif (state == 'q'):
			val = s.recv(1)
			board[int(val)] = 'x'
			
		#This state is to update player 2's board with player 1's move
		elif (state == 'w'):
			val = s.recv(1)
			board[int(val)] = 'o'
			
		#This state is to terminate the client
		elif (state == 't'):
			break
			
		#This state is to terminate the client and declare a winner
		elif (state == 'x' or state == 'o'):
			print state, " wins!"
			break
except:
	print "exception"
finally:
	s.close()
