# -*- coding: utf-8 -*-
"""
Created on Fri Jan 26 21:44:46 2018

@author: ThinkPad
"""

import numpy as np
import datetime
from program import *

begin = datetime.datetime.now()

maze = np.array([[ -0, -10, -10,  -0], 
                 [ -0,  -0,  -0, -10],
                 [ -0,  -0,  10, -10],
                 [ -0,  -0,  -0,  -0],
                 [ -0, -10,  -0,  -0]])
x = 4
y = 5
x0 = 1
y0 = 1

ql = QL(maze, x, y, x0, y0)


paint = Paint(x, y)
sucs = 0
fails = 0


for i in range(30):
    if ql.training(paint):
        sucs = sucs + 1
    else:
        fails = fails + 1
        
print("\n\n the total successful time is %d\n the failed time is %d\n\n" %(sucs, fails))

end = datetime.datetime.now()
print(end - begin)

paint.window.destroy()
paint.window.mainloop()

















