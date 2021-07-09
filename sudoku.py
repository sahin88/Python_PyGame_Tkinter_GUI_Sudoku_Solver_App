import pygame
import requests
import numpy as np
import os
from tkinter import *
from tkinter import messagebox


class Sudoku:
	def __init__(self,width, height):
		pygame.init()
		self.height=550
		self.width=650
		self.grid=requests.get('https://sugoku.herokuapp.com/board?difficulty=easy').json()['board']
		self.orginal_grid=[[self.grid[x][y] for y in range(len(self.grid))] for x in range(len(self.grid))]
		self.font=pygame.font.SysFont('dejavuserif',25)
		self.re_font=pygame.font.SysFont('dejavuserif',55)
		self.color=(0,0,0)
		self.line_color=(255,0,0)
		self.buffer=5
		self.background_color=(0,255,255)
		self.solutions=[]
		
		self.main()

	def make_window(self, data):
		os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (800,900)
		self.win2=pygame.display.set_mode((self.height, self.width))
		pygame.display.set_caption("Sudoku Solver Solution")
		self.win2.fill((255,255,255))
		
		for i in range(10):
			if(i%3==0):
					pygame.draw.line(self.win2,self.line_color,(50+50*i,50),(50+50*i,500),6)
					pygame.draw.line(self.win2,self.line_color, (50,50+50*i),(500,50+50*i),6)
			pygame.draw.line(self.win2,self.line_color,(50+50*i,50),(50+50*i,500),2)
			pygame.draw.line(self.win2,self.line_color,(50,50+50*i),(500,50+50*i),2)
		pygame.display.update()

		for  x in  range(len(data)):
			for y in  range(len(data)):
				value=self.font.render(str(data[x][y]), True, self.color)
				self.win2.blit(value,((y+1)*50+12,(x+1)*50+12))
		pygame.display.update()

		
		while True:
			for event in pygame.event.get():
				if event.type==pygame.QUIT:
					pygame.quit()
					return		
			pygame.display.update()		




	def isPlaceSafe(self, item,row,column):

		#chek horizontal
		for i in range(9):
			if(self.orginal_grid[row][i]==item):
				return False

		#check 	Vertical
		for j in range(9):
			if(self.orginal_grid[j][column]==item):
				return False

		#check Square
		for i0 in range(3):
			for j0 in range(3):
				
				if(self.orginal_grid[(row//3)*3+i0][(column//3)*3+j0]==item):					
					return False
		return True



	def solve(self):
		for row in range(9):
			for column in range(9):
				if self.orginal_grid[row][column]==0:
					for i in range(1,10):
						if self.isPlaceSafe(i, row,column):
							self.orginal_grid[row][column]=i
							self.solve()
							self.orginal_grid[row][column]=0
					return 

		if self.orginal_grid!=self.grid:
			root = Tk()

			text = self.orginal_grid
			buttons = [[None]*9]*9


			for i in range(9):
			    for j in range(9):
			        btn_text = StringVar()
			        btn_text.set('{}'.format(text[i][j]))
			      
			        if (i//3==0 and j//3==0):
			            buttons[i][j] = Button(root, bg='#b3ecec')
			            buttons[i][j].config(textvariable = btn_text , width = 5, height = 5 )
			            buttons[i][j].grid(row = i, column = j)
			        elif(i//3==0 and j//3==1):
			            buttons[i][j] = Button(root, bg='#1167b1')
			            buttons[i][j].config(textvariable = btn_text , width = 5, height = 5 )
			            buttons[i][j].grid(row = i, column = j)
			        elif(i//3==0 and j//3==2):
			            buttons[i][j] = Button(root, bg='#f8ed62')
			            buttons[i][j].config(textvariable = btn_text , width = 5, height = 5 )
			            buttons[i][j].grid(row = i, column = j)
			        elif(i//3==1 and j//3==0):
			            buttons[i][j] = Button(root, bg='#3CB371')
			            buttons[i][j].config(textvariable = btn_text , width = 5, height = 5)
			            buttons[i][j].grid(row = i, column = j)
			        elif(i//3==1 and j//3==1):
			            buttons[i][j] = Button(root, bg='#ffc0cb')
			            buttons[i][j].config(textvariable = btn_text , width = 5, height = 5)
			            buttons[i][j].grid(row = i, column = j)
			        elif(i//3==1 and j//3==2):
			            buttons[i][j] = Button(root, bg='#ff7b7b')
			            buttons[i][j].config(textvariable = btn_text , width = 5, height = 5)
			            buttons[i][j].grid(row = i, column = j)
			        elif(i//3==2 and j//3==0):
			            buttons[i][j] = Button(root, bg='#3b9e14')
			            buttons[i][j].config(textvariable = btn_text , width = 5, height = 5)
			            buttons[i][j].grid(row = i, column = j)
			        elif(i//3==2 and j//3==1):
			            buttons[i][j] = Button(root, bg='#e0115f')
			            buttons[i][j].config(textvariable = btn_text , width = 5, height = 5)
			            buttons[i][j].grid(row = i, column = j)
			        elif(i//3==2 and j//3==2):
			            buttons[i][j] = Button(root, bg='#2a9df4')
			            buttons[i][j].config(textvariable = btn_text , width = 5, height = 5)
			            buttons[i][j].grid(row = i, column = j)
			        
			root.mainloop()
		else:
			Tk().wm_withdraw() #to hide the main window
			messagebox.showinfo('Congratulations you have done','OK')



	def insert_item(self, position):
		pos_x, pos_y=position[1],position[0]
		print(pos_x, pos_y)
		while True:
			for event in pygame.event.get():
				print("")
				if event.type==pygame.QUIT:
					return
				if event.type==pygame.KEYDOWN:
					if (self.orginal_grid[(pos_x-1)][(pos_y-1)]!=0):						
						return 
					if (event.key==48):
						self.grid[pos_x-1][pos_y-1] = event.key - 48
						pygame.draw.rect(self.win, self.background_color, (position[0]*50 + self.buffer, position[1]*50+ self.buffer,50 -2*self.buffer , 50 - 2*self.buffer))
						pygame.display.update()
						return 
					if (0 < event.key - 48 <10):
						pygame.draw.rect(self.win, (0,255,0), (position[0]*50 + self.buffer, position[1]*50+self.buffer,50 -2* self.buffer , 50 - 2* self.buffer))
						value = self.font.render(str(event.key-48), True, (0,0,0))
						self.win.blit(value, (position[0]*50 +15, position[1]*50))
						self.grid[pos_x-1][pos_y-1] = event.key - 48
						pygame.display.update()
						return
					return

	def main(self):
		pygame.init()
		self.win=pygame.display.set_mode((self.height, self.width))
		pygame.display.set_caption("Sudoku Solver")
		self.win.fill(self.background_color)
		for i in range(10):
			if(i%3==0):
					pygame.draw.line(self.win,self.line_color,(50+50*i,50),(50+50*i,500),6)
					pygame.draw.line(self.win,self.line_color, (50,50+50*i),(500,50+50*i),6)
			pygame.draw.line(self.win,self.line_color,(50+50*i,50),(50+50*i,500),2)
			pygame.draw.line(self.win,self.line_color,(50,50+50*i),(500,50+50*i),2)
		pygame.display.update()

		for  x in  range(len(self.grid)):
			for y in  range(len(self.grid)):
				value=self.font.render(str(self.grid[x][y]), True, self.color)
				self.win.blit(value,((y+1)*50+12,(x+1)*50+12))
		pygame.display.update()

		text = self.font.render('Check' , True , (0,0,255))
		self.win.blit(text, (220,570))
		pygame.display.update()
		while True:
			for event in pygame.event.get():
				if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
					pos=pygame.mouse.get_pos()
					if(50<=pos[0]<=500 and 50<=pos[1]<=500):
						self.insert_item((pos[0]//50, pos[1]//50))
					elif (225<=pos[0]<=295 and 575<=pos[1]<=595):
						self.solve()
							
				if event.type==pygame.QUIT:
					pygame.quit()
					return

		
			pygame.display.update()		

clss=Sudoku(500,500)















