"""
Generate the 3-panel heterogeneous nucleation visualization GIF.
Uses the exact same rendering code as the marimo notebook.
"""

import math
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import io
import os

# Create assets folder
os.makedirs('assets', exist_ok=True)

# =============================================================================
# COLORS (same as notebook)
# =============================================================================
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

# =============================================================================
# HELPER FUNCTIONS (same as notebook)
# =============================================================================

def render_latex(latex_str, fontsize=12, color='white'):
    """Render LaTeX string to PIL Image with transparent background"""
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

# =============================================================================
# PANEL DRAWING FUNCTIONS (same as notebook)
# =============================================================================

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
    
    # Dashed circle for full sphere
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
    
    # Surface tension arrows
    draw.line([(tpX, tpY), (tpX - L, tpY)], fill=BLACK, width=5)
    al = 20
    ah_pts = [(tpX - L, tpY), (tpX - L + al, tpY - al*0.35), (tpX - L + al, tpY + al*0.35)]
    draw.polygon(ah_pts, fill=BLACK)
    draw_arrow(draw, tpX, tpY, tpX + L, tpY, WHITE, 5, arrow_len=20)
    nlX = tpX - L * math.cos(theta_rad)
    nlY = tpY - L * math.sin(theta_rad)
    draw_arrow(draw, tpX, tpY, nlX, nlY, GOLD, 5, arrow_len=20)
    
    # Dashed tangent extension
    ext = 95
    draw_dashed(draw, tpX - ext*math.cos(theta_rad), tpY - ext*math.sin(theta_rad),
                tpX + ext*0.3*math.cos(theta_rad), tpY + ext*0.3*math.sin(theta_rad),
                (180, 160, 80), 4, 3, 1)
    
    # Contact angle arc
    ar = 38
    draw.arc([tpX-ar, tpY-ar, tpX+ar, tpY+ar], start=180, end=180+theta_deg, fill=GREEN, width=5)
    draw.ellipse([tpX-5, tpY-5, tpX+5, tpY+5], fill=WHITE, outline=GREEN, width=2)
    
    # Paste LaTeX labels
    gamma_sn = labels['gamma_sn']
    gamma_sl = labels['gamma_sl']
    gamma_nl = labels['gamma_nl']
    img.paste(gamma_sn, (int(tpX - L - gamma_sn.width//2 - 5), int(tpY - 30)), gamma_sn)
    img.paste(gamma_sl, (int(tpX + L + 5), int(tpY - 30)), gamma_sl)
    img.paste(gamma_nl, (int(nlX - gamma_nl.width - 5), int(nlY - 20)), gamma_nl)
    
    # Text labels
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
    
    # Legend box
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
    
    # Grid
    for s_val in [0.25, 0.5, 0.75]:
        y = to_y(s_val)
        draw.line([(plot_x, y), (plot_x + plot_w, y)], fill=(40, 50, 70), width=1)
    for th_val in [45, 90, 135]:
        x = to_x(th_val)
        draw.line([(x, plot_y), (x, plot_y + plot_h)], fill=(40, 50, 70), width=1)
    
    # Axes
    draw.line([(plot_x, plot_y + plot_h), (plot_x + plot_w, plot_y + plot_h)], fill=WHITE, width=2)
    draw.line([(plot_x, plot_y), (plot_x, plot_y + plot_h)], fill=WHITE, width=2)
    
    # Curve
    pts = [(to_x(th), to_y(S(th))) for th in range(0, 181, 2)]
    draw.line(pts, fill=CYAN, width=3)
    
    # Current point
    curr_x, curr_y = to_x(theta_deg), to_y(S(theta_deg))
    draw.ellipse([curr_x-8, curr_y-8, curr_x+8, curr_y+8], fill=GREEN, outline=WHITE, width=2)
    draw_dashed(draw, curr_x, plot_y + plot_h, curr_x, curr_y, GRAY, 4, 3, 1)
    draw_dashed(draw, plot_x, curr_y, curr_x, curr_y, GRAY, 4, 3, 1)
    
    # X-axis label
    x_label = labels['x_axis_theta']
    img.paste(x_label, (plot_x + plot_w//2 - x_label.width//2, plot_y + plot_h + 25), x_label)
    
    for th_val in [0, 45, 90, 135, 180]:
        x = to_x(th_val)
        draw.text((x, plot_y + plot_h + 14), str(th_val), fill=WHITE, anchor="mm", font=f_normal)
    
    # Y-axis label
    y_label = labels['y_axis_s']
    img.paste(y_label, (px + 5, plot_y - 22), y_label)
    
    for s_val in [0, 0.25, 0.5, 0.75, 1.0]:
        y = to_y(s_val)
        draw.text((plot_x - 8, y), f"{s_val:.2f}", fill=WHITE, anchor="rm", font=f_normal)
    
    # Equation
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
    
    # Grid
    for g_val in [0.25, 0.5, 0.75, 1.0]:
        y = to_y(g_val)
        draw.line([(plot_x, y), (plot_x + plot_w, y)], fill=(40, 50, 70), width=1)
    for r_val in [0.5, 1.0]:
        x = to_x(r_val)
        draw.line([(x, plot_y), (x, plot_y + plot_h)], fill=(40, 50, 70), width=1)
    
    # Axes
    draw.line([(plot_x, zero_y), (plot_x + plot_w, zero_y)], fill=WHITE, width=2)
    draw.line([(plot_x, plot_y), (plot_x, plot_y + plot_h)], fill=WHITE, width=2)
    
    # Homogeneous curve (dashed)
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
    
    # Heterogeneous curve
    het_pts = []
    for i in range(101):
        r = i/100 * r_max
        g = dG(r, sf)
        if 0 <= g <= dg_max:
            het_pts.append((to_x(r), to_y(g)))
    if len(het_pts) >= 2:
        draw.line(het_pts, fill=CYAN, width=3)
    
    # Critical points
    r_star_x = to_x(1.0)
    hom_peak_y = to_y(1.0)
    het_peak_y = to_y(sf)
    
    draw.line([(r_star_x, plot_y), (r_star_x, zero_y)], fill=(60, 80, 100), width=1)
    draw_dashed(draw, r_star_x, zero_y, r_star_x, hom_peak_y, ORANGE, 4, 3, 1)
    draw.ellipse([r_star_x-5, hom_peak_y-5, r_star_x+5, hom_peak_y+5], fill=GRAY, outline=WHITE)
    draw_dashed(draw, r_star_x+2, zero_y, r_star_x+2, het_peak_y, ORANGE, 4, 3, 1)
    draw.ellipse([r_star_x-7, het_peak_y-7, r_star_x+7, het_peak_y+7], fill=ORANGE, outline=WHITE, width=2)
    
    # Barrier arrow
    if sf < 0.85:
        ax = r_star_x + 22
        draw.line([(ax, zero_y-2), (ax, het_peak_y+2)], fill=ORANGE, width=2)
        draw.polygon([(ax, het_peak_y), (ax-4, het_peak_y+8), (ax+4, het_peak_y+8)], fill=ORANGE)
        draw.polygon([(ax, zero_y), (ax-4, zero_y-8), (ax+4, zero_y-8)], fill=ORANGE)
    
    # Legend
    lx, ly = plot_x + plot_w - 5, plot_y + 12
    draw.line([(lx-115, ly), (lx-88, ly)], fill=GRAY, width=2)
    draw.text((lx-84, ly), "Homogeneous", fill=WHITE, anchor="lm", font=f_small)
    draw.line([(lx-115, ly+16), (lx-88, ly+16)], fill=CYAN, width=3)
    draw.text((lx-84, ly+16), "Heterogeneous", fill=WHITE, anchor="lm", font=f_small)
    
    # X-axis label
    x_label = labels['x_axis_r']
    img.paste(x_label, (plot_x + plot_w//2 - x_label.width//2, plot_y + plot_h + 25), x_label)
    
    for r_val in [0, 0.5, 1.0, 1.5]:
        x = to_x(r_val)
        label = "r*" if r_val == 1.0 else f"{r_val:.1f}"
        draw.text((x, zero_y + 14), label, fill=WHITE, anchor="mm", font=f_normal)
    
    # Y-axis label
    y_label = labels['y_axis_dg']
    img.paste(y_label, (px + 2, plot_y - 18), y_label)
    
    for g_val in [0, 0.5, 1.0]:
        y = to_y(g_val)
        draw.text((plot_x - 8, y), f"{g_val:.1f}", fill=WHITE, anchor="rm", font=f_normal)
    
    # Equation
    barrier_eq = labels['barrier_eq']
    paste_with_background(img, barrier_eq, plot_x + 8, plot_y + int(plot_h * 0.25), bg_color=(25, 40, 65))


def draw_frame(theta_deg, labels, fonts):
    img = Image.new('RGBA', (WIDTH, HEIGHT), BG_COLOR + (255,))
    draw = ImageDraw.Draw(img)
    
    gap = 8
    panel_w = (WIDTH - 4*gap) // 3
    panel_h = HEIGHT - 2*gap
    
    draw_geometry_panel(img, draw, theta_deg, gap, gap, panel_w, panel_h, fonts, labels)
    draw_shape_factor_panel(img, draw, theta_deg, gap*2 + panel_w, gap, panel_w, panel_h, fonts, labels)
    draw_barrier_panel(img, draw, theta_deg, gap*3 + panel_w*2, gap, panel_w, panel_h, fonts, labels)
    
    return img.convert('RGB')


# =============================================================================
# MAIN - Generate GIF
# =============================================================================
if __name__ == "__main__":
    print("Generating 3-panel visualization GIF...")
    print("Pre-rendering LaTeX labels...")
    
    labels = get_latex_labels()
    fonts = get_fonts()
    
    frames = []
    
    # Sweep from 15° to 165° and back
    angles = list(range(15, 166, 2)) + list(range(164, 14, -2))
    
    print(f"Rendering {len(angles)} frames...")
    
    for i, theta in enumerate(angles):
        if i % 20 == 0:
            print(f"  Frame {i+1}/{len(angles)} (θ = {theta}°)")
        frame = draw_frame(theta, labels, fonts)
        frames.append(frame)
    
    print("Saving GIF...")
    frames[0].save(
        'assets/heterogeneous_nucleation.gif',
        save_all=True,
        append_images=frames[1:],
        duration=60,  # ms per frame
        loop=0
    )
    
    # Also save to root for backward compatibility
    frames[0].save(
        'heterogeneous_nucleation.gif',
        save_all=True,
        append_images=frames[1:],
        duration=60,
        loop=0
    )
    
    print(f"\nDone! Created:")
    print(f"  - assets/heterogeneous_nucleation.gif")
    print(f"  - heterogeneous_nucleation.gif")
