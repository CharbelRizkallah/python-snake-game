from tkinter import *
import random
import time

root = Tk()
root.title("Snake")
root.resizable(0,0)
wdth = 600
hgth = 600

size = 25

rows = int(hgth/size)
cols = int(wdth/size)

#game score
score = 0
header = Canvas(root,height=50,width=wdth)
header.pack()
Scores = header.create_text(wdth/2,25,text=str(score),font = 20)

canvas = Canvas(root,width=size * cols ,height=size * rows,bd=0,highlightthickness=0)
canvas.pack()
root.update()
color = "black"
headcolor = "green"
snakecolor = "lime"
foodcolor = "red"
ongoing = True

#making the grid
grid = []
for i in range(rows):
    grid.append([])

for i in range(rows):
    for j in range(cols):
        grid[i].append(j)
        grid[i][j] = 0

#drawing the canvas
for i in range(rows):
    for j in range(cols):
        grid[i][j] = canvas.create_rectangle(j*size,i*size,j*size+size,i*size+size,fill=color,outline = color)


#head of the snake
class Head:
    x = 0
    y = 0

    def __init__(self,canvas,color):

        pos = canvas.coords(grid[0][0])
        self.canvas = canvas
        self.color = color
        self.id = canvas.create_rectangle(pos[0],pos[1],pos[2],pos[3],fill = self.color,outline = self.color)
        self.dx = 1
        self.dy = 0
        root.bind("<KeyPress-Left>",self.move_left)
        root.bind("<KeyPress-Right>",self.move_right)
        root.bind("<KeyPress-Up>",self.move_up)
        root.bind("<KeyPress-Down>",self.move_down)
        self.old = canvas.coords(self.id)

    def get_grid(self):
        for i in range(rows):
            for j in range(cols):
                pos = canvas.coords(grid[i][j])
                bpos = canvas.coords(self.id)
                if pos[0] == bpos[0] and pos[1] == bpos[1] and pos[2] == bpos[2] and pos[3] == bpos[3]:
                    global x
                    global y
                    x = j
                    y = i

    def draw(self):
        global y
        global x

        self.get_grid()
        if y + self.dy < 0 :
            y = rows
        if y + self.dy == rows:
            y = -1
        if x + self.dx < 0 :
            x = cols
        if x + self.dx == cols:
            x = -1

        self.old = canvas.coords(self.id)

        pos = canvas.coords(grid[y+self.dy][x+self.dx])
        canvas.delete(self.id)
        self.id = canvas.create_rectangle(pos[0],pos[1],pos[2],pos[3],fill = self.color,outline = self.color)


    def move_left(self,evt):
        if self.dx != 1:
            self.dx = -1
            self.dy = 0
        
    
    def move_right(self,evt):
        if self.dx != -1:
            self.dx = +1
            self.dy = 0
    
    def move_up(self,evt):
        if self.dy != 1:
            self.dy = -1
            self.dx = 0
    
    def move_down(self,evt):
        if self.dy != -1:
            self.dy = +1
            self.dx = 0

head = Head(canvas,headcolor)

#making the tail
class Tail:
    def __init__(self,canvas,color,head):

        self.canvas = canvas
        self.color = color
        self.head = head
        self.id = canvas.create_rectangle(self.head.old[0],self.head.old[1],self.head.old[2],self.head.old[3],fill = self.color,outline = self.color)
        self.old = canvas.coords(self.id)

    
    def draw(self):
        self.old = canvas.coords(self.id)
        canvas.delete(self.id)
        self.id = canvas.create_rectangle(self.head.old[0],self.head.old[1],self.head.old[2],self.head.old[3],fill = self.color,outline = self.color)
        for t in tail:
            tpos = canvas.coords(t.id)
            hpos = canvas.coords(head.id)
            if hpos[0] == tpos[0] and hpos[1] == tpos[1] and hpos[2] == tpos[2] and hpos[3] == tpos[3]:
                global ongoing
                ongoing = False



tail = []
first = Tail(canvas,snakecolor,head)
tail.append(first)
s = 0

#making the food
class Food:
    correct = True
    stop = False
    
    def __init__(self,canvas,color,head):
        self.canvas = canvas
        self.color = color
        self.head = head

        while self.correct:
            y = random.randint(0,rows-1)
            x = random.randint(0,cols-1)
            pos = canvas.coords(grid[y][x])
            for t in tail:
                tpos = canvas.coords(t.id)
                if pos[0] == tpos[0] and pos[1] == tpos[1] and pos[2] == tpos[2] and pos[3] == tpos[3]:
                    self.stop = True
            if self.stop != True:
                hpos = canvas.coords(self.head.id)
                if pos[0] != hpos[0] or pos[1] != hpos[1] or pos[2] != hpos[2] or pos[3] != hpos[3]:
                    self.correct = False



        self.id = canvas.create_oval(pos[0],pos[1],pos[2],pos[3],fill=self.color)
        self.created = True

    def draw(self):
        global score
        global Scores

        if self.created != True:
            self.correct = True
            while self.correct:
                y = random.randint(0,rows-1)
                x = random.randint(0,cols-1)
                pos = canvas.coords(grid[y][x])
                for t in tail:
                    tpos = canvas.coords(t.id)
                    if pos[0] == tpos[0] and pos[1] == tpos[1] and pos[2] == tpos[2] and pos[3] == tpos[3]:
                        self.stop = True
                if self.stop != True:
                    hpos = canvas.coords(self.head.id)
                    if pos[0] != hpos[0] or pos[1] != hpos[1] or pos[2] != hpos[2] or pos[3] != hpos[3]:
                        self.correct = False
            self.id = canvas.create_oval(pos[0],pos[1],pos[2],pos[3],fill=self.color)
            self.created = True
        
        fpos = canvas.coords(self.id)
        hhpos = canvas.coords(self.head.id)

        if fpos[0] == hhpos[0] and fpos[1] == hhpos[1] and fpos[2] == hhpos[2] and fpos[3] == hhpos[3]:
            global s
            canvas.delete(self.id)
            self.created = False
            score += 10 
            header.delete(Scores)
            Scores = header.create_text(wdth/2,25,text=str(score),font = 20)
            add = Tail(canvas,snakecolor,tail[s])
            s += 1
            tail.append(add)


food = Food(canvas,foodcolor,head)




while ongoing:
    head.draw()
    for t in tail:
        t.draw()
    food.draw()
    root.update_idletasks()
    root.update()
    time.sleep(0.1)

print(tail.count)

root.mainloop()
