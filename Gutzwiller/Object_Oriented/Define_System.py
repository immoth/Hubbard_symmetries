
from Define_Paulis import I,X,Y,Z, cd,c,n, Mdot, bkt
import scipy.linalg as ln
import numpy as np
import matplotlib.pyplot as plt


class system:
    lattice_types = ['square','triangle','line']
    
    def __init__(self,lattice,sites):
        self.lattice = lattice
        self.N = sites
        if self.lattice not in self.lattice_types:
            raise Exception('lattice must be on of: ' + str(self.lattice_types))
        
        if self.lattice == 'square':
            if self.N not in [4,8]:
                raise Exception('I have only defined the square lattices for 4 sites and 8 sites')
        
        if self.lattice == 'triangle':
            if self.N != 4:
                raise Exception('I have only defined the triangle lattices for 4 sites')
    
    def neighbors(self):
        if self.lattice == 'line':
            N = self.N
            nbrs = []
            for i in range(N-1):
                nbrs.append([i,i+1])
                nbrs.append([i+1,i])
            nbrs.append([N-1,0])
            nbrs.append([0,N-1])
            return nbrs
        if self.lattice == 'square':
            if self.N == 4:
                nbrs = [[0,1],[1,2],[2,3],[0,3],
                        [1,0],[2,1],[3,2],[3,0]]
                return nbrs
            if self.N == 8:
                nbrs = [[0,1],[0,3],[0,4],[0,6],
                        [1,0],[1,2],[1,5],[1,7],
                        [2,1],[2,3],[2,4],[2,6],
                        [3,0],[3,2],[3,5],[3,7],
                        [4,0],[4,2],[4,5],[4,7],
                        [5,1],[5,3],[5,4],[5,6],
                        [6,0],[6,2],[6,5],[6,7],
                        [7,1],[7,3],[7,4],[7,6]]
                return nbrs
        if self.lattice == 'triangle':
            nbrs = [[0,1],[0,2],[0,3],
                    [1,0],[1,2],[1,3],
                    [2,0],[2,1],[2,3],
                    [3,0],[3,1],[3,2]]
            return nbrs
        return None
    
    def K(self,k):
        nbrs = self.neighbors()
        N = self.N
        Kout = 0*I(2*N)
        for pair in nbrs:
            i = pair[0]
            j = pair[1]
            Kout = Kout + k*Mdot([cd(i,2*N),c(j,2*N)])
            Kout = Kout + k*Mdot([cd(i+N,2*N),c(j+N,2*N)])
        return Kout
    
    
    def D(self,d):
        N = self.N
        Dout = 0*I(2*N)
        for i in range(0,N):
            Dout = Dout + Mdot([n(i,2*N),n(i+N,2*N)])
        return d*Dout

    def M(self,u):
        N = self.N
        Dout = 0*I(2*N)
        for i in range(0,N):
            Dout = Dout + n(i,2*N) 
            Dout = Dout + n(i+N,2*N)
        return u*Dout
    
    def H(self,k,u,d):
        return self.K(k) + self.D(d) + self.M(u)
    
    def G(self,g):
        N = self.N
        out = I(2*N)
        for i in range(N):
            out = Mdot([ out , I(2*N) + (np.exp(-g)-1)*Mdot([n(i,2*N),n(i+N,2*N)]) ])
        return out
    
    def K_single(self, k):
        N = self.N
        nbrs = self.neighbors()
        h = [[0 for i in range(N)] for j in range(N)]
        for pair in nbrs:
            h[pair[0]][pair[1]] = -k
        return h
        
    def Fl(self):
        e,y = ln.eigh(self.K_single(1))
        return np.transpose(y)

    def Fld(self):
        e,y = ln.eigh(self.K_single(1))
        return np.conjugate(y)

    def ad(self,n):
        F = self.Fl()
        N = len(F)
        Fd = np.conjugate(np.transpose(F))
        out = Fd[0][n]*cd(0,N)
        for i in range(1,N):
            out = out + Fd[i][n]*cd(i,N)
        return out

    def a(self,n):
        F = self.Fl()
        N = len(F)
        Fd = np.conjugate(np.transpose(F))
        out = F[n][0]*c(0,N)
        for i in range(1,N):
            out = out + F[n][i]*c(i,N)
        return out
    
    def psi0(self):
        N = self.N
        y = [0 for i in range(2**N)]
        y[0] = 1
        return y

    def psi1(self,n_list):
        psi1 = self.psi0()
        for n in n_list:
            ad = self.ad(n)
            psi1 = Mdot([ad,psi1])
        return psi1
    
    def psi_spin(self,n_list):
        psi1 = self.psi1(n_list)
        return np.kron(psi1,psi1)
    
    def pauli_strings(self):
        N=self.N
        nbrs = self.neighbors()
        pauli = ''
        for i in range(N):
            pauli = pauli + 'Z'
        paulis = [pauli]
        for pair in nbrs:
            if pair[0] < pair[1]:
                pauliX = ''
                pauliY = ''
                nonp = 'I'
                for i in range(N):
                    if i == pair[0]:
                        pauliX = pauliX + 'X'
                        pauliY = pauliY + 'Y'
                        nonp = 'Z'
                    elif i == pair[1]:
                        pauliX = pauliX + 'X'
                        pauliY = pauliY + 'Y'
                        nonp = 'I'
                    else:
                        pauliX = pauliX + nonp
                        pauliY = pauliY + nonp
                paulis.append(pauliX)
                paulis.append(pauliY)
        return paulis
    

    def draw(self):
        if self.lattice == 'square':
            if self.N == 4:
                circles_y = [0,1,1,0]
                circles_x = [0,0,1,1]
                lines_y = [0,1,1,0,0]
                lines_x = [0,0,1,1,0]
                plt.scatter(circles_x,circles_y,s=500)
                plt.plot(lines_x,lines_y)
                plt.ylim(-1,2)
                plt.xlim(-1,2)
            if self.N == 8:
                circles_y = [1,1,1,1,0,0,0,0]
                circles_x = [0,1,2,3,3,2,1,0]
                lines_y = [1,1,1,1,0,0,0,0,1,1,0,0,1]
                lines_x = [0,1,2,3,3,2,1,0,0,1,1,2,2]
                plt.scatter(circles_x,circles_y,s=500)
                plt.plot(lines_x,lines_y)
                plt.ylim(-1,2)
                plt.xlim(-1,4)
                
        if self.lattice == 'triangle':
            circles_y = [1,2,1,0]
            circles_x = [0,1,2,1]
            lines_y = [1,2,1,0,1,1,2,0]
            lines_x = [0,1,2,1,0,2,1,1]
            plt.scatter(circles_x,circles_y,s=500)
            plt.plot(lines_x,lines_y)
            plt.ylim(-1,3)
            plt.xlim(-1,3)
        if self.lattice == 'line':
            N = self.N
            circles_y = [0 for i in range(int(np.floor(N/2)))] + [1 for i in range(int(np.ceil(N/2)))]
            circles_x = [i for i in range(int(np.floor(N/2)))] + [int(np.floor(N/2))-1 - i for i in range(int(np.ceil(N/2)))]
            lines_y = [0 for i in range(int(np.floor(N/2)))] + [1 for i in range(int(np.ceil(N/2)))] + [0]
            lines_x = [i for i in range(int(np.floor(N/2)))] + [int(np.floor(N/2))-1 - i for i in range(int(np.ceil(N/2)))] + [0]
            plt.scatter(circles_x,circles_y,s=500)
            plt.plot(lines_x,lines_y)
            plt.ylim(-1,2)
            plt.xlim(-2,int(np.ceil(N/2)))
        return plt.show()

   
            
