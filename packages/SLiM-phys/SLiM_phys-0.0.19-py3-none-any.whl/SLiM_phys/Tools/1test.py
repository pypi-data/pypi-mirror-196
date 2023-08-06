import numpy as np 
from DispersionRelationDeterminantFullConductivityZeff import A_maker
[x_max, del_x,w1, v1,Zeff,eta,alpha,beta,ky,ModIndex,mu,xstar]=\
	[10,0.01,2.5,0.1,2.5,1.5,1,0.03,0.01,1,0,10.]

A_maker(x_max, del_x,w1, v1,Zeff,eta,\
    alpha,beta,ky,ModIndex,mu,xstar)