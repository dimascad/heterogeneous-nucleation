# Heterogeneous Nucleation Visualization

Interactive visualization demonstrating how contact angle affects heterogeneous nucleation barriers in materials science.

![Heterogeneous Nucleation Animation](heterogeneous_nucleation.gif)

## 🔬 Live Demo

**[Try the Interactive Visualization](https://dimascad.github.io/heterogeneous-nucleation/)**

Use the slider to adjust the contact angle and see how it affects:
- Nucleus geometry (spherical cap shape)
- Shape factor S(θ)
- Nucleation energy barrier ΔG*

## Physics Background

### Heterogeneous vs Homogeneous Nucleation

Nucleation is the first step in phase transformations (e.g., solidification, precipitation). **Homogeneous nucleation** occurs uniformly throughout a material, while **heterogeneous nucleation** occurs at preferential sites like surfaces, grain boundaries, or impurities.

Heterogeneous nucleation is favored because it requires less energy - the nucleus forms as a **spherical cap** rather than a full sphere, reducing the total surface energy.

### The Shape Factor S(θ)

The key relationship is governed by the **shape factor**:

```
S(θ) = (2 + cos θ)(1 - cos θ)² / 4
```

This determines how much the nucleation barrier is reduced:

```
ΔG*_het = S(θ) · ΔG*_hom
```

Where:
- **θ** is the contact angle between the nucleus and substrate
- **ΔG\*_het** is the heterogeneous nucleation barrier
- **ΔG\*_hom** is the homogeneous nucleation barrier

### Contact Angle Effects

| Contact Angle | S(θ) | Barrier Reduction | Wetting |
|---------------|------|-------------------|---------|
| θ → 0° | → 0 | Nearly eliminated | Excellent |
| θ = 60° | 0.16 | 84% reduction | Good |
| θ = 90° | 0.50 | 50% reduction | Moderate |
| θ = 120° | 0.84 | 16% reduction | Poor |
| θ → 180° | → 1 | No reduction | Non-wetting |

### Surface Tension Balance

At the triple point (where nucleus, liquid, and substrate meet), Young's equation describes the force balance:

```
γ_SL = γ_SN + γ_NL · cos θ
```

Where:
- **γ_SL** = Substrate-Liquid interfacial energy
- **γ_SN** = Substrate-Nucleus interfacial energy  
- **γ_NL** = Nucleus-Liquid interfacial energy

## Visualization Panels

1. **Nucleus Geometry** (Left): Shows the spherical cap nucleus on the substrate with surface tension vectors and contact angle. The dashed circle shows the full sphere that the cap is part of, with radius r.

2. **Shape Factor S(θ)** (Middle): Plots S(θ) vs contact angle, showing how the barrier reduction factor varies from 0 to 1.

3. **Nucleation Barrier ΔG*** (Right): Compares the energy barrier curves for homogeneous (dashed) and heterogeneous (solid) nucleation. Both peak at the same critical radius r*, but the heterogeneous barrier is lower by factor S(θ).

## Running Locally

### Option 1: View the static GIF
Simply open `heterogeneous_nucleation.gif` in any image viewer.

### Option 2: Run the interactive app
```bash
pip install marimo pillow
marimo run app.py
```

### Option 3: Serve the WASM version locally
```bash
python -m http.server
# Open http://localhost:8000 in your browser
```

## Files

- `app.py` - Marimo notebook source code
- `index.html` - Exported WASM web application
- `generate_v2.py` - GIF generation script
- `heterogeneous_nucleation.gif` - Animated visualization

## References

- Porter, D.A. & Easterling, K.E., *Phase Transformations in Metals and Alloys*
- Callister, W.D., *Materials Science and Engineering: An Introduction*
