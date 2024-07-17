import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


# Ekvation för värmeledning i en stång
# du/dt - k*nibla^2*u = 0
# u(x,t) => du/dt - k*( du^2/dx^2) = 0

#Löser med euler frammåt


#Parametrar
k = 0.5             #Värmeledningskoefficient
staff_length = 5
Nx = 100 # grid_points
dx = staff_length/(Nx - 1 )
#dt = 0.01
dt =  0.2*dx**2/(k)
T = 1
Nt = int(T / dt) # time_points



#Skapa grid dvs stav
x = np.linspace(0, staff_length,Nx) #Array representerar endim
#print(x)



#Bivilkor wikipedia
u = np.zeros(Nx) #0 överallt
u[int(0.4*Nx):int(0.6*Nx)] = 15      #förutom vid 40-60% av stångens längd



#plot och figur
fig, ax = plt.subplots()
line, = ax.plot(x, u, label='Initialvillkor')


"""
    for n in range(Nt): #Iterera över tiden

        for i in range(1, Nx-1): #Iterera över positionen
            u_next[i] = u[i] + k* dt/(dx**2) * (u[i+1] -2*u[i] + u[i-1])
        #u = np.copy(u_next)
        u = u_next



        if (n % 100 == 0):
            plt.plot(x, u, label=f't={n*dt:.3f}s')
    """

def update_sol(frame):
    global u
    #Lös
    u_next = np.zeros(Nx)

    for i in range(1, Nx-1): #Iterera över positionen
            u_next[i] = u[i] + k* dt/(dx**2) * (u[i+1] -2*u[i] + u[i-1])

    u = u_next
    line.set_ydata(u)  # Uppdatera y-data i linjen
    ax.set_title(f'Tid: {frame*dt:.3f} s')
    return line,


        #Rita lösning vid vissa tidssteg

#animation
ani = FuncAnimation(fig, update_sol, frames=Nt, interval=50, repeat = False)

ax.set_xlabel('Position x')
ax.set_ylabel('Temperatur u')
#ax.set_title('Värmeledning i en dimension')
plt.legend()

# Visa animationen
plt.show()





        
"""
# Slutlig visualisering
plt.xlabel('Position x')
plt.ylabel('Temperatur u')
plt.title('Värmeledning i en dimension')
plt.legend()
plt.show()
"""
