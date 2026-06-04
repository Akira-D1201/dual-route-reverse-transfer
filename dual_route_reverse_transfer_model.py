# -*- coding: utf-8 -*-
"""
Dual-Route Reverse Transfer Model

Model A (Orthographic Route): Simulates cognate word recognition based on the BIA+ framework.
Model B (Conceptual Route): Simulates picture-driven word production based on non-selective activation.

Compares L1 Chinese activation decline during 6 months of L3 Japanese learning
under two cognitive pathways.
"""

import numpy as np
import matplotlib.pyplot as plt

# =============================================
# 1. Shared Parameters
# =============================================
L1_baseline = 0.8  # Chinese word baseline activation
L2_baseline = 0.5  # English word baseline activation
L3_baseline_start = 0.1  # Japanese word initial baseline

learning_rate = 0.008  # Daily increase in L3 baseline
days = 180  # Simulate 6 months (180 days)
measurement_days = [0, 30, 90, 180]  # Month 0, 1, 3, 6
inhibition = 0.7  # Mutual inhibition strength
decay = 0.1  # Natural decay rate
input_strength = 0.1  # External input strength
steps = 100  # Time steps per trial


# =============================================
# 2. Model A: Orthographic Route (BIA+ Framework)
# =============================================
def simulate_orthographic(L1_base, L3_base, L2_base=0.5):
    """
    Simulate written cognate recognition.
    Orthographic input activates L1 and L3 (shared script),
    while L2 receives negligible activation.
    """
    L1_act = np.zeros(steps)
    L2_act = np.zeros(steps)
    L3_act = np.zeros(steps)

    L1_act[0] = 0.0
    L2_act[0] = 0.0
    L3_act[0] = 0.0

    for t in range(1, steps):
        # External input
        inp_L1 = input_strength * L1_base
        inp_L2 = input_strength * 0.01  # L2 nearly silent
        inp_L3 = input_strength * L3_base

        # Decay
        decay_L1 = decay * L1_act[t - 1]
        decay_L2 = decay * L2_act[t - 1]
        decay_L3 = decay * L3_act[t - 1]

        # Mutual inhibition
        inhib_L1 = inhibition * (L2_act[t - 1] + L3_act[t - 1])
        inhib_L2 = inhibition * (L1_act[t - 1] + L3_act[t - 1])
        inhib_L3 = inhibition * (L1_act[t - 1] + L2_act[t - 1])

        # Update activation
        L1_act[t] = L1_act[t - 1] + inp_L1 - decay_L1 - inhib_L1
        L2_act[t] = L2_act[t - 1] + inp_L2 - decay_L2 - inhib_L2
        L3_act[t] = L3_act[t - 1] + inp_L3 - decay_L3 - inhib_L3

        # Ensure non-negative
        L1_act[t] = max(0, L1_act[t])
        L2_act[t] = max(0, L2_act[t])
        L3_act[t] = max(0, L3_act[t])

    return np.max(L1_act)


# =============================================
# 3. Model B: Conceptual Route (Non-Selective Activation)
# =============================================
def simulate_conceptual(L1_base, L2_base, L3_base):
    """
    Simulate picture-driven word production.
    Conceptual input activates all language nodes simultaneously.
    Returns (L1_peak, L2_peak) to track L2 dynamics.
    """
    L1_act = np.zeros(steps)
    L2_act = np.zeros(steps)
    L3_act = np.zeros(steps)

    L1_act[0] = 0.0
    L2_act[0] = 0.0
    L3_act[0] = 0.0

    for t in range(1, steps):
        # External input: all languages receive activation proportional to proficiency
        inp_L1 = input_strength * L1_base
        inp_L2 = input_strength * L2_base
        inp_L3 = input_strength * L3_base

        # Decay
        decay_L1 = decay * L1_act[t - 1]
        decay_L2 = decay * L2_act[t - 1]
        decay_L3 = decay * L3_act[t - 1]

        # Mutual inhibition
        inhib_L1 = inhibition * (L2_act[t - 1] + L3_act[t - 1])
        inhib_L2 = inhibition * (L1_act[t - 1] + L3_act[t - 1])
        inhib_L3 = inhibition * (L1_act[t - 1] + L2_act[t - 1])

        # Update activation
        L1_act[t] = L1_act[t - 1] + inp_L1 - decay_L1 - inhib_L1
        L2_act[t] = L2_act[t - 1] + inp_L2 - decay_L2 - inhib_L2
        L3_act[t] = L3_act[t - 1] + inp_L3 - decay_L3 - inhib_L3

        L1_act[t] = max(0, L1_act[t])
        L2_act[t] = max(0, L2_act[t])
        L3_act[t] = max(0, L3_act[t])

    return np.max(L1_act), np.max(L2_act)


# =============================================
# 4. Longitudinal Simulation Loop
# =============================================
results_A = {}
results_B_L1 = {}
results_B_L2 = {}
daily_A = []
daily_B_L1 = []
daily_B_L2 = []

L3_current = L3_baseline_start
for day in range(days + 1):
    peak_A = simulate_orthographic(L1_baseline, L3_current)
    peak_B_L1, peak_B_L2 = simulate_conceptual(L1_baseline, L2_baseline, L3_current)
    daily_A.append(peak_A)
    daily_B_L1.append(peak_B_L1)
    daily_B_L2.append(peak_B_L2)

    if day in measurement_days:
        month = {0: 0, 30: 1, 90: 3, 180: 6}[day]
        results_A[month] = peak_A
        results_B_L1[month] = peak_B_L1
        results_B_L2[month] = peak_B_L2
        print(
            f"Day {day} (Month {month}): A L1={peak_A:.4f}, B L1={peak_B_L1:.4f}, B L2={peak_B_L2:.4f}, L3 base={L3_current:.4f}")

    L3_current += learning_rate

# =============================================
# 5. Visualization
# =============================================
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Left panel: Daily activation trajectories
ax = axes[0]
ax.plot(daily_A, label='Model A: L1 (Orthographic)', color='blue', alpha=0.8)
ax.plot(daily_B_L1, label='Model B: L1 (Conceptual)', color='red', alpha=0.8)
ax.plot(daily_B_L2, label='Model B: L2 (Conceptual)', color='green', linestyle='--', alpha=0.8)
ax.set_title('Activation Over 6 Months of L3 Learning')
ax.set_xlabel('Day')
ax.set_ylabel('Peak Activation')
ax.legend()
ax.axhline(y=0.8, color='gray', linestyle='--', alpha=0.5)

# Right panel: Bar chart at measurement points
ax = axes[1]
months = [0, 1, 3, 6]
x = np.arange(len(months))
width = 0.35
bars_A = ax.bar(x - width / 2, [results_A[m] for m in months], width, label='Model A L1', color='blue', alpha=0.7)
bars_B = ax.bar(x + width / 2, [results_B_L1[m] for m in months], width, label='Model B L1', color='red', alpha=0.7)
ax.set_title('L1 Peak at Measurement Points')
ax.set_ylabel('L1 Peak Activation')
ax.set_xticks(x)
ax.set_xticklabels([f'Month {m}' for m in months])
ax.legend()
ax.set_ylim(0, 1.0)

plt.tight_layout()
plt.savefig('dual_route_comparison.png', dpi=150)
plt.show()

print("\n===== Simulation Complete =====")
print("Chart saved as 'dual_route_comparison.png'")