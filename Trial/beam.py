import numpy as np
import math

dof = []
noe = int (input("Input number of element(s) : "))
dof.append(noe)
non = int (input("Input number of nodal(s) : "))
dof.append(non)
print (dof)

cox = []
for i in range(non):
  x = float (input("Input x coordinate value of node " +str(i+1)+ " : "))
  cox.append(x)
print (cox)

E = []
I = []
question1 = str (input("Do all element(s) have same material properties? (Y/N) : "))
if question1 in ["Y","y"]:
  e = float (input("Input E value of all elements : "))
  inert = float (input("Input I value of all elements : "))
  for i in range (noe):
    E.append(e)
    I.append(inert)
elif question1 in ["N","n"]:
  for i in range(noe):
    e = float (input("Input E value of element " +str(i+1)+ " : "))
    E.append(e)
    inert = float (input("Input I value of element " +str(i+1)+ " : "))
    I.append(inert)
print(E, I)

length = []
initial = []
final = []
for i in range(noe):
    start = int (input("Input initial node for element " +str(i+1)+ " : "))
    initial.append(start)
    end = int (input("Input final node for element " +str(i+1)+ " : "))
    final.append(end)
    L = cox[i+1]-cox[i]
    length.append(L)
print (initial, final, length)

node_sup = []
type_sup = []
nos = int (input('Input number of support : '))
tos = ('F = Fixed','P = Pinned','R = Roller')
for i in range (nos):
    ns_pos = int (input('Select node position of support '+str(i+1)+' : '))
    node_sup.append(ns_pos)
    print (tos)
    stype = str (input('Select type of support '+str(i+1)+' : '))      
    type_sup.append(stype)

sms = []
k1 = []
for i in range (noe):
  j = length[i]
  kons = E[i]*I[i]/(j**3)
  sme = np.array([[12, 6*j, -12, 6*j],
                [6*j, 4*j**2, -6*j, 2*j**2],
                [-12, -6*j, 12, -6*j],
                [6*j, 2*j**2, -6*j, 4*j**2]])
  sm = kons*sme
  sms.append(sm)
  k1.append(kons)
  print ('Global stiffness matrix of element '+str(i+1)+' is :')
  print (sm)
a = np.zeros(((non*2),(non*2)))
for i in range(noe):
  a[2*i:2*i+4,2*i:2*i+4] = a[2*i:2*i+4,2*i:2*i+4] + sms[i]
tsm = a
print ('Stiffness matrix is :')
print (tsm)

node_load = []
dist_load = []
force_matrix0 = []
gforce_matrix0 = []
nol = int (input("Input number of load(s) : "))
for i in range(nol):
    question2 = str (input("Is the load " +str(i+1)+ " a distributed load? (Y/N) : "))
    if question2 in ["N","n"]:
        lm = np.zeros((non*2,1))
        ToL = ('1 = Vertical Deflection','2 = Moment')
        nl_pos = int(input('Select node position of load '+str(i+1)+' : '))
        node_load.append(nl_pos)
        print (ToL)
        loadtype = str (input('Select type of load '+str(i+1)+' : '))
        if loadtype in ['1']:
            magnitude = float(input('Input the magnitude of vertical deflection '+str(i+1)+' in force unit : '))
            print ('Magnitude of vertical deflection load '+str(i+1)+' is: ')
            print (magnitude)
            lm[nl_pos*2-2] = magnitude
        elif loadtype in ['2']:
            magnitude = float(input('Input the magnitude of moment '+str(i+1)+' in moment unit : '))
            print ('Magnitude of moment '+str(i+1)+' is: ')
            print (magnitude)
            lm[nl_pos*2-1] = magnitude
        print ('Load matrix is :')
        print (lm)
        gfm0 = lm
        gforce_matrix0.append(gfm0)
    elif question2 in ["Y","y"]:
        app_loadel = int (input("Which element is applied by distribute load " +str(i+1)+ " : "))
        o = app_loadel-1
        print ("1 = Rectangle, 2 = Right Triangle, 3 = Isosceles Triangle, 4 = Parabolic")
        question3 = str (input("Shape of distributed load : "))
        w = float (input("Input the magnitude of distributed load " +str(i+1)+ " in force/length unit : "))
        dist_load.append(w)
        if question3 in ["1"]:
            fm0 = np.array([[(-w*length[o])/2],
                            [(-w*length[o]**2)/12],
                            [(-w*length[o])/2],
                            [(w*length[o]**2)/12]]) 
            force_matrix0.append(fm0)
        elif question3 in ["2"]:
            question4 = str (input("Which side has greater load? (L/R) : "))
            if question4 in ["L","l"]:
                fm0 = np.array([[(-7*w*length[o])/20],
                                [(-w*length[o]**2)/20],
                                [(-3*w*length[o])/20],
                                [(w*length[o]**2)/30]])
            elif question4 in ["R","r"]:
                fm0 = np.array([[(-3*w*length[o])/20],
                                [(-w*length[o]**2)/30],
                                [(-7*w*length[o])/20],
                                [(w*length[o]**2)/20]])
            force_matrix0.append(fm0)
        elif question3 in ["3"]:
            fm0 = np.array([[(-w*length[o])/4],
                            [(-5*w*length[o]**2)/96],
                            [(-w*length[o])/4],
                            [(5*w*length[o]**2)/96]]) 
            force_matrix0.append(fm0)
        elif question3 in ["4"]:
            fm0 = np.array([[(-w*length[o])/3],
                            [(-w*length[o]**2)/15],
                            [(-w*length[o])/3],
                            [(w*length[o]**2)/15]]) 
            force_matrix0.append(fm0)
        pos1 = initial[o]*2
        pos2 = final[o]*2
        position = [pos1-1, pos1, pos2-1, pos2]
        gfm0 = np.zeros(((non*2),1))
        for j in range(4):
            p1 = position[j]-1
            gfm0[p1,0] = fm0[j,0]
        gforce_matrix0.append(gfm0)
print (np.around(force_matrix0,3))
print (np.around(gforce_matrix0,3))
print (" ")
tgfm0 = sum(gforce_matrix0)
print (np.around(tgfm0, 3))

lmv = np.zeros(((non*2),1))
lmv = np.asarray(lmv, dtype= str)
for i in range(non):
  lmv[0+i*2] = ('v'+str(i+1))
  lmv[1+i*2] = ('psi'+str(i+1))

tsms = tsm
lm1 = tgfm0
lmv1 = lmv
dimf = np.ones(((non*2),1))
for i in range(nos-1, -1, -1):
  if type_sup[i] in ['f','F']:
    tsms = np.delete(tsms, node_sup[i]*2-1, 0)
    tsms = np.delete(tsms, node_sup[i]*2-1, 1)
    lm1 = np.delete(lm1, node_sup[i]*2-1, 0)
    lmv1 = np.delete(lmv1, node_sup[i]*2-1, 0)
    tsms = np.delete(tsms, node_sup[i]*2-2, 0)
    tsms = np.delete(tsms, node_sup[i]*2-2, 1)
    lm1 = np.delete(lm1, node_sup[i]*2-2, 0)
    lmv1 = np.delete(lmv1, node_sup[i]*2-2, 0)
    dimf[node_sup[i]*2-1] = 0
    dimf[node_sup[i]*2-2] = 0
  elif type_sup[i] in ['R','r','P','p']:
    tsms = np.delete(tsms, node_sup[i]*2-2, 0)
    tsms = np.delete(tsms, node_sup[i]*2-2, 1)
    lm1 = np.delete(lm1, node_sup[i]*2-2, 0)
    lmv1 = np.delete(lmv1, node_sup[i]*2-2, 0)
    dimf[node_sup[i]*2-2] = 0

print ('Stiffness matrix (simplify) is : ')
print (tsms)
print ('Load matrix (simplify) is : ')
print (lm1)

dism = np.matmul(np.linalg.inv(tsms),lm1)
print ('Displacement Matrix is : ')
print (dism)
print ('where :')
print (lmv1)

for i in range(len(dism)):
  for j in range(non*2):
    if dimf[j] == 1:
      dimf[j] = dism[i]
      break
    else:
      dimf[j] = dimf[j]
print ('Total displacement matrix is :')
print (dimf)

fm = np.matmul(tsm,dimf)
print (fm)
fmz = fm-tgfm0
print (np.around(fmz,3))


