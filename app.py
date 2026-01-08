# ================================================================
# HETEROGENEOUS NUCLEATION - FULLY INTEGRATED NOTEBOOK
# ================================================================
# 
# Complete structure with physics, derivations, and visualization
#
# PART 1: THE PHYSICS (Cells 1-13)
#   - Why nucleation has a barrier
#   - Why surfaces help
#   - Surface tension balance
#
# PART 2: THE DERIVATION (Cells 14-22)
#   - Step 1: Spherical cap geometry
#   - Step 2: Volume calculus
#   - Step 3: Shape factor
#   - Step 4: Energy barrier
#
# PART 3: THE COMPLETE PICTURE (Cells 23-26)
#   - Interactive 3-panel visualization
#   - Key takeaways
#
# ================================================================


# ======================= CELL 1: IMPORTS =======================
import marimo as mo


# ======================= CELL 2: TITLE AND LEARNING PATH =======================
mo.md(r"""
# Heterogeneous Nucleation: From Surface Tensions to Energy Barriers

*An interactive exploration of how surfaces catalyze phase transformations*

---

## Learning Path

| Part | Topic | Question Answered |
|------|-------|-------------------|
| **Part 1** | The Physics | *Why does nucleation have a barrier? Why do surfaces help?* |
| **Part 2** | The Derivation | *How do we calculate the shape factor S(θ)?* |
| **Part 3** | The Complete Picture | *Interactive visualization bringing it all together* |

---
""")


# ======================= CELL 3: PART 1 HEADER =======================
mo.md(r"""
# Part 1: The Physics
## *Why does nucleation have a barrier? Why do surfaces help?*
""")


# ======================= CELL 4: ENERGY COMPETITION INTRO =======================
mo.md(r"""
## 1.1 The Energy Competition: Surface vs Volume

When a nucleus forms, **two energy terms compete**:

| Term | Scales as | Effect | Why? |
|------|-----------|--------|------|
| **Surface energy** | $r^2$ (area) | **Cost** ↑ | Creating interface requires energy |
| **Volume energy** | $r^3$ (volume) | **Benefit** ↓ | New phase is more stable |

This competition creates a **critical radius $r^*$** - the tipping point between growth and dissolution.
""")


# ======================= CELL 5: ENERGY COMPETITION SLIDER =======================
r_competition_slider = mo.ui.slider(
    start=0.05,
    stop=2.0,
    step=0.01,
    value=0.5,
    label="Nucleus radius r"
)
r_competition_slider


# ======================= CELL 6: ENERGY COMPETITION VISUALIZATION =======================
import math

r_comp = r_competition_slider.value
r_star = 1.0

gamma = 1.0
deltaGv = 2.0

surface_energy = 4 * math.pi * r_comp * r_comp * gamma
volume_energy = (4/3) * math.pi * r_comp * r_comp * r_comp * deltaGv
total_deltaG = surface_energy - volume_energy

surface_at_rstar = 4 * math.pi * r_star * r_star * gamma
volume_at_rstar = (4/3) * math.pi * r_star * r_star * r_star * deltaGv
deltaG_star = surface_at_rstar - volume_at_rstar

max_energy = max(surface_at_rstar * 1.8, volume_at_rstar * 1.8)
surface_height = (surface_energy / max_energy) * 180
volume_height = (volume_energy / max_energy) * 180

surface_dominates = surface_energy > volume_energy
ratio = surface_energy / max(volume_energy, 0.001)

is_subcritical = r_comp < r_star * 0.95
is_critical = r_star * 0.95 <= r_comp <= r_star * 1.05
is_supercritical = r_comp > r_star * 1.05

state_color = "#f87171" if is_subcritical else "#facc15" if is_critical else "#22c55e"
winner_text = "EQUAL (r = r*)" if is_critical else "↑ SURFACE WINS → Shrinks" if surface_dominates else "↓ VOLUME WINS → Grows"
winner_bg = "#422006" if is_critical else "#450a0a" if surface_dominates else "#052e16"

def generate_curve_points(curve_type, max_e):
    points = []
    for i in range(1, 201):
        x = i * 0.01 * 2
        if curve_type == 'surface':
            y = 4 * math.pi * x * x * gamma
        elif curve_type == 'volume':
            y = (4/3) * math.pi * x * x * x * deltaGv
        else:
            y = 4 * math.pi * x * x * gamma - (4/3) * math.pi * x * x * x * deltaGv
        svg_x = 50 + x * 130
        svg_y = 200 - (y / max_e) * 150 if curve_type != 'total' else 160 - (y / deltaG_star) * 70
        points.append(f"{svg_x},{svg_y}")
    return " ".join(points)

surface_curve = generate_curve_points('surface', max_energy)
volume_curve = generate_curve_points('volume', max_energy)

surface_dot_x = 50 + r_comp * 130
surface_dot_y = 200 - (surface_energy / max_energy) * 150
volume_dot_x = 50 + r_comp * 130
volume_dot_y = 200 - (volume_energy / max_energy) * 150

html = f'''
<div style="background: #0f172a; padding: 20px; border-radius: 12px; font-family: system-ui, sans-serif; color: #fff;">
  <div style="display: flex; gap: 20px; flex-wrap: wrap;">
    <div style="flex: 1; min-width: 280px;">
      <div style="background: #1e293b; border-radius: 8px; padding: 16px;">
        <div style="color: #94a3b8; font-size: 14px; margin-bottom: 16px; text-align: center;">
          Energy Magnitude at r = {r_comp:.2f}
        </div>
        <div style="display: flex; justify-content: center; align-items: flex-end; height: 220px; gap: 50px;">
          <div style="display: flex; flex-direction: column; align-items: center;">
            <div style="color: #f87171; font-size: 13px; margin-bottom: 4px;">{surface_energy:.2f}</div>
            <div style="width: 70px; height: {max(surface_height, 4):.0f}px; background: #f87171; border-radius: 4px 4px 0 0; display: flex; align-items: center; justify-content: center;">
              <span style="font-size: 20px;">↑</span>
            </div>
            <div style="margin-top: 8px; text-align: center;">
              <div style="color: #f87171; font-size: 14px; font-weight: bold;">Surface</div>
              <div style="color: #94a3b8; font-size: 12px;">4πr²γ</div>
              <div style="color: #64748b; font-size: 11px;">∝ r²</div>
            </div>
          </div>
          <div style="display: flex; flex-direction: column; align-items: center;">
            <div style="color: #22c55e; font-size: 13px; margin-bottom: 4px;">{volume_energy:.2f}</div>
            <div style="width: 70px; height: {max(volume_height, 4):.0f}px; background: #22c55e; border-radius: 4px 4px 0 0; display: flex; align-items: center; justify-content: center;">
              <span style="font-size: 20px;">↓</span>
            </div>
            <div style="margin-top: 8px; text-align: center;">
              <div style="color: #22c55e; font-size: 14px; font-weight: bold;">Volume</div>
              <div style="color: #94a3b8; font-size: 12px;">⁴⁄₃πr³ΔGᵥ</div>
              <div style="color: #64748b; font-size: 11px;">∝ r³</div>
            </div>
          </div>
        </div>
        <div style="margin-top: 16px; padding: 12px; border-radius: 6px; background: {winner_bg}; border: 1px solid {state_color}; text-align: center;">
          <div style="font-size: 12px; color: #94a3b8;">Which dominates?</div>
          <div style="font-size: 16px; font-weight: bold; color: {state_color}; margin-top: 4px;">{winner_text}</div>
          <div style="font-size: 11px; color: #64748b; margin-top: 4px;">Ratio: {ratio:.2f} : 1</div>
        </div>
      </div>
    </div>
    <div style="flex: 1; min-width: 340px;">
      <div style="background: #1e293b; border-radius: 8px; padding: 16px;">
        <div style="color: #94a3b8; font-size: 14px; margin-bottom: 8px; text-align: center;">Why r³ Eventually Wins</div>
        <svg width="340" height="230" viewBox="0 0 340 230">
          <line x1="50" y1="200" x2="320" y2="200" stroke="#334155" stroke-width="1"/>
          <line x1="50" y1="30" x2="50" y2="200" stroke="#334155" stroke-width="1"/>
          <line x1="{50 + r_star * 130}" y1="30" x2="{50 + r_star * 130}" y2="200" stroke="#facc15" stroke-width="1.5" stroke-dasharray="4,4" opacity="0.6"/>
          <text x="{50 + r_star * 130}" y="215" fill="#facc15" font-size="11" text-anchor="middle">r*</text>
          <polyline points="{surface_curve}" fill="none" stroke="#f87171" stroke-width="2.5"/>
          <polyline points="{volume_curve}" fill="none" stroke="#22c55e" stroke-width="2.5"/>
          <circle cx="{surface_dot_x}" cy="{surface_dot_y}" r="7" fill="#f87171" stroke="#fff" stroke-width="2"/>
          <circle cx="{volume_dot_x}" cy="{volume_dot_y}" r="7" fill="#22c55e" stroke="#fff" stroke-width="2"/>
          <line x1="{surface_dot_x}" y1="{surface_dot_y}" x2="{volume_dot_x}" y2="{volume_dot_y}" stroke="{state_color}" stroke-width="2" stroke-dasharray="4,2"/>
          <text x="290" y="120" fill="#f87171" font-size="12">r² (surface)</text>
          <text x="290" y="70" fill="#22c55e" font-size="12">r³ (volume)</text>
          <text x="185" y="225" fill="#94a3b8" font-size="11" text-anchor="middle">Radius r</text>
        </svg>
        <div style="margin-top: 8px; padding: 10px; background: #0f172a; border-radius: 6px; font-size: 12px; color: #94a3b8; line-height: 1.6;">
          <strong style="color: #e2e8f0;">Key insight:</strong><br>
          • Small r: r² > r³ → <span style="color: #f87171;">surface dominates</span><br>
          • Large r: r³ > r² → <span style="color: #22c55e;">volume dominates</span><br>
          • At r*: They're equal → the tipping point!
        </div>
      </div>
    </div>
  </div>
  <div style="margin-top: 16px; padding: 16px; background: #334155; border-radius: 8px;">
    <div style="text-align: center; margin-bottom: 8px;">
      <span style="color: #f87171; font-size: 15px;">Surface (+{surface_energy:.2f})</span>
      <span style="color: #64748b; margin: 0 12px;">−</span>
      <span style="color: #22c55e; font-size: 15px;">Volume (−{volume_energy:.2f})</span>
      <span style="color: #64748b; margin: 0 12px;">=</span>
      <span style="color: #a78bfa; font-size: 18px; font-weight: bold;">ΔG = {total_deltaG:.2f}</span>
    </div>
    <div style="text-align: center; color: {state_color}; font-size: 14px;">
      {"Net energy INCREASES with r → system wants to SHRINK" if is_subcritical else "Net energy at MAXIMUM → critical point" if is_critical else "Net energy DECREASES with r → system wants to GROW"}
    </div>
  </div>
</div>
'''
mo.Html(html)


# ======================= CELL 7: NUCLEUS FATE INTRO =======================
mo.md(r"""
## 1.2 The Fate of a Nucleus

The critical radius $r^*$ is where the energy curve peaks. This determines whether a nucleus survives or dies:

- $r < r^*$: System lowers energy by shrinking → nucleus **dissolves**
- $r = r^*$: At the peak → unstable equilibrium (tipping point)
- $r > r^*$: System lowers energy by growing → nucleus **survives**

*Drag the slider to see the nucleus fate change:*
""")


# ======================= CELL 8: NUCLEUS FATE SLIDER =======================
r_fate_slider = mo.ui.slider(
    start=0.05,
    stop=2.0,
    step=0.01,
    value=0.5,
    label="Nucleus radius r"
)
r_fate_slider


# ======================= CELL 9: NUCLEUS FATE VISUALIZATION =======================
r_fate = r_fate_slider.value
r_star_fate = 1.0

gamma_f = 1.0
deltaGv_f = 2.0
surface_f = 4 * math.pi * r_fate * r_fate * gamma_f
volume_f = (4/3) * math.pi * r_fate * r_fate * r_fate * deltaGv_f
deltaG_f = surface_f - volume_f
deltaG_star_f = 4 * math.pi * r_star_fate**2 * gamma_f - (4/3) * math.pi * r_star_fate**3 * deltaGv_f

is_sub = r_fate < r_star_fate * 0.95
is_crit = r_star_fate * 0.95 <= r_fate <= r_star_fate * 1.05
is_super = r_fate > r_star_fate * 1.05

nucleus_color = "#f87171" if is_sub else "#facc15" if is_crit else "#22c55e"
fate_text = "SHRINKS (dissolves)" if is_sub else "CRITICAL (tipping point)" if is_crit else "GROWS (survives!)"
arrow_dir = "←" if is_sub else "⟷" if is_crit else "→"
fate_explanation = "Surface energy dominates → system lowers energy by shrinking" if is_sub else "At the peak → unstable equilibrium, could go either way" if is_crit else "Volume energy dominates → system lowers energy by growing"
fate_bg = "#450a0a" if is_sub else "#422006" if is_crit else "#052e16"

ball_x = 60 + r_fate * 130
ball_y_f = 180 - (deltaG_f / deltaG_star_f) * 100

nucleus_size = 30 + r_fate * 50
r_star_size = 30 + r_star_fate * 50

curve_points_fate = []
for i in range(1, 201):
    x = i * 0.01 * 2
    s = 4 * math.pi * x * x * gamma_f
    v = (4/3) * math.pi * x * x * x * deltaGv_f
    y = s - v
    svg_x = 60 + x * 130
    svg_y = 180 - (y / deltaG_star_f) * 100
    curve_points_fate.append(f"{svg_x},{svg_y}")
curve_path = " ".join(curve_points_fate)

arrow_left_points = f"{ball_x - 28},{ball_y_f} {ball_x - 40},{ball_y_f - 7} {ball_x - 40},{ball_y_f + 7}"
arrow_right_points = f"{ball_x + 28},{ball_y_f} {ball_x + 40},{ball_y_f - 7} {ball_x + 40},{ball_y_f + 7}"

html_fate = f'''
<div style="background: #0f172a; padding: 20px; border-radius: 12px; font-family: system-ui, sans-serif; color: #fff;">
  <div style="display: flex; gap: 20px; flex-wrap: wrap;">
    <div style="flex: 1; min-width: 320px;">
      <div style="background: #1e293b; border-radius: 8px; padding: 16px; text-align: center;">
        <div style="color: #94a3b8; font-size: 13px; margin-bottom: 8px;">Energy Landscape (ball on a hill)</div>
        <svg width="340" height="220" viewBox="0 0 340 220">
          <rect x="60" y="60" width="{r_star_fate * 130}" height="120" fill="#f87171" opacity="0.1"/>
          <rect x="{60 + r_star_fate * 130}" y="60" width="130" height="120" fill="#22c55e" opacity="0.1"/>
          <text x="125" y="75" fill="#f87171" font-size="11" text-anchor="middle">Shrinks</text>
          <text x="255" y="75" fill="#22c55e" font-size="11" text-anchor="middle">Grows</text>
          <line x1="60" y1="180" x2="320" y2="180" stroke="#475569" stroke-width="1"/>
          <line x1="{60 + r_star_fate * 130}" y1="60" x2="{60 + r_star_fate * 130}" y2="195" stroke="#facc15" stroke-width="2" stroke-dasharray="6,4" opacity="0.7"/>
          <text x="{60 + r_star_fate * 130}" y="210" fill="#facc15" font-size="13" text-anchor="middle" font-weight="bold">r*</text>
          <polyline points="{curve_path}" fill="none" stroke="#a78bfa" stroke-width="3.5"/>
          <circle cx="{ball_x}" cy="{ball_y_f}" r="14" fill="{nucleus_color}"/>
          {"<polygon points='" + arrow_left_points + "' fill='" + nucleus_color + "'/>" if is_sub else ""}
          {"<polygon points='" + arrow_right_points + "' fill='" + nucleus_color + "'/>" if is_super else ""}
          {"<polygon points='" + arrow_left_points + "' fill='" + nucleus_color + "' opacity='0.4'/><polygon points='" + arrow_right_points + "' fill='" + nucleus_color + "' opacity='0.4'/>" if is_crit else ""}
          <text x="190" y="205" fill="#94a3b8" font-size="11" text-anchor="middle">Radius r</text>
          <text x="45" y="130" fill="#a78bfa" font-size="11" text-anchor="middle" transform="rotate(-90, 45, 130)">ΔG</text>
          <text x="330" y="{180 - 100}" fill="#a78bfa" font-size="10">ΔG*</text>
        </svg>
      </div>
    </div>
    <div style="flex: 1; min-width: 250px;">
      <div style="background: #1e293b; border-radius: 8px; padding: 16px; text-align: center; height: 100%; display: flex; flex-direction: column;">
        <div style="color: #94a3b8; font-size: 13px; margin-bottom: 8px;">Nucleus Size</div>
        <div style="flex: 1; display: flex; align-items: center; justify-content: center; position: relative; min-height: 140px;">
          <div style="position: absolute; width: {r_star_size}px; height: {r_star_size}px; border-radius: 50%; border: 2px dashed #facc15; opacity: 0.4;"></div>
          <div style="width: {nucleus_size}px; height: {nucleus_size}px; border-radius: 50%; background: {nucleus_color}; display: flex; align-items: center; justify-content: center; box-shadow: 0 0 {20 + r_fate * 15}px {nucleus_color}40; transition: all 0.1s;">
            <span style="font-size: {max(16, nucleus_size * 0.35)}px; color: #000; font-weight: bold; opacity: 0.6;">{arrow_dir}</span>
          </div>
        </div>
        <div style="color: #facc15; font-size: 11px; margin-top: 8px; opacity: 0.7;">Dashed = critical size (r*)</div>
      </div>
    </div>
  </div>
  <div style="margin-top: 16px; padding: 16px; border-radius: 8px; background: {fate_bg}; border: 2px solid {nucleus_color}; text-align: center;">
    <div style="font-size: 13px; color: #94a3b8; margin-bottom: 4px;">
      r = {r_fate:.2f} {"<" if is_sub else "≈" if is_crit else ">"} r* = {r_star_fate:.1f}
    </div>
    <div style="font-size: 22px; font-weight: bold; color: {nucleus_color};">{fate_text}</div>
    <div style="font-size: 12px; color: #94a3b8; margin-top: 8px;">{fate_explanation}</div>
  </div>
  <div style="margin-top: 12px; display: flex; justify-content: center; gap: 24px; color: #94a3b8; font-size: 13px;">
    <span>ΔG/ΔG* = <strong style="color: #a78bfa;">{deltaG_f / deltaG_star_f:.3f}</strong></span>
    <span>r/r* = <strong style="color: {nucleus_color};">{r_fate / r_star_fate:.2f}</strong></span>
  </div>
</div>
'''
mo.Html(html_fate)


# ======================= CELL 10: SURFACE TENSION INTRO =======================
mo.md(r"""
## 1.3 Surface Tension Balance → Contact Angle θ

On a **surface**, the nucleus forms a **spherical cap** instead of a full sphere. The shape is determined by **three surface tensions** pulling at the contact point:

| Tension | Interface | What it represents |
|---------|-----------|-------------------|
| $\gamma_{SL}$ | Substrate-Liquid | Energy of original interface |
| $\gamma_{SN}$ | Substrate-Nucleus | Energy where nucleus wets substrate |
| $\gamma_{NL}$ | Nucleus-Liquid | Energy of the curved cap surface |

These balance according to **Young's Equation**: 

$$\gamma_{SL} = \gamma_{SN} + \gamma_{NL} \cos\theta$$

*Adjust the surface tensions to see how they determine θ:*
""")


# ======================= CELL 11: SURFACE TENSION SLIDERS =======================
gamma_sl_slider = mo.ui.slider(start=10, stop=90, step=1, value=50)
gamma_sn_slider = mo.ui.slider(start=10, stop=90, step=1, value=30)
gamma_nl_slider = mo.ui.slider(start=10, stop=90, step=1, value=40)

mo.vstack([
    mo.md("**Surface Tensions (arbitrary units):**"),
    mo.hstack([
        mo.vstack([mo.md("$\\\\gamma_{SL}$ (Solid-Liquid)"), gamma_sl_slider]),
        mo.vstack([mo.md("$\\\\gamma_{SN}$ (Solid-Nucleus)"), gamma_sn_slider]),
        mo.vstack([mo.md("$\\\\gamma_{NL}$ (Nucleus-Liquid)"), gamma_nl_slider]),
    ], justify="start", gap=2)
])


# ======================= CELL 12: SURFACE TENSION VISUALIZATION =======================
gamma_sl = gamma_sl_slider.value
gamma_sn = gamma_sn_slider.value
gamma_nl = gamma_nl_slider.value

cos_theta_y = (gamma_sl - gamma_sn) / gamma_nl
cos_theta_y = max(-1, min(1, cos_theta_y))

theta_rad_y = math.acos(cos_theta_y)
theta_deg_y = theta_rad_y * 180 / math.pi

S_y = ((2 + cos_theta_y) * (1 - cos_theta_y)**2) / 4

if theta_deg_y < 30:
    wetting = "Excellent"
    wetting_color = "#22c55e"
elif theta_deg_y < 60:
    wetting = "Good"
    wetting_color = "#22c55e"
elif theta_deg_y < 90:
    wetting = "Moderate"
    wetting_color = "#facc15"
elif theta_deg_y < 120:
    wetting = "Poor"
    wetting_color = "#f97316"
else:
    wetting = "Very Poor"
    wetting_color = "#f87171"

center_x = 200
center_y = 140
contact_x = center_x + 70 * math.sin(theta_rad_y)

vec_scale = 1.3
gamma_sl_end_x = contact_x + gamma_sl * vec_scale
gamma_sn_end_x = contact_x - gamma_sn * vec_scale
gamma_nl_end_x = contact_x - gamma_nl * vec_scale * math.cos(theta_rad_y)
gamma_nl_end_y = center_y - gamma_nl * vec_scale * math.sin(theta_rad_y)

R_cap = 70
cap_left_x = center_x - R_cap * math.sin(theta_rad_y)
cap_right_x = center_x + R_cap * math.sin(theta_rad_y)
large_arc_y = 1 if theta_deg_y > 90 else 0
cap_path = f"M {cap_left_x} {center_y} A {R_cap} {R_cap} 0 {large_arc_y} 1 {cap_right_x} {center_y} Z"

# Contact angle arc - from substrate (pointing LEFT) to tangent of nucleus
arc_r = 35
arc_start_x = contact_x - arc_r  # pointing left along substrate
arc_start_y = center_y
arc_end_angle = 180 - theta_deg_y
arc_end_x = contact_x + arc_r * math.cos(math.radians(arc_end_angle))
arc_end_y = center_y - arc_r * math.sin(math.radians(arc_end_angle))

html_tension = f'''
<div style="background: #0f172a; padding: 20px; border-radius: 12px; font-family: system-ui, sans-serif; color: #fff;">
  <div style="display: flex; gap: 20px; flex-wrap: wrap;">
    <div style="flex: 0 0 260px;">
      <div style="background: #1e293b; border-radius: 8px; padding: 16px;">
        <div style="background: #0f172a; padding: 12px; border-radius: 6px; margin-bottom: 16px;">
          <div style="color: #94a3b8; font-size: 11px; margin-bottom: 8px; text-align: center;">Young's Equation</div>
          <div style="font-family: monospace; font-size: 13px; text-align: center; line-height: 1.8;">
            <span style="color: #ffffff;">γ<sub>SL</sub></span> = 
            <span style="color: #000000; background: #888; padding: 0 3px; border-radius: 2px;">γ<sub>SN</sub></span> + 
            <span style="color: #ffd700;">γ<sub>NL</sub></span>·cos<span style="color: #64ff96;">θ</span>
          </div>
          <div style="font-family: monospace; font-size: 11px; text-align: center; margin-top: 8px; color: #94a3b8;">
            cos<span style="color: #64ff96;">θ</span> = (<span style="color: #ffffff;">{gamma_sl}</span> - <span style="color: #888888;">{gamma_sn}</span>) / <span style="color: #ffd700;">{gamma_nl}</span> = {cos_theta_y:.3f}
          </div>
        </div>
        <div style="font-size: 12px; line-height: 2; margin-bottom: 16px;">
          <div><span style="color: #ffffff;">■ γ<sub>SL</sub></span> Solid-Liquid (pulls right)</div>
          <div><span style="color: #555555; background: #888; padding: 0 4px; border-radius: 2px;">■ γ<sub>SN</sub></span> Solid-Nucleus (pulls left)</div>
          <div><span style="color: #ffd700;">■ γ<sub>NL</sub></span> Nucleus-Liquid (along cap)</div>
        </div>
        <div style="background: #334155; padding: 10px; border-radius: 6px; font-size: 11px; color: #94a3b8;">
          <strong style="color: #e2e8f0;">Try this:</strong><br>
          Increase γ<sub>SL</sub> → <span style="color: #64ff96;">θ</span> decreases → better wetting!
        </div>
      </div>
    </div>
    <div style="flex: 1; min-width: 380px;">
      <div style="background: #1e293b; border-radius: 8px; padding: 16px;">
        <svg width="100%" height="260" viewBox="0 0 400 260">
          <defs>
            <marker id="arrW" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
              <path d="M0,0 L0,6 L6,3 z" fill="#ffffff"/>
            </marker>
            <marker id="arrK" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
              <path d="M0,0 L0,6 L6,3 z" fill="#000000"/>
            </marker>
            <marker id="arrGold" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
              <path d="M0,0 L0,6 L6,3 z" fill="#ffd700"/>
            </marker>
          </defs>
          <rect x="0" y="{center_y}" width="400" height="120" fill="#334155"/>
          <line x1="0" y1="{center_y}" x2="400" y2="{center_y}" stroke="#f97316" stroke-width="3"/>
          <text x="360" y="{center_y + 20}" fill="#f97316" font-size="11">substrate</text>
          <text x="30" y="40" fill="#94a3b8" font-size="12">Liquid</text>
          <path d="{cap_path}" fill="rgba(255, 130, 170, 0.5)" stroke="#ff82aa" stroke-width="2"/>
          <text x="{center_x}" y="{center_y - 45 - (30 if theta_deg_y > 90 else 0)}" fill="#ff82aa" font-size="12" text-anchor="middle">Nucleus</text>
          <circle cx="{contact_x}" cy="{center_y}" r="5" fill="#fff"/>
          
          <!-- γ_SL: WHITE (solid-liquid) pointing right -->
          <line x1="{contact_x}" y1="{center_y}" x2="{gamma_sl_end_x}" y2="{center_y}" stroke="#ffffff" stroke-width="4" marker-end="url(#arrW)"/>
          <text x="{contact_x + gamma_sl * 0.65}" y="{center_y - 10}" fill="#ffffff" font-size="11" text-anchor="middle">γ<tspan baseline-shift="sub" font-size="8">SL</tspan></text>
          
          <!-- γ_SN: BLACK (solid-nucleus) pointing left -->
          <line x1="{contact_x}" y1="{center_y}" x2="{gamma_sn_end_x}" y2="{center_y}" stroke="#000000" stroke-width="4" marker-end="url(#arrK)"/>
          <text x="{contact_x - gamma_sn * 0.65}" y="{center_y - 10}" fill="#888888" font-size="11" text-anchor="middle">γ<tspan baseline-shift="sub" font-size="8">SN</tspan></text>
          
          <!-- γ_NL: GOLD (nucleus-liquid) along cap surface -->
          <line x1="{contact_x}" y1="{center_y}" x2="{gamma_nl_end_x}" y2="{gamma_nl_end_y}" stroke="#ffd700" stroke-width="4" marker-end="url(#arrGold)"/>
          <text x="{gamma_nl_end_x - 15}" y="{gamma_nl_end_y - 8}" fill="#ffd700" font-size="11">γ<tspan baseline-shift="sub" font-size="8">NL</tspan></text>
          
          <!-- Contact angle arc: GREEN, from substrate (left) to tangent, sweep clockwise -->
          <path d="M {arc_start_x} {arc_start_y} A {arc_r} {arc_r} 0 0 1 {arc_end_x} {arc_end_y}" fill="none" stroke="#64ff96" stroke-width="3"/>
          <text x="{contact_x - arc_r - 12}" y="{center_y - 15}" fill="#64ff96" font-size="16" font-weight="bold">θ</text>
        </svg>
      </div>
    </div>
  </div>
  <div style="margin-top: 16px; padding: 16px; background: #1e293b; border-radius: 8px; display: flex; gap: 30px; flex-wrap: wrap; justify-content: center;">
    <div style="text-align: center;">
      <div style="color: #94a3b8; font-size: 12px;">Contact Angle</div>
      <div style="color: #64ff96; font-size: 28px; font-weight: bold;">θ = {theta_deg_y:.1f}°</div>
    </div>
    <div style="text-align: center;">
      <div style="color: #94a3b8; font-size: 12px;">Wetting</div>
      <div style="color: {wetting_color}; font-size: 20px; font-weight: bold;">{wetting}</div>
    </div>
    <div style="text-align: center;">
      <div style="color: #94a3b8; font-size: 12px;">Shape Factor S(θ)</div>
      <div style="color: #a78bfa; font-size: 20px; font-weight: bold;">{S_y:.4f}</div>
    </div>
    <div style="text-align: center;">
      <div style="color: #94a3b8; font-size: 12px;">Barrier Reduction</div>
      <div style="color: #ec4899; font-size: 20px; font-weight: bold;">{S_y*100:.1f}%</div>
    </div>
  </div>
</div>
'''
mo.Html(html_tension)


# ======================= CELL 13: TRANSITION TO DERIVATION =======================
mo.md(r"""
---

## So How Much Does the Barrier Decrease?

We've seen that:
- Nucleation has an energy barrier $\Delta G^*$
- Surfaces help by letting the nucleus form a **spherical cap** instead of a full sphere
- The contact angle $\theta$ determines the cap shape

But **how do we calculate exactly how much the barrier is reduced?**

The answer lies in the **shape factor $S(\theta)$** - the ratio of the cap's volume to a full sphere's volume. 

Let's derive it step by step...

---
""")


# ======================= CELL 14: PART 2 HEADER =======================
mo.md(r"""
# Part 2: The Derivation
## *How do we calculate the shape factor S(θ)?*

We'll work through four steps:

1. **Geometry** → Understand the spherical cap shape
2. **Volume** → Calculate the cap volume using calculus  
3. **Shape Factor** → Find $S(\theta) = V_{cap} / V_{sphere}$
4. **Energy Barrier** → Connect to $\Delta G^*_{het} = S(\theta) \cdot \Delta G^*_{hom}$
""")


# ======================= CELL 15: STEP 1 GEOMETRY INTRO =======================
mo.md(r"""
## Step 1: Spherical Cap Geometry

The nucleus forms a **spherical cap** - a portion of a sphere cut by a plane (the substrate).

Key geometric relationships from the right triangle:

| Quantity | Formula | Meaning |
|----------|---------|---------|
| Cap height | $h = R(1 - \cos\theta)$ | How tall the cap is |
| Contact radius | $a = R\sin\theta$ | Half-width where cap meets substrate |
| Sphere radius | $R$ | Radius of the full sphere |

*Adjust θ to see how the geometry changes:*
""")


# ======================= CELL 16: STEP 1 GEOMETRY SLIDER =======================
theta_geom_slider = mo.ui.slider(
    start=10,
    stop=170,
    step=1,
    value=60,
    label="Contact Angle θ (degrees)"
)
theta_geom_slider


# ======================= CELL 17: STEP 1 GEOMETRY VISUALIZATION =======================
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Arc, Polygon
import io
import base64

def draw_step1_geometry(theta_deg):
    BG_COLOR = (15/255, 25/255, 45/255)
    PANEL_BG = (20/255, 32/255, 55/255)
    SUBSTRATE_COLOR = (255/255, 165/255, 0/255)
    NUCLEUS_COLOR = (255/255, 100/255, 150/255)
    NUCLEUS_EDGE = (255/255, 80/255, 130/255)
    WHITE = (1, 1, 1)
    YELLOW = (255/255, 220/255, 100/255)
    ORANGE = (255/255, 180/255, 100/255)
    CYAN = (100/255, 240/255, 255/255)
    GREEN = (100/255, 255/255, 150/255)
    GRAY = (150/255, 150/255, 160/255)
    DASHED_CIRCLE = (150/255, 170/255, 200/255)
    
    fig, (ax_geom, ax_explain) = plt.subplots(1, 2, figsize=(10, 5), 
                                               gridspec_kw={'width_ratios': [1.2, 1]},
                                               facecolor=BG_COLOR)
    
    ax_geom.set_facecolor(BG_COLOR)
    ax_geom.set_xlim(-120, 120)
    ax_geom.set_ylim(-120, 140)
    ax_geom.set_aspect('equal')
    ax_geom.axis('off')
    
    R = 70
    substrate_y = 0
    theta_rad = math.radians(theta_deg)
    cos_t = math.cos(theta_rad)
    sin_t = math.sin(theta_rad)
    
    Cy = -R * cos_t
    Cx = 0
    a = R * abs(sin_t)
    h = R * (1 - cos_t)
    Ty = substrate_y + h
    Tx = 0
    Px = a
    Py = substrate_y
    Bx, By = 0, substrate_y
    
    circle = plt.Circle((Cx, Cy), R, fill=False, linestyle='--', 
                        color=DASHED_CIRCLE, linewidth=1.5, alpha=0.7, zorder=2)
    ax_geom.add_patch(circle)
    
    n_pts = 100
    angle_right = math.atan2(substrate_y - Cy, a)
    angle_left = math.atan2(substrate_y - Cy, -a)
    
    if angle_left >= angle_right:
        angles = np.linspace(angle_right, angle_left, n_pts)
    else:
        angles = np.linspace(angle_right, angle_left + 2*np.pi, n_pts)
    
    arc_x = Cx + R * np.cos(angles)
    arc_y = Cy + R * np.sin(angles)
    above = arc_y >= substrate_y - 0.5
    arc_x, arc_y = arc_x[above], arc_y[above]
    
    if len(arc_x) >= 2:
        poly_x = np.concatenate([[-a], arc_x, [a]])
        poly_y = np.concatenate([[substrate_y], arc_y, [substrate_y]])
        nucleus = Polygon(list(zip(poly_x, poly_y)), 
                         facecolor=NUCLEUS_COLOR, edgecolor=NUCLEUS_EDGE,
                         linewidth=2.5, closed=True, zorder=3, alpha=0.85)
        ax_geom.add_patch(nucleus)
    
    ax_geom.plot([-110, 110], [substrate_y, substrate_y], 
                color=SUBSTRATE_COLOR, linewidth=3, zorder=4)
    ax_geom.text(95, substrate_y + 5, 'substrate', fontsize=9, color=SUBSTRATE_COLOR)
    
    ax_geom.plot(Tx, Ty, 'o', markersize=8, color=YELLOW, zorder=10)
    ax_geom.text(Tx + 5, Ty + 5, 'T', fontsize=12, color=YELLOW, fontweight='bold')
    ax_geom.plot(Cx, Cy, 'o', markersize=8, color=WHITE, zorder=10)
    ax_geom.text(Cx - 12, Cy + 5, 'C', fontsize=12, color=WHITE, fontweight='bold')
    ax_geom.plot(Bx, By, 'o', markersize=6, color=ORANGE, zorder=10)
    ax_geom.text(Bx - 12, By - 12, 'B', fontsize=10, color=ORANGE)
    ax_geom.plot(Px, Py, 'o', markersize=8, color=WHITE, zorder=10)
    ax_geom.text(Px + 5, Py - 12, 'P', fontsize=12, color=WHITE, fontweight='bold')
    
    ax_geom.plot([Cx, Px], [Cy, Py], color=NUCLEUS_EDGE, linewidth=2.5, zorder=5)
    ax_geom.text((Cx + Px)/2 + 8, (Cy + Py)/2, 'R', fontsize=14, color=NUCLEUS_EDGE, fontweight='bold')
    
    ax_geom.annotate('', xy=(Tx + 15, Ty), xytext=(Tx + 15, By),
                    arrowprops=dict(arrowstyle='<->', color=ORANGE, lw=2))
    ax_geom.text(Tx + 22, (Ty + By)/2, 'h', fontsize=14, color=ORANGE, fontweight='bold')
    
    if abs(Cy) > 5 and -100 < Cy < 100:
        ax_geom.annotate('', xy=(Cx - 20, Cy), xytext=(Cx - 20, By),
                        arrowprops=dict(arrowstyle='<->', color=CYAN, lw=2))
        ax_geom.text(Cx - 55, (Cy + By)/2, r'R cos$\theta$', fontsize=10, color=CYAN)
    
    ax_geom.annotate('', xy=(Px, By - 20), xytext=(Bx, By - 20),
                    arrowprops=dict(arrowstyle='<->', color=ORANGE, lw=2))
    ax_geom.text((Bx + Px)/2, By - 35, r'a = R sin$\theta$', fontsize=10, color=ORANGE, ha='center')
    
    rect = patches.Rectangle((Bx, By), 8, 8, fill=False, edgecolor=WHITE, linewidth=1.5, zorder=6)
    ax_geom.add_patch(rect)
    
    arc_radius = 20
    theta1 = 180 - theta_deg
    theta2 = 180
    contact_arc = Arc((Px, Py), arc_radius*2, arc_radius*2,
                      angle=0, theta1=theta1, theta2=theta2,
                      color=GREEN, linewidth=3, zorder=8)
    ax_geom.add_patch(contact_arc)
    label_angle = math.radians(180 - theta_deg/2)
    label_x = Px + (arc_radius + 12) * math.cos(label_angle)
    label_y = Py + (arc_radius + 12) * math.sin(label_angle)
    ax_geom.text(label_x, label_y, r'$\theta$', fontsize=16, color=GREEN, fontweight='bold', ha='center', va='center')
    
    ax_explain.set_facecolor(PANEL_BG)
    ax_explain.set_xlim(0, 100)
    ax_explain.set_ylim(0, 100)
    ax_explain.axis('off')
    
    ax_explain.text(5, 95, 'From the right triangle (SOH-CAH-TOA):', fontsize=10, color=WHITE)
    ax_explain.text(5, 85, 'Adjacent:', fontsize=10, color=CYAN)
    ax_explain.text(30, 85, r'CB = R cos$\theta$', fontsize=10, color=CYAN)
    ax_explain.text(5, 77, 'Opposite:', fontsize=10, color=ORANGE)
    ax_explain.text(30, 77, r'BP = a = R sin$\theta$', fontsize=10, color=ORANGE)
    ax_explain.text(5, 62, 'Cap height derivation:', fontsize=10, color=WHITE)
    ax_explain.text(5, 52, r'h = CT − CB = R − R cos$\theta$', fontsize=10, color=GRAY)
    ax_explain.text(5, 40, r'h = R(1 − cos$\theta$)', fontsize=14, color=ORANGE, fontweight='bold')
    
    rect_box = patches.FancyBboxPatch((5, 5), 90, 25, boxstyle="round,pad=0.02",
                                   facecolor=(30/255, 50/255, 80/255), edgecolor=YELLOW, linewidth=2)
    ax_explain.add_patch(rect_box)
    ax_explain.text(10, 22, f'Current values (θ = {theta_deg:.0f}°):', fontsize=10, color=YELLOW, fontweight='bold')
    ax_explain.text(10, 12, f'h = {(1-cos_t):.3f}R  |  a = {abs(sin_t):.3f}R', fontsize=10, color=WHITE)
    
    fig.suptitle('Step 1: Spherical Cap Geometry', fontsize=16, color=YELLOW, fontweight='bold', y=0.98)
    plt.tight_layout()
    return fig

theta_g = theta_geom_slider.value
fig_geom = draw_step1_geometry(theta_g)
buffer_geom = io.BytesIO()
fig_geom.savefig(buffer_geom, format='png', dpi=120, facecolor=(15/255, 25/255, 45/255), edgecolor='none', bbox_inches='tight')
buffer_geom.seek(0)
plt.close(fig_geom)
img_base64_geom = base64.b64encode(buffer_geom.getvalue()).decode()
mo.Html(f'<img src="data:image/png;base64,{img_base64_geom}" style="max-width: 100%;">')


# ======================= CELL 18: STEP 2 VOLUME INTRO =======================
mo.md(r"""
## Step 2: Spherical Cap Volume (Calculus)

To find the cap volume, we integrate using the **disk method**: slice the cap into thin horizontal disks and sum their volumes.

*Drag the slider to move the disk slice through the cap:*
""")


# ======================= CELL 19: DISK SLICE SLIDER =======================
y_slice_slider = mo.ui.slider(
    start=0.05,
    stop=0.95,
    step=0.01,
    value=0.5,
    label="Disk position (fraction of cap height)"
)
y_slice_slider


# ======================= CELL 20: DISK INTEGRATION VISUALIZATION =======================
theta_vol = 70  # Fixed theta for this visualization
theta_rad_vol = math.radians(theta_vol)
cos_t_vol = math.cos(theta_rad_vol)
h_frac = 1 - cos_t_vol  # h/R

# Get slider value
y_frac = y_slice_slider.value  # 0 to 1 within the cap

# In our coordinate system:
# - Sphere center at origin
# - Cap goes from y = R-h = R*cos(theta) to y = R
# - We normalize by R, so y goes from cos(theta) to 1

y_min = cos_t_vol  # Bottom of cap (R-h)/R = cos(theta)
y_max = 1.0        # Top of cap (R/R = 1)
y_current = y_min + y_frac * (y_max - y_min)  # Current slice position

# Disk radius at this y: r(y) = sqrt(R² - y²), normalized: r/R = sqrt(1 - (y/R)²)
r_disk = math.sqrt(max(0, 1 - y_current**2))

# For display, scale everything
scale = 120  # pixels per unit R
cx_vol, cy_vol = 180, 160  # center of sphere in SVG

# Key points in SVG coordinates (y increases downward in SVG)
sphere_top_y = cy_vol - scale  # y = R (top of sphere)
sphere_bottom_y = cy_vol + scale  # y = -R (bottom)
cap_bottom_y = cy_vol - y_min * scale  # y = R-h (bottom of cap)
cap_top_y = cy_vol - y_max * scale  # y = R (top of cap)
slice_y = cy_vol - y_current * scale  # current slice position

# Disk endpoints at current y
disk_left_x = cx_vol - r_disk * scale
disk_right_x = cx_vol + r_disk * scale

# Cap arc (portion of circle from y=R-h to y=R)
cap_x_at_bottom = math.sqrt(max(0, 1 - y_min**2)) * scale

# For the disk, create an ellipse to show 3D perspective
disk_height = 12  # Ellipse minor axis for 3D effect

html_vol = f'''
<div style="background: #0f172a; padding: 20px; border-radius: 12px; font-family: system-ui, sans-serif; color: #fff;">
  
  <h3 style="color: #f59e0b; margin-bottom: 4px; text-align: center;">Disk Integration Visualization</h3>
  <p style="color: #94a3b8; text-align: center; margin-bottom: 16px; font-size: 13px;">
    θ = {theta_vol}° (fixed for illustration)
  </p>
  
  <div style="display: flex; gap: 20px; flex-wrap: wrap;">
    
    <!-- Left: SVG Visualization -->
    <div style="flex: 1; min-width: 320px;">
      <div style="background: #1e293b; border-radius: 8px; padding: 16px;">
        <svg width="360" height="320" viewBox="0 0 360 320">
          
          <!-- Coordinate axes (dashed) -->
          <line x1="{cx_vol}" y1="280" x2="{cx_vol}" y2="20" stroke="#475569" stroke-width="1" stroke-dasharray="4,4"/>
          <line x1="40" y1="{cy_vol}" x2="320" y2="{cy_vol}" stroke="#475569" stroke-width="1" stroke-dasharray="4,4"/>
          <text x="{cx_vol + 8}" y="30" fill="#64748b" font-size="11">y</text>
          <text x="310" y="{cy_vol - 8}" fill="#64748b" font-size="11">x</text>
          
          <!-- Full sphere outline (dashed) -->
          <circle cx="{cx_vol}" cy="{cy_vol}" r="{scale}" fill="none" stroke="#64748b" stroke-width="2" stroke-dasharray="6,4"/>
          
          <!-- Cap region (shaded) -->
          <path d="M {cx_vol - cap_x_at_bottom} {cap_bottom_y} 
                   A {scale} {scale} 0 0 1 {cx_vol + cap_x_at_bottom} {cap_bottom_y}
                   L {cx_vol + cap_x_at_bottom} {cap_bottom_y}
                   A {scale} {scale} 0 0 0 {cx_vol - cap_x_at_bottom} {cap_bottom_y} Z" 
                fill="rgba(249, 115, 22, 0.25)" stroke="none"/>
          
          <!-- Cap arc (solid) -->
          <path d="M {cx_vol - cap_x_at_bottom} {cap_bottom_y} A {scale} {scale} 0 0 1 {cx_vol + cap_x_at_bottom} {cap_bottom_y}" 
                fill="none" stroke="#f97316" stroke-width="3"/>
          
          <!-- Base of cap (horizontal line at y = R-h) -->
          <line x1="{cx_vol - cap_x_at_bottom}" y1="{cap_bottom_y}" x2="{cx_vol + cap_x_at_bottom}" y2="{cap_bottom_y}" 
                stroke="#f97316" stroke-width="2"/>
          
          <!-- Current disk slice (3D ellipse effect) -->
          <ellipse cx="{cx_vol}" cy="{slice_y}" rx="{r_disk * scale}" ry="{disk_height}" 
                   fill="rgba(34, 197, 94, 0.5)" stroke="#22c55e" stroke-width="2.5"/>
          
          <!-- Disk radius line r(y) -->
          <line x1="{cx_vol}" y1="{slice_y}" x2="{disk_right_x}" y2="{slice_y}" 
                stroke="#22c55e" stroke-width="2"/>
          <text x="{cx_vol + r_disk * scale / 2}" y="{slice_y - 8}" fill="#22c55e" font-size="12" 
                text-anchor="middle" font-weight="bold">r(y)</text>
          
          <!-- dy thickness indicator -->
          <line x1="{disk_right_x + 15}" y1="{slice_y - disk_height}" x2="{disk_right_x + 15}" y2="{slice_y + disk_height}" 
                stroke="#a855f7" stroke-width="2"/>
          <line x1="{disk_right_x + 10}" y1="{slice_y - disk_height}" x2="{disk_right_x + 20}" y2="{slice_y - disk_height}" 
                stroke="#a855f7" stroke-width="2"/>
          <line x1="{disk_right_x + 10}" y1="{slice_y + disk_height}" x2="{disk_right_x + 20}" y2="{slice_y + disk_height}" 
                stroke="#a855f7" stroke-width="2"/>
          <text x="{disk_right_x + 28}" y="{slice_y + 4}" fill="#a855f7" font-size="11" font-weight="bold">dy</text>
          
          <!-- Y-axis labels -->
          <!-- y = R (top) -->
          <line x1="{cx_vol - 8}" y1="{cap_top_y}" x2="{cx_vol + 8}" y2="{cap_top_y}" stroke="#f59e0b" stroke-width="2"/>
          <text x="{cx_vol - 45}" y="{cap_top_y + 4}" fill="#f59e0b" font-size="11">y = R</text>
          
          <!-- y = R-h (base of cap) -->
          <line x1="{cx_vol - 8}" y1="{cap_bottom_y}" x2="{cx_vol + 8}" y2="{cap_bottom_y}" stroke="#f59e0b" stroke-width="2"/>
          <text x="{cx_vol - 55}" y="{cap_bottom_y + 4}" fill="#f59e0b" font-size="11">y = R−h</text>
          
          <!-- y = 0 (center) -->
          <text x="{cx_vol + 12}" y="{cy_vol + 4}" fill="#64748b" font-size="10">0</text>
          
          <!-- Current y level -->
          <line x1="{cx_vol - 8}" y1="{slice_y}" x2="{cx_vol + 8}" y2="{slice_y}" stroke="#22c55e" stroke-width="2"/>
          <text x="{cx_vol - 25}" y="{slice_y + 4}" fill="#22c55e" font-size="11">y</text>
          
          <!-- h dimension arrow on right -->
          <line x1="320" y1="{cap_top_y}" x2="320" y2="{cap_bottom_y}" stroke="#ec4899" stroke-width="2"/>
          <polygon points="320,{cap_top_y} 316,{cap_top_y + 8} 324,{cap_top_y + 8}" fill="#ec4899"/>
          <polygon points="320,{cap_bottom_y} 316,{cap_bottom_y - 8} 324,{cap_bottom_y - 8}" fill="#ec4899"/>
          <text x="330" y="{(cap_top_y + cap_bottom_y) / 2 + 4}" fill="#ec4899" font-size="13" font-weight="bold">h</text>
          
          <!-- Integration arrow on left -->
          <line x1="35" y1="{cap_bottom_y - 5}" x2="35" y2="{cap_top_y + 5}" stroke="#f59e0b" stroke-width="2"/>
          <polygon points="35,{cap_top_y + 5} 31,{cap_top_y + 15} 39,{cap_top_y + 15}" fill="#f59e0b"/>
          <text x="25" y="{(cap_top_y + cap_bottom_y) / 2}" fill="#f59e0b" font-size="14">∫</text>
          
          <!-- Labels -->
          <text x="{cx_vol}" y="305" fill="#f97316" font-size="12" text-anchor="middle" font-weight="bold">Cap</text>
          <text x="{cx_vol}" y="{cy_vol + scale + 25}" fill="#64748b" font-size="10" text-anchor="middle">Rest of sphere</text>
          
        </svg>
      </div>
    </div>
    
    <!-- Right: Explanation panel -->
    <div style="flex: 1; min-width: 280px;">
      <div style="background: #1e293b; border-radius: 8px; padding: 16px;">
        
        <div style="background: #334155; padding: 12px; border-radius: 6px; margin-bottom: 12px;">
          <div style="color: #f59e0b; font-size: 14px; font-weight: bold; margin-bottom: 8px;">
            🔍 What we're integrating:
          </div>
          <div style="color: #94a3b8; font-size: 13px; line-height: 1.8;">
            <span style="color: #22c55e;">Green disk</span>: Slice at height y<br>
            <span style="color: #a855f7;">Purple dy</span>: Infinitesimal thickness<br>
            <span style="color: #22c55e;">r(y)</span>: Disk radius = √(R² − y²)<br>
            <span style="color: #f97316;">Orange region</span>: The cap we want
          </div>
        </div>
        
        <div style="background: #334155; padding: 12px; border-radius: 6px; margin-bottom: 12px;">
          <div style="color: #67e8f9; font-size: 14px; font-weight: bold; margin-bottom: 8px;">
            📐 Current slice values:
          </div>
          <div style="font-family: monospace; font-size: 13px; color: #fff; line-height: 1.8;">
            <div>y/R = <span style="color: #22c55e;">{y_current:.3f}</span></div>
            <div>r(y)/R = <span style="color: #22c55e;">{r_disk:.3f}</span></div>
            <div>Disk area = <span style="color: #f59e0b;">π({r_disk:.3f})²R²</span></div>
            <div style="margin-top: 8px; padding-top: 8px; border-top: 1px solid #475569;">
              <span style="color: #94a3b8;">Integration bounds:</span><br>
              y: <span style="color: #f59e0b;">{y_min:.3f}R</span> → <span style="color: #f59e0b;">R</span>
            </div>
          </div>
        </div>
        
        <div style="background: #0f3460; padding: 12px; border-radius: 6px; border: 1px solid #3b82f6;">
          <div style="color: #93c5fd; font-size: 13px; line-height: 1.6;">
            <strong>The integral:</strong><br>
            <div style="font-family: monospace; text-align: center; margin-top: 8px; font-size: 14px;">
              V = ∫<sub>R−h</sub><sup>R</sup> π(R² − y²) dy
            </div>
          </div>
        </div>
        
        <div style="margin-top: 12px; padding: 10px; background: #1a1a2e; border-radius: 6px; font-size: 11px; color: #94a3b8;">
          <strong style="color: #e2e8f0;">💡 Insight:</strong> Each disk contributes π·r(y)²·dy to the volume. We sum all disks from the base of the cap to the top.
        </div>
        
      </div>
    </div>
    
  </div>
</div>
'''
mo.Html(html_vol)


# ======================= CELL 21: STEP 2 VOLUME DERIVATION =======================
mo.md(r"""
### Detailed Integration

**Setup:** Place sphere center at origin. Cap extends from $y = R - h$ to $y = R$.

**Evaluate the integral:**

$$V = \pi \left[ R^2 y - \frac{y^3}{3} \right]_{R-h}^{R}$$

**At $y = R$:**
$$R^2(R) - \frac{R^3}{3} = R^3 - \frac{R^3}{3} = \frac{2R^3}{3}$$

**At $y = R-h$:**
$$R^2(R-h) - \frac{(R-h)^3}{3}$$

**Expand $(R-h)^3$:**
$$(R-h)^3 = R^3 - 3R^2h + 3Rh^2 - h^3$$

**Subtract and simplify:**
$$V = \pi \left[ \frac{2R^3}{3} - \left( \frac{2R^3}{3} - Rh^2 + \frac{h^3}{3} \right) \right] = \pi \left( Rh^2 - \frac{h^3}{3} \right)$$

$$\boxed{V_{cap} = \frac{\pi h^2}{3}(3R - h)}$$

Now substitute $h = R(1 - \cos\theta)$...
""")


# ======================= CELL 22: STEP 3 SHAPE FACTOR =======================
mo.md(r"""
## Step 3: The Shape Factor $S(\theta)$

**Substitute** $h = R(1 - \cos\theta)$ into the volume formula:

$$h^2 = R^2(1 - \cos\theta)^2$$

$$3R - h = 3R - R(1 - \cos\theta) = R(2 + \cos\theta)$$

$$V_{cap} = \frac{\pi R^3}{3}(1 - \cos\theta)^2(2 + \cos\theta)$$

**Compare to sphere volume:** $V_{sphere} = \frac{4}{3}\pi R^3$

**The shape factor is the ratio:**

$$S(\theta) = \frac{V_{cap}}{V_{sphere}} = \frac{\frac{\pi R^3}{3}(1 - \cos\theta)^2(2 + \cos\theta)}{\frac{4}{3}\pi R^3}$$

$$\boxed{S(\theta) = \frac{(2 + \cos\theta)(1 - \cos\theta)^2}{4}}$$

This is **the key result** - it tells us what fraction of a full sphere the cap represents!
""")


# ======================= CELL 23: STEP 4 ENERGY BARRIER =======================
mo.md(r"""
## Step 4: The Energy Barrier Connection

For **homogeneous nucleation** (full sphere in bulk liquid):

$$\Delta G^*_{hom} = \frac{16\pi\gamma^3}{3(\Delta G_v)^2}$$

For **heterogeneous nucleation** (spherical cap on substrate), you only need to form a *cap*, not a full sphere. The barrier scales with the volume:

$$\boxed{\Delta G^*_{het} = S(\theta) \cdot \Delta G^*_{hom}}$$

### Physical Meaning

| Contact Angle | $S(\theta)$ | Barrier | Physical Meaning |
|---------------|-------------|---------|------------------|
| $\theta = 0°$ | $S = 0$ | None! | Perfect wetting - no barrier |
| $\theta = 60°$ | $S = 0.156$ | 15.6% | Good wetting - 84% reduction |
| $\theta = 90°$ | $S = 0.5$ | 50% | Hemisphere - half the barrier |
| $\theta = 120°$ | $S = 0.844$ | 84.4% | Poor wetting - only 16% reduction |
| $\theta = 180°$ | $S = 1$ | 100% | No wetting - same as homogeneous |

**Key insight:** Better wetting (lower θ) → lower S(θ) → **easier nucleation!**
""")


# ======================= CELL 24: TRANSITION TO VISUALIZATION =======================
mo.md(r"""
---

## Summary of the Derivation

We've traced the complete path:

1. **Geometry:** The contact angle $\theta$ determines the cap shape via $h = R(1-\cos\theta)$

2. **Volume:** Integration gives $V_{cap} = \frac{\pi h^2}{3}(3R-h)$

3. **Shape Factor:** The ratio $S(\theta) = \frac{(2+\cos\theta)(1-\cos\theta)^2}{4}$

4. **Barrier:** $\Delta G^*_{het} = S(\theta) \cdot \Delta G^*_{hom}$

Now let's see all of this come together in an interactive visualization...

---
""")


# ======================= CELL 25: PART 3 HEADER =======================
mo.md(r"""
# Part 3: The Complete Picture
## *Interactive visualization bringing it all together*

With the physics understood and the math derived, explore how contact angle controls heterogeneous nucleation:

- **Left panel:** Nucleus geometry with surface tension vectors
- **Middle panel:** Shape factor $S(\theta)$ curve  
- **Right panel:** Nucleation barrier reduction
""")


# ======================= CELL 26: MAIN SLIDER =======================
theta_slider = mo.ui.slider(
    start=10,
    stop=170,
    step=1,
    value=90,
    label="Contact Angle θ (degrees)",
    full_width=True
)
theta_slider


# ======================= CELL 27: THE WORKING 3-PANEL VISUALIZATION =======================
def _():
    import math
    from PIL import Image, ImageDraw, ImageFont
    import matplotlib.pyplot as plt
    import matplotlib
    matplotlib.use('Agg')
    import io
    import base64
    import numpy as np

    WIDTH = 1100
    HEIGHT = 500

    BG_COLOR = (15, 25, 45)
    PANEL_BG = (20, 32, 55)
    SUBSTRATE_COLOR = (70, 100, 140)
    SUBSTRATE_HATCH = (55, 85, 120)
    NUCLEUS_COLOR = (255, 130, 170)
    NUCLEUS_OUTLINE = (255, 80, 130)

    WHITE = (255, 255, 255)
    YELLOW = (255, 220, 100)
    ORANGE = (255, 180, 100)
    CYAN = (100, 240, 255)
    GREEN = (100, 255, 150)
    RED = (255, 100, 100)
    GOLD = (255, 215, 0)
    GRAY = (150, 150, 160)
    LIGHT_GRAY = (120, 120, 130)
    BLACK = (0, 0, 0)

    plt.rcParams['mathtext.fontset'] = 'stix'
    plt.rcParams['font.family'] = 'STIXGeneral'

    def render_latex(latex_str, fontsize=12, color='white'):
        fig, ax = plt.subplots(figsize=(4, 0.5), dpi=100)
        fig.patch.set_alpha(0)
        ax.axis('off')
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        text = ax.text(0.0, 0.5, latex_str, fontsize=fontsize, color=color,
                       ha='left', va='center', transform=ax.transAxes)
        buf = io.BytesIO()
        fig.savefig(buf, format='png', transparent=True, bbox_inches='tight', 
                    pad_inches=0.01, dpi=100)
        plt.close(fig)
        buf.seek(0)
        img = Image.open(buf).convert('RGBA')
        bbox = img.getbbox()
        if bbox:
            img = img.crop(bbox)
        return img

    def get_latex_labels():
        labels = {}
        labels['gamma_sn'] = render_latex(r'$\gamma_{SN}$', fontsize=14, color='black')
        labels['gamma_sl'] = render_latex(r'$\gamma_{SL}$', fontsize=14, color='white')
        labels['gamma_nl'] = render_latex(r'$\gamma_{NL}$', fontsize=14, color='#FFD700')
        labels['shape_eq'] = render_latex(r'$S(\theta) = \frac{(2+\cos\theta)(1-\cos\theta)^2}{4}$', fontsize=13, color='#64F0FF')
        labels['barrier_eq'] = render_latex(r'$\Delta G^*_{het} = S(\theta) \cdot \Delta G^*_{hom}$', fontsize=11, color='#FFB464')
        labels['young_eq'] = render_latex(r'$\gamma_{SL} = \gamma_{SN} + \gamma_{NL}\cos\theta$', fontsize=10, color='white')
        labels['y_axis_s'] = render_latex(r'$S(\theta)$', fontsize=12, color='#64F0FF')
        labels['y_axis_dg'] = render_latex(r'$\Delta G / \Delta G^*_{hom}$', fontsize=10, color='#FFB464')
        labels['x_axis_theta'] = render_latex(r'Contact Angle $\theta$ (degrees)', fontsize=11, color='#64FF96')
        labels['x_axis_r'] = render_latex(r'Normalized Radius $r/r^*$', fontsize=11, color='white')
        labels['gamma_sn_leg'] = render_latex(r'$\gamma_{SN}$', fontsize=10, color='white')
        labels['gamma_sl_leg'] = render_latex(r'$\gamma_{SL}$', fontsize=10, color='white')
        labels['gamma_nl_leg'] = render_latex(r'$\gamma_{NL}$', fontsize=10, color='#FFD700')
        return labels

    def get_dynamic_label(sf):
        return render_latex(rf'$\Delta G^*_{{het}} = {sf*100:.1f}\%$ of $\Delta G^*_{{hom}}$', fontsize=12, color='#FFB464')

    def S(theta_deg):
        theta = math.radians(theta_deg)
        c = math.cos(theta)
        return (2 + c) * (1 - c) ** 2 / 4

    def draw_arrow(draw, x1, y1, x2, y2, color, width=3, arrow_len=10):
        draw.line([(x1, y1), (x2, y2)], fill=color, width=width)
        angle = math.atan2(y2 - y1, x2 - x1)
        al = arrow_len
        pts = [(x2, y2),
               (x2 - al*math.cos(angle-0.35), y2 - al*math.sin(angle-0.35)),
               (x2 - al*math.cos(angle+0.35), y2 - al*math.sin(angle+0.35))]
        draw.polygon(pts, fill=color)

    def draw_dashed(draw, x1, y1, x2, y2, color, dash, gap, width=1):
        dx, dy = x2 - x1, y2 - y1
        dist = math.sqrt(dx*dx + dy*dy)
        if dist < 1:
            return
        dx, dy = dx/dist, dy/dist
        pos = 0
        while pos < dist:
            end = min(pos + dash, dist)
            draw.line([(x1 + dx*pos, y1 + dy*pos), (x1 + dx*end, y1 + dy*end)], fill=color, width=width)
            pos += dash + gap

    def paste_with_background(img, label, x, y, bg_color=(30, 45, 70), padding=4):
        draw = ImageDraw.Draw(img)
        w, h = label.size
        draw.rectangle([x - padding, y - padding, x + w + padding, y + h + padding], 
                       fill=bg_color, outline=(60, 80, 110))
        img.paste(label, (x, y), label)

    def get_fonts():
        try:
            f_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)
            f_normal = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 13)
            f_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14)
            f_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
            f_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
            f_bigtitle = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
        except:
            f_small = f_normal = f_medium = f_large = f_title = f_bigtitle = ImageFont.load_default()
        return f_small, f_normal, f_medium, f_large, f_title, f_bigtitle

    def draw_nucleus(draw, cx, baseY, theta_deg, a=60):
        theta_rad = math.radians(theta_deg)
        sin_t = max(math.sin(theta_rad), 0.05)
        cos_t = math.cos(theta_rad)
        R = a / sin_t
        R = min(R, 400)
        Cy = baseY + R * cos_t
        alpha_R = math.atan2(baseY - Cy, a)
        alpha_L = math.atan2(baseY - Cy, -a)
        if alpha_L <= alpha_R:
            span = alpha_R - alpha_L
        else:
            span = alpha_R - (alpha_L - 2*math.pi)
        arc_pts = []
        for i in range(61):
            t = i / 60
            angle = alpha_R - t * span
            px = cx + R * math.cos(angle)
            py = Cy + R * math.sin(angle)
            if py <= baseY + 1:
                arc_pts.append((px, py))
        if len(arc_pts) >= 2:
            poly = [(cx - a, baseY)] + arc_pts + [(cx + a, baseY)]
            draw.polygon(poly, fill=NUCLEUS_COLOR, outline=NUCLEUS_OUTLINE)
            draw.line(arc_pts, fill=NUCLEUS_OUTLINE, width=3)
        h = R * (1 - cos_t)
        return (h, Cy, R)

    def draw_geometry_panel(img, draw, theta_deg, px, py, pw, ph, fonts, labels):
        f_small, f_normal, f_medium, f_large, f_title, f_bigtitle = fonts
        draw.rectangle([px, py, px+pw, py+ph], fill=PANEL_BG, outline=LIGHT_GRAY)
        draw.text((px + pw//2, py + 18), "NUCLEUS GEOMETRY", fill=YELLOW, anchor="mm", font=f_bigtitle)
        cx = px + pw//2
        baseY = py + int(ph * 0.58)
        substrate_top = baseY
        substrate_bottom = baseY + 35
        draw.rectangle([px+5, substrate_top, px+pw-5, substrate_bottom], fill=SUBSTRATE_COLOR)
        for i in range(px, px+pw, 8):
            draw.line([(i, substrate_top), (i+12, substrate_bottom)], fill=SUBSTRATE_HATCH, width=1)
        a = 55
        h, Cy, R = draw_nucleus(draw, cx, baseY, theta_deg, a)
        theta_rad = math.radians(theta_deg)
        if 25 < theta_deg < 150 and R < 200:
            if theta_deg < 100 and R < 150 and R > 30:
                num_segments = 40
                arc_pts = []
                for i in range(num_segments + 1):
                    t = i / num_segments
                    right_angle = math.atan2(baseY - Cy, a)
                    left_angle = math.atan2(baseY - Cy, -a)
                    if i == 0:
                        angle = right_angle
                    else:
                        arc_span = (2*math.pi) - (left_angle - right_angle)
                        angle = right_angle - t * arc_span
                    px_arc = cx + R * math.cos(angle)
                    py_arc = Cy + R * math.sin(angle)
                    arc_pts.append((px_arc, py_arc))
                for i in range(len(arc_pts) - 1):
                    if i % 4 < 2:
                        if (py + 35 < arc_pts[i][1] < py + ph - 5 and 
                            py + 35 < arc_pts[i+1][1] < py + ph - 5 and
                            px + 5 < arc_pts[i][0] < px + pw - 5):
                            draw.line([arc_pts[i], arc_pts[i+1]], fill=(150, 170, 200), width=2)
            if py + 45 < Cy < baseY + 60:
                draw.ellipse([cx-5, Cy-5, cx+5, Cy+5], fill=WHITE, outline=(100,100,120))
        tpX, tpY = cx + a, baseY
        L = 90
        draw.line([(tpX, tpY), (tpX - L, tpY)], fill=BLACK, width=5)
        al = 20
        ah_pts = [(tpX - L, tpY), (tpX - L + al, tpY - al*0.35), (tpX - L + al, tpY + al*0.35)]
        draw.polygon(ah_pts, fill=BLACK)
        draw_arrow(draw, tpX, tpY, tpX + L, tpY, WHITE, 5, arrow_len=20)
        nlX = tpX - L * math.cos(theta_rad)
        nlY = tpY - L * math.sin(theta_rad)
        draw_arrow(draw, tpX, tpY, nlX, nlY, GOLD, 5, arrow_len=20)
        ext = 95
        draw_dashed(draw, tpX - ext*math.cos(theta_rad), tpY - ext*math.sin(theta_rad),
                    tpX + ext*0.3*math.cos(theta_rad), tpY + ext*0.3*math.sin(theta_rad),
                    (180, 160, 80), 4, 3, 1)
        ar = 38
        draw.arc([tpX-ar, tpY-ar, tpX+ar, tpY+ar], start=180, end=180+theta_deg, fill=GREEN, width=5)
        draw.ellipse([tpX-5, tpY-5, tpX+5, tpY+5], fill=WHITE, outline=GREEN, width=2)
        gamma_sn = labels['gamma_sn']
        gamma_sl = labels['gamma_sl']
        gamma_nl = labels['gamma_nl']
        img.paste(gamma_sn, (int(tpX - L - gamma_sn.width//2 - 5), int(tpY - 30)), gamma_sn)
        img.paste(gamma_sl, (int(tpX + L + 5), int(tpY - 30)), gamma_sl)
        img.paste(gamma_nl, (int(nlX - gamma_nl.width - 5), int(nlY - 20)), gamma_nl)
        draw.text((cx, substrate_bottom - 12), "Substrate", fill=WHITE, anchor="mm", font=f_small)
        draw.text((px + 12, py + 42), "Liquid", fill=WHITE, font=f_normal)
        if h > 20:
            draw.text((cx, baseY - min(h*0.5, 50)), "Nucleus", fill=WHITE, anchor="mm", font=f_normal)
        sf = S(theta_deg)
        draw.text((px + 12, py + 65), f"θ = {theta_deg:.0f}°", fill=GREEN, font=f_large)
        draw.text((px + 12, py + 88), f"S(θ) = {sf:.4f}", fill=CYAN, font=f_normal)
        if theta_deg < 30:
            wetting, wcolor = "Excellent wetting", GREEN
        elif theta_deg < 60:
            wetting, wcolor = "Good wetting", GREEN
        elif theta_deg < 90:
            wetting, wcolor = "Moderate wetting", YELLOW
        elif theta_deg < 120:
            wetting, wcolor = "Poor wetting", ORANGE
        elif theta_deg < 150:
            wetting, wcolor = "Very poor wetting", RED
        else:
            wetting, wcolor = "Non-wetting", RED
        draw.text((px + 12, py + 108), wetting, fill=wcolor, font=f_small)
        ly = py + ph - 55
        legend_box = [px + 5, ly - 2, px + 160, ly + 48]
        draw.rectangle(legend_box, fill=(45, 65, 95), outline=(80, 100, 130))
        draw.line([(px + 10, ly + 8), (px + 28, ly + 8)], fill=BLACK, width=3)
        gamma_sn_leg = labels['gamma_sn_leg']
        img.paste(gamma_sn_leg, (px + 30, ly + 2), gamma_sn_leg)
        draw.text((px + 58, ly + 8), "Solid-Nucl", fill=WHITE, anchor="lm", font=f_small)
        draw.line([(px + 10, ly + 22), (px + 28, ly + 22)], fill=WHITE, width=3)
        gamma_sl_leg = labels['gamma_sl_leg']
        img.paste(gamma_sl_leg, (px + 30, ly + 16), gamma_sl_leg)
        draw.text((px + 58, ly + 22), "Solid-Liq", fill=WHITE, anchor="lm", font=f_small)
        draw.line([(px + 10, ly + 36), (px + 28, ly + 36)], fill=GOLD, width=3)
        gamma_nl_leg = labels['gamma_nl_leg']
        img.paste(gamma_nl_leg, (px + 30, ly + 30), gamma_nl_leg)
        draw.text((px + 58, ly + 36), "Nucl-Liq", fill=GOLD, anchor="lm", font=f_small)
        draw.text((px + pw - 60, ly + 6), "Young's equation:", fill=GRAY, anchor="rt", font=f_small)
        young = labels['young_eq']
        paste_with_background(img, young, px + pw - young.width - 55, ly + 18, bg_color=(35, 50, 75))

    def draw_shape_factor_panel(img, draw, theta_deg, px, py, pw, ph, fonts, labels):
        f_small, f_normal, f_medium, f_large, f_title, f_bigtitle = fonts
        draw.rectangle([px, py, px+pw, py+ph], fill=PANEL_BG, outline=LIGHT_GRAY)
        draw.text((px + pw//2, py + 18), "SHAPE FACTOR S(θ)", fill=YELLOW, anchor="mm", font=f_bigtitle)
        sf = S(theta_deg)
        draw.text((px + pw//2, py + 42), f"S({theta_deg:.0f}°) = {sf:.4f}", fill=CYAN, anchor="mm", font=f_medium)
        margin = {'l': 55, 'r': 15, 't': 60, 'b': 55}
        plot_x = px + margin['l']
        plot_y = py + margin['t']
        plot_w = pw - margin['l'] - margin['r']
        plot_h = ph - margin['t'] - margin['b']
        def to_x(th): return plot_x + (th / 180) * plot_w
        def to_y(s): return plot_y + plot_h - s * plot_h
        for s_val in [0.25, 0.5, 0.75]:
            y = to_y(s_val)
            draw.line([(plot_x, y), (plot_x + plot_w, y)], fill=(40, 50, 70), width=1)
        for th_val in [45, 90, 135]:
            x = to_x(th_val)
            draw.line([(x, plot_y), (x, plot_y + plot_h)], fill=(40, 50, 70), width=1)
        draw.line([(plot_x, plot_y + plot_h), (plot_x + plot_w, plot_y + plot_h)], fill=WHITE, width=2)
        draw.line([(plot_x, plot_y), (plot_x, plot_y + plot_h)], fill=WHITE, width=2)
        pts = [(to_x(th), to_y(S(th))) for th in range(0, 181, 2)]
        draw.line(pts, fill=CYAN, width=3)
        curr_x, curr_y = to_x(theta_deg), to_y(S(theta_deg))
        draw.ellipse([curr_x-8, curr_y-8, curr_x+8, curr_y+8], fill=GREEN, outline=WHITE, width=2)
        draw_dashed(draw, curr_x, plot_y + plot_h, curr_x, curr_y, GRAY, 4, 3, 1)
        draw_dashed(draw, plot_x, curr_y, curr_x, curr_y, GRAY, 4, 3, 1)
        x_label = labels['x_axis_theta']
        img.paste(x_label, (plot_x + plot_w//2 - x_label.width//2, plot_y + plot_h + 25), x_label)
        for th_val in [0, 45, 90, 135, 180]:
            x = to_x(th_val)
            draw.text((x, plot_y + plot_h + 14), str(th_val), fill=WHITE, anchor="mm", font=f_normal)
        y_label = labels['y_axis_s']
        img.paste(y_label, (px + 5, plot_y - 22), y_label)
        for s_val in [0, 0.25, 0.5, 0.75, 1.0]:
            y = to_y(s_val)
            draw.text((plot_x - 8, y), f"{s_val:.2f}", fill=WHITE, anchor="rm", font=f_normal)
        shape_eq = labels['shape_eq']
        paste_with_background(img, shape_eq, plot_x + 8, plot_y + 8, bg_color=(25, 40, 65))

    def draw_barrier_panel(img, draw, theta_deg, px, py, pw, ph, fonts, labels):
        f_small, f_normal, f_medium, f_large, f_title, f_bigtitle = fonts
        draw.rectangle([px, py, px+pw, py+ph], fill=PANEL_BG, outline=LIGHT_GRAY)
        draw.text((px + pw//2, py + 18), "NUCLEATION BARRIER ΔG*", fill=YELLOW, anchor="mm", font=f_bigtitle)
        sf = S(theta_deg)
        pct_label = get_dynamic_label(sf)
        img.paste(pct_label, (px + pw//2 - pct_label.width//2, py + 32), pct_label)
        margin = {'l': 55, 'r': 15, 't': 60, 'b': 55}
        plot_x = px + margin['l']
        plot_y = py + margin['t']
        plot_w = pw - margin['l'] - margin['r']
        plot_h = ph - margin['t'] - margin['b']
        def dG(r, s=1): 
            return s * (3*r**2 - 2*r**3) if r > 0 else 0
        r_max = 1.5
        dg_max = 1.15
        def to_x(r): return plot_x + (r/r_max) * plot_w
        def to_y(g): return plot_y + (dg_max - max(g, 0)) / dg_max * plot_h
        zero_y = to_y(0)
        for g_val in [0.25, 0.5, 0.75, 1.0]:
            y = to_y(g_val)
            draw.line([(plot_x, y), (plot_x + plot_w, y)], fill=(40, 50, 70), width=1)
        for r_val in [0.5, 1.0]:
            x = to_x(r_val)
            draw.line([(x, plot_y), (x, plot_y + plot_h)], fill=(40, 50, 70), width=1)
        draw.line([(plot_x, zero_y), (plot_x + plot_w, zero_y)], fill=WHITE, width=2)
        draw.line([(plot_x, plot_y), (plot_x, plot_y + plot_h)], fill=WHITE, width=2)
        prev = None
        for i in range(0, 101, 1):
            r = i/100 * r_max
            g = dG(r, 1.0)
            if 0 <= g <= dg_max:
                pt = (to_x(r), to_y(g))
                if prev and i % 3 < 2:
                    draw.line([prev, pt], fill=GRAY, width=2)
                prev = pt
            else:
                prev = None
        het_pts = []
        for i in range(101):
            r = i/100 * r_max
            g = dG(r, sf)
            if 0 <= g <= dg_max:
                het_pts.append((to_x(r), to_y(g)))
        if len(het_pts) >= 2:
            draw.line(het_pts, fill=CYAN, width=3)
        r_star_x = to_x(1.0)
        hom_peak_y = to_y(1.0)
        het_peak_y = to_y(sf)
        draw.line([(r_star_x, plot_y), (r_star_x, zero_y)], fill=(60, 80, 100), width=1)
        draw_dashed(draw, r_star_x, zero_y, r_star_x, hom_peak_y, ORANGE, 4, 3, 1)
        draw.ellipse([r_star_x-5, hom_peak_y-5, r_star_x+5, hom_peak_y+5], fill=GRAY, outline=WHITE)
        draw_dashed(draw, r_star_x+2, zero_y, r_star_x+2, het_peak_y, ORANGE, 4, 3, 1)
        draw.ellipse([r_star_x-7, het_peak_y-7, r_star_x+7, het_peak_y+7], fill=ORANGE, outline=WHITE, width=2)
        if sf < 0.85:
            ax = r_star_x + 22
            draw.line([(ax, zero_y-2), (ax, het_peak_y+2)], fill=ORANGE, width=2)
            draw.polygon([(ax, het_peak_y), (ax-4, het_peak_y+8), (ax+4, het_peak_y+8)], fill=ORANGE)
            draw.polygon([(ax, zero_y), (ax-4, zero_y-8), (ax+4, zero_y-8)], fill=ORANGE)
        lx, ly = plot_x + plot_w - 5, plot_y + 12
        draw.line([(lx-115, ly), (lx-88, ly)], fill=GRAY, width=2)
        draw.text((lx-84, ly), "Homogeneous", fill=WHITE, anchor="lm", font=f_small)
        draw.line([(lx-115, ly+16), (lx-88, ly+16)], fill=CYAN, width=3)
        draw.text((lx-84, ly+16), "Heterogeneous", fill=WHITE, anchor="lm", font=f_small)
        x_label = labels['x_axis_r']
        img.paste(x_label, (plot_x + plot_w//2 - x_label.width//2, plot_y + plot_h + 25), x_label)
        for r_val in [0, 0.5, 1.0, 1.5]:
            x = to_x(r_val)
            label = "r*" if r_val == 1.0 else f"{r_val:.1f}"
            draw.text((x, zero_y + 14), label, fill=WHITE, anchor="mm", font=f_normal)
        y_label = labels['y_axis_dg']
        img.paste(y_label, (px + 2, plot_y - 18), y_label)
        for g_val in [0, 0.5, 1.0]:
            y = to_y(g_val)
            draw.text((plot_x - 8, y), f"{g_val:.1f}", fill=WHITE, anchor="rm", font=f_normal)
        barrier_eq = labels['barrier_eq']
        paste_with_background(img, barrier_eq, plot_x + 8, plot_y + int(plot_h * 0.25), bg_color=(25, 40, 65))

    def draw_frame(theta_deg, labels):
        img = Image.new('RGBA', (WIDTH, HEIGHT), BG_COLOR + (255,))
        draw = ImageDraw.Draw(img)
        fonts = get_fonts()
        gap = 8
        panel_w = (WIDTH - 4*gap) // 3
        panel_h = HEIGHT - 2*gap
        draw_geometry_panel(img, draw, theta_deg, gap, gap, panel_w, panel_h, fonts, labels)
        draw_shape_factor_panel(img, draw, theta_deg, gap*2 + panel_w, gap, panel_w, panel_h, fonts, labels)
        draw_barrier_panel(img, draw, theta_deg, gap*3 + panel_w*2, gap, panel_w, panel_h, fonts, labels)
        return img.convert('RGB')

    labels = get_latex_labels()
    theta = theta_slider.value
    img = draw_frame(theta, labels)
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.getvalue()).decode()
    return mo.Html(f'<img src="data:image/png;base64,{img_base64}" style="max-width: 100%;">')

_()


# ======================= CELL 27: KEY TAKEAWAYS =======================
mo.md(r"""
---

## Key Takeaways

1. **Nucleation has a barrier** because surface energy ($\propto r^2$) dominates at small sizes, while volume energy ($\propto r^3$) only wins at larger sizes.

2. **Surfaces help** by reducing the amount of new interface that must be created. The nucleus forms a spherical cap instead of a full sphere.

3. **The contact angle $\theta$** is determined by the balance of three surface tensions (Young's equation):
$$\gamma_{SL} = \gamma_{SN} + \gamma_{NL}\cos\theta$$

4. **The shape factor $S(\theta)$** captures how much the barrier is reduced:
   - $\theta = 0°$ → $S = 0$ (no barrier - perfect wetting)
   - $\theta = 90°$ → $S = 0.5$ (half the barrier)
   - $\theta = 180°$ → $S = 1$ (no reduction - like homogeneous nucleation)

5. **The nucleation barrier** is reduced by factor $S(\theta)$:
$$\Delta G^*_{het} = S(\theta) \cdot \Delta G^*_{hom}$$

---

### Real-World Applications

This is why:
- **Dust particles** seed raindrops (heterogeneous nucleation in clouds)
- **Grain boundaries** are preferred sites for precipitate formation  
- **Nucleating agents** are added to control crystal formation
- **Surface treatments** can promote or inhibit phase transformations
""")
