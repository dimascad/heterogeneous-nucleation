import marimo

__generated_with = "0.13.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    # Slider for contact angle
    theta_slider = mo.ui.slider(
        start=10,
        stop=170,
        step=1,
        value=90,
        label="Contact Angle θ (degrees)",
        full_width=True
    )
    theta_slider
    return (theta_slider,)


@app.cell
def _(theta_slider):
    import math
    from PIL import Image, ImageDraw, ImageFont
    import io
    import base64

    WIDTH = 1100
    HEIGHT = 500

    # High contrast color scheme
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


    def draw_dashed(draw, x1, y1, x2, y2, color, total_len, dash, gap, width=1):
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
            top_of_cap_y = baseY - h
            
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
            
            if py + 45 < Cy < baseY + 30:
                draw_dashed(draw, cx, min(Cy, baseY-3), cx, top_of_cap_y, WHITE, 6, 4, 2)
                mid_y = (min(Cy, baseY - 10) + top_of_cap_y) / 2
                if mid_y > py + 55 and mid_y < baseY - 15:
                    draw.text((cx + 12, mid_y), "r", fill=WHITE, font=f_large)
        
        tpX, tpY = cx + a, baseY
        L = 90
        
        draw.line([(tpX, tpY), (tpX - L, tpY)], fill=(0, 0, 0), width=5)
        al = 20
        ah_pts = [(tpX - L, tpY),
                  (tpX - L + al, tpY - al*0.35),
                  (tpX - L + al, tpY + al*0.35)]
        draw.polygon(ah_pts, fill=(0, 0, 0))
        
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
        
        draw.text((tpX - L - 16, tpY - 24), "γₛₙ", fill=(0, 0, 0), font=f_title)
        draw.text((tpX + L + 10, tpY - 24), "γₛₗ", fill=WHITE, font=f_title)
        draw.text((nlX - 36, nlY - 14), "γₙₗ", fill=GOLD, font=f_title)
        
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
        legend_box = [px + 5, ly - 2, px + 155, ly + 48]
        draw.rectangle(legend_box, fill=(45, 65, 95), outline=(80, 100, 130))
        
        draw.line([(px + 10, ly + 8), (px + 28, ly + 8)], fill=(0, 0, 0), width=3)
        draw.text((px + 32, ly + 8), "γₛₙ Solid-Nucleus", fill=(0, 0, 0), anchor="lm", font=f_small)
        
        draw.line([(px + 10, ly + 22), (px + 28, ly + 22)], fill=WHITE, width=3)
        draw.text((px + 32, ly + 22), "γₛₗ Solid-Liquid", fill=WHITE, anchor="lm", font=f_small)
        
        draw.line([(px + 10, ly + 36), (px + 28, ly + 36)], fill=GOLD, width=3)
        draw.text((px + 32, ly + 36), "γₙₗ Nucleus-Liquid", fill=GOLD, anchor="lm", font=f_small)
        
        draw.text((px + pw - 8, ly + 8), "Young's equation:", fill=GRAY, anchor="rt", font=f_small)
        draw.text((px + pw - 8, ly + 26), "γₛₗ = γₛₙ + γₙₗ·cosθ", fill=WHITE, anchor="rt", font=f_normal)


    def draw_shape_factor_panel(draw, theta_deg, px, py, pw, ph, fonts):
        """Middle panel: S(θ) vs θ curve with proper axes"""
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
        
        draw.text((plot_x + plot_w//2, plot_y + plot_h + 32), "Contact Angle θ (degrees)", 
                  fill=GREEN, anchor="mm", font=f_medium)
        
        for th_val in [0, 45, 90, 135, 180]:
            x = to_x(th_val)
            draw.text((x, plot_y + plot_h + 14), str(th_val), fill=WHITE, anchor="mm", font=f_normal)
        
        draw.text((px + 6, plot_y - 22), "S(θ)", fill=CYAN, font=f_large)
        
        for s_val in [0, 0.25, 0.5, 0.75, 1.0]:
            y = to_y(s_val)
            draw.text((plot_x - 8, y), f"{s_val:.2f}", fill=WHITE, anchor="rm", font=f_normal)
        
        eq_x = plot_x + int(plot_w * 0.72)
        eq_y = plot_y + int(plot_h * 0.78)
        draw.text((eq_x, eq_y), "S(θ) = (2+cosθ)(1−cosθ)²/4", fill=CYAN, anchor="mm", font=f_normal)


    def draw_barrier_panel(draw, theta_deg, px, py, pw, ph, fonts):
        """Right panel: ΔG vs r with barrier comparison"""
        f_small, f_normal, f_medium, f_large, f_title, f_bigtitle = fonts
        
        draw.rectangle([px, py, px+pw, py+ph], fill=PANEL_BG, outline=LIGHT_GRAY)
        draw.text((px + pw//2, py + 18), "NUCLEATION BARRIER ΔG*", fill=YELLOW, anchor="mm", font=f_bigtitle)
        
        sf = S(theta_deg)
        
        draw.text((px + pw//2, py + 42), f"ΔG*ₕₑₜ = {sf*100:.1f}% of ΔG*ₕₒₘ", fill=ORANGE, anchor="mm", font=f_medium)
        
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
        
        draw.text((plot_x + plot_w//2, plot_y + plot_h + 32), "Normalized Radius r/r*", 
                  fill=WHITE, anchor="mm", font=f_medium)
        
        for r_val in [0, 0.5, 1.0, 1.5]:
            x = to_x(r_val)
            label = "r*" if r_val == 1.0 else f"{r_val:.1f}"
            draw.text((x, zero_y + 14), label, fill=WHITE, anchor="mm", font=f_normal)
        
        draw.text((px + 5, plot_y - 12), "ΔG/ΔG*ₕₒₘ", fill=ORANGE, font=f_medium)
        
        for g_val in [0, 0.5, 1.0]:
            y = to_y(g_val)
            draw.text((plot_x - 8, y), f"{g_val:.1f}", fill=WHITE, anchor="rm", font=f_normal)
        
        eq_x = plot_x + int(plot_w * 0.30)
        eq_y = plot_y + int(plot_h * 0.15)
        draw.text((eq_x, eq_y), "ΔG*ₕₑₜ = S(θ)·ΔG*ₕₒₘ", fill=ORANGE, anchor="mm", font=f_medium)


    def draw_frame(theta_deg):
        img = Image.new('RGB', (WIDTH, HEIGHT), BG_COLOR)
        draw = ImageDraw.Draw(img)
        fonts = get_fonts()
        
        gap = 8
        panel_w = (WIDTH - 4*gap) // 3
        panel_h = HEIGHT - 2*gap
        
        draw_geometry_panel(draw, theta_deg, gap, gap, panel_w, panel_h, fonts)
        draw_shape_factor_panel(draw, theta_deg, gap*2 + panel_w, gap, panel_w, panel_h, fonts)
        draw_barrier_panel(draw, theta_deg, gap*3 + panel_w*2, gap, panel_w, panel_h, fonts)
        
        return img

    # Generate the image for current theta
    theta = theta_slider.value
    img = draw_frame(theta)
    
    # Convert to displayable format
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.getvalue()).decode()
    
    import marimo as mo
    mo.Html(f'<img src="data:image/png;base64,{img_base64}" style="max-width: 100%;">')
    return


@app.cell
def _():
    import marimo as mo
    mo.md("""
    ## Heterogeneous Nucleation Visualization

    This interactive visualization demonstrates how **contact angle θ** affects heterogeneous nucleation:

    - **Left panel**: Shows the nucleus geometry as a spherical cap on a substrate, with surface tension vectors (γₛₙ, γₛₗ, γₙₗ) and the contact angle θ
    - **Middle panel**: The shape factor S(θ) curve - this determines how much the nucleation barrier is reduced
    - **Right panel**: Comparison of homogeneous vs heterogeneous nucleation energy barriers

    ### Key Physics

    The shape factor is given by:
    
    **S(θ) = (2 + cos θ)(1 - cos θ)² / 4**

    This determines the heterogeneous nucleation barrier:
    
    **ΔG*_het = S(θ) · ΔG*_hom**

    - At θ → 0° (perfect wetting): S → 0, barrier nearly eliminated
    - At θ = 90°: S = 0.5, barrier halved  
    - At θ → 180° (no wetting): S → 1, no reduction (same as homogeneous)

    Use the slider above to explore how different contact angles affect nucleation!
    """)
    return


if __name__ == "__main__":
    app.run()
