"""
Graphene-hBN Hybrid Polariton Waveguide for Wave-based Neuromorphic Computing
- Plasmon-phonon polariton hybridization
- Serpentine waveguide geometry
- Input-dependent interference → EPSP/IPSP-like mapping
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from utils.wave_solver import PolaritonWaveSolver
from utils.materials import graphene_kubo_effective, hbn_anisotropic
from utils.plotting import plot_4panel_with_inset

# ====================== Parameters ======================
class Config:
    # Grid
    Nx, Ny = 400, 300
    Lx, Ly = 40.0, 30.0  # μm
    
    # Sources
    source_A_pos = np.array([-12.0, -3.0])
    source_B_pos = np.array([11.0, 4.5])
    amp_A = 1.0
    amp_B = 0.58          # tuned for (1,1) suppression
    
    # Phase
    phase_bias = np.pi / 2.15
    
    # Wave parameters (THz regime)
    k0 = 3.0              # base wave number
    alpha = 6.5           # tanh steepness
    
    # Readout positions (multi-readout)
    readout_points = [
        np.array([-15.5, -1.2]),
        np.array([-14.8, 2.5]),
        np.array([8.5, -4.0]),
        np.array([9.2, 5.1])
    ]

# ====================== Main ======================
def main():
    config = Config()
    solver = PolaritonWaveSolver(config)
    
    inputs = [(0,0), (0,1), (1,0), (1,1)]
    results = {}
    
    print("Running 4 input combinations...\n")
    
    for a, b in inputs:
        phi_A = a * np.pi
        phi_B = b * np.pi + config.phase_bias
        
        E_total = solver.propagate(phi_A, phi_B, amp_A=config.amp_A, amp_B=config.amp_B)
        I = np.abs(E_total)**2
        
        # Multi-readout
        intensities = [I[int(p[1]), int(p[0])] for p in config.readout_points]  # grid index 변환 필요 (실제 코드에서는 interpolation 권장)
        avg_I = np.mean(intensities)
        Vout = np.tanh(config.alpha * avg_I)
        binary = 1 if Vout > 0.5 else 0
        
        results[(a,b)] = {
            'avg_intensity': avg_I,
            'Vout': Vout,
            'binary': binary
        }
        
        print(f"Input ({a},{b}) → Avg I = {avg_I:.4f}, Vout = {Vout:.4f}, Binary = {binary}")
    
    # Figure 생성
    fig = plot_4panel_with_inset(solver, results, config)
    fig.savefig("figures/polariton_interference_final_with_inset.png", dpi=300, bbox_inches='tight')
    plt.show()
    
    print("\nSimulation completed. Figure saved to figures/")

if __name__ == "__main__":
    main()
