#AAH extended
import random
import numpy as np
import matplotlib.pyplot as plt
import scipy
import scipy.linalg as la
import math,cmath
from scipy.sparse import diags
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["Times New Roman"]

SMALL_SIZE = 25
MEDIUM_SIZE = 25
BIGGER_SIZE = 25

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)
#Creating the spectral density matrix
n=20;#laatice sites
no=10;#bath lattice point
b = (1+np.sqrt(5))/2
sitegammaindx = [0, n-1, no-1]
sitegammastrn0 = [1.0,1.0,0.0]
sitegammastrnlow = [1.0,1.0,0.1]
sitegamaastrnhigher = [1.0,1.0,0.5]
sitegammastrn = [1.0, 1.0, 1.0]
arrayofsitegamstrn = [sitegammastrn0, sitegammastrnlow, sitegamaastrnhigher, sitegammastrn]
to = 3.0 #bath tunneling potential
t = 1.0 #system hopping
lamba = 0.5
alpha = 0.0
#sitepotential = 0.0;#bath site potential(constant)
siteindx = np.array(range(1, n))
sitepotentialAAH = 2*lamba*np.cos(2*np.pi*b*(siteindx))/(1+alpha*np.cos(2*np.pi*b*(siteindx)))
diagonals = [sitepotentialAAH,t*np.ones(n-1), t*np.ones(n-1)]
offset = [0,-1,1]
sys_Ham = diags(diagonals,offset,dtype='complex_').toarray()
print(sys_Ham)
eigvals, eigvecs = la.eig(sys_Ham)
energyval = (eigvals.real)
print(energyval)
def Rand(start, end, num):
    res = []
 
    for j in range(num):
        res.append(random.uniform(start, end))
 
    return res
def rnger(number,epsion):
    mat = []
    mat.append(number + epsion)
    mat.append(number - epsion)
    return mat
def makeeigran(eigvals, epsion, number):
    temp = []
    mat = []
    for i in range(len(eigvals)):
        temp.append(Rand(rnger(eigvals[i],epsion)[0],rnger(eigvals[i],epsion)[1],number))
    for k in range(len(eigvals)):
        for l in range(number):
            mat.append(temp[k][l])
    
    return mat
def makelist(pointer):
    moin = []
    for i in range(len(pointer)):
        moin.append(pointer[i])
    return moin
def selfenergy(gamma,energy):
    mat = ((gamma**2)/(2*to**2))*(energy - np.sqrt(4*to**2-energy**2)*1j)
    return mat
def specden(gamma,site,energy):#spectral density matrix(-2Im(sigma))
    mat = -2*(selfenergy(gamma,energy).imag)
    return mat
#Green's functions
def ret_gre(energy, arraysitgamstrn):
    k = [np.ones(n-1),np.ones(n),np.ones(n-1)]
    offset = [-1,0,1]
    mat = diags(k,offset,dtype='complex_').toarray()
    for i in range(n-1):
        mat[i, i] = (energy - sitepotentialAAH[i]) / t
    for i in range(3):
        mat[sitegammaindx[i],sitegammaindx[i]] = (energy - sitepotentialAAH[i] - selfenergy(arraysitgamstrn[i],energy))/t
    return (np.linalg.det(mat)/t)


def adv_gre(energy, arraysitegamstrn):
    return np.transpose(np.conjugate(ret_gre(energy, arraysitegamstrn)))

#transmission probability
def trnasmission(sgindx1,sgstrn1,sgindx2,sgstrn2,energy, arraysitegamstrn):
    spcdn1 = specden(sgstrn1,sgindx1,energy)
    retgre = ret_gre(energy, arraysitegamstrn)
    spcdn2 = specden(sgstrn2,sgindx2,energy)
    advgre = adv_gre(energy, arraysitegamstrn)
    mat = (spcdn1*spcdn2)/((retgre)**2)
    return abs(mat)
pun = np.linspace(start=-2.0*to,stop=2.0*to,endpoint=True,num=10)
grofer = makeeigran(energyval, 0.01, 4) + makelist(energyval)
free_energy = [*pun,*grofer]
np.savetxt('free_energ.txt', free_energy)
for sgstrn in arrayofsitegamstrn:
    print(sgstrn)
    mat = np.zeros(len(free_energy), dtype = float)
    for i in range(1,len(free_energy)-1):
        print(i)
        fe = free_energy[i]
        rl = trnasmission(sitegammaindx[1],sgstrn[1],sitegammaindx[0],sgstrn[0],fe, sgstrn).real
        nr = trnasmission(sitegammaindx[2],sgstrn[2],sitegammaindx[1],sgstrn[1],fe, sgstrn).real
        nl = trnasmission(sitegammaindx[2],sgstrn[2],sitegammaindx[0],sgstrn[0],fe, sgstrn).real
        rn = trnasmission(sitegammaindx[1],sgstrn[1],sitegammaindx[2],sgstrn[2],fe, sgstrn).real
        if nr + nl == 0:
            mat[i] = rl
        else:
            mat[i] = (rl+(rn*nl)/(nr+nl))
    plot = [m if m>1.0E-18 else 1.0E-18 for m in mat]
    print(plot)
    plt.plot(free_energy, plot,'o',label =  f'$\gamma = {sgstrn[2]}$')
    np.savetxt('datafile_for'+ str(sgstrn[2]) + '.txt', plot, )

plt.title('$G/G_o$ v/s $\epsilon_{F}$ for various probe strength ($\lambda = 0.5$)')
plt.xlabel('$\epsilon_{F}$')
plt.ylabel('$G/G_o$')
plt.yscale('log')
plt.grid()
plt.legend()
plt.show()

