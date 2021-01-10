
import random,os,time
import pygame
# Константы
sun=1880 # также поменять на строке 169
ticks=0
time=(200,200,200)
root=pygame.display.set_mode((640,640),pygame.RESIZABLE)
size=4
# Углы поворота 45°
angles={0:[-1,-1],1:[-1,0],2:[-1,1],3:[0,1],4:[1,1],5:[1,0],6:[1,-1],7:[0,-1]}	

class Bot():
	def __init__(self,code:list,pos:list,type="none"):
		self.code=code
		self.pos=pos
		self.counter=0
		self.angle=0
		self.energy=200
		self.type=type
		self.killed=0
		if "inf" in self.type:
			self.energy=2**100
	def is_me(self,code):
		c=0
		for i in range(len(code)):
				if self.code[i]==code[i]:
					c+=1
		return c>len(code)-2
	def born(self):
		npos=[random.randint(-1,1),random.randint(-1,1)]
		code=self.code
		if random.randint(0,5)==5 and not "mutate" in self.type:
			code[random.randint(0,len(code)-1)]=random.randint(0,22)
		if pole[(self.pos[0]+npos[0])%len(pole)][(self.pos[1]+npos[0])%len(pole[0])]==0:
			pole[(self.pos[0]+npos[0])%len(pole)][(self.pos[1]+npos[1])%len(pole[0])]=Bot(code,[(self.pos[0]+npos[0])%len(pole),(self.pos[1]+npos[0])%len(pole[0])],type=self.type)
	def rotate(self,num):
		self.angle=(self.angle+num)%8
	def cycle(self):
		global pole
		self.energy-=10
		if self.energy<100:
			pole[self.pos[0]][self.pos[1]]=0
			return
		if self.energy>250 and not "alone" in self.type:
			self.energy-=200
			self.born()
		
		for cycle_count in range(300):
			i=self.code[self.counter%len(self.code)]
			self.counter%=len(self.code)
			# Фотосинтез
			if i==0:
				self.counter+=1
				self.energy+=sun/len(pole)*(len(pole)-self.pos[1])
				return 
			# Движение
			if i>0 and i<9:
				self.counter+=1
				moves={1:[-1,-1],2:[-1,0],3:[-1,1],4:[0,1],5:[1,1],6:[1,0],7:[1,-1],8:[0,-1]}		
			
				if pole[(self.pos[0]+moves[i][0])%len(pole)][(self.pos[1]+moves[i][1])%len(pole[0])]==0:
					pole[self.pos[0]][self.pos[1]]=0
					pole[(self.pos[0]+moves[i][0])%len(pole)][(self.pos[1]+moves[i][1])%len(pole[0])]=self
					self.pos=[(self.pos[0]+moves[i][0])%len(pole),(self.pos[1]+moves[i][1])%len(pole[0])]
					return
			# Кушать
			if i>8 and i<17:
				self.counter+=1
				moves={9:[-1,-1],10:[-1,0],11:[-1,1],12:[0,1],13:[1,1],14:[1,0],15:[1,-1],16:[0,-1]}		
				# Если там бот
				if pole[(self.pos[0]+moves[i][0])%len(pole)][(self.pos[1]+moves[i][1])%len(pole[0])]!=0:
					# Скушать
					self.energy+=pole[(self.pos[0]+moves[i][0])%len(pole)][(self.pos[1]+moves[i][1])%len(pole[0])].energy
					pole[(self.pos[0]+moves[i][0])%len(pole)][(self.pos[1]+moves[i][1])%len(pole[0])]=0
					self.killed+=1
				return
			if i==17:
				self.rotate(1)
				self.counter+=1
			if i==18:
				self.rotate(-1)
				self.counter+=1
			if i==19:
				# Перемещение относительно поворота
				self.counter+=1
				moves=angles[self.angle]
				if pole[(self.pos[0]+moves[0])%len(pole)][(self.pos[1]+moves[1])%len(pole[0])]==0:
					pole[self.pos[0]][self.pos[1]]=0
					pole[(self.pos[0]+moves[0])%len(pole)][(self.pos[1]+moves[1])%len(pole[0])]=self
					self.pos=[(self.pos[0]+moves[0])%len(pole),(self.pos[1]+moves[1])%len(pole[0])]
					return
			if i==20:
				moves=angles[self.angle]
				res=0
				if pole[(self.pos[0]+moves[0])%len(pole)][(self.pos[1]+moves[1])%len(pole[0])]==0:
					res=1
				else:
					if self.is_me(pole[(self.pos[0]+moves[0])%len(pole)][(self.pos[1]+moves[1])%len(pole[0])].code):
						res=2
					else:
						res=3
				self.counter=self.code[(self.counter+res)%len(self.code)]
			if i==21:
				# Кушать относительно угла поворота
				moves=angles[self.angle]
				self.counter+=1
	
				# Если там бот
				if pole[(self.pos[0]+moves[0])%len(pole)][(self.pos[1]+moves[1])%len(pole[0])]!=0:
					# Скушать
					self.energy+=pole[(self.pos[0]+moves[0])%len(pole)][(self.pos[1]+moves[1])%len(pole[0])].energy
					pole[(self.pos[0]+moves[0])%len(pole)][(self.pos[1]+moves[1])%len(pole[0])]=0
					self.killed+=1
				return
			if i==22:
				moves=angles[self.angle]
				counters=[0,0,0]
				for i in range(-1,1):
					for j in range(-1,1):
						if not i==0 and not j==0:
							if pole[(self.pos[0]+i)%len(pole)][(self.pos[1]+j)%len(pole[0])]==0:
								counters[0]+=1
							else:
								if self.is_me(pole[(self.pos[0]+i)%len(pole)][(self.pos[1]+j)%len(pole[0])].code):
									counters[1]+=1
								else:
									counters[2]+=1
				count=counters[self.code[(self.counter+1)%len(self.code)]%3]
				need=self.code[(self.counter+2)%len(self.code)]%9
				if count<need:
					self.counter=self.code[(self.counter+3)%len(self.code)]
				elif count==need:
					self.counter=self.code[(self.counter+4)%len(self.code)]
				else:
					self.counter=self.code[(self.counter+5)%len(self.code)]
pole=[[0 for i in range(200)] for i in range(200)]
#pole[1][5]=Bot([0,18,19],[1,5],type=["mutate"])
#pole[3][5]=Bot([0,18,22,1,8,8,0,0,18,20,14,8,13,21,19],[3,5],type=["mutate"])
#pole[1][3]=Bot([0,22,2,1,0,7,7,18,20,7,12,12,18,19],[1,3]),type=["mutate","alone"])
pole[2][3]=Bot([0,0,0,0,0,0,0,0,0,0,0,0,0,0],[2,3])
pygame.init()

while 1:
	root.fill(time)
	shtuka=200
	for i in range(len(pole)):
		for j in range(len(pole[i])):
			if pole[i][j]!=0:
					pygame.draw.rect(root,(bool(pole[i][j].killed)*255,pole[i][j].energy%256,0),[i*size,j*size,size,size])
	for i in pole:
		for j in i:
			if j!=0:
				j.cycle()
	ticks+=1
	if ticks%300==0:
		if time==(200,200,200):
			time=(0,0,0)
			sun=0
		else:
			time=(200,200,200)
			sun=1880
	bots=0
	traf=0
	also=0
	for i in pole:
		for j in i:
			if j!=0:
				bots+=1
				if j.killed==0:
					traf+=1
				else:
					also+=1
	root.blit(pygame.font.SysFont("sans", 20).render(str(bots)+' '+str(traf)+' '+str(also)+" "+str(pole[0][0].code if pole[0][0]!=0 else 0),1,(255,0,0)),[40,1200])
	pygame.display.update()