import math
import numpy as np
np.set_printoptions (9, suppress=True)

NoE = int (input('Number of Element '))
NoN = int (input('Number of Nodal '))
DoF = NoE*NoN

Cox = []
Coz = []
for i in range (NoN):
    x = float (input('Input x coordinate value of nodal '+str(i+1)+' in meter '))
    z = float (input('Input z coordinate value of nodal '+str(i+1)+' in meter '))
    Cox.append(x)
    Coz.append(z)

print ('Cox : ')
print (Cox)
print ('CoZ : ')
print (Coz)

E = []
G = []
I = []
J = []
mp = str (input('Do all element have same material properties? (Y/N) '))
if mp in ['n','N']:
    for i in range (NoE):
        em = float (input('Input the value of elasticity modulus of element '+str(i+1)+' in Pascal '))
        sm = float (input('Input the value of shear modulus of element '+str(i+1)+' in Pascal '))
        planar_i = float (input('Input the value of planar inertia of element '+str(i+1)+' in m^4 '))
        polar_i = float (input('Input the value of polar inertia of element '+str(i+1)+' in m^4 '))
        E.append (em)
        G.append (sm)
        I.append (planar_i)
        J.append (polar_i)
elif mp in ['y','Y']:
    em = float (input('Input the value of elasticity modulus of all element in Pascal '))
    sm = float (input('Input the value of shear modulus of all element in Pascal '))
    planar_i = float (input('Input the value of planar inertia of all element in m^4 '))
    polar_i = float (input('Input the value of polar inertia of all element in m^4 '))
    for i in range (NoE):
        E.append (em)
        G.append (sm)
        I.append (planar_i)
        J.append (polar_i)

Initial = []
Last = []
Length = []
kons1 = []
kons2 = []
kons3 = []
kons4 = []
kons5 = []
Sinel = []
Cosel = []
for i in range (NoE):
    a = int (input('Input initial node for element '+str(i+1)+': '))
    Initial.append (a)
    u = int (input('Input final node for element '+str(i+1)+': '))
    Last.append (u)

    x1 = Cox [a-1]
    z1 = Coz [a-1]
    x2 = Cox [u-1]
    z2 = Coz [u-1]

    L = math.sqrt((x2-x1)**2 + (z2-z1)**2)
    kon1 = (12*E[i]*I[i]/(L**3))
    kon2 = (6*E[i]*I[i]/(L**2))
    kon3 = (G[i]*J[i]/L)
    kon4 = (4*E[i]*I[i]/L)
    kon5 = (2*E[i]*I[i]/L)
    sin = (z2-z1)/L
    cos = (x2-x1)/L

    Length.append (L)
    kons1.append (kon1)
    kons2.append (kon2)
    kons3.append (kon3)
    kons4.append (kon4)
    kons5.append (kon5)
    Sinel.append (sin)
    Cosel.append (cos)

    print ('Length of element '+str(i+1)+' (in meter) : ')
    print (L)
    print ()
    print ('12EI/L^3 of element '+str(i+1)+' : ')
    print (kon1)
    print ()
    print ('6EI/L^2 of element '+str(i+1)+' : ')
    print (kon2)
    print ()
    print ('GJ/L of element '+str(i+1)+' : ')
    print (kon3)
    print ()
    print ('4EI/L of element '+str(i+1)+' : ')
    print (kon4)
    print ()
    print ('2EI/L of element '+str(i+1)+' : ')
    print (kon5)
    print ()
    print ('Sin of element '+str(i+1)+' : ')
    print (sin)
    print ()
    print ('Cos of element '+str(i+1)+' : ')
    print (cos)
    print ()

node_os = []
NoS = int (input('Input number of support : '))
ToS = ('F = Fixed','P = Pinned','R = Roller')
for i in range (NoS):
    ns_pos = int (input('Select node position of support '+str(i+1)+' : '))
    node_os.append(ns_pos)
   
lm = np.zeros((NoN*3,1))
node_ol = []
NoL = int(input('Input number of load : '))
ToL = ('1 = Vertical Deflection','2 = Bending Rotation','3 = Torsional Rotation')
for i in range (NoL):
    nl_pos = int(input('Select node position of load '+str(i+1)+' : '))
    node_ol.append(nl_pos)
    print (ToL)
    loadtype = str (input('Input type of load '+str(i+1)+' : '))
    if loadtype in ['1']:
        magnitude = float(input('Input the magnitude of vertical deflection '+str(i+1)+' in N : '))
        print ('Magnitude of vertical deflection of load '+str(i+1)+' is: ')
        print (magnitude)
        lm[nl_pos*3-3] = magnitude
    elif loadtype in ['2']:
        magnitude = float(input('Input the magnitude of bending rotation '+str(i+1)+' in Nm : '))
        print ('Magnitude of bending rotation of load '+str(i+1)+' is: ')
        print (magnitude)
        lm[nl_pos*3-3] = magnitude
    elif loadtype in ['3']:
        magnitude = float(input('Input the magnitude of torsional rotation '+str(i+1)+' in Nm : '))
        print ('Magnitude of torsional rotation of load '+str(i+1)+' is: ')
        print (magnitude)
        lm[nl_pos*3-3] = magnitude
print ('Load matrix is :')
print (lm)

Tgls = []
kgls = []
kgs = []
Tglts = []
kglts = []
kgts = []
for i in range (NoE):
    S = Sinel[i]
    C = Cosel[i]
    Tgl = np.array ([[1, 0, 0, 0, 0, 0],
                    [0, C, S, 0, 0, 0],
                    [0, -S, C, 0, 0, 0],
                    [0, 0, 0, 1, 0, 0],
                    [0, 0, 0, 0, C, S],
                    [0, 0, 0, 0, -S, C]])
    kgl = np.array ([[kons1[i],0,kons2[i],-kons1[i],0,kons2[i]],
                    [0,kons3[i],0,0,-kons3[i],0],
                    [kons2[i],0,kons4[i],-kons2[i],0,kons5[i]],
                    [-kons1[i],0,-kons2[i],kons1[i],0,-kons2[i]],
                    [0,-kons3[i],0,0,kons3[i],0],
                    [kons2[i],0,kons5[i],-kons2[i],0,kons4[i]]])
    Tgls.append(Tgl)
    kgls.append(kgl)
    o1 = Tgl.transpose()
    o2 = np.matmul(o1,kgl)
    kg = np.matmul(o2,Tgl)
    kgs.append(kg)
    if Last[i] in node_os:
        Tglt= Tgl[:3,:3]
        kglt= kgl[:3,:3]
        kgt = kg[:3,:3]
    elif Initial[i] in node_os:
        Tglt= Tgl[3:6,3:6]
        kglt= kgl[3:6,3:6]
        kgt = kg[3:6,3:6]
    Tglts.append(Tglt)
    kglts.append(kglt)
    kgts.append(kgt)
    print ('The transformation matrix relating local to global degrees of freedom for element '+str(i+1)+' is : ')
    print (Tglt)
    print ('Local stiffness matrix of element '+str(i+1)+' is ')
    print (kglt)
    print ('Global stiffness matrix of element '+str(i+1)+' is ')
    print (kgt)

Kg = np.sum(kgts, axis=0)
print ('Total global stiffness matrix is :')
print (Kg)

def get_lmf(input):
    for i in range(int(len(input)/3)):
        if input[i*3] != 0:
            return input[i*3:(i+1)*3]
tlef = get_lmf(lm)
print ('Total Local element forces is :')
print (tlef)

d = np.matmul(np.linalg.inv(Kg),tlef) 
dl = np.zeros((NoN*3,1))
for i in range(NoL): 
    dl[(node_ol[i]-1)*3:(node_ol[i]-1)*3+3] = d
print ('Total local element displacement is : ')
print (d)

dlts = []
lefs = []
for i in range(NoE):
    a1 = Initial[i]*3-3
    a2 = Initial[i]*3-2
    a3 = Initial[i]*3-1
    a4 = Last[i]*3-3
    a5 = Last[i]*3-2
    a6 = Last[i]*3-1
    dlt = dl[[a1,a2,a3,a4,a5,a6],:]
    dlts.append(dlt)
    print ('Local element displacement for element '+str(i+1)+' is : ')
    print (dlt)
    t1 = np.matmul(Tgls[i],dlt)
    lef = np.matmul(kgls[i],t1)
    lefs.append(lef)
    print ('Local element forces for element '+str(i+1)+' is : ')
    print (lef)

b1s = []
lefts = []
gnfs = []
for i in range(NoE):
    b1 = Tglts[i].transpose()
    b1s.append(b1)
    lef1 = lefs[i]
    if Last[i] in node_ol:
        left = lef1[3:,:]
    elif Initial[i] in node_ol:
        left = lef1[:3,:]
    lefts.append(left)
    gnf = np.matmul(b1,left)
    gnfs.append(gnf)
    print ('The global-coordinate force and moments for element '+str(i+1)+' is :')
    print (gnf)

fam = tlef-np.cumsum(gnfs, axis=0)[-1]
print ('Force and moment equilibrium are verified as follows : ')
print (fam)