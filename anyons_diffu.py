from matplotlib import animation
import scipy.sparse as sp
import numpy as np
from tqdm import tqdm
import pymatching

# Opérateurs de Pauli
X = sp.csr_matrix([[0, 1], [1, 0]], dtype=complex)
Z = sp.csr_matrix([[1, 0], [0, -1]], dtype=complex)
L = 100 # réduit pour que le MWPM soit faisable en temps raisonnable
N = L**2  # nombre de sites

def edge_h(i0, j0):
    return (i0 % L) * L + (j0 % L), 'h'

def edge_v(i0, j0):
    return edge_h(i0, j0)[0] + L**2, 'v'

def adjacent_plaquettes(e, L):
    idx = e[0] if e[1] == 'h' else e[0] - L * L
    i, j = idx // L, idx % L
    if e[1] == 'h':
        return [(i-1) % L, j], [i, j]
    else:
        return [i, (j-1) % L], [i, j]

def star(i0, j0):
    return [edge_h(i0, j0-1), edge_h(i0, j0), edge_v(i0-1, j0), edge_v(i0, j0)]

def plaquette(i0, j0):
    return [edge_h(i0, j0), edge_h(i0+1, j0), edge_v(i0, j0), edge_v(i0, j0+1)]

def Av(i0, j0):
    return None

def Bp(i0, j0):
    return None

# ── Matrice de parité pour pymatching ────────────────────────────────────────
def build_parity_matrix(L):
    rows, cols = [], []
    for i in range(L):
        for j in range(L):
            p_idx = i * L + j
            for e in plaquette(i, j):
                rows.append(p_idx)
                cols.append(e[0])
    H = sp.csr_matrix(
        ([1] * len(rows), (rows, cols)),
        shape=(L * L, 2 * L * L),
        dtype=np.uint8
    )
    return H

matcher = pymatching.Matching(build_parity_matrix(L))

# ── Step modifié : retourne aussi les arêtes flippées ────────────────────────
def step(syndrome, error_track, p, L):
    aretes = [edge_h(i,j) for i in range(L) for j in range(L)] + \
             [edge_v(i,j) for i in range(L) for j in range(L)]
    for e in aretes:
        if np.random.rand() < p:
            error_track[e[0]] ^= True
            for pl in adjacent_plaquettes(e, L):
                syndrome[pl[0], pl[1]] *= -1
    return syndrome, error_track

# ── Correction MWPM ───────────────────────────────────────────────────────────
def correct(syndrome, error_track):
    syndrome_flat = (syndrome.flatten() == -1).astype(np.uint8)
    correction = matcher.decode(syndrome_flat)
    for e_idx in np.where(correction)[0]:
        e = (e_idx, 'h') if e_idx < L*L else (e_idx, 'v')
        for pl in adjacent_plaquettes(e, L):
            syndrome[pl[0], pl[1]] *= -1
    error_track ^= correction.astype(bool)
    logical_z1 = np.sum(error_track[:L]) % 2
    logical_z2 = np.sum(error_track[L*L : L*L + L*L : L]) % 2
    logical_error = bool(logical_z1 or logical_z2)
    return syndrome, error_track, logical_error

def energy(syndrome):
    return np.sum(syndrome == -1)

def simulate(L, p, n_steps):
    syndrome = np.ones((L, L))
    syndrome[L//2, L//2] = -1
    syndrome[2, 0] = -1
    error_track = np.zeros(2 * L * L, dtype=bool)
    history = [syndrome.copy()]
    correction_interval = 3
    logical_history = [False]
    for _ in tqdm(range(n_steps)):
        syndrome, error_track = step(syndrome, error_track, p, L)
        if _ % correction_interval == 0:  # corriger tous les k pas
            syndrome, error_track, log_err = correct(syndrome, error_track)
        
        history.append(syndrome.copy())
        logical_history.append(log_err)
    return history, logical_history

### PIPELINE simulation :
n_steps = 300
p = 0.99999999999999999999999999999
def simu():
    
    return simulate(L, p, n_steps)

grid_state, logical_history = simu()
anyons_over_time = [(1 - s) / 2 for s in grid_state]

## Animation
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Panneau gauche — heatmap
im = ax1.imshow(anyons_over_time[0], vmin=0, vmax=1,
                cmap='inferno', interpolation='nearest')
cbar = fig.colorbar(im, ax=ax1)
cbar.set_label("Densité d'anyons")
ax1.set_title("Syndrome (après correction MWPM) avec la probabilité de flip p={}".format(p))

# Panneau droit — énergie
energies = [energy(s) for s in grid_state]
line, = ax2.plot([], [], color='yellow')
ax2.set_xlim(0, len(grid_state))
ax2.set_ylim(0, max(energies) * 1.1 + 1)
ax2.set_xlabel("Pas de temps")
ax2.set_ylabel("Nombre d'anyons")
ax2.set_title("Énergie")
ax2.set_facecolor('black')

status_text = ax1.text(0.5, -0.08, '', transform=ax1.transAxes,
                       ha='center', fontsize=10)

def update(frame):
    im.set_array(anyons_over_time[frame])
    line.set_data(range(frame), energies[:frame])
    if logical_history[frame]:
        status_text.set_text("⚠ ERREUR LOGIQUE")
        status_text.set_color('red')
    else:
        status_text.set_text("✓ État logique préservé")
        status_text.set_color('lime')
    return im, line, status_text

ani = animation.FuncAnimation(
    fig, update, frames=len(anyons_over_time), interval=30, blit=True)
plt.tight_layout()
plt.show()