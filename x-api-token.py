# -*- coding:UTF-8 -*-

import math,random

e=list(map(lambda _:math.floor(62*random.random())+0,range(16)))
u="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

t=''.join(map(lambda y:u[y],e))

n2=[578, 573, 567, 560, 535, 564, 531, 559, 549, 568, 568, 536, 555, 527, 583, 586]

n=map(lambda x:x-526,n2)
e2=map(lambda x,y:x+e[y],n,range(16))
m = ''.join(map(lambda x:u[x%62],e2))
print(t+m)
