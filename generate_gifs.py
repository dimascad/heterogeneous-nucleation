"""
Generate GIFs for all interactive visualizations in the heterogeneous nucleation notebook.
Outputs to assets/ folder.
"""

import math
import io
import os
from PIL import Image, ImageDraw, ImageFont

# Create assets folder
os.makedirs('assets', exist_ok=True)

# Colors
BG_COLOR = (15, 23, 42)
PANEL_BG = (30, 41, 59)
WHITE = (255, 255, 255)
GRAY = (148, 163, 184)
RED = (248, 113, 113)
GREEN = (34, 197, 94)
YELLOW = (250, 204, 21)
ORANGE = (249, 115, 22)
CYAN = (100, 240, 255)
PURPLE = (167, 139, 250)
PINK = (236, 72, 153)
GOLD = (255, 215, 0)

def get_font(size=12):
    try:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)
    except:
        return ImageFont.load_default()

def S(theta_deg):
    """Shape factor"""
    theta = math.radians(theta_deg)
    c = math.cos(theta)
    return (2 + c) * (1 - c) ** 2 / 4


# =============================================================================
# GIF 1: Energy Competition
# =============================================================================
def generate_energy_competition_gif():
    frames = []
    width, height = 500, 300
    
    for frame in range(60):
        # Oscillate r/r* from 0.2 to 1.8
        t = frame / 59
        r_ratio = 0.2 + 1.6 * (0.5 - 0.5 * math.cos(t * 2 * math.pi))
        
        img = Image.new('RGB', (width, height), BG_COLOR)
        draw = ImageDraw.Draw(img)
        font = get_font(11)
        font_lg = get_font(14)
        
        # Plot area
        plot_x, plot_y = 60, 40
        plot_w, plot_h = 380, 200
        
        # Axes
        draw.line([(plot_x, plot_y + plot_h), (plot_x + plot_w, plot_y + plot_h)], fill=WHITE, width=2)
        draw.line([(plot_x, plot_y), (plot_x, plot_y + plot_h)], fill=WHITE, width=2)
        
        # Labels
        draw.text((plot_x + plot_w // 2, plot_y + plot_h + 25), "r / r*", fill=WHITE, anchor="mm", font=font)
        draw.text((plot_x - 10, plot_y + plot_h // 2), "ΔG", fill=WHITE, anchor="rm", font=font)
        
        # Draw curves
        max_r = 2.0
        max_e = 1.5
        
        def to_x(r): return plot_x + (r / max_r) * plot_w
        def to_y(e): return plot_y + plot_h - ((e + 0.5) / max_e) * plot_h
        
        # Surface energy (red, positive, r^2)
        surface_pts = []
        for i in range(100):
            r = i / 99 * max_r
            e = 0.4 * r ** 2
            if e < max_e:
                surface_pts.append((to_x(r), to_y(e)))
        if len(surface_pts) > 1:
            draw.line(surface_pts, fill=RED, width=2)
        
        # Volume energy (green, negative, -r^3)
        volume_pts = []
        for i in range(100):
            r = i / 99 * max_r
            e = -0.3 * r ** 3
            if e > -0.5:
                volume_pts.append((to_x(r), to_y(e)))
        if len(volume_pts) > 1:
            draw.line(volume_pts, fill=GREEN, width=2)
        
        # Net energy (purple)
        net_pts = []
        for i in range(100):
            r = i / 99 * max_r
            e = 0.4 * r ** 2 - 0.3 * r ** 3
            if -0.5 < e < max_e:
                net_pts.append((to_x(r), to_y(e)))
        if len(net_pts) > 1:
            draw.line(net_pts, fill=PURPLE, width=3)
        
        # Current point
        r = r_ratio
        e_net = 0.4 * r ** 2 - 0.3 * r ** 3
        px, py = to_x(r), to_y(e_net)
        draw.ellipse([px-8, py-8, px+8, py+8], fill=YELLOW, outline=WHITE, width=2)
        
        # Zero line
        draw.line([(plot_x, to_y(0)), (plot_x + plot_w, to_y(0))], fill=GRAY, width=1)
        
        # r* marker
        draw.line([(to_x(1), plot_y), (to_x(1), plot_y + plot_h)], fill=GRAY, width=1)
        draw.text((to_x(1), plot_y + plot_h + 10), "r*", fill=YELLOW, anchor="mm", font=font)
        
        # Legend
        draw.text((plot_x + 10, plot_y + 5), "Surface ∝ r²", fill=RED, font=font)
        draw.text((plot_x + 10, plot_y + 20), "Volume ∝ -r³", fill=GREEN, font=font)
        draw.text((plot_x + 10, plot_y + 35), "Net ΔG", fill=PURPLE, font=font)
        
        # Current value
        draw.text((width - 20, 20), f"r/r* = {r_ratio:.2f}", fill=YELLOW, anchor="rt", font=font_lg)
        
        frames.append(img)
    
    frames[0].save('assets/energy_competition.gif', save_all=True, append_images=frames[1:], 
                   duration=80, loop=0)
    print("Created energy_competition.gif")


# =============================================================================
# GIF 2: Nucleus Fate
# =============================================================================
def generate_nucleus_fate_gif():
    frames = []
    width, height = 500, 280
    
    for frame in range(60):
        t = frame / 59
        r_ratio = 0.3 + 1.4 * (0.5 - 0.5 * math.cos(t * 2 * math.pi))
        
        img = Image.new('RGB', (width, height), BG_COLOR)
        draw = ImageDraw.Draw(img)
        font = get_font(11)
        font_lg = get_font(16)
        
        plot_x, plot_y = 60, 50
        plot_w, plot_h = 380, 160
        
        # Energy curve
        def dG(r): return 3 * r**2 - 2 * r**3 if r > 0 else 0
        def to_x(r): return plot_x + (r / 1.8) * plot_w
        def to_y(g): return plot_y + plot_h - g * plot_h * 0.9
        
        # Draw curve
        pts = [(to_x(i/100 * 1.8), to_y(dG(i/100 * 1.8))) for i in range(100)]
        draw.line(pts, fill=PURPLE, width=3)
        
        # Ball position
        ball_x = to_x(r_ratio)
        ball_y = to_y(dG(r_ratio))
        
        # Draw ball
        draw.ellipse([ball_x-12, ball_y-12, ball_x+12, ball_y+12], fill=ORANGE, outline=WHITE, width=2)
        
        # Arrows showing direction
        if r_ratio < 0.95:
            # Shrinks - arrow left
            draw.polygon([(ball_x - 30, ball_y), (ball_x - 45, ball_y - 8), (ball_x - 45, ball_y + 8)], fill=RED)
            fate = "SHRINKS"
            fate_color = RED
        elif r_ratio > 1.05:
            # Grows - arrow right
            draw.polygon([(ball_x + 30, ball_y), (ball_x + 45, ball_y - 8), (ball_x + 45, ball_y + 8)], fill=GREEN)
            fate = "GROWS"
            fate_color = GREEN
        else:
            fate = "CRITICAL"
            fate_color = YELLOW
        
        # r* line
        draw.line([(to_x(1), plot_y), (to_x(1), plot_y + plot_h + 10)], fill=GRAY, width=1)
        draw.text((to_x(1), plot_y + plot_h + 20), "r*", fill=YELLOW, anchor="mm", font=font)
        
        # Axes
        draw.line([(plot_x, plot_y + plot_h), (plot_x + plot_w, plot_y + plot_h)], fill=WHITE, width=2)
        draw.text((plot_x + plot_w // 2, plot_y + plot_h + 35), "r / r*", fill=WHITE, anchor="mm", font=font)
        
        # Status
        draw.text((width // 2, 20), fate, fill=fate_color, anchor="mm", font=font_lg)
        draw.text((width - 20, 20), f"r/r* = {r_ratio:.2f}", fill=WHITE, anchor="rt", font=font)
        
        frames.append(img)
    
    frames[0].save('assets/nucleus_fate.gif', save_all=True, append_images=frames[1:],
                   duration=80, loop=0)
    print("Created nucleus_fate.gif")


# =============================================================================
# GIF 3: Surface Tensions (Young's Equation)
# =============================================================================
def generate_surface_tensions_gif():
    frames = []
    width, height = 550, 300
    
    for frame in range(60):
        t = frame / 59
        # Vary gamma_sl to change theta
        gamma_sl = 30 + 40 * (0.5 - 0.5 * math.cos(t * 2 * math.pi))
        gamma_sn = 30
        gamma_nl = 50
        
        cos_theta = (gamma_sl - gamma_sn) / gamma_nl
        cos_theta = max(-1, min(1, cos_theta))
        theta_rad = math.acos(cos_theta)
        theta_deg = math.degrees(theta_rad)
        
        img = Image.new('RGB', (width, height), BG_COLOR)
        draw = ImageDraw.Draw(img)
        font = get_font(11)
        font_lg = get_font(14)
        
        # Drawing area
        cx, cy = 300, 160
        
        # Substrate
        draw.rectangle([100, cy, 500, cy + 60], fill=(51, 65, 85))
        draw.line([(100, cy), (500, cy)], fill=ORANGE, width=3)
        
        # Nucleus cap
        R = 70
        if abs(math.sin(theta_rad)) > 0.01:
            cap_left = cx - R * math.sin(theta_rad)
            cap_right = cx + R * math.sin(theta_rad)
            large_arc = 1 if theta_deg > 90 else 0
            # Approximate cap with polygon
            pts = [(cap_left, cy)]
            for i in range(21):
                angle = math.pi - theta_rad + (2 * theta_rad - math.pi) * i / 20
                if theta_deg <= 90:
                    angle = -theta_rad + (theta_rad * 2) * i / 20 + math.pi/2
                px = cx + R * math.cos(math.pi/2 - theta_rad + theta_rad * 2 * i / 20)
                py = cy - R * math.sin(math.pi/2 - theta_rad + theta_rad * 2 * i / 20)
                if py <= cy:
                    pts.append((px, py))
            pts.append((cap_right, cy))
            if len(pts) > 2:
                draw.polygon(pts, fill=(255, 130, 170, 128))
        
        # Contact point
        contact_x = cx + R * math.sin(theta_rad)
        draw.ellipse([contact_x-5, cy-5, contact_x+5, cy+5], fill=WHITE)
        
        # Surface tension vectors
        vec_len = 60
        
        # γ_SL (white, right)
        draw.line([(contact_x, cy), (contact_x + vec_len, cy)], fill=WHITE, width=4)
        draw.polygon([(contact_x + vec_len, cy), (contact_x + vec_len - 10, cy - 6), 
                      (contact_x + vec_len - 10, cy + 6)], fill=WHITE)
        
        # γ_SN (black, left)  
        draw.line([(contact_x, cy), (contact_x - vec_len, cy)], fill=(0, 0, 0), width=4)
        draw.polygon([(contact_x - vec_len, cy), (contact_x - vec_len + 10, cy - 6),
                      (contact_x - vec_len + 10, cy + 6)], fill=(0, 0, 0))
        
        # γ_NL (gold, along cap)
        nl_x = contact_x - vec_len * math.cos(theta_rad)
        nl_y = cy - vec_len * math.sin(theta_rad)
        draw.line([(contact_x, cy), (nl_x, nl_y)], fill=GOLD, width=4)
        
        # Contact angle arc
        arc_r = 30
        arc_bbox = [contact_x - arc_r - arc_r, cy - arc_r, contact_x - arc_r + arc_r, cy + arc_r]
        draw.arc([contact_x - arc_r, cy - arc_r, contact_x + arc_r, cy + arc_r], 
                 start=180, end=180 + theta_deg, fill=(100, 255, 150), width=3)
        
        # Labels
        draw.text((contact_x - arc_r - 15, cy - 20), "θ", fill=(100, 255, 150), font=font_lg)
        
        # Info panel
        draw.rectangle([10, 10, 160, 120], fill=PANEL_BG)
        draw.text((20, 20), f"γSL = {gamma_sl:.0f}", fill=WHITE, font=font)
        draw.text((20, 40), f"γSN = {gamma_sn:.0f}", fill=GRAY, font=font)
        draw.text((20, 60), f"γNL = {gamma_nl:.0f}", fill=GOLD, font=font)
        draw.text((20, 90), f"θ = {theta_deg:.1f}°", fill=(100, 255, 150), font=font_lg)
        
        frames.append(img)
    
    frames[0].save('assets/surface_tensions.gif', save_all=True, append_images=frames[1:],
                   duration=80, loop=0)
    print("Created surface_tensions.gif")


# =============================================================================
# GIF 4: Disk Integration
# =============================================================================
def generate_disk_integration_gif():
    frames = []
    width, height = 450, 350
    
    theta_vol = 70
    theta_rad = math.radians(theta_vol)
    cos_t = math.cos(theta_rad)
    
    for frame in range(50):
        t = frame / 49
        y_frac = 0.05 + 0.9 * (0.5 - 0.5 * math.cos(t * 2 * math.pi))
        
        img = Image.new('RGB', (width, height), BG_COLOR)
        draw = ImageDraw.Draw(img)
        font = get_font(11)
        
        scale = 100
        cx, cy = 200, 180
        
        y_min = cos_t
        y_max = 1.0
        y_current = y_min + y_frac * (y_max - y_min)
        r_disk = math.sqrt(max(0, 1 - y_current**2))
        
        cap_bottom_y = cy - y_min * scale
        cap_top_y = cy - y_max * scale
        slice_y = cy - y_current * scale
        cap_x = math.sqrt(max(0, 1 - y_min**2)) * scale
        
        # Full sphere (dashed) - draw as circle outline
        for i in range(0, 360, 8):
            a1 = math.radians(i)
            a2 = math.radians(i + 4)
            x1, y1 = cx + scale * math.cos(a1), cy - scale * math.sin(a1)
            x2, y2 = cx + scale * math.cos(a2), cy - scale * math.sin(a2)
            draw.line([(x1, y1), (x2, y2)], fill=GRAY, width=2)
        
        # Cap region (shaded)
        cap_pts = [(cx - cap_x, cap_bottom_y)]
        for i in range(21):
            angle = math.asin(cap_x / scale) + (math.pi - 2 * math.asin(cap_x / scale)) * i / 20
            px = cx + scale * math.cos(angle - math.pi/2 + math.asin(cap_x/scale) + math.pi/2)
            py = cy - scale * math.sin(angle - math.pi/2 + math.asin(cap_x/scale) + math.pi/2)
            # Simpler: just trace the top arc
            frac = i / 20
            ang = math.pi/2 - math.asin(cap_x/scale) + 2 * math.asin(cap_x/scale) * frac
            px = cx + scale * math.cos(ang)
            py = cy - scale * math.sin(ang)
            if py <= cap_bottom_y:
                cap_pts.append((px, py))
        cap_pts.append((cx + cap_x, cap_bottom_y))
        if len(cap_pts) > 2:
            draw.polygon(cap_pts, fill=(249, 115, 22, 60))
        
        # Cap outline
        draw.arc([cx - scale, cy - scale, cx + scale, cy + scale], 
                 start=-90 - math.degrees(math.asin(cap_x/scale)),
                 end=-90 + math.degrees(math.asin(cap_x/scale)), 
                 fill=ORANGE, width=3)
        
        # Base of cap
        draw.line([(cx - cap_x, cap_bottom_y), (cx + cap_x, cap_bottom_y)], fill=ORANGE, width=2)
        
        # Disk slice (ellipse)
        disk_left = cx - r_disk * scale
        disk_right = cx + r_disk * scale
        draw.ellipse([disk_left, slice_y - 8, disk_right, slice_y + 8], 
                     fill=(34, 197, 94, 128), outline=GREEN, width=2)
        
        # r(y) line
        draw.line([(cx, slice_y), (disk_right, slice_y)], fill=GREEN, width=2)
        draw.text((cx + r_disk * scale / 2, slice_y - 15), "r(y)", fill=GREEN, anchor="mm", font=font)
        
        # dy indicator
        draw.line([(disk_right + 15, slice_y - 8), (disk_right + 15, slice_y + 8)], fill=PURPLE, width=2)
        draw.text((disk_right + 25, slice_y), "dy", fill=PURPLE, anchor="lm", font=font)
        
        # Y-axis labels
        draw.text((cx - 50, cap_top_y), "y = R", fill=ORANGE, anchor="rm", font=font)
        draw.text((cx - 50, cap_bottom_y), "y = R−h", fill=ORANGE, anchor="rm", font=font)
        
        # Integration arrow
        draw.line([(30, cap_bottom_y - 5), (30, cap_top_y + 5)], fill=ORANGE, width=2)
        draw.polygon([(30, cap_top_y + 5), (26, cap_top_y + 15), (34, cap_top_y + 15)], fill=ORANGE)
        draw.text((20, (cap_top_y + cap_bottom_y) / 2), "∫", fill=ORANGE, font=get_font(16))
        
        # Info
        draw.text((width - 20, 20), f"y/R = {y_current:.3f}", fill=GREEN, anchor="rt", font=font)
        draw.text((width - 20, 40), f"r(y)/R = {r_disk:.3f}", fill=GREEN, anchor="rt", font=font)
        
        # Title
        draw.text((width // 2, 320), "Disk Integration: V = ∫π(R² − y²)dy", fill=WHITE, anchor="mm", font=font)
        
        frames.append(img)
    
    frames[0].save('assets/disk_integration.gif', save_all=True, append_images=frames[1:],
                   duration=100, loop=0)
    print("Created disk_integration.gif")


# =============================================================================
# GIF 5: Three-Panel Dashboard
# =============================================================================
def generate_three_panel_gif():
    frames = []
    width, height = 700, 300
    
    for frame in range(60):
        t = frame / 59
        theta_deg = 15 + 150 * t  # Sweep from 15° to 165°
        theta_rad = math.radians(theta_deg)
        cos_t = math.cos(theta_rad)
        sin_t = math.sin(theta_rad)
        sf = S(theta_deg)
        
        img = Image.new('RGB', (width, height), BG_COLOR)
        draw = ImageDraw.Draw(img)
        font = get_font(10)
        font_lg = get_font(12)
        
        panel_w = 220
        gap = 10
        
        # === Panel 1: Geometry ===
        p1_x = gap
        draw.rectangle([p1_x, gap, p1_x + panel_w, height - gap], fill=PANEL_BG)
        
        cx1, cy1 = p1_x + panel_w // 2, 160
        R = 50
        
        # Substrate
        draw.rectangle([p1_x + 10, cy1, p1_x + panel_w - 10, cy1 + 30], fill=(51, 65, 85))
        draw.line([(p1_x + 10, cy1), (p1_x + panel_w - 10, cy1)], fill=ORANGE, width=2)
        
        # Cap
        if sin_t > 0.05:
            a = R * sin_t
            cap_pts = [(cx1 - a, cy1)]
            for i in range(21):
                frac = i / 20
                ang = math.pi - theta_rad + 2 * theta_rad * frac
                px = cx1 + R * math.cos(ang - math.pi/2)
                py = cy1 - R * math.sin(ang - math.pi/2)
                if py <= cy1:
                    cap_pts.append((px, py))
            cap_pts.append((cx1 + a, cy1))
            if len(cap_pts) > 2:
                draw.polygon(cap_pts, fill=(255, 130, 170))
        
        draw.text((p1_x + panel_w // 2, 25), "Geometry", fill=YELLOW, anchor="mm", font=font_lg)
        draw.text((p1_x + 15, height - 35), f"θ = {theta_deg:.0f}°", fill=(100, 255, 150), font=font_lg)
        
        # === Panel 2: Shape Factor ===
        p2_x = gap * 2 + panel_w
        draw.rectangle([p2_x, gap, p2_x + panel_w, height - gap], fill=PANEL_BG)
        
        plot_x, plot_y = p2_x + 40, 50
        plot_w, plot_h = 160, 180
        
        # Axes
        draw.line([(plot_x, plot_y + plot_h), (plot_x + plot_w, plot_y + plot_h)], fill=WHITE, width=1)
        draw.line([(plot_x, plot_y), (plot_x, plot_y + plot_h)], fill=WHITE, width=1)
        
        # S(θ) curve
        pts = []
        for i in range(181):
            sx = plot_x + (i / 180) * plot_w
            sy = plot_y + plot_h - S(i) * plot_h
            pts.append((sx, sy))
        draw.line(pts, fill=CYAN, width=2)
        
        # Current point
        curr_x = plot_x + (theta_deg / 180) * plot_w
        curr_y = plot_y + plot_h - sf * plot_h
        draw.ellipse([curr_x - 6, curr_y - 6, curr_x + 6, curr_y + 6], fill=GREEN, outline=WHITE)
        
        draw.text((p2_x + panel_w // 2, 25), "S(θ)", fill=YELLOW, anchor="mm", font=font_lg)
        draw.text((p2_x + 15, height - 35), f"S = {sf:.3f}", fill=CYAN, font=font_lg)
        
        # === Panel 3: Barrier ===
        p3_x = gap * 3 + panel_w * 2
        draw.rectangle([p3_x, gap, p3_x + panel_w, height - gap], fill=PANEL_BG)
        
        plot_x3, plot_y3 = p3_x + 40, 50
        
        # Homogeneous curve (dashed approximation)
        def dG(r, s=1): return s * (3*r**2 - 2*r**3) if r > 0 else 0
        
        hom_pts = []
        het_pts = []
        for i in range(100):
            r = i / 99 * 1.5
            sx = plot_x3 + (r / 1.5) * plot_w
            hom_y = plot_y3 + plot_h - dG(r, 1) * plot_h * 0.85
            het_y = plot_y3 + plot_h - dG(r, sf) * plot_h * 0.85
            hom_pts.append((sx, hom_y))
            het_pts.append((sx, het_y))
        
        # Draw dashed homogeneous
        for i in range(0, len(hom_pts) - 1, 4):
            if i + 2 < len(hom_pts):
                draw.line([hom_pts[i], hom_pts[i+2]], fill=GRAY, width=2)
        
        # Heterogeneous (solid)
        draw.line(het_pts, fill=CYAN, width=2)
        
        # Axes
        draw.line([(plot_x3, plot_y3 + plot_h), (plot_x3 + plot_w, plot_y3 + plot_h)], fill=WHITE, width=1)
        draw.line([(plot_x3, plot_y3), (plot_x3, plot_y3 + plot_h)], fill=WHITE, width=1)
        
        draw.text((p3_x + panel_w // 2, 25), "ΔG* Barrier", fill=YELLOW, anchor="mm", font=font_lg)
        draw.text((p3_x + 15, height - 35), f"{sf*100:.0f}% of hom.", fill=PINK, font=font_lg)
        
        frames.append(img)
    
    frames[0].save('assets/three_panel.gif', save_all=True, append_images=frames[1:],
                   duration=80, loop=0)
    print("Created three_panel.gif")


# =============================================================================
# Main
# =============================================================================
if __name__ == "__main__":
    print("Generating GIFs...")
    generate_energy_competition_gif()
    generate_nucleus_fate_gif()
    generate_surface_tensions_gif()
    generate_disk_integration_gif()
    generate_three_panel_gif()
    print("\nAll GIFs created in assets/ folder!")
