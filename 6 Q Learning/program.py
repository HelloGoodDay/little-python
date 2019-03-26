# -*- coding: utf-8 -*-
'''
USAGE
sumx -- length of window
sumy -- width of window
paint = Paint(sumx, sumy)
ql = QL(maze, sumx, sumy, cx[0], cy[0], cx[1], cy[1])
ql.training(paint)
    
paint.window.mainloop()
'''
'''
算法备注：
Q(s,a) = r + gamma*max(Q(s2,a2))
每走一步计数为-1

Q(s,a) = Q(s,a) + alpha*(r + gamma*max(Q(s2,a2)) - Q(s,a))
       = (1-alpha)*Q(s,a) + alpha*(r + gamma*max(Q(s2,a2)))
每走一步计数为0（设为-1时会出现有的全负）
'''
"""
Q learning
Q(s,a) = r + gamma( maxQ(s2, a2))
s -- current statement
a -- action based on s
s2-- changed statement after a
a2-- next action
r -- reward of a
gamma -- cost index， 牺牲当前利益换取长远利益的程度
"""

import numpy as np
import random
import time
from tkinter import *

'''
 windows paint
 ------------------------------------------------------------------------------
'''
class Paint:   
    def __init__(self,x, y):
        self.sleep_time = 0.2
        
        self.TRAP = -10
        self.TREATURE = 10
        self.WALK = 0
        self.x = x
        self.y = y
    
        self.width = 3   #size of dot
        self.linewidth = 1
        self.width1 = -1  #size of line
        
        self.window = Tk()
        self.window.title('MazeConfusion')
        self.window.resizable(0,0)
        
        # 添加画布，长度为5*5，每个格子为100像素
        self.canvas = Canvas(self.window, width=x * self.width, height=y * self.width)
        self.canvas.pack()
        # 设定画布的位置，这里设定为（0， 0）
        self.canvas.grid(row=0, column=0)
        # 添加search按钮
        #self.searchMapButton = Button(self.window,text = 'search')
        #self.searchMapButton.grid(row = 1,column = 0)
        # 添加画布，显示机器人的位置
        #robotView = Canvas(window,width=x * width, height=y * width)
        #robotView.grid(row = 0,column = 2)
    
    '''
    paint statement
    '''
    def Map(self, maze):
        width = self.width
        linewidth = self.linewidth
        for i in range(self.x):
            for j in range(self.y):
                if maze[j, i] == self.WALK:
                    self.canvas.create_rectangle(
                            i * width, j * width, (i + 1) * width, (j + 1) * width, fill='white', outline='gray', width=linewidth)
                elif maze[j, i] == self.TREATURE:
                    self.canvas.create_rectangle(
                            i * width, j * width, (i + 1) * width, (j + 1) * width, fill='blue', outline='blue', width=linewidth)
                elif maze[j, i] == self.TRAP:
                    self.canvas.create_rectangle(
                            i * width, j * width, (i + 1) * width, (j + 1) * width, fill='red', outline='gray', width=linewidth)
    def Robot(self, robotPos):
        width = self.width
        width1 = self.width1
        # 用圆形表示当前位置
        #print(robotPos)
        self.robot = self.canvas.create_oval((robotPos[0]-1)*width+width1,  (robotPos[1]-1)*width+width1, 
                                           (robotPos[0])*width-width1, (robotPos[1])*width-width1, fill='black')
    
    def move(self, robotPos):
        width = self.width
        width1 = self.width1
        self.canvas.coords(self.robot, (robotPos[0]-1)*width+width1, (robotPos[1]-1)*width+width1, 
                    (robotPos[0])*width-width1, (robotPos[1])*width-width1)
        self.canvas.update()
        time.sleep(self.sleep_time)




'''
 Q learning   
------------------------------------------------------------------------------- 
 attention:
     position of robot is begin as (1,1)
'''
class QL:  
    def __init__(self, maze, x, y, x0, y0, x1, y1):
        self.gamma = 0.7
        self.alpha = 0.8
        self.reach_reward = 10
        self.trainingtime = 30
        
        self.maze = maze
        self.x = x
        self.y = y
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.robotPos = (x0, y0)
    
        self.q_matrix = np.zeros((x*y, 5))

    
    def pos_init(self):
        self.robotPos = (self.x0, self.y0)
    
    '''
    # state, 1-up, 2-down, 3-left, 4-right, 5-wait 
    '''
    def get_valid_action(self,robotPos0):
        a = []
        if(robotPos0[1]>1):
            a.append(1)
        if(robotPos0[1]<self.y):
            a.append(2)
        if(robotPos0[0]>1):
            a.append(3)
        if(robotPos0[0]<self.x):
            a.append(4)
        a.append(5)
        
        if(robotPos0[0] < self.x1):
            a.append(4)
        if(robotPos0[0] > self.x1):
            a.append(3)
        if(robotPos0[1] < self.y1):
            a.append(2)
        if(robotPos0[1] > self.y1):
            a.append(1)
        return a
    
    '''
    get robot position after action
    return the next postion
    '''
    def get_next_state(self,action):
        robotPos = self.robotPos
        newx = robotPos[0]
        newy = robotPos[1]
        if action == 1:
            newy = newy - 1
        if action == 2:
            newy = newy + 1
        if action == 3:
            newx = newx - 1
        if action == 4:
            newx = newx + 1
        robotPos2 = (newx, newy)
        return robotPos2
    
    def get_reward(self,robotPos0):
        reward = self.maze[robotPos0[1]-1, robotPos0[0]-1]
        return reward
    
    def get_Q_index(self,pos):
        index = (pos[1]-1)*self.x + pos[0] - 1
        return index
    
    def if_reach(self):
        robotPos = self.robotPos
        if robotPos[0]<1 or robotPos[0]>self.x or robotPos[1]<1 or robotPos[1]>self.y:
            return False
            print("error!")
        if self.get_reward(robotPos) == self.reach_reward:
            return True
        else:
            return False


#Paint.Map(maze, x, y)
#Robot()
#canvas.update()

#sucs = 0
#fails = 0
#for j in range(300):    
 
    def training(self, paint = 1):
        if paint != 1:
             print("init pic")
             paint.Map(self.maze)
             paint.Robot(self.robotPos)
             paint.window.update()
        # Q training
        for i in range(self.trainingtime):
            self.pos_init()
            while self.if_reach() == False:
                valid_actions = self.get_valid_action(self.robotPos)
                action = random.choice(valid_actions)
                next_pos = self.get_next_state(action)
                
                valid_actions = self.get_valid_action(next_pos)
                future_rewards = []
                for next_action in valid_actions:
                    future_rewards.append( self.q_matrix[ self.get_Q_index(next_pos), 
                                                         next_action - 1] )
                #Q(s,a) = r + gamma*max(Q(s2,a2))
                q_state = self.get_reward(next_pos) + self.gamma*max(future_rewards)
                #Q(s,a) = Q(s,a) + alpha*(r + gamma*max(Q(s2,a2)) - Q(s,a))
                #       = (1-alpha)*Q(s,a) + alpha*(r + gamma*max(Q(s2,a2)))
                q_state = (1-self.alpha)*self.q_matrix[ self.get_Q_index(self.robotPos), 
                          action -1] + self.alpha*q_state
                
                self.q_matrix[ self.get_Q_index(self.robotPos), action -1] = q_state
                self.robotPos = next_pos
                
                #print(robotPos)
                if paint != 1:
                    paint.move(self.robotPos)
            
                
        print('Final Q-table:')
        print(self.q_matrix)        
        #time.sleep(2)
        
        # moving after training
        # paint robot
        steps = 0
        rewards = 0
        self.pos_init()
        if paint != 1:
            paint.move(self.robotPos)
        while self.if_reach() == False:
            next_Q_matrix = self.q_matrix[self.get_Q_index(self.robotPos), :]
            a = np.argwhere(next_Q_matrix == max(next_Q_matrix))
            # max action, chose randomly
            action = random.choice(a) + 1
            self.robotPos = self.get_next_state(action)
            
            if paint != 1:
                paint.move(self.robotPos)
            
            if(self.robotPos[0]<1 or self.robotPos[1]<1 or 
               self.robotPos[0]>self.y or self.robotPos[1]>self.x):
                return False

            steps = steps+1
            rewards = rewards + self.get_reward(self.robotPos)
            if self.get_reward(self.robotPos) < -1:
                return False
             
        print("made it! number of steps is %d, reward is %.1f" %(steps, rewards))
        
        if(rewards > 0 and steps == 4):
            return True
        
        
#print(q_matrix)  
#print("\n\n the total successful time is %d\n the failed time is %d\n\n" %(sucs, fails))
 
#end = datetime.datetime.now()
#print(end - begin)
#window.mainloop()







