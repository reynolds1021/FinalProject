"""
2-D animation of the heat equation
Assumptions: a 4- wall 'box' with uniform temperatures
Finite element method is used to solve PDE
Import various math, numpy and plot libraries
"""


import numpy as np
from math import pi,sin
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm

"""
1.plt.ion() produces animation effect
2. Generate 3-D plot
"""


plt.ion()
fig = plt.figure()
ax = fig.gca(projection='3d') 

"""
Initialize box dimensions in meters (in this case, it is a cube)
"""

L_x = 0.1
L_y = 0.1

"""
Number of finite elements
"""


n = 15

"""
Initialize temperature of walls at 0 degrees Celsius
"""


T_1 = 0
T_2 = 0
T_3 = 0
T_4 = 0

"""
Finite element size
"""

dx = L_x/n
dy = L_y/n

"""
User-specified thermal diffusivity (alpha) (in this case, aluminum is used)
1 minute of run time
Time steps (delta) of 0.1 second
"""

alpha = 9.7 * 10**(-5)
t_total = 60
dt = 0.1

"""
Produce arrays for each spatial dimension (e.g., x,y) as the average 
of each time step
"""

x = np.linspace(dx/2, L_x - dx/2, n)
y = np.linspace(dy/2, L_y - dy/2, n)

"""
Generate a 2-D array from the vectors above (note the lower- and uppercase variables 
are used so that they can be manipulated separately).
"""

X,Y = np.meshgrid(x,y)

"""
Assign a temperature distribution for each spatial dimension, using list comprehension.
A sinusoidal one has been chosen so that the
temp has a maximum in the middle of the box and a minimum at the vertices.
"""

T_x = np.array([60*sin(pi*i/L_x) for i in x])
T_y = np.array([60*sin(pi*i/L_y) for i in y])

"""
Create a 2D array from the above temperature distributions.(Note the lower- 
and uppercase variables are used so that they can be manipulated separately).
"""

T_X, T_Y = np.meshgrid(T_x,T_y)

"""
Initialize an empty array
"""

dT_x_dt = np.empty(n)
dT_y_dt = np.empty(n)

"""
In steps of dt, create an vector of points to the
final time using arange function. 
"""

t = np.arange(0,t_total,dt)

for j in range(1,len(t)):

    ax.clear()

    for i in range(1,n-1):

        """
        Discretize the spatial differentials (dx, dy)
        """
        
        dT_x_dt[i] = alpha*((T_x[i+1]-(2*T_x[i])+T_x[i-1])/dx**2)
        dT_y_dt[i] = alpha*((T_y[i+1]-(2*T_y[i])+T_y[i-1])/dx**2)

    """
    Use the uniform wall temperatures for the boundary conditions
    """
    
    dT_x_dt[0] = alpha*((T_x[1]-(2*T_x[0])+T_1)/dx**2) 
    dT_y_dt[0] = alpha*((T_y[1]-(2*T_y[0])+T_3)/dx**2)
    dT_x_dt[n-1] = alpha*((T_2-(2*T_x[n-1])+T_x[n-2])/dx**2)
    dT_y_dt[n-1] = alpha*((T_4-(2*T_y[n-1])+T_y[n-2])/dx**2)

   
    """
    Update the temperature distribution arrays with the boundary conditions data
    """
    T_x = T_x + dT_x_dt*dt
    T_y = T_y + dT_y_dt*dt
    T_X, T_Y = np.meshgrid(T_x,T_y)

    """
    Z is a function of two variables i.e., f = Z(x,y)
    and represents the temperature in two spatial dimensions. (x,y). 
    Write Z as sum of the two temperature arrays to generate a surface plot.
    """
    
    Z = (T_X + T_Y)

    """
    1. Customize the plot and label the axes
    2. Finally, create the continous plot
    """


    surf = ax.plot_surface(X,Y,Z, cmap=cm.rainbow,
                           linewidth=0, antialiased = False)

    ax.set_zlim(0,120)
    ax.set_xlim(0,0.1)
    ax.set_ylim(0,0.1)
    ax.set_xlabel('x: Distance (meters)')
    ax.set_ylabel('y: Distance (meters)')
    ax.set_zlabel('Temperature (Celsius)')
    plt.show()
    plt.pause(0.01)

    