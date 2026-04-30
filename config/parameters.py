"""
Configuration parameters for Graphene-hBN Polariton Neuromorphic Simulation
"""

import numpy as np

class Config:
    def __init__(self):
        # Grid parameters
        self.Nx = 420
        self.Ny = 320
        self.Lx = 42.0   # μm
        self.Ly = 32.0   # μm
        
        # Source positions (strong asymmetry)
        self.source_A_pos = np.array([-13.5, -3.2])
        self.source_B_pos = np.array([12.0, 4.8])
        
        # Amplitudes
        self.amp_A = 1.00
        self.amp_B = 0.58
        
        # Phase control
        self.phase_bias = np.pi / 2.15
        
        # Wave parameters
        self.freq = 5.0          # THz
        self.k0 = 3.0            # base wave number (effective)
        self.alpha = 6.5         # tanh mapping steepness
        
        # Readout positions (multi-readout for robustness)
        self.readout_points = [
            np.array([-16.2, -1.8]),
            np.array([-13.5,  2.1]),
            np.array([  7.8, -3.5]),
            np.array([ 10.5,  4.2])
        ]
        
        # Figure settings
        self.figsize = (14, 11)
        self.dpi = 300
        self.cmap = 'viridis'
        
    def print_info(self):
        print("=== Simulation Configuration ===")
        print(f"Grid: {self.Nx} × {self.Ny} ({self.Lx}μm × {self.Ly}μm)")
        print(f"Source A: {self.source_A_pos}, amp={self.amp_A}")
        print(f"Source B: {self.source_B_pos}, amp={self.amp_B}")
        print(f"Phase bias: {self.phase_bias:.3f} rad")
        print(f"Readout points: {len(self.readout_points)} locations")
        print(f"tanh alpha: {self.alpha}")
        print("===============================\n")
