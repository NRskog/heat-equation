import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation, FFMpegWriter



def parameters():
    # Parametrar (slumpade)
    k = 25                # Värmeledningskoefficient
    Lx = 50                 # antal punkter x,y
    Ly = 50
    Nx = 40                 # grid_points
    Ny = 40
    dx = Lx / (Nx - 1)
    dy = Ly / (Ny - 1)
    dt = 0.2 * dx * dy / k  # Courant-Friedrichs-Lewy (eller CFL)
    T = 2                   # Total tid
    Nt = int(T / dt)        # Antal tidpunkter
    
    # Skapa grid dvs platta 2D
    x = np.linspace(0, Lx, Nx)
    y = np.linspace(0, Ly, Ny)
    X, Y = np.meshgrid(x, y)

    return k, Lx, Ly, Nx, Ny, dx, dy, dt, T, Nt, X, Y


def boundary_conditions(Nx, Ny):
    # Randvilkor, valde slumpmässiga
    u = np.zeros((Nx, Ny)) 
    u[Nx // 2, Ny // 2] = 20
    u[Nx // 4, Ny // 4] = 42
    u[3 * Nx // 4, 3 * Ny // 4] = 23
    u[Nx // 3, 2 * Ny // 3] = 10
    u[2 * Nx // 3, Ny // 3] = 5
    u[2 * Nx // 5, 4 * Ny // 5] = 30
    u[4 * Nx // 5, Ny // 5] = 25
    u[Nx // 5, Ny // 5] = 35
    u[3 * Nx // 5, 3 * Ny // 5] = 28
    u[4 * Nx // 5, 3 * Ny // 5] = 32

    return u


def update_solution(u, k, Nx, Ny, dx, dy, dt):
    u_next = np.zeros((Nx, Ny))


    for i in range(Nx):
        for j in range(Ny):
            if i == 0 or i == Nx-1 or j == 0 or j == Ny-1:
                u_next[i, j] = u[i, j]  # Behåll kantvärden oförändrade
            else:
                dd_x = (u[i+1, j] - 2*u[i, j] + u[i-1, j]) / (dx**2)
                dd_y = (u[i, j+1] - 2*u[i, j] + u[i, j-1]) / (dy**2)
                u_next[i, j] = u[i, j] + k * dt * (dd_x + dd_y)
    #u = u_next.copy()
    return u_next



def animate_plot(k, Lx, Ly, Nx, Ny, dx, dy, dt, T, Nt, X, Y):
    # Plot och figur för 3D-yta
    u = boundary_conditions(Nx, Ny)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(X, Y, u, cmap='jet', edgecolor='none', vmin=20, vmax=42)
    fig.colorbar(surf)
    ax.set_xlabel('Pos x')
    ax.set_ylabel('Pos y')
    ax.set_zlabel('Temp u')
    ax.set_title('Värmeledning i 2 dimensioner')




    def update_animation(frame):
        nonlocal u
        u = update_solution(u, k, Nx, Ny, dx, dy, dt)
        ax.clear()
        ax.plot_surface(X, Y, u, cmap='jet', edgecolor='none')
        ax.set_xlabel('Pos x')
        ax.set_ylabel('Pos y')
        ax.set_zlabel('Temperatur u')
        ax.set_title(f'Tid: {frame*dt:.3f} s')
       
        return ax,

    # Animation
    ani = FuncAnimation(fig, update_animation, frames=Nt, interval=50, repeat=False)
    

    # Sparar animatrionen
    #writer = FFMpegWriter(fps=15, metadata=dict(artist='Me'), bitrate=1800)
    #ani.save('heat_anim2.mp4', writer=writer)
    
    return ani, fig

    
   

def main():
    k, Lx, Ly, Nx, Ny, dx, dy, dt, T, Nt, X, Y = parameters()
    ani, fig = animate_plot(k, Lx, Ly, Nx, Ny, dx, dy, dt, T, Nt, X, Y)

    plt.show(block=False)
    plt.pause(20)
    plt.close()

if __name__ == "__main__":
    main()

