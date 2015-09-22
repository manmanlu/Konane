import copy

class Node():
	def __init__(self,mode,parent,currentBoard,depth, isMax):
		self.score = 0
		self.mode = mode
		self.parent = parent #parent is a node
		self.children =[]
		self.currentBoard = currentBoard
		self.depth = depth
		self.action=[] # the action this board can make
		self.isMax = isMax #True if isMax, False if not

	
class Robot:
	def __init__(self,n,mode):
		self.size=n
		self.mode=mode
	def generateAllMoves(self, board, mode):
		result=Set()
		for i in range(self.size):
			for j in range(self.size):
				if board[i][j]==mode:
					boardCopy=deepcopy(board)
					result.update(self.generateOneMove(boardCopy,(i,j),mode,[(i,j)]))
		"""print len(result)
		for x in result:
			print Konane(self.size).boardToString(x.board)
			print x.actionList
			print x.mode
			print "***************************" """
		return result #this is a moveNode sets

	def getChildrenForANode(self, node): #Get Children for one board and also fill all the possible actions for this node
		result = self.generateAllMoves(node.currentBoard, node.mode)
		if node.mode == 'X':
			childrenMode = 'O'
		if node.mode == 'O':
			childrenMode = 'X'

		for x in result:
			child = Node(childrenMode,node,x.board[:],node.depth+1, not node.isMax)
			child.action = x.actionList[:]
			child.parent = node
			node.children.append(child)
		return node.children

	def generateOneMove(self, board,(i,j),mode,actions):
		moveNodeSet=Set()
		if mode == 'X':
			notMode = 'O'
		if mode == 'O':
			notMode = 'X'
		parent = MoveNode(board, None, mode)
		parent.actionList = actions[:]
		"""print "I am printint parent.actionList"
		print parent.actionList"""
		if self.getValidMoves(board, (i,j), mode)==[]:	
			return moveNodeSet
		else:
			"""print self.getValidMoves(board, (i,j), mode)"""
			for move in self.getValidMoves(board, (i,j), mode):				
				moveNode = MoveNode(self.generateNextState(board,(i,j),move,mode),parent,notMode)
				moveNode.actionList = parent.actionList[:]
				moveNode.actionList.append(move)
				moveNodeSet.add(moveNode)
				"""print Konane(self.size).boardToString(moveNode.board)
				print moveNode.actionList
				print "***************************" """
				moveNodeSet.update(self.generateOneMove(moveNode.board,moveNode.actionList[len(moveNode.actionList)-1],mode,moveNode.actionList))			
			return moveNodeSet


	def getValidMoves(self, board, (x,y), mode):
		moves=[]
		if Konane(self.size).isValid(board,(x,y),(x-2,y),mode):
			moves.append((x-2,y))
		if Konane(self.size).isValid(board,(x,y),(x+2,y),mode):
			moves.append((x+2,y))
		if Konane(self.size).isValid(board,(x,y),(x,y-2),mode):
			moves.append((x,y-2))
		if Konane(self.size).isValid(board,(x,y),(x,y+2),mode):
			moves.append((x,y+2))
		return moves

	def generateNextState(self,board,(x,y),(m,n),mode):
		boardCopy = deepcopy(board)
		if Konane(self.size).isValid(board,(x,y),(m,n),mode):
			boardCopy[x][y]='.'
			boardCopy[m][n]=mode
			boardCopy[x+(m-x)/2][y+(n-y)/2]='.'	
			"""print Konane(self.size).boardToString(boardCopy)	"""
			return boardCopy
	def evaluateLeafNode1(self, node): #evalutes the leaf Node: number of avaliable max moves - number of avaliable not max move
		if node.mode == 'X':
			notMe = 'O'
		else:
			notMe = 'X'
		if node.isMax:
			return len(self.generateAllMoves(node.currentBoard, node.mode)) - len(self.generateAllMoves(node.currentBoard, notMe))
		else:
			return len(self.generateAllMoves(node.currentBoard, notMe)) - len(self.generateAllMoves(node.currentBoard, node.mode))	

	def evaluateLeafNode(self, node): #evalutes the leaf Node: number of avaliable max moves - number of avaliable not max move
		if node.mode == 'X':
			notMeNode = Node('O', node.parent, node.currentBoard,node.depth, not node.isMax)
				
		else:
			notMeNode = Node('X', node.parent, node.currentBoard,node.depth, not node.isMax)
		"""if node.isMax:
			return len(self.generateAllMoves(node.currentBoard, node.mode)) - len(self.generateAllMoves(node.currentBoard, notMe))
		else:
			return len(self.generateAllMoves(node.currentBoard, notMe)) - len(self.generateAllMoves(node.currentBoard, node.mode))"""

		if node.isMax:
			#if Konane(self.size).isLost(node.currentBoard, node.mode):
			#	return float("-inf")
			#elif Konane(self.size).isLost(node.currentBoard, notMeNode.mode):
			#	return float("inf")
			#else:
			score  = len(self.getChildrenForANode(node)) - len(self.getChildrenForANode(notMeNode))
			
			while(node.parent!=None):
				node = node.parent
			node.score= node.score+1
			return score
		else:
			#if Konane(self.size).isLost(node.currentBoard, notMeNode.mode):
			#	return float("-inf")
			#elif Konane(self.size).isLost(node.currentBoard, node.mode):
			#	return float("inf")
			#else:
			score= len(self.getChildrenForANode(notMeNode)) - len(self.getChildrenForANode(node))
			while(node.parent!=None):
				node = node.parent
			node.score= node.score+1
			return score

	def minimax(self, node):
		if node.depth==3: #is a leafNode
			"""print "------------I am evaluating----------"""
			return (self.evaluateLeafNode(node), node.action)

		if Konane(self.size).isLost(node.currentBoard, node.mode):# this is a leafNode
			"""print "------------I am evaluating----------"""
			return (self.evaluateLeafNode(node), node.action)

		ns = self.getChildrenForANode(node)#all children of node

		"""print "--------",node.depth,"----------"
		for x in ns:
			print x.action
			print x.mode
			print "isMax = ", x.isMax
			print "****************" """
		"""print "--------Branch Factor: ", len(ns), "---------------------"""


		if len(ns)==0: # this is a leafNode
			"""print "------------I am evaluating----------"""
			return (self.evaluateLeafNode(node), node.action)

		if len(ns)==1:#children is a leafNode
			"""print "------------I am evaluating----------"""
			return (self.evaluateLeafNode(node), ns[0].action)


		if node.isMax:
			cbv = float("-inf")
			bestmove = []
			for n in ns:
				"""print "-----------------max-----------------"
				print "actionList of ", n, "is ", n.actionList"""
				t = self.minimax(n)
				bv = t[0]
				move  = t[1]
				
				if bv > cbv:
					cbv = bv
					bestmove = n.action[:]
					
			"""print "MAX: ", node, " cbv = ", cbv, " bestmove = ", bestmove """
			return (cbv,bestmove)
		else:
			cbv = float("inf")
			bestmove = []
			for n in ns:
				t = self.minimax(n)
				bv = t[0]
				move = t[1]
				
				if bv < cbv:
					cbv = bv
					bestmove = n.action[:]
			"""print "MIN: ", node, " cbv = ", cbv, " bestmove = ", bestmove """
			return (cbv,bestmove) 


	def minimaxAB(self, node, A, B):

		if node.depth==6: #is a leafNode
			print "------------I am evaluating----------"
			return (self.evaluateLeafNode(node), node.action)

		if Konane(self.size).isLost(node.currentBoard, node.mode):# this is a leafNode
			print "------------I am evaluating----------"
			return (self.evaluateLeafNode(node), node.action)

		ns = self.getChildrenForANode(node)#all children of node
		"""print "--------",node.depth,"----------"
		for x in ns:
			print x.action
			print x.mode
			print "isMax = ", x.isMax
			print "****************"  """
		print "--------Branch Factor: ", len(ns), "---------------------"

		if len(ns)==0: # this is a leafNode
			print "------------I am evaluating----------"
			return (self.evaluateLeafNode(node), node.action)

		if len(ns)==1:#children is a leafNode
			print "------------I am evaluating----------"
			return (self.evaluateLeafNode(node), ns[0].action)

		if node.isMax:
			cbv = float("-inf")
			bestmove = []
			for n in ns:
				"""print "-----------------max-----------------"
				print "actionList of ", n, "is ", n.actionList"""
				t = self.minimaxAB(n,A,B)
				bv = t[0]
				move  = t[1]
				
				if bv > A:
					A = bv
					bestmove = n.action[:]

				if A >= B:
					print "---------I am cutting off---------"
					return (B,bestmove)
			"""print "cbv", cbv
			print "bestmove", bestmove"""
			return (A,bestmove)

		else:
			cbv = float("inf")
			bestmove = []
			for n in ns:
				t = self.minimaxAB(n,A,B)
				bv = t[0]
				move = t[1]
				
				if bv < B:
					B = bv
					bestmove = n.action[:]
				"""print "cbv", cbv
				print "bestmove",bestmove"""
				if A >= B:
					print "---------I am cutting off---------" 
					return (A,bestmove)
			return (B,bestmove) 

	def readRobotMoves(self, moves, board,mode):
		p,q = moves[len(moves)-1]
		for i in range(len(moves)-1):
			x,y = moves[i]
			m,n = moves[i+1]
			board[x][y]='.'
			board[m][n]= '.'
			board[x+(m-x)/2][y+(n-y)/2]='.'	

		board[p][q] = mode
		return board


	def robotSecondMove(self,board):
		moves=[]
		if board[self.size-1][0]==".":
			moves.append((self.size-1,1))
			moves.append((self.size-2,0))
		elif board[0][self.size-1]==".":
			moves.append((0,self.size-2))
			moves.append((1,self.size-1))
		elif board[self.size/2-1][self.size/2]==".":
			moves.append((self.size/2-1,self.size/2+1))
			moves.append((self.size/2-1,self.size/2-1))
			moves.append((self.size/2,self.size/2))
			moves.append((self.size/2-2,self.size/2))
		elif board[self.size/2][self.size/2-1]==".":
			moves.append((self.size/2-1,self.size/2-1))
			moves.append((self.size/2+1,self.size/2-1))
			moves.append((self.size/2,self.size/2-2))
			moves.append((self.size/2,self.size/2))
		ran=random.choice(range(0,len(moves),1))
		
		inputmove=moves[ran]
		x,y=(inputmove[0],inputmove[1])
		board[x][y]="."
		return board

	def robotFirstMove(self,board):
		validMove=[(0,self.size-1),(self.size-1,0),(self.size/2-1,self.size/2),(self.size/2,self.size/2-1)]
		ran = random.choice(range(0,len(validMove),1))
		inputmove =validMove[ran]
		x,y=(inputmove[0],inputmove[1])
		board[x][y]="."
		return board



##################################################################################################
from sets import Set
from copy import copy, deepcopy
import random
import traceback

class Konane:

	def __init__(self,n):
		self.size=n
		self.board=[]
		self.generateBoard()
		
	def generateBoard(self):
		for n in range(self.size):
			row = []
			for i in range(self.size):
				if n%2==0:
					if i%2 ==0: row.append('O')
					else:
						row.append('X')
				else:
					if i%2 ==0: row.append('X')
					else:
						row.append('O')
			self.board.append(row)

		"""print self.boardToString(self.board)"""

	def boardToString(self, board):
		for k in range(self.size+1):
			if k==0: print ' ',
			else:
				print k,
		print '\n'

		for n in range(self.size):
			for i in range(self.size+1):	
				if i==0: print self.size-n,				
				else:
					print board[self.size-1-n][i-1],
			print '\n'

	

	def firstMove(self,board,(x,y)):
		validMove=[(0,self.size-1),(self.size-1,0),(self.size/2-1,self.size/2),(self.size/2,self.size/2-1)]
		
		if (x,y) in validMove:
			board[x][y]='.'
			return True
		else:
			print "Invalid move. Please Choose another piece."
			return False
		

	def secondMove(self,board,(x,y)):
		moves=[]
		if board[self.size-1][0]==".":
			moves.append((self.size-1,1))
			moves.append((self.size-2,0))
		elif board[0][self.size-1]==".":
			moves.append((0,self.size-2))
			moves.append((1,self.size-1))
		elif board[self.size/2-1][self.size/2]==".":
			moves.append((self.size/2-1,self.size/2+1))
			moves.append((self.size/2-1,self.size/2-1))
			moves.append((self.size/2,self.size/2))
			moves.append((self.size/2-2,self.size/2))
		elif board[self.size/2][self.size/2-1]==".":
			moves.append((self.size/2-1,self.size/2-1))
			moves.append((self.size/2+1,self.size/2-1))
			moves.append((self.size/2,self.size/2-2))
			moves.append((self.size/2,self.size/2))
		if (x,y) in moves:
			board[x][y]="."
			return True 
		else:
			print "Invalid move. Please Choose another piece."
			return False

		

	def	processInput(self, n):
		if self.validInput(n):
			move=n.split(',')
		
			x=int(move[0])-1
		
			y=int(move[1])-1
			return (x,y)
		else:
			return (-1,-1)
	
	def validInt(self,n):
		try:
   			val = int(n)

		except ValueError:
   				print("That's not an integer!Please try again.")
   				return False
   		return True 

	def validInput(self,n):
		move=n.split(',')

		if type(move) is not list:
			return False
		if len(move) != 2:
			print "Please enter valid moves!"
			return False

		try:
			x=int(move[0])
		except ValueError:
			print"Please enter valid number coordinates!"
			return False
		try:
			y=int(move[1])
		except ValueError:
			print"Please enter valid number coordinates!"
			return False
		else:
			return True


	
	def isValid(self,board,(x,y),(m,n),mode):
		t=(x,y)
		h=(m,n)
		m=h[0]
		n=h[1]
		x=t[0]
		y=t[1]
		if m>=0 and m < self.size and n>=0 and n<self.size and board[m][n]=='.':
			if x>=0 and x < self.size and y>=0 and y<self.size:
				if mode =='X':
					if board[x][y]== 'X':
						if n-y==0:
							if abs(x-m)==2:	
								if board[x+(m-x)/2][y+(n-y)/2]=='O':	
									#print "Okay"		
									return True
								else:
									#print "You should choose a piece with 'O' in between" 
									return False
							else:
								#print "You should choose a piece with 'O' in between" 
								return False
						if m-x==0:
							if abs(y-n)==2:
								if board[x+(m-x)/2][y+(n-y)/2]=='O':	
									#print "Okay"
									return True
					else:
						#print "You should choose X"
						return False
				elif mode =='O':
					if board[x][y]=='O':
						if n-y==0:
							if abs(x-m)==2:
								if board[x+(m-x)/2][y+(n-y)/2]=='X':	
									return True
						if m-x==0:
							if abs(y-n)==2:
								if board[x+(m-x)/2][y+(n-y)/2]=='X':	
									return True
					else:
						#print "You should choose O"
						return False
			else:
				#print "Please pick a valid piece"
				return False
		else:
			#print "This is not a valid move" 
			return False

	def makeMove(self,board,(x,y),(m,n),mode):
		if self.isValid(board,(x,y),(m,n),mode):
			print "I am making move"
			board[x][y]='.'
			board[m][n]=mode
			board[x+(m-x)/2][y+(n-y)/2]='.'			
			self.boardToString(board)
			return board

	def isLost(self, board, mode):
		if mode == 'X':
			for i in range(self.size):
				for j in range(self.size):
					if board[i][j]=='X':
						if self.isValid(board,(i,j),(i-2,j),'X') or self.isValid(board,(i,j),(i+2,j),'X') or self.isValid(board,(i,j),(i,j-2),'X') or self.isValid(board,(i,j),(i,j+2),'X'): 
							return False
			print mode," is LOST!!!"		
			return True

		if mode == 'O':
			for i in range(self.size):
				for j in range(self.size):
					if board[i][j]=='O':
						if self.isValid(board,(i,j),(i-2,j),'O') or self.isValid(board,(i,j),(i+2,j),'O') or self.isValid(board,(i,j),(i,j-2),'O') or self.isValid(board,(i,j),(i,j+2),'O'): 
							return False
			print mode," is LOST!!!"	
			return True


class MoveNode:
	def __init__(self,board,parent, mode):
		self.board = board
		self.actionList=[]
		self.parent = parent
		self.mode = mode #this mode is after this action, the next player's mode, i.e. parent is O and actionList is [3,4] and the mode is X but this is actually after the action
		#never mind, actually this mode is the mode of the node