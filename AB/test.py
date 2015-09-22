from game import *
import sys, traceback,re

def main():
	print "Welcome to the Konane Game!"
	print "Rules:\nFirst, the X player removes a dark piece either at the center or corners.\nNext the O player removes a light piece adjacent to the space created by the first move."
	print "Then the players alternate moves, each jumping one of his/her own pieces over one horizontally or vertically adjacent opponent piece, landing in a space on the other side, and removing the jumped piece. "
	print "If desired, this may be continued in a multiple move, as long as the same piece is moved in a straight line. "

	size = raw_input("Choose Board Size(6 or 8): ")
	try:
   		val = int(size)
	except ValueError:
   		print("That's not an integer!The game will exit.")
   		sys.exit(0)
	size=int(size)
	
	if (size is not 6 and size is not 8):
		print "Size is out of range! Please start the game again."
		sys.exit(0)

	gameBoard=Konane(size)
	robot=Robot(size,'')
	gameBoard.boardToString(gameBoard.board)


	playerMode = raw_input("Pick a side(X moves first, O moves next): ")
	while not re.match("[XxOo]", playerMode):
		playerMode = raw_input("Error input! Please choose either X or O:")
	

	if (playerMode == "X" or playerMode== "x"):
		fm = raw_input("Enter your First Move(either from the center or corners): ")
		while (not gameBoard.processInput(fm)):
			fm = raw_input("Enter your First Move(either from the center or corners): ")
		while (not gameBoard.firstMove(gameBoard.board,gameBoard.processInput(fm))):
				fm = raw_input("Enter your First Move(either from the center or corners): ")
		gameBoard.boardToString(gameBoard.board)
		robot.mode='O'
		print "The computer will play 'O'. It is going to make a move..."
		gameBoard.boardToString(robot.robotSecondMove(gameBoard.board))
	
	else:
		print "The computer will play 'X'. It is going to make a move..."
		robot.mode = 'X'
		gameBoard.boardToString(robot.robotFirstMove(gameBoard.board))
		
		sm = raw_input("You can only move the piece next to the '.'\nEnter your Move: ")
		while (not gameBoard.processInput(sm)):
			sm = raw_input("\nEnter your Move: ")
		while (not gameBoard.secondMove(gameBoard.board,gameBoard.processInput(sm))):
			sm = raw_input("\nEnter your Move: ")
		gameBoard.boardToString(gameBoard.board) 
	
	
	


	print "I am here"
	while( not (gameBoard.isLost(gameBoard.board, playerMode)) and not ( gameBoard.isLost(gameBoard.board, robot.mode))):
		if (playerMode == "X" or playerMode== "x"):
			print "I am in while loop"
			numMoves=  raw_input("Number of moves do you want to make: ")
			while (not gameBoard.validInt(numMoves)):
				numMoves=  raw_input("Number of moves do you want to make: ")
			numMoves=int(numMoves)
			while (numMoves > 0):
				chess =  raw_input("Pick a piece: ")
				while (not gameBoard.validInput(chess)):
					chess = raw_input("Pick a piece: ")
				move  = raw_input("Make a Move: ")
				while (not gameBoard.validInput(move)):
					move= raw_input("Make a Move: ")
				while (not gameBoard.isValid(gameBoard.board,gameBoard.processInput(chess),gameBoard.processInput(move),'X')):
		 			chess =  raw_input("Pick a piece: ")
					while (not gameBoard.validInput(chess)):
						chess = raw_input("Pick a piece: ")
					move  = raw_input("Make a Move: ")
					while (not gameBoard.validInput(move)):
						move= raw_input("Make a Move: ")
				numMoves= numMoves -1
				gameBoard.borad=gameBoard.makeMove(gameBoard.board,gameBoard.processInput(chess),gameBoard.processInput(move),'X')[:]
			print "wait for computer to make a move"
			y = Node(robot.mode,None,gameBoard.board,0,True)
			t = robot.minimaxAB(y,float("-inf"),float("inf"))
			#t = robot.minimax(y)
			moves = t[1]
			print "number of evaluations:", y.score
			print "number of cut-offs:", y.cutoffs
			print "Robot moves are ", moves
			gameBoard.board = robot.readRobotMoves(moves, y.currentBoard, y.mode)[:]
			print gameBoard.boardToString(gameBoard.board)

			
		if (playerMode == "O" or playerMode== "o"):
			print "wait for computer to make a move"
			y = Node(robot.mode,None,gameBoard.board,0,True)
			t = robot.minimaxAB(y,float("-inf"),float("inf"))
			#t = robot.minimax(y)
			moves = t[1]
			print "number of evaluations:", y.score
			print "number of cut-offs:", y.cutoffs
			print "Robot moves are ", moves
			gameBoard.board = robot.readRobotMoves(moves, y.currentBoard, y.mode)[:]
			print gameBoard.boardToString(gameBoard.board)
			print "Now it is your turn."
			numMoves=  raw_input("Number of moves you want to make: ")
			while (not gameBoard.validInt(numMoves)):
				numMoves=  raw_input("Number of moves you want to make: ")
			numMoves=int(numMoves)
			while (numMoves > 0):
				chess =  raw_input("Pick a piece: ")
				while (not gameBoard.validInput(chess)):
					chess = raw_input("Pick a piece: ")
				move  = raw_input("Make a Move: ")
				while (not gameBoard.validInput(move)):
					move= raw_input("Make a Move: ")
				while (not gameBoard.isValid(gameBoard.board,gameBoard.processInput(chess),gameBoard.processInput(move),'O')):
		 			chess =  raw_input("Pick a piece: ")
					while (not gameBoard.validInput(chess)):
						chess = raw_input("Pick a piece: ")
					move  = raw_input("Make a Move: ")
					while (not gameBoard.validInput(move)):
						move= raw_input("Make a Move: ")
				numMoves= numMoves -1
				gameBoard.borad=gameBoard.makeMove(gameBoard.board,gameBoard.processInput(chess),gameBoard.processInput(move),'O')[:]
				
if __name__ == "__main__":
    main()


"""
board1=Konane(6)
board1.firstMove(board1.board,board1.processInput("4,3"))
board1.secondMove(board1.board,board1.processInput("4,4"))
board1.makeMove(board1.board,board1.processInput("4,1"),board1.processInput("4,3"),'X')
board1.makeMove(board1.board,board1.processInput("6,1"),board1.processInput("4,1"),'X')
board1.makeMove(board1.board,board1.processInput("6,3"),board1.processInput("6,1"),'X')
print "-------------------------------------------------------------------------" 
r=Robot(6)
r.generateAllMoves(board1.board, 'O')

board1.makeMove(board1.board,board1.processInput("3,4"),board1.processInput("1,4"),'X')
r=Robot(4)
r.generateAllMoves(board1.board, 'O')"""
"""board1.isValid(board1.board,board1.processInput("4,3"),board1.processInput("4,5"),'X')"""
"""board1.makeMove(board1.board,board1.processInput("4,3"),board1.processInput("1,5"),'X')
board1.makeMove(board1.board,board1.processInput("4,8"),board1.processInput("4,6"),'O')
board1.makeMove(board1.board,board1.processInput("2,3"),board1.processInput("4,3"),'X')""" 


