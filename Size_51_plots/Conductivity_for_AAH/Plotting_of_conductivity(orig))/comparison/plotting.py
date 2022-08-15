import random
import numpy as np
import matplotlib.pyplot as plt
import scipy
import scipy.linalg as la
import math,cmath
from scipy.sparse import diags
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["Times New Roman"]
plt.rcParams['figure.figsize'] = [18, 6]

SMALL_SIZE = 18
MEDIUM_SIZE = 18
BIGGER_SIZE = 18
large_SIZE = 35

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=22)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=2)
s= 15
sgstrn = [0.0,0.1,2.0,5.0]
colormark =[['green',"."],['blue',"."],['red',"."],['tab:cyan',"."],['tab:cyan',"."],['tab:olive',"."]]
ax1 = plt.subplot(121)
for i in range(4):
    plot = np.loadtxt('(0.5)datafile_for'+ str(sgstrn[i]) + ' (copy 1).txt', dtype = 'float')
    keep_point = np.where(plot > 1.0E-3)
    plot=plot[keep_point]
    free_energy = np.loadtxt('free_energ.txt',dtype = 'float')
    free_energy=free_energy[keep_point]
    plt.scatter(free_energy, plot,s,c = colormark[i][0],marker = colormark[i][1],alpha = .8,label =  f'$\gamma = {sgstrn[i]}$')
    plt.title('Symmetric probe')
    plt.xlabel('$\epsilon_{F}$')
    plt.ylabel('$G/G_o$')
    plt.yscale('log')
    plt.grid(True)
    plt.text(-3.1, 0.7,'(a)')
    plt.legend()
    plt.xlim((-3.5,+3.5))
sgstrn = [0.0,0.1,2.0,5.0]
ax2 = plt.subplot(122)
for i in range(4):
    plot = np.loadtxt('(0.5)datafile_for_biased'+ str(sgstrn[i]) + '.txt', dtype = 'float')
    keep_point = np.where(plot > 1.0E-3)
    plot=plot[keep_point]
    free_energy = np.loadtxt('free_energ.txt',dtype = 'float')
    free_energy=free_energy[keep_point]
    plt.scatter(free_energy, plot,s,c = colormark[i][0],marker = colormark[i][1],alpha = .8,label =  f'$\gamma = {sgstrn[i]}$')
    plt.title('Biased probe')
    plt.xlabel('$\epsilon_{F}$')
    plt.yscale('log')
    plt.grid(True)
    plt.text(-3.1, 0.7,'(b)')
    plt.xlim((-3.5,+3.5))
plt.savefig('Figure_of Conductivity_compare.pdf')
plt.show()
