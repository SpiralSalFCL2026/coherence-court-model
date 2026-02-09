"""
coherence_model.py

Cultural Entropy Dynamics Model (1950–2030)

A minimal dynamical systems model illustrating compounding cultural entropy
under extraction pressure, volatility, and declining substrate stability.

Author: Sal Attaguile
License: CC BY 4.0
"""

import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# DECADAL INPUT DATA (Normalized 0–1)
# ============================================================

decades = ['1950s', '1960s', '1970s', '1980s',
           '1990s', '2000s', '2010s', '2020s']

# Substrate Stability
S_values = np.array([0.85, 0.65, 0.45, 0.55,
                     0.40, 0.35, 0.25, 0.30])

# Extraction Pressure
X_values = np.array([0.15, 0.45, 0.70, 0.80,
                     0.85, 0.90, 0.95, 0.95])

# Volatility / Fragmentation
F_values = np.array([0.20, 0.50, 0.65, 0.75,
                     0.85, 0.90, 0.95, 1.00])


# ============================================================
# MODEL PARAMETERS
# ============================================================

alpha = 1.0        # Extraction sensitivity
delta = 0.8        # Volatility sensitivity
beta  = 1.5        # Stabilizing strength

gamma = 0.28       # Compounding / self-reinforcement
lambda_relax = 1.1 # Relaxation rate

k = 0.75           # Recognition decay strength
R_max = 1.0        # Max recognition


# ============================================================
# TIME DISCRETIZATION
# ============================================================

t_dec = np.linspace(0, 8, 801)    # 0 = 1950, 8 = 2030
dt = t_dec[1] - t_dec[0]

# Map continuous time to decades
decade_idx = np.floor(t_dec).astype(int)
decade_idx = np.clip(decade_idx, 0, len(S_values) - 1)

S_t = S_values[decade_idx]
X_t = X_values[decade_idx]
F_t = F_values[decade_idx]


# ============================================================
# ENTROPY FORCING TERM
# ============================================================

D_t = alpha * X_t + delta * F_t - beta * S_t


# ============================================================
# DYNAMICAL SIMULATION (Forward Euler)
# ============================================================

E = np.zeros_like(t_dec)
E[0] = 0.4  # Initial entropy (circa 1950)

for i in range(1, len(t_dec)):

    # Instantaneous equilibrium entropy
    E_inst = np.exp(D_t[i])

    # Entropy evolution with compounding + relaxation
    dE_dt = gamma * E[i-1] + lambda_relax * (E_inst - E[i-1])

    E[i] = E[i-1] + dE_dt * dt


# Recognition coherence (exponential decay)
R = R_max * np.exp(-k * E)

years = 1950 + t_dec * 10


# ============================================================
# VISUALIZATION
# ============================================================

fig, (ax1, ax2) = plt.subplots(
    2, 1,
    figsize=(11, 8),
    sharex=True,
    gridspec_kw={'height_ratios': [3, 1]}
)


# Main dynamics
ax1.plot(
    years, E,
    color='#d32f2f',
    lw=2.8,
    label='Cultural Entropy E(t)'
)

ax1.plot(
    years, np.exp(D_t),
    color='#d32f2f',
    lw=1.6,
    alpha=0.6,
    ls='--',
    label='Static exp(D(t))'
)

ax1.plot(
    years, R,
    color='#1976d2',
    lw=2.8,
    label='Recognition R(t)'
)

ax1.set_ylabel('Normalized Level')
ax1.set_title('Cultural Entropy Dynamics (1950–2030)')
ax1.legend()
ax1.grid(True, alpha=0.3)


# Drivers
ax2.plot(years, S_t, color='#388e3c', label='Stability S(t)')
ax2.plot(years, X_t, color='#f57c00', label='Extraction X(t)')
ax2.plot(years, F_t, color='#7b1fa2', label='Volatility F(t)')

ax2.set_xlabel('Year')
ax2.set_ylabel('Normalized (0–1)')
ax2.legend(loc='upper left', ncol=3)
ax2.grid(True, alpha=0.3)


plt.tight_layout()
plt.show()


# ============================================================
# SUMMARY TABLE
# ============================================================

print("Decade | E(dynamic) | R     | Static exp(D)")
print("-------------------------------------------")

for i, dec in enumerate(decades):
    idx = np.argmin(np.abs(t_dec - i))

    print(
        f"{dec:6s} | "
        f"{E[idx]:6.2f}      | "
        f"{R[idx]:.2f}  | "
        f"{np.exp(D_t[idx]):6.2f}"
    )