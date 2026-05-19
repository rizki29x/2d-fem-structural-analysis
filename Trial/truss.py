import numpy as np
import math

dof = []
noe = int (input("Input number of element : "))
dof.append(noe)
non = int (input("Input number of nodal : "))
dof.append(non)
m = noe*non

cox = []
coy = []
for i in range(non):
  x = float (input("Input x coordinate value of node " +str(i+1)+ " : "))
  cox.append(x)
  y = float (input("Input y coordinate value of node " +str(i+1)+ " : "))
  coy.append(y)
print (cox, coy)

E = []
A = []
question1 = str (input("Do all elements have the same material properties? (Y/N) : "))
if question1 in ["Y","y"]:
  e = float (input("Input E value of all elements : "))
  a = float (input("Input A value of all elements : "))
  for i in range (noe):
    E.append(e)
    A.append(a)
elif question1 in ["N","n"]:
  for i in range(noe):
    e = float (input("Input E value of element " +str(i+1)+ " : "))
    E.append(e)
    a = float (input("Input A value of element " +str(i+1)+ " : "))
    A.append(a)
print(E, A)

initial = []
final = []
length = []
cons = []
sinels = []
cosels = []
for i in range(noe):
  start = int (input("Input initial node for element " +str(i+1)+ " : "))
  initial.append(start)
  end = int (input("Input final node for element " +str(i+1)+ " : "))
  final.append(end)

  x1 = cox [start-1]
  x2 = cox [end-1]
  y1 = coy [start-1]
  y2 = coy [end-1]

  L = math.sqrt((x2-x1)**2+(y2-y1)**2)
  con = A[i]*E[i]/L
  sinel = (y2-y1)/L
  cosel = (x2-x1)/L
  length.append(L)
  cons.append(con)
  sinels.append(sinel)
  cosels.append(cosel)
print (initial, final, length, cons, sinels, cosels)


node_sup = []
type_sup = []
nos = int (input("Input number of support : "))
tos = ('F = Fixed','P = Pinned','R = Roller')
for i in range(nos):
  ns_pos = int (input('Select node position of support '+str(i+1)+' : '))
  node_sup.append(ns_pos)
  print (tos)
  stype = str (input('Select type of support '+str(i+1)+' : '))      
  type_sup.append(stype)
print (node_sup, type_sup)

load_matrix = np.zeros((non*2,1))
print (load_matrix)
node_load = []
nol = int (input('Input number of load : '))
tol = ('1 = Vertical load','2 = horizontal load')
for i in range(nol):
  nl_pos = int(input('Select node position of load '+str(i+1)+' : '))
  node_load.append(nl_pos)
  print (tol)
  loadtype = str (input('Select type of load '+str(i+1)+' : '))
  if loadtype in ["1"]:
     magnitude = float(input('Input the magnitude of vertical load '+str(i+1)+' in force unit : '))
     print ('Magnitude of vertical deflection load '+str(i+1)+' is: ')
     print (magnitude)
     load_matrix[nl_pos*2-1] = magnitude
  elif loadtype in ['2']:
      magnitude = float(input('Input the magnitude of horizontal load '+str(i+1)+' in moment unit : '))
      print ('Magnitude of horizontal load '+str(i+1)+' is: ')
      print (magnitude)
      load_matrix[nl_pos*2-2] = magnitude
print (load_matrix)


lmv = np.zeros((non*2,1))
lmv = np.asarray(lmv, dtype= str)
for i in range(non):
  lmv[0+i*2] = ('u'+str(i+1))
  lmv[1+i*2] = ('v'+str(i+1))
print (lmv)

# esms = Element Stiffness Matrix
# gsms = Global Stiffness Matrix
esms = []
gsms = []
for i in range(noe):
    ss = sinels[i]**2
    cc = cosels[i]**2
    cs = sinels[i]*cosels[i]
    esm = cons[i]*np.array([[cc, cs, -cc, -cs],
                            [cs, ss, -cs, -ss],
                            [-cc, -cs, cc, cs],
                            [-cs, -ss, cs, ss]])
    esms.append(esm)
    print ('Element stiffness matrix of element '+str(i+1)+' : ')
    print (np.around(esm, 3))
    pos1 = initial[i]*2
    pos2 = final[i]*2
    position = [pos1-1, pos1, pos2-1, pos2]
    gsm = np.zeros(((non*2),(non*2)))
    for j in range(4):
      for k in range(4):
        p1 = position[j]-1
        p2 = position[k]-1
        gsm[p1,p2] = esm[j,k]
    gsms.append(gsm)
    print ('Global stiffness matrix of element '+str(i+1)+' : ')
    print (np.around(gsm, 3))
    
tgsm = sum(gsms)
print ('Total global stiffness matrix is :')
print (np.around(tgsm, 3))

tsms = tgsm
lm1 = load_matrix
lmv1 = lmv
dimf = np.ones(((non*2),1))
for i in range(nos-1, -1, -1):
  if type_sup[i] in ['f','F','P','p']:
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
  elif type_sup[i] in ['R','r']:
    tsms = np.delete(tsms, node_sup[i]*2-1, 0)
    tsms = np.delete(tsms, node_sup[i]*2-1, 1)
    lm1 = np.delete(lm1, node_sup[i]*2-1, 0)
    lmv1 = np.delete(lmv1, node_sup[i]*2-1, 0)
    dimf[node_sup[i]*2-1] = 0

print ('Stiffness matrix (simplify) is : ')
print (np.around(tsms,3))
print ('Load matrix (simplify) is : ')
print (lm1)
print (lmv1)

tsms_invers = np.linalg.inv(np.around(tsms,3))
dism = np.matmul(tsms_invers, lm1)
print ('Displacement Matrix is : ')
print (dism)
print ('where :')
print (lmv1)
print (len(dism))
for i in range(len(dism)):
  for j in range(non*2):
    if dimf[j] == 1:
      dimf[j] = dism[i]
      break
    else:
      dimf[j] = dimf[j]
print ('Total displacement matrix is :')
print (dimf)

edms = []
see = []
for i in range(noe):
  c = cosels[i]
  s = sinels[i]
  con2 = (cons[i]/A[i])* np.array([-c, -s, c, s])
  pos1 = initial[i]*2-1
  pos2 = final[i]*2-1
  position = [pos1-1, pos1, pos2-1, pos2]
  edm = np.zeros((4,1))
  for j in range(4):
    p1 = position[j]
    edm[j,0] = dimf[p1,0]
  soe = np.matmul(con2, edm) 
  edms.append(edm)
  print ('Displacement matrix of element '+str(i+1)+' :')
  print (edm)
  print ('Stress of element '+str(i+1)+' =', soe)