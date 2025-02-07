import numpy as np
# a = [['1','2','3'],['4','5','3'], ['7','8','3'],['9','10','3']]
# c = np.array(a)
# d = np.array([[11, 11,11],[0,0,0],[0,0,0],[0,0,0]])
# f = np.array([[]]).reshape(0,3)
# e = np.array([[]]).reshape(0,3)
# for row in range(len(c)):
#     e = np.concatenate((a[row][:1],d[row][1:]))
#     e = np.array([e])
#     #print(e)
#     f = np.concatenate((f,e[0:]))

# print(f)
# #b = np.array(b)

# a = []
# b = np.random.randint(0,10)
# while b in a:
#     b = np.random.randint(0,10)
# a.append(b)
# print(a)

a = {'a':1, 'b':3, 'c':2}
for key in a:
    print(key)