"""
Polariton Wave Solver
- Pseudospectral method for 2D wave propagation
- Graphene plasmon + hBN phonon polariton hybridization modeling
- Serpentine waveguide geometry with path-dependent phase accumulation
"""

import numpy as np
from scipy.fft import fft2, ifft2, fftfreq


class PolaritonWaveSolver:
    def __init__(self, config):
        self.config = config
        
        # Grid setup
        self.Nx = config.Nx
        self.Ny = config.Ny
        self.Lx = config.Lx
        self.Ly = config.Ly
        self.dx = self.Lx / self.Nx
        self.dy = self.Ly / self.Ny
        
        # Coordinate grids
        self.x = np.linspace(-self.Lx/2, self.Lx/2, self.Nx)
        self.y = np.linspace(-self.Ly/2, self.Ly/2, self.Ny)
        self.X, self.Y = np.meshgrid(self.x, self.y, indexing='xy')
        
        # Wave number grid for pseudospectral method
        self.kx = 2 * np.pi * fftfreq(self.Nx, d=self.dx)
        self.ky = 2 * np.pi * fftfreq(self.Ny, d=self.dy)
        self.KX, self.KY = np.meshgrid(self.kx, self.ky, indexing='xy')
        self.K2 = self.KX**2 + self.KY**2
        
        # Material properties
        self.k0 = config.k0
        self.k_plasmon = self.k0 * (1.8 + 0.3j)   # Graphene plasmon effective (Kubo-inspired)
        
        # hBN coupling zone (rectangular slab)
        self.hbn_mask = self._create_hbn_mask()
        
        # Serpentine waveguide mask (thick channel)
        self.waveguide_mask = self._create_serpentine_waveguide()
        
        print("PolaritonWaveSolver initialized.")

    def _create_hbn_mask(self):
        """hBN phonon polariton coupling zone"""
        mask = np.zeros((self.Ny, self.Nx), dtype=bool)
        x_c, y_c = 8.0, 0.0
        width, height = 12.0, 8.0
        mask |= (np.abs(self.X - x_c) < width/2) & (np.abs(self.Y - y_c) < height/2)
        return mask

    def _create_serpentine_waveguide(self):
        """Serpentine graphene waveguide (piecewise + sinusoidal modulation)"""
        # Base serpentine path: y = f(x)
        y_path = (0.8 * np.sin(0.7 * self.X) + 
                  0.35 * np.sin(1.9 * self.X) + 
                  0.12 * self.X)
        
        # Waveguide thickness
        thickness = 1.8
        mask = np.abs(self.Y - y_path) < thickness
        
        # Add some piecewise linear feeling (extra modulation)
        mask |= np.abs(self.Y - y_path - 0.8 * np.sin(0.4 * self.X)) < 0.6
        
        return mask

    def _get_path_dependent_phase(self, phi_source, source_pos):
        """Path-dependent phase accumulation along serpentine waveguide"""
        # Approximate path length from source
        dist = np.sqrt((self.X - source_pos[0])**2 + (self.Y - source_pos[1])**2)
        
        # Add serpentine modulation effect
        serpentine_mod = 0.4 * np.sin(1.2 * self.X) + 0.25 * np.sin(2.5 * self.X)
        
        phase = self.k_plasmon.real * dist + serpentine_mod + phi_source
        return phase

    def propagate(self, phi_A=0.0, phi_B=0.0, amp_A=1.0, amp_B=0.58):
        """
        Propagate two phase-controlled sources
        Returns total complex field E_total
        """
        E = np.zeros((self.Ny, self.Nx), dtype=complex)
        
        # Source A contribution
        phase_A = self._get_path_dependent_phase(phi_A, self.config.source_A_pos)
        contrib_A = amp_A * np.exp(1j * phase_A)
        E += contrib_A * self.waveguide_mask.astype(complex)
        
        # Source B contribution
        phase_B = self._get_path_dependent_phase(phi_B, self.config.source_B_pos)
        contrib_B = amp_B * np.exp(1j * phase_B)
        E += contrib_B * self.waveguide_mask.astype(complex)
        
        # Apply hBN hybridization effect (stronger confinement + loss)
        E[self.hbn_mask] *= (1.0 + 0.8j)   # anisotropic polariton enhancement + absorption
        
        # Mild damping (graphene loss)
        E *= np.exp(-0.08 * np.abs(self.X))
        
        # Pseudospectral propagation (simple free space + plasmon dispersion approximation)
        E_fft = fft2(E)
        # Apply dispersion operator (mild low-pass + plasmon-like)
        propagator = np.exp(-0.02 * self.K2**0.5) * np.exp(1j * 0.3 * self.K2**0.5)
        E_fft *= propagator
        E = ifft2(E_fft)
        
        return E
