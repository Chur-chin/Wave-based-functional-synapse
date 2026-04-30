# COMSOL Multiphysics Setup Guide for Graphene-hBN Polariton Synapse

## 1. Model Wizard
- Space Dimension: 2D
- Physics: Electromagnetic Waves, Frequency Domain (emw)
- Study: Frequency Domain + Parametric Sweep

## 2. Geometry
- Graphene Serpentine Waveguide
  - Width: 1.2 ~ 1.8 μm
  - Length: ~35 μm
  - Shape: Spline or Piecewise Line (6~8 bends) + sinusoidal modulation
- hBN Slab: Rectangle (width 10~15 μm, height 6~8 μm) at center-right

## 3. Materials
**Graphene** (Surface Current):
- Surface Conductivity → Kubo formula (user-defined)
  - Fermi level: 0.3 ~ 0.6 eV (tunable)
  - Scattering rate: 10~20 meV
  - Frequency: 1~10 THz

**hBN** (Anisotropic):
- Relative permittivity tensor:
  - ε_xx = ε_yy = 1 + f(ω)   (Reststrahlen band: negative ε region)
  - ε_zz = 3.0 ~ 5.0
- Use "User Defined" with imaginary part for loss

## 4. Physics Settings
- Two Ports (Port 1 = Source A, Port 2 = Source B)
  - Port type: Numeric
  - Phase: Parametric (0 or π for binary input)
- Perfectly Matched Layer (PML) on all boundaries

## 5. Study
- Parametric Sweep:
  - Parameter: phi_B (0, π)
  - Combine with input combinations (00, 01, 10, 11)

## 6. Results
- Plot: emw.Ez, emw.normE ( |E|² )
- 4-panel figure export
- Line integration or point probe at readout zones
- Export intensity data for MATLAB/Python post-processing

## Recommended Parameters
- Frequency: 5 THz (mid-THz)
- Mesh: Extremely fine in waveguide and hBN region
- Solver: Direct (MUMPS) or Iterative

## Next
- Add nonlinear mapping (tanh) in MATLAB LiveLink
- Fermi level sweep for active tuning
