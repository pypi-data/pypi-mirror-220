import numpy as np
import random
from tqdm import tqdm
from decimal import Decimal 

def d(x):
    return Decimal(x)

def dl(x):
    for i in x:
        i=Decimal(i)
    return x


def sig(x, activ):
    if activ== 'leaky relu':
        i=0
        L=[]
        while i<len(x):
            if float(x[i])<=0:
                L.append(0.01*x[i])
            if float(x[i])>0:
                L.append(x[i])
            i=i+1
    if activ== 'relu':
        i=0
        L=[]
        while i<len(x):
            if float(x[i])<=0:
                L.append(0.01*x[i])
            else:
                L.append(0)
    if activ== 'sigmoid':
        i=0
        L=[]
        while i<len(x):
            L.append(1/(1+(d(np.e**(-x[i])))))
            i=i+1
    if activ== 'tanh':
        i=0
        L=[]
        while i<len(x):
            A=d(np.e**(float(x[i])))
            B=d(np.e**(-float(x[i])))
            L.append(d((A-B)/(A+B)))
            i=i+1
    return np.array(L)

def sigp(x, activ):
    if activ== 'leaky relu':
        if x>0:
            X=1
        if x<=0:
            X=0.01
    if activ== 'relu':
        if x>0:
            X=1
        else:
            X=0
    if activ=='sigmoid':
        X= d((np.e**x)/((1+(np.e**(-x)))**2))
    if activ== 'tanh':
        A=d(np.e**x)
        B=d(np.e**(-x))
        X= d(1-((A-B)/(A+B))**2)
    return X

def im(x):
    i=0
    L=[]
    for i in range(len(x)):
        for j in range(len(x[i])):
            x[i][j] = float(x[i][j]) / 256
    return x

def neural_network(I, w, b, activ):
    F=[]
    for i in range (len(w)):
        
        L1=I.dot(w[i])+b[i]
        F.append(L1)
        L1=sig(L1, activ)
        F.append(L1)
        I=L1

    return F


def xavier(a, b):
    wx=[]
    v= np.sqrt(2/(a+b))
    for i in range(a):
        wy=[]
        for j in range(b):
            wy.append(random.normalvariate(0, v))
        wx.append(wy)
    return np.array(wx)

def xavier_innitialise(I, U, D, O):
    w=[]
    b=[]
    w.append(xavier(I, D))
    for i in range(U-1):
        w.append(xavier(D, D))
    w.append(xavier(D, O))

    for i in range (U):
        b.append(np.zeros(D))
    b.append(np.zeros(O))

    return [w, b]

def uniform_innitialise(I, U, D, O, a1, a2):
    w=[]
    b=[]
    w1=[]
    for i in range(I):
        wx=[]
        for j in range(D):
            wx.append(random.uniform(a1, a2))
        w1.append(wx)
    w.append(np.array(w1))

    for k in range(U-1):
        wx=[]
        for i in range(D):
            wy=[]
            for j in range(D):
                wy.append(random.uniform(a1, a2))
            wx.append(wy)
        w.append(np.array(wx))
    
    wf=[]

    for i in range(D):
        wx=[]
        for j in range(O):
            wx.append(random.uniform(a1,a2))
        wf.append(wx)
    
    w.append(np.array(wf))

    for i in range (U):
        b.append(np.zeros(D))
    b.append(np.zeros(O))

    return [w, b]

def normal_innitialise(I, U, D, O, mu, sd):
    w=[]
    b=[]
    w1=[]
    for i in range(I):
        wx=[]
        for j in range(D):
            wx.append(random.normalvariate(mu, sd))
        w1.append(wx)
    w.append(np.array(w1))

    for k in range(U-1):
        wx=[]
        for i in range(D):
            wy=[]
            for j in range(D):
                wy.append(random.normalvariate(mu, sd))
            wx.append(wy)
        w.append(np.array(wx))
    
    wf=[]

    for i in range(D):
        wx=[]
        for j in range(O):
            wx.append(random.normalvariate(mu, sd))
        wf.append(wx)
    
    w.append(np.array(wf))

    for i in range (U):
        b.append(np.zeros(D))
    b.append(np.zeros(O))

    return [w, b]


def cost(I, w, b, A, activ):
    
    L=[]
    for i in range(len(I)):
        X= neural_network(I[i], w, b, activ)[7]-A[i]
        for j in range(len(A[0])):
            L.append((X[j])**2)
    return (sum(L)/len(I))   


def grad(I, w, b, A, activ):

    U=len(w)-1

    O=len(A[0])

    D= len(w[1][0])

    F=[]
    for i in range(len(I)):
        F.append(neural_network(I[i], w, b, activ))
    L=[]
    for i in range(len(I)):
        x=[]
        X= F[i][2*U+1]-A[i]
        for j in range(O):
            x.append((X[j]))
        L.append(x)

    GW=[]
    GB=[]
    AGI=[]

    GWF=[]
    for k in range(D):
        GWFB= []
        for j in range(len(A[0])):
            S1=[]
            for i in range(len(I)):
                S1.append(d(2*L[i][j]*sigp(F[i][2*U][j], activ)*F[i][2*U-1][k]))
            GWFB.append(sum(S1)/len(I))
        GWF.append(GWFB)
    GWF= np.array(GWF)
    GBF=[]
    for j in range(O):
        S1=[]
        for i in range(len(I)):
            S1.append(d(2*L[i][j]*sigp(F[i][2*U][j], activ)))
        GBF.append(sum(S1)/len(I))
    GBF= np.array(GBF)
    GIF=[]
    AGIF=[]
    for k in range(D):
        S1=[]
        for i in range(len(I)):
            S2=[]
            for j in range(O):
                S2.append(d(2*L[i][j]*sigp(F[i][2*U][j], activ)*w[U][k][j]))
            S1.append(sum(S2))
        AGIF.append(S1)
        GIF.append(sum(S1)/len(I))
    GIF= np.array(GIF)

    GW.insert(0, GWF)
    GB.insert(0, GBF)
    AGI.insert(0, AGIF)

    for y in range(U-1):
        GWx=[]
        GBx=[]
        T1=[]
        for k in range(D):
            S1=[]
            for j in range(D):
                S2=[]
                for i in range(len(I)):
                    S2.append(d(AGI[0][k][i]*sigp(F[i][2*U-2-2*y][k], activ)*F[i][2*U-3-2*y][j]))
                S1.append(sum(S2)/len(I))
            T1.append(S1)
        
        for k in range (D):
            T2=[]
            for j in range (D):
                T2.append(T1[j][k])
            GWx.append(T2)
        GWx= np.array(GWx)
        for k in range(D):
            S2=[]
            for i in range(len(I)):
                S2.append(d(AGI[0][k][i]*sigp(F[i][2*U-2-2*y][k], activ)))
            GBx.append(sum(S2)/len(I))
        GBx= np.array(GBx)
        GIx=[]
        AGIx=[]
        for k in range(D):
            S1=[]
            for i in range(len(I)):
                S2=[]
                for j in range(D):
                    S2.append(d(AGI[0][j][i]*sigp(F[i][2*U-2-2*y][j], activ)*w[U-y-1][k][j]))
                S1.append(sum(S2))
            AGIx.append(S1)
            GIx.append(sum(S1)/len(I))
        GIx= np.array(GIx)

        GW.insert(0, GWx)
        GB.insert(0, GBx)
        AGI.insert(0, AGIx)
    
    GW1=[]
    GB1=[]
    T1=[]
    for k in range(D):
        S1=[]
        for j in range(len(I[0])):
            S2=[]
            for i in range(len(I)):
                S2.append(d(AGI[0][k][i]*sigp(F[i][0][k], activ)*I[i][j]))
            S1.append(sum(S2)/len(I))
        T1.append(S1)
    
    for k in range (len(I[0])):
        T2=[]
        for j in range (D):
            T2.append(T1[j][k])
        GW1.append(T2)
    GW1= np.array(GW1)
    for k in range(D):
        S2=[]
        for i in range(len(I)):
            S2.append(d(AGI[0][k][i]*sigp(F[i][0][k], activ)))
        GB1.append(sum(S2)/len(I))
    GB1= np.array(GB1)

    GW.insert(0, GW1)
    GB.insert(0, GB1)
    
    GRAD= [GW, GB]
    return GRAD





def train(I, w, b, A, Ns, h, T, activ):

    for i in tqdm(range(T)):
        
        

        L=[]
        for i1 in range(Ns):
            L.append(random.randint(0, len(I)-1))
        Is=[]
        for i2 in range(Ns):
            Is.append(I[L[i2]])
        Is=np.array(Is)

        ACs=[]

        for l in range(Ns):
            ACs.append(A[L[l]])
        ACs= np.array(ACs)

        X=grad(Is, w, b, ACs, activ)

        for i3 in range(len(w)):
            for j in range (len(w[i3])):
                for k in range(len(w[i3][0])):
                    w[i3][j][k]=d(w[i3][j][k])-h*d(X[0][i3][j][k])
        

        for i4 in range(len(b)):
            for j in range(len(b[i4])):
                b[i4][j]=d(b[i4][j])-h*d(X[1][i4][j])

    return [w, b]
