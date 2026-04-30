"""
Publication-quality plotting module for Polariton Interference Figures
- 4-panel intensity map
- Inset zoom on best readout zone
- Scale bar, propagation arrows, waveguide contour, hBN zone
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.colors import PowerNorm
import matplotlib.patheffects as path_effects

def plot_4panel_with_inset(solver, results, config, save_path=None):
    """
    Create publication-ready 4-panel figure with inset
    
    Parameters:
        solver: PolaritonWaveSolver instance
        results: dict of simulation results
        config: Config instance
    """
    fig, axes = plt.subplots(2, 2, figsize=config.figsize, dpi=config.dpi)
    axes = axes.ravel()
    
    inputs = [(0,0), (0,1), (1,0), (1,1)]
    titles = ['(a) 00', '(b) 01', '(c) 10', '(d) 11']
    
    # Compute intensity for all inputs
    intensities = {}
    for a, b in inputs:
        phi_A = a * np.pi
        phi_B = b * np.pi + config.phase_bias
        E = solver.propagate(phi_A=phi_A, phi_B=phi_B, 
                            amp_A=config.amp_A, amp_B=config.amp_B)
        intensities[(a,b)] = np.abs(E)**2
    
    # Global max for consistent color scale
    global_max = max([I.max() for I in intensities.values()])
    
    for i, (inp, title) in enumerate(zip(inputs, titles)):
        ax = axes[i]
        I = intensities[inp] ** 0.58          # Contrast enhancement
        
        # Main intensity plot
        im = ax.imshow(I, extent=[-config.Lx/2, config.Lx/2, -config.Ly/2, config.Ly/2],
                       origin='lower', cmap=config.cmap, 
                       norm=PowerNorm(gamma=0.6, vmin=0, vmax=global_max**0.58))
        
        # Waveguide contour
        ax.contour(solver.waveguide_mask, levels=[0.5], colors='white', 
                   linewidths=2.2, alpha=0.85, extent=[-config.Lx/2, config.Lx/2, -config.Ly/2, config.Ly/2])
        
        # hBN coupling zone
        ax.add_patch(Rectangle((2.5, -3.8), 13.0, 7.6, fill=False, 
                              edgecolor='cyan', linestyle='--', linewidth=2.0, alpha=0.9))
        
        # Readout points
        for pos in config.readout_points:
            ax.plot(pos[0], pos[1], '*', color='red', markersize=11, 
                   markeredgecolor='white', markeredgewidth=1.5)
        
        # Propagation arrow
        ax.arrow(-18, -6, 12, 1.5, head_width=1.2, head_length=1.8, 
                fc='white', ec='white', linewidth=2.0, alpha=0.8)
        
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel('x (μm)', fontsize=12)
        ax.set_ylabel('y (μm)', fontsize=12)
        ax.grid(False)
        
        # Inset in panel (b) only
        if i == 1:  # panel (b) 01
            ax_inset = ax.inset_axes([0.62, 0.58, 0.35, 0.35])
            inset_I = I
            ax_inset.imshow(inset_I, extent=[-config.Lx/2, config.Lx/2, -config.Ly/2, config.Ly/2],
                            origin='lower', cmap=config.cmap, 
                            norm=PowerNorm(gamma=0.6))
            
            # Waveguide & hBN in inset
            ax_inset.contour(solver.waveguide_mask, levels=[0.5], colors='white', linewidths=1.8)
            ax_inset.add_patch(Rectangle((2.5, -3.8), 13.0, 7.6, fill=False, 
                                        edgecolor='cyan', linestyle='--', linewidth=1.8))
            
            # Highlight best readout zone
            ax_inset.set_xlim(-18.5, -11.0)
            ax_inset.set_ylim(-5.0, 3.0)
            ax_inset.set_xticks([])
            ax_inset.set_yticks([])
            ax_inset.set_title("Best Readout Zone", fontsize=9, pad=4)
            
            # Zoom indicator
            ax.indicate_inset_zoom(ax_inset, edgecolor="yellow", linewidth=2.0, alpha=0.9)
    
    # Colorbar
    cbar = fig.colorbar(im, ax=axes.ravel().tolist(), shrink=0.75, pad=0.03)
    cbar.set_label('|E|² (normalized)', fontsize=13)
    
    # Scale bar
    scale_x = -19
    scale_y = -14
    ax = axes[3]
    ax.plot([scale_x, scale_x+5], [scale_y, scale_y], 'w-', linewidth=4)
    ax.text(scale_x + 2.5, scale_y - 1.2, '5 μm', color='white', 
            ha='center', va='top', fontsize=11, fontweight='bold',
            path_effects=[path_effects.withStroke(linewidth=3, foreground='black')])
    
    fig.suptitle('Graphene-hBN Hybrid Plasmon-Phonon Polariton Interference\n'
                 'for Wave-based Functional Synaptic Integration', 
                 fontsize=16, fontweight='bold', y=0.96)
    
    plt.tight_layout(rect=[0, 0, 1, 0.94])
    
    if save_path:
        plt.savefig(save_path, dpi=config.dpi, bbox_inches='tight')
        print(f"Figure saved: {save_path}")
    
    return fig
