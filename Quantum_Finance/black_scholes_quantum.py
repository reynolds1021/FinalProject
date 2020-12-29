import numpy as np
from numpy import linspace #Linspace package used to generate evenly spaced vectors
import matplotlib.pyplot as plt #Import plot library
from mpl_toolkits.mplot3d import Axes3D #Import 3-D plot library
from matplotlib.ticker import LinearLocator, FormatStrFormatter #Import ticker library
from matplotlib import cm #Import colormap utilties

np.seterr(all='raise') #Set error handling to known state

Asian = 'Asian'
European = 'European'
Linear = 'Linear'
Non_Linear = 'Non_linear'


"""
Class to determine the option and equation type
"""

class CallType(object):

    def __init__(self, ct, et):

        self.ct = ct
        self.et = et 
       
        

    def call_type(self, ct):

        if ct == 'E':
            return European

        elif ct == 'A':
           return Asian

        else:
            print("You have entered an invalid option. Please try again!")

    def eqn_type(self, et): 

        if et ==  'NL':
            return Non_Linear

        elif et == 'L':
           return Linear

        else:
            print("You have entered an invalid option. Please try again!")

        


        








class Solver(object):
    """
    Class to solve for BS partial differential equation (PDE)
    Based on numerical methods used to solve 1-D diffusion (heat) equation (finite element and Runge-Kutta)
    
    """

    def __init__(self, s_max, t_max, k, beta, sigma, r, option_type, eq_type):
        """
        BS Equation parameters:
        :s_max: Max price
        :t_max: Max expiration time
        :k: Strike price
        :beta: Non-linear scaling parameter 
        :sigma: Asset price volatility
        :r: Risk-free interest rate
        """

        self.option_type = option_type
        self.eq_type = eq_type

        """ 
        Option pricing parameters (specify precision; float for all...)
        """
        self.sigma = np.float64(sigma)
        self.r = np.float64(r)
        self.k = np.float64(k)
        self.beta = np.float64(beta)

        """
        Specify the value and precision of the step (delta s and t)...
        """
        self.ds = np.float64(s_max / 40.0)
        self.dt = 0.01

        """
        self.dt = self.r*self.ds/(self.sigma ** 2)
        Max s, max t
        """

        self.s_max = np.float64(s_max)
        self.t_max = np.float64(t_max)
        self.dt = (self.ds ** 2) / (39 * self.sigma ** 2 + 0.5 * self.r) / s_max ** 2
        self.s_array_size = int(self.s_max / self.ds)
        self.t_array_size = int(self.t_max / self.dt)

        
        """
        Initialize price and time vectors using linspace; precision=float
        """
        self.s = linspace(0, self.s_max, self.s_array_size)
        self.ds = self.s[2] - self.s[1]
        
        self.t = linspace(0, self.t_max, self.t_array_size)
        self.U_st = np.zeros((self.s_array_size, self.t_array_size), dtype=np.float64)
        self.U_max = 0.0


   

       



    def init_val(self, s): 
        """
        Specify initial value for given asset price (S): U(s, t=0).
        s: Option price at time, t_0
        return: Initial value for given S
        """

        v_i = max(s - self.k, 0) 

        return v_i

        """
        PDE solver for non-linear BS European Calls
        returns boolean to handle potential calculation errors
        """

    def pde(self, eq_type):
        
        self.eq_type = eq_type 

        """
        Specify the call type, European or Asian
        Equate initial conditions u(s,t=0) to the initial value defined above 
        """

       

        for s_i in range(self.s_array_size):
            self.U_st[s_i, 0] = self.init_val(self.s[s_i])

        """
        Calculate for t + dt
        Starting at t_1 ( t_0 was used for the initial condition)
        Value for t_i to t
        """
        try:
            
            for t_i in range(1, self.t_array_size):
                
                t = self.t[t_i]
                s_i = 0

                
                for s_i in range(1, self.s_array_size - 1):
                    """
                    Compute U[x0...s_max, t_i]
                    Compute U at spatial vector calculated above U(x_i, t_n)
                    R is the spatial Ordinary Diff Eq (ODE)
                    Compute depending on equation type
                    """
                    s = self.s[s_i]
                    if eq_type == Non_Linear:
                    
                        R_1 = -self.beta * self.U_st[s_i, t_i - 1] ** 3
                        R_2 = self.r * s * (self.U_st[s_i + 1, t_i - 1] - self.U_st[s_i, t_i - 1]) / self.ds
                        R_3 = 0.5 * (self.sigma ** 2) * (s ** 2) * (
                            self.U_st[s_i - 1, t_i - 1] - 2 * self.U_st[s_i, t_i - 1] + self.U_st[
                                s_i + 1, t_i - 1]) / (self.ds ** 2)

                        R_sum = R_1 + R_2 + R_3

                    else:
                        R_1 = -self.r * self.U_st[s_i, t_i - 1]
                        R_2 = self.r * s * (self.U_st[s_i + 1, t_i - 1] - self.U_st[s_i - 1, t_i - 1]) / (2 * self.ds)
                        R_3 = 0.5 * (self.sigma ** 2) * (s ** 2) * (
                            self.U_st[s_i - 1, t_i - 1] - 2 * self.U_st[s_i, t_i - 1] + self.U_st[
                                s_i + 1, t_i - 1]) / (self.ds ** 2)

                        R_sum = R_1 + R_2 + R_3    

                       
                    """
                    Runge-Kutta 4[th] order (RK4) numerical method:
                    Equate RK4 coeficients to calculated R values 
                    """
                    
                    rk_1 = self.dt * R_sum
                    rk_2 = self.dt * (R_sum + 0.5 * rk_1)
                    rk_3 = self.dt * (R_sum + 0.5 * rk_2)
                    rk_4 = self.dt * (R_sum + rk_3)

                    """
                    Function U(s,t) in time domain
                    """
                    self.U_st[s_i, t_i] = self.U_st[s_i, t_i - 1] + (1.0 / 6.0) * (rk_1 + 2.0 * rk_2 + 2.0 * rk_3 + rk_4)

                    """
                    Find max U_st to create plot
                    """
                    if self.U_max < self.U_st[s_i, t_i]:
                        self.U_max = self.U_st[s_i, t_i]
                    """
                    Insert boundary conditions RK at s = 0, and s = s_max
                    """

                self.U_st[0, t_i] = 0
                self.U_st[s_i + 1, t_i] = self.s[s_i + 1] - self.k

                """    
                Error handling returning boolean if parameters are out of bounds...
                """
   
        except FloatingPointError as e:
            print("Overflow at t = {} and s = {}, {}, program will now close!".format(t, s, e)) 
   
            return False

        return True

    def plot(self, option_type, eq_type):

        self.option_type = option_type
        self.eq_type = eq_type  


        """
        Plot 3-D chart for European option 

        """
       
        """
        Re-orient the figure 
        """

        

        fig = plt.figure(figsize=(12, 8)) 
        fig.subplots_adjust(left=0, bottom=0, right=1, top=0.86)

        """
        RK Method 3-D plot 
        """

        ax = fig.gca(projection='3d')
        ax.view_init(azim=-100, elev=18)
        self.s, self.t = np.meshgrid(self.s, self.t)

        """
        Surface plot params 

        """

        Uxt = np.transpose(self.U_st)
        surf = ax.plot_surface(self.s, self.t, Uxt, cmap=cm.jet) 
        fig.tight_layout()

        """
        Specify axes labels
        """
        ax.set_xlabel('S') 
        ax.set_ylabel('t')
        ax.set_zlabel('V[S,t]')

        """
        Format non-linear scaling parameter (beta)
        Do not print if equation is linear
        """

        nl_param= "\nbeta={:0.6f}".format(self.beta) if self.eq_type == Non_Linear else ''

        """
        Format axes:
        Note: Special math symbols (e.g., epsilon) intialized by in$...
        """
        
        
        ax.text2D(0.8, 0.83, "{} Black-Scholes {} Option."
                              "\nStrike price: K={}"
                              "\nInitial condition: V(S, t=0)=max(S-K, 0)"
                              "\nBoundary condition: V(S=0, t)=0"
                              "\nBoundary condition: V(S=$S_M)=S_M - K$" 
                              "\n$S\in$(0, {:0.2f}) and $t\in$(0, {})" 
                              "\n$\sigma=${}, $r=${}"
                  .format(self.eq_type, self.option_type, self.k, self.s_max, self.t_max, self.sigma, self.r) + nl_param, size=10,
                  transform=ax.transAxes)

       


        """
        Customize the z-axis.
        """
        ax.set_zlim(0, self.U_max)
        ax.zaxis.set_major_locator(LinearLocator(10))
        ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

        """
        Add a color bar attributing values to colors
        """
        fig.colorbar(surf, shrink=0.5, aspect=5)
        plt.show()

"""
Create an instance of the CallType class to determine call and equation type
Key:
'A': Asian
'E': European
'L': Linear
'NL': Non_linear

"""

c = CallType('A', 'L')
o = c.call_type('A')
e = c.eqn_type('L')




if __name__ == '__main__' and c == European:

    """
    Main to call above methods to generate 3-D plot at user-specified values
    Note: Both European and Asian calls have zero risk free interest rates;
    their params are the same except for x_max
    Create instance of the Solver class and call pde and plot methods...
    """
    x_max = 150 
    t_max = 1 
    k = 100 
    beta = 0.000001 
    sigma = 0.2 
    r = 0 
    



else:

    x_max = 166.67
    t_max = 1 
    k = 100 
    beta =  0.1
    sigma = 0.2 
    r = 0 



    

    
    p = Solver(x_max, t_max, k=k, beta=beta, sigma=sigma, r=r, option_type=o, eq_type=e)
    p.pde(e)
    p.plot(o,e)

    




    

    