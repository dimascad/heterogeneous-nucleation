#!/usr/bin/env python3
"""
Heterogeneous Nucleation Visualization
Three panels: Geometry | S(θ) curve | ΔG barrier curve
With proper axis labels, units, and high-contrast colors
"""

import math
from PIL import Image, ImageDraw, ImageFont

WIDTH = 1100
HEIGHT = 500

# High contrast color scheme
BG_COLOR = (15, 25, 45)
PANEL_BG = (20, 32, 55)
SUBSTRATE_COLOR = (70, 100, 140)
SUBSTRATE_HATCH = (55, 85, 120)
NUCLEUS_COLOR = (255, 130, 170)
NUCLEUS_OUTLINE = (255, 80, 130)

# Text colors - high contrast on dark blue
WHITE = (255, 255, 255)
YELLOW = (255, 220, 100)
ORANGE = (255, 180, 100)
CYAN = (100, 240, 255)
GREEN = (100, 255, 150)
RED = (255, 100, 100)
GOLD = (255, 215, 0)
GRAY = (150, 150, 160)
LIGHT_GRAY = (120, 120, 130)


def S(theta_deg):
    """Shape factor S(θ) = (2 + cosθ)(1 - cosθ)² / 4"""
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


def draw_dashed(draw, x1, y1, x2, y2, color, dash=5, gap=3, width=1):
    length = math.hypot(x2-x1, y2-y1)
    if length == 0:
        return
    dx, dy = (x2-x1)/length, (y2-y1)/length
    pos = 0
    while pos < length:
        sx, sy = x1 + pos*dx, y1 + pos*dy
        ep = min(pos + dash, length)
        draw.line([(sx, sy), (x1 + ep*dx, y1 + ep*dy)], fill=color, width=width)
        pos += dash + gap


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
    """Draw spherical cap nucleus. Returns (height, center_y, R)."""
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
        if len(arc_pts) >= 2:
            draw.line(arc_pts, fill=NUCLEUS_OUTLINE, width=3)
    
    h = R * (1 - cos_t)
    return (h, Cy, R)


def draw_geometry_panel(draw, theta_deg, px, py, pw, ph, fonts):
    """Left panel: nucleus geometry with surface tensions"""
    f_small, f_normal, f_medium, f_large, f_title, f_bigtitle = fonts
    
    # Panel background
    draw.rectangle([px, py, px+pw, py+ph], fill=PANEL_BG, outline=LIGHT_GRAY)
    draw.text((px + pw//2, py + 18), "NUCLEUS GEOMETRY", fill=YELLOW, anchor="mm", font=f_bigtitle)
    
    cx = px + pw//2
    baseY = py + int(ph * 0.58)  # Position for nucleus
    
    # Substrate - very thin strip (1/4 of previous height)
    substrate_top = baseY
    substrate_bottom = baseY + 35  # Just 35 pixels tall
    draw.rectangle([px+5, substrate_top, px+pw-5, substrate_bottom], fill=SUBSTRATE_COLOR)
    for i in range(px, px+pw, 8):
        draw.line([(i, substrate_top), (i+12, substrate_bottom)], fill=SUBSTRATE_HATCH, width=1)
    
    # Nucleus
    a = 55
    h, Cy, R = draw_nucleus(draw, cx, baseY, theta_deg, a)
    
    # Draw radius of curvature visualization
    theta_rad = math.radians(theta_deg)
    
    # Only draw if radius is reasonable size to display
    if 25 < theta_deg < 150 and R < 200:
        top_of_cap_y = baseY - h
        
        # For lower angles, draw dashed arc to complete the circle below the substrate
        # This shows the full sphere that the spherical cap belongs to
        if theta_deg < 100 and R < 150 and R > 30:
            # Draw dashed arc for the part of the circle BELOW the substrate (inside it)
            # The cap is above baseY, so we draw the arc below baseY
            num_segments = 40
            arc_pts = []
            for i in range(num_segments + 1):
                # Go from right contact point, down around, to left contact point
                # Angles from the center Cy: the cap spans from about -theta to +theta from horizontal
                # We want to draw the OTHER part of the circle
                start_angle = -math.pi/2 + theta_rad  # right side, going down
                end_angle = -math.pi/2 - theta_rad + 2*math.pi  # left side, coming up (going the long way)
                
                # Actually simpler: draw from angle going down from right contact point
                # Right contact is at angle = asin(a/R) above horizontal from center
                # We want the arc that goes DOWN and around
                
                t = i / num_segments
                # Arc from right contact, down through bottom, to left contact
                angle = (math.pi/2 - theta_rad) + t * (2*math.pi - 2*(math.pi/2 - theta_rad))
                angle = (math.pi/2 - theta_rad) + t * (2*theta_rad - math.pi)
                
            # Simpler approach: draw arc from one contact point to the other, going THROUGH the bottom
            for i in range(num_segments + 1):
                t = i / num_segments
                # Start at right contact point angle, go clockwise (down) to left contact point
                # Right contact: angle where circle intersects baseY on right = asin((baseY-Cy)/R)... 
                # Actually, at right contact point (cx+a, baseY): angle from center (cx, Cy) is:
                right_angle = math.atan2(baseY - Cy, a)  # angle to right contact point
                left_angle = math.atan2(baseY - Cy, -a)  # angle to left contact point
                
                # We want to go from right_angle DOWN to left_angle (the long way, through bottom)
                # right_angle is positive (pointing up-right from center below)
                # left_angle is positive (pointing up-left)
                # Going clockwise from right: right_angle -> 0 -> -pi -> left_angle-2pi
                
                if i == 0:
                    angle = right_angle
                else:
                    # Interpolate going the "down" way
                    arc_span = (2*math.pi) - (left_angle - right_angle)
                    angle = right_angle - t * arc_span
                
                px_arc = cx + R * math.cos(angle)
                py_arc = Cy + R * math.sin(angle)
                arc_pts.append((px_arc, py_arc))
            
            # Draw as dashed line
            for i in range(len(arc_pts) - 1):
                if i % 4 < 2:  # Dashed pattern
                    # Only draw if within panel bounds
                    if (py + 35 < arc_pts[i][1] < py + ph - 5 and 
                        py + 35 < arc_pts[i+1][1] < py + ph - 5 and
                        px + 5 < arc_pts[i][0] < px + pw - 5):
                        draw.line([arc_pts[i], arc_pts[i+1]], fill=(150, 170, 200), width=2)
        
        # Draw center of curvature point
        if py + 45 < Cy < baseY + 60:
            draw.ellipse([cx-5, Cy-5, cx+5, Cy+5], fill=WHITE, outline=(100,100,120))
        
        # Draw radius line from center to the apex of the cap
        if py + 45 < Cy < baseY + 30:
            draw_dashed(draw, cx, min(Cy, baseY-3), cx, top_of_cap_y, WHITE, 6, 4, 2)
            # Label "r" at midpoint
            mid_y = (min(Cy, baseY - 10) + top_of_cap_y) / 2
            if mid_y > py + 55 and mid_y < baseY - 15:
                draw.text((cx + 12, mid_y), "r", fill=WHITE, font=f_large)
    
    # Surface tension vectors - LONGER and THICKER
    tpX, tpY = cx + a, baseY
    L = 90
    
    # γ_SN - points LEFT - plain BLACK - THICKER
    draw.line([(tpX, tpY), (tpX - L, tpY)], fill=(0, 0, 0), width=5)
    # Arrowhead - BIGGER - pointing LEFT
    al = 20
    ah_pts = [(tpX - L, tpY),
              (tpX - L + al, tpY - al*0.35),
              (tpX - L + al, tpY + al*0.35)]
    draw.polygon(ah_pts, fill=(0, 0, 0))
    
    # γ_SL - points RIGHT (white) - THICKER
    draw_arrow(draw, tpX, tpY, tpX + L, tpY, WHITE, 5, arrow_len=20)
    
    # γ_NL - points UP-LEFT along tangent (gold) - THICKER
    nlX = tpX - L * math.cos(theta_rad)
    nlY = tpY - L * math.sin(theta_rad)
    draw_arrow(draw, tpX, tpY, nlX, nlY, GOLD, 5, arrow_len=20)
    
    # Tangent dashed line
    ext = 95
    draw_dashed(draw, tpX - ext*math.cos(theta_rad), tpY - ext*math.sin(theta_rad),
                tpX + ext*0.3*math.cos(theta_rad), tpY + ext*0.3*math.sin(theta_rad),
                (180, 160, 80), 4, 3, 1)
    
    # Contact angle arc - BRIGHT GREEN - WIDER
    ar = 38
    draw.arc([tpX-ar, tpY-ar, tpX+ar, tpY+ar], start=180, end=180+theta_deg, fill=GREEN, width=5)
    
    # Triple point dot
    draw.ellipse([tpX-5, tpY-5, tpX+5, tpY+5], fill=WHITE, outline=GREEN, width=2)
    
    # Vector labels - TITLE font (largest bold), positioned for longer vectors
    draw.text((tpX - L - 16, tpY - 24), "γₛₙ", fill=(0, 0, 0), font=f_title)
    draw.text((tpX + L + 10, tpY - 24), "γₛₗ", fill=WHITE, font=f_title)
    draw.text((nlX - 36, nlY - 14), "γₙₗ", fill=GOLD, font=f_title)
    
    # Region labels
    draw.text((cx, substrate_bottom - 12), "Substrate", fill=WHITE, anchor="mm", font=f_small)
    draw.text((px + 12, py + 42), "Liquid", fill=WHITE, font=f_normal)
    if h > 20:
        draw.text((cx, baseY - min(h*0.5, 50)), "Nucleus", fill=WHITE, anchor="mm", font=f_normal)
    
    # Info display - GREEN for theta (consistent everywhere), CYAN for S(θ)
    sf = S(theta_deg)
    draw.text((px + 12, py + 65), f"θ = {theta_deg:.0f}°", fill=GREEN, font=f_large)
    draw.text((px + 12, py + 88), f"S(θ) = {sf:.4f}", fill=CYAN, font=f_normal)
    
    # Wetting description
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
    
    # Surface tension legend at bottom - with LIGHT BLUE BACKGROUND box
    ly = py + ph - 55
    legend_box = [px + 5, ly - 2, px + 155, ly + 48]
    draw.rectangle(legend_box, fill=(45, 65, 95), outline=(80, 100, 130))
    
    # Legend entries (no header, just the items)
    draw.line([(px + 10, ly + 8), (px + 28, ly + 8)], fill=(0, 0, 0), width=3)
    draw.text((px + 32, ly + 8), "γₛₙ Solid-Nucleus", fill=(0, 0, 0), anchor="lm", font=f_small)
    
    draw.line([(px + 10, ly + 22), (px + 28, ly + 22)], fill=WHITE, width=3)
    draw.text((px + 32, ly + 22), "γₛₗ Solid-Liquid", fill=WHITE, anchor="lm", font=f_small)
    
    draw.line([(px + 10, ly + 36), (px + 28, ly + 36)], fill=GOLD, width=3)
    draw.text((px + 32, ly + 36), "γₙₗ Nucleus-Liquid", fill=GOLD, anchor="lm", font=f_small)
    
    # Young's equation - bottom right
    draw.text((px + pw - 8, ly + 8), "Young's equation:", fill=GRAY, anchor="rt", font=f_small)
    draw.text((px + pw - 8, ly + 26), "γₛₗ = γₛₙ + γₙₗ·cosθ", fill=WHITE, anchor="rt", font=f_normal)


def draw_shape_factor_panel(draw, theta_deg, px, py, pw, ph, fonts):
    """Middle panel: S(θ) vs θ curve with proper axes"""
    f_small, f_normal, f_medium, f_large, f_title, f_bigtitle = fonts
    
    draw.rectangle([px, py, px+pw, py+ph], fill=PANEL_BG, outline=LIGHT_GRAY)
    draw.text((px + pw//2, py + 18), "SHAPE FACTOR S(θ)", fill=YELLOW, anchor="mm", font=f_bigtitle)
    
    # Current value annotation - TOP CENTER, CYAN to match the curve
    sf = S(theta_deg)
    draw.text((px + pw//2, py + 42), f"S({theta_deg:.0f}°) = {sf:.4f}", fill=CYAN, anchor="mm", font=f_medium)
    
    # Plot area - more space now that equation moves inside
    margin = {'l': 55, 'r': 15, 't': 60, 'b': 55}
    plot_x = px + margin['l']
    plot_y = py + margin['t']
    plot_w = pw - margin['l'] - margin['r']
    plot_h = ph - margin['t'] - margin['b']
    
    def to_x(th): return plot_x + (th / 180) * plot_w
    def to_y(s): return plot_y + plot_h - s * plot_h
    
    # Grid lines
    for s_val in [0.25, 0.5, 0.75]:
        y = to_y(s_val)
        draw.line([(plot_x, y), (plot_x + plot_w, y)], fill=(40, 50, 70), width=1)
    for th_val in [45, 90, 135]:
        x = to_x(th_val)
        draw.line([(x, plot_y), (x, plot_y + plot_h)], fill=(40, 50, 70), width=1)
    
    # Axes
    draw.line([(plot_x, plot_y + plot_h), (plot_x + plot_w, plot_y + plot_h)], fill=WHITE, width=2)
    draw.line([(plot_x, plot_y), (plot_x, plot_y + plot_h)], fill=WHITE, width=2)
    
    # S(θ) curve - CYAN
    pts = [(to_x(th), to_y(S(th))) for th in range(0, 181, 2)]
    draw.line(pts, fill=CYAN, width=3)
    
    # Current point - GREEN to match θ color everywhere
    curr_x, curr_y = to_x(theta_deg), to_y(S(theta_deg))
    draw.ellipse([curr_x-8, curr_y-8, curr_x+8, curr_y+8], fill=GREEN, outline=WHITE, width=2)
    
    # Dashed lines to current point
    draw_dashed(draw, curr_x, plot_y + plot_h, curr_x, curr_y, GRAY, 4, 3, 1)
    draw_dashed(draw, plot_x, curr_y, curr_x, curr_y, GRAY, 4, 3, 1)
    
    # X-axis label - GREEN for θ - LARGER
    draw.text((plot_x + plot_w//2, plot_y + plot_h + 32), "Contact Angle θ (degrees)", 
              fill=GREEN, anchor="mm", font=f_medium)
    
    # X-axis tick labels - LARGER
    for th_val in [0, 45, 90, 135, 180]:
        x = to_x(th_val)
        draw.text((x, plot_y + plot_h + 14), str(th_val), fill=WHITE, anchor="mm", font=f_normal)
    
    # Y-axis label - CYAN for S(θ) - LARGER, positioned higher to avoid overlap with 1.00
    draw.text((px + 6, plot_y - 22), "S(θ)", fill=CYAN, font=f_large)
    
    # Y-axis tick labels - LARGER
    for s_val in [0, 0.25, 0.5, 0.75, 1.0]:
        y = to_y(s_val)
        draw.text((plot_x - 8, y), f"{s_val:.2f}", fill=WHITE, anchor="rm", font=f_normal)
    
    # Shape factor equation ON THE PLOT - middle-right-bottom area (below curve)
    eq_x = plot_x + int(plot_w * 0.72)
    eq_y = plot_y + int(plot_h * 0.78)
    draw.text((eq_x, eq_y), "S(θ) = (2+cosθ)(1−cosθ)²/4", fill=CYAN, anchor="mm", font=f_normal)


def draw_barrier_panel(draw, theta_deg, px, py, pw, ph, fonts):
    """Right panel: ΔG vs r with barrier comparison"""
    f_small, f_normal, f_medium, f_large, f_title, f_bigtitle = fonts
    
    draw.rectangle([px, py, px+pw, py+ph], fill=PANEL_BG, outline=LIGHT_GRAY)
    draw.text((px + pw//2, py + 18), "NUCLEATION BARRIER ΔG*", fill=YELLOW, anchor="mm", font=f_bigtitle)
    
    sf = S(theta_deg)
    
    # Barrier percentage annotation - TOP CENTER, ORANGE for ΔG
    draw.text((px + pw//2, py + 42), f"ΔG*ₕₑₜ = {sf*100:.1f}% of ΔG*ₕₒₘ", fill=ORANGE, anchor="mm", font=f_medium)
    
    # Plot area - more space now that equation moves inside
    margin = {'l': 55, 'r': 15, 't': 60, 'b': 55}
    plot_x = px + margin['l']
    plot_y = py + margin['t']
    plot_w = pw - margin['l'] - margin['r']
    plot_h = ph - margin['t'] - margin['b']
    
    def dG(r, s=1): 
        return s * (3*r**2 - 2*r**3) if r > 0 else 0
    
    r_max = 1.5
    dg_max = 1.15
    dg_min = 0
    
    def to_x(r): return plot_x + (r/r_max) * plot_w
    def to_y(g): return plot_y + (dg_max - max(g, 0)) / dg_max * plot_h
    
    zero_y = to_y(0)
    
    # Grid lines
    for g_val in [0.25, 0.5, 0.75, 1.0]:
        y = to_y(g_val)
        draw.line([(plot_x, y), (plot_x + plot_w, y)], fill=(40, 50, 70), width=1)
    for r_val in [0.5, 1.0]:
        x = to_x(r_val)
        draw.line([(x, plot_y), (x, plot_y + plot_h)], fill=(40, 50, 70), width=1)
    
    # Axes
    draw.line([(plot_x, zero_y), (plot_x + plot_w, zero_y)], fill=WHITE, width=2)
    draw.line([(plot_x, plot_y), (plot_x, plot_y + plot_h)], fill=WHITE, width=2)
    
    # Homogeneous curve (dashed gray) - S=1, only where ΔG >= 0
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
    
    # Heterogeneous curve (solid cyan) - current S(θ), only where ΔG >= 0
    het_pts = []
    for i in range(101):
        r = i/100 * r_max
        g = dG(r, sf)
        if 0 <= g <= dg_max:
            het_pts.append((to_x(r), to_y(g)))
    if len(het_pts) >= 2:
        draw.line(het_pts, fill=CYAN, width=3)
    
    # Critical point markers
    r_star_x = to_x(1.0)
    hom_peak_y = to_y(1.0)
    het_peak_y = to_y(sf)
    
    # Vertical line at r* showing BOTH curves peak here
    # Light vertical band to highlight r* region
    draw.line([(r_star_x, plot_y), (r_star_x, zero_y)], fill=(60, 80, 100), width=1)
    
    # Dashed vertical line to homogeneous peak - ORANGE
    draw_dashed(draw, r_star_x, zero_y, r_star_x, hom_peak_y, ORANGE, 4, 3, 1)
    draw.ellipse([r_star_x-5, hom_peak_y-5, r_star_x+5, hom_peak_y+5], fill=GRAY, outline=WHITE)
    
    # Dashed vertical line to heterogeneous peak - ORANGE
    draw_dashed(draw, r_star_x+2, zero_y, r_star_x+2, het_peak_y, ORANGE, 4, 3, 1)
    draw.ellipse([r_star_x-7, het_peak_y-7, r_star_x+7, het_peak_y+7], fill=ORANGE, outline=WHITE, width=2)
    
    # Barrier height arrow (if significant difference) - ORANGE
    if sf < 0.85:
        ax = r_star_x + 22
        draw.line([(ax, zero_y-2), (ax, het_peak_y+2)], fill=ORANGE, width=2)
        draw.polygon([(ax, het_peak_y), (ax-4, het_peak_y+8), (ax+4, het_peak_y+8)], fill=ORANGE)
        draw.polygon([(ax, zero_y), (ax-4, zero_y-8), (ax+4, zero_y-8)], fill=ORANGE)
    
    # Legend - spelled out, positioned in top right with enough space
    lx, ly = plot_x + plot_w - 5, plot_y + 12
    draw.line([(lx-115, ly), (lx-88, ly)], fill=GRAY, width=2)
    draw.text((lx-84, ly), "Homogeneous", fill=WHITE, anchor="lm", font=f_small)
    draw.line([(lx-115, ly+16), (lx-88, ly+16)], fill=CYAN, width=3)
    draw.text((lx-84, ly+16), "Heterogeneous", fill=WHITE, anchor="lm", font=f_small)
    
    # X-axis label - LARGER
    draw.text((plot_x + plot_w//2, plot_y + plot_h + 32), "Normalized Radius r/r*", 
              fill=WHITE, anchor="mm", font=f_medium)
    
    # X-axis tick labels - LARGER
    for r_val in [0, 0.5, 1.0, 1.5]:
        x = to_x(r_val)
        label = "r*" if r_val == 1.0 else f"{r_val:.1f}"
        draw.text((x, zero_y + 14), label, fill=WHITE, anchor="mm", font=f_normal)
    
    # Y-axis label - ORANGE for ΔG - LARGER
    draw.text((px + 5, plot_y - 12), "ΔG/ΔG*ₕₒₘ", fill=ORANGE, font=f_medium)
    
    # Y-axis tick labels - LARGER
    for g_val in [0, 0.5, 1.0]:
        y = to_y(g_val)
        draw.text((plot_x - 8, y), f"{g_val:.1f}", fill=WHITE, anchor="rm", font=f_normal)
    
    # Barrier reduction equation ON THE PLOT - top left area (above het curve)
    eq_x = plot_x + int(plot_w * 0.30)
    eq_y = plot_y + int(plot_h * 0.15)
    draw.text((eq_x, eq_y), "ΔG*ₕₑₜ = S(θ)·ΔG*ₕₒₘ", fill=ORANGE, anchor="mm", font=f_medium)


def draw_frame(theta_deg):
    img = Image.new('RGB', (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    fonts = get_fonts()
    
    gap = 12
    pw = (WIDTH - 4*gap) // 3
    ph = HEIGHT - 2*gap
    
    draw_geometry_panel(draw, theta_deg, gap, gap, pw, ph, fonts)
    draw_shape_factor_panel(draw, theta_deg, 2*gap + pw, gap, pw, ph, fonts)
    draw_barrier_panel(draw, theta_deg, 3*gap + 2*pw, gap, pw, ph, fonts)
    
    return img


def main():
    # Generate preview images
    for th in [20, 60, 90, 120, 160]:
        img = draw_frame(th)
        img.save(f'preview_{th}.png')
        print(f'Saved preview_{th}.png')
    
    # Generate GIF
    frames = []
    angles = list(range(10, 171, 2)) + list(range(170, 9, -2))
    print(f"Generating {len(angles)} frames...")
    for theta in angles:
        frames.append(draw_frame(theta))
    
    frames[0].save('heterogeneous_nucleation.gif', save_all=True, 
                   append_images=frames[1:], duration=50, loop=0)
    print('Saved heterogeneous_nucleation.gif')


if __name__ == "__main__":
    main()
