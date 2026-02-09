"""
Test-04: Vacuum Symmetry Breaking

Purpose
-------
This test evaluates system behavior starting from a true vacuum state
(energy = 0 everywhere) under uniform background energy intake.

Two regimes are tested:

1) Perfect Symmetry
   - No fluctuation
   - Expected: global phase transition (entire grid evolves identically)

2) Realistic Vacuum
   - Micro-fluctuation added
   - Expected: symmetry breaking and local structure formation

This test demonstrates whether structure requires microscopic fluctuation.
"""

import numpy as np
import matplotlib.pyplot as plt
import os

# -----------------------
# CONFIGURATION
# -----------------------

GRID_SIZE = 51
STEPS = 500

# Energy input
BASE_INTAKE = 0.01

# Set to 0.0 for perfect vacuum symmetry
# Set to small value (e.g. 0.0001) for realistic vacuum
FLUCTUATION = 0.0001

# Thresholds
SHELL_THRESHOLD = 1.0
HELIUM_THRESHOLD = 2.0
CORE_NEIGHBORS_REQUIRED = 4

# States
EMPTY, SHELL, HELIUM, CORE = 0, 1, 2, 3
STATE_NAMES = {
    0: "EMPTY",
    1: "SHELL",
    2: "HELIUM",
    3: "CORE"
}

# Output folder
OUTPUT_DIR = "results"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# -----------------------
# INITIALIZATION
# -----------------------

state = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
energy = np.zeros((GRID_SIZE, GRID_SIZE))

# -----------------------
# NEIGHBOR FUNCTION
# -----------------------

def neighbors(i, j):
    for di in [-1, 0, 1]:
        for dj in [-1, 0, 1]:
            if di == 0 and dj == 0:
                continue
            ni, nj = i + di, j + dj
            if 0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE:
                yield ni, nj

# -----------------------
# SIMULATION LOOP
# -----------------------

for step in range(STEPS):

    # Background energy intake
    if FLUCTUATION > 0:
        noise = np.random.uniform(-FLUCTUATION, FLUCTUATION, (GRID_SIZE, GRID_SIZE))
        energy += BASE_INTAKE + noise
    else:
        energy += BASE_INTAKE

    new_state = state.copy()

    # Threshold transitions
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            e = energy[i, j]

            if e >= HELIUM_THRESHOLD:
                new_state[i, j] = HELIUM
            elif e >= SHELL_THRESHOLD:
                new_state[i, j] = SHELL

    # Helium collapse rule
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if new_state[i, j] == HELIUM:
                helium_neighbors = sum(
                    1 for ni, nj in neighbors(i, j)
                    if new_state[ni, nj] == HELIUM
                )
                if helium_neighbors >= CORE_NEIGHBORS_REQUIRED:
                    new_state[i, j] = CORE

    state = new_state

# -----------------------
# RESULTS
# -----------------------

unique, counts = np.unique(state, return_counts=True)
results = dict(zip(unique, counts))

print("\nFinal State Counts:")
for s in range(4):
    print(f"{STATE_NAMES[s]}: {results.get(s, 0)}")

# Save image
plt.figure(figsize=(6, 6))
plt.imshow(state, cmap="viridis")
plt.colorbar(label="State")
plt.title("Test-04 Final State")
plt.savefig(os.path.join(OUTPUT_DIR, "Test-04_Final_State.png"))
plt.close()

print("\nResult image saved to results/Test-04_Final_State.png")
