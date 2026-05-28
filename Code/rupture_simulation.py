"""
rupture_simulation.py
---------------------

Simulates a single universe cycle in the Quantized Rupture Cosmology.
Computes singularity density evolution, rupture time, excitation mode,
and entropy production.

Author: Paul Jarvis
"""

import numpy as np

class UniverseCycle:
    def __init__(self,
                 A=1.0,
                 p=2.0,
                 tau=3.0,
                 alpha=1.0,
                 rho_crit=1000.0,
                 dt=0.001):
        self.A = A
        self.p = p
        self.tau = tau
        self.alpha = alpha
        self.rho_crit = rho_crit
        self.dt = dt

        self.t = 0.0
        self.rho_s = 0.0
        self.entropy = 0.0

    def bh_rate(self, t):
        """Black hole formation rate: A t^p exp(-t/tau)."""
        return self.A * (t ** self.p) * np.exp(-t / self.tau)

    def step(self):
        """Advance the simulation by one timestep."""
        rate = self.bh_rate(self.t)
        self.rho_s += self.alpha * rate * self.dt
        self.entropy += rate * self.dt
        self.t += self.dt

    def excitation_mode(self, overshoot):
        """Quantized rupture mode."""
        if overshoot < 500:
            return 1
        elif overshoot < 2000:
            return 2
        elif overshoot < 5000:
            return 3
        return 4

    def run(self):
        """Run the universe until rupture."""
        while self.rho_s < self.rho_crit:
            self.step()

        overshoot = self.rho_s - self.rho_crit
        m = self.excitation_mode(overshoot)
        N = 6 * m

        return {
            "rupture_time": self.t,
            "entropy_produced": self.entropy,
            "overshoot": overshoot,
            "mode": m,
            "children": N
        }
