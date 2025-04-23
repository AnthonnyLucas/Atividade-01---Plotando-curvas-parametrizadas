import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button, Slider
from mpl_toolkits.mplot3d import Axes3D

# --- Dados das curvas ---
t1 = np.linspace(0, 2 * np.pi, 1000)
x1 = np.sin(t1) + 0.5 * np.cos(5 * t1) + 0.25 * np.sin(13 * t1)
y1 = np.cos(t1) + 0.5 * np.sin(5 * t1) + 0.25 * np.cos(13 * t1)

t2 = np.linspace(0, 2 * np.pi * 10, 1000)
x2 = np.cos(t2)
y2 = np.sin(t2)
z2 = (10 / (2 * np.pi * 10)) * t2

# --- Setup da figura e subplots ---
fig = plt.figure(figsize=(12, 7), facecolor='#1e1e1e')
plt.subplots_adjust(bottom=0.3)

ax2d = fig.add_subplot(121)
ax3d = fig.add_subplot(122, projection='3d')
ax3d.set_visible(False)

line2d, = ax2d.plot([], [], color='purple')
line3d, = ax3d.plot([], [], [], color='purple')

# --- Variáveis globais ---
ani = None
paused = False
current_view = "2D"

# --- Estilo customizado para eixos ---
def estilizar_axes(ax):
    ax.set_facecolor('#1e1e1e')
    ax.tick_params(colors='white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    if hasattr(ax, 'zaxis'):
        ax.zaxis.label.set_color('white')
        ax.zaxis.set_tick_params(colors='white')
    ax.title.set_color('white')
    ax.grid(True, color='gray', linestyle='--', alpha=0.4)

# --- Funções de configuração dos gráficos ---
def configurar_eixos_2d():
    ax2d.clear()
    ax2d.set_xlim(np.min(x1) - 0.5, np.max(x1) + 0.5)
    ax2d.set_ylim(np.min(y1) - 0.5, np.max(y1) + 0.5)
    ax2d.set_title('Curva Parametrizada 2D')
    ax2d.set_xlabel('x')
    ax2d.set_ylabel('y')
    estilizar_axes(ax2d)
    return ax2d.plot([], [], color='purple')[0]

def configurar_eixos_3d():
    ax3d.clear()
    ax3d.set_xlim([-1.5, 1.5])
    ax3d.set_ylim([-1.5, 1.5])
    ax3d.set_zlim([0, 10])
    ax3d.set_title('Hélice Circular (Mola)')
    ax3d.set_xlabel('x')
    ax3d.set_ylabel('y')
    ax3d.set_zlabel('z')
    estilizar_axes(ax3d)
    return ax3d.plot([], [], [], color='purple')[0]

# --- Funções de atualização ---
def update_2d(frame):
    line2d.set_data(x1[:frame], y1[:frame])
    return line2d,

def update_3d(frame):
    line3d.set_data(x2[:frame], y2[:frame])
    line3d.set_3d_properties(z2[:frame])
    return line3d,

# --- Controle principal ---
def iniciar_animacao(view):
    global ani, paused, line2d, line3d
    if ani is not None and ani.event_source is not None:
        ani.event_source.stop()

    paused = False
    intervalo = slider_vel.val

    if view == "2D":
        ax3d.set_visible(False)
        ax2d.set_visible(True)
        line2d = configurar_eixos_2d()
        ani = FuncAnimation(fig, update_2d, frames=len(t1),
                            interval=intervalo, blit=False, repeat=False)
    else:
        ax2d.set_visible(False)
        ax3d.set_visible(True)
        line3d = configurar_eixos_3d()
        ani = FuncAnimation(fig, update_3d, frames=len(t2),
                            interval=intervalo, blit=False, repeat=False)

    btn_toggle.label.set_text("⏸ Pausar")
    fig.canvas.draw_idle()

# --- Botões e interações ---
def show_2d(event):
    global current_view
    current_view = "2D"
    iniciar_animacao("2D")

def show_3d(event):
    global current_view
    current_view = "3D"
    iniciar_animacao("3D")

def toggle_animation(event):
    global paused, ani
    if ani is not None and ani.event_source is not None:
        if paused:
            ani.event_source.start()
            btn_toggle.label.set_text("⏸ Pausar")
        else:
            ani.event_source.stop()
            btn_toggle.label.set_text("▶ Continuar")
        paused = not paused

def change_speed(val):
    global ani
    if ani is not None and ani.event_source is not None:
        ani.event_source.interval = val

# --- Widgets ---
ax_button_2d = plt.axes([0.1, 0.15, 0.2, 0.06], facecolor='#2e2e2e')
btn_2d = Button(ax_button_2d, 'Mostrar Curva 2D', color='#444', hovercolor='gray')
btn_2d.on_clicked(show_2d)

ax_button_3d = plt.axes([0.7, 0.15, 0.2, 0.06], facecolor='#2e2e2e')
btn_3d = Button(ax_button_3d, 'Mostrar Hélice 3D', color='#444', hovercolor='gray')
btn_3d.on_clicked(show_3d)

ax_button_toggle = plt.axes([0.4, 0.15, 0.2, 0.06], facecolor='#2e2e2e')
btn_toggle = Button(ax_button_toggle, '⏸ Pausar', color='#444', hovercolor='gray')
btn_toggle.on_clicked(toggle_animation)

ax_slider = plt.axes([0.25, 0.05, 0.5, 0.03], facecolor='#2e2e2e')
slider_vel = Slider(ax_slider, 'Velocidade (ms)', 1, 50, valinit=5, valstep=1)
slider_vel.on_changed(change_speed)

# --- Início com animação 2D ---
iniciar_animacao("2D")
plt.show()
