import math
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfgen import canvas

# ============================================================
# PAGE SETUP
# ============================================================

PAGE_WIDTH_MM = 2102.5
PAGE_HEIGHT_MM = 594
MARGIN_MM = 10

PAGE_WIDTH = PAGE_WIDTH_MM * mm
PAGE_HEIGHT = PAGE_HEIGHT_MM * mm

# ============================================================
# GEOMETRY (USER-DRIVEN)
# ============================================================

MAIN_LENGTH_MM = 400

# --- GROUPS ---
GROUP_COUNT = 6
GROUP_FAN_LENGTH = 550
GROUP_PARALLEL_LENGTH = 550
GROUP_FAN_SPREAD_DEG = 8
GROUP_PARALLEL_ANGLE_DEG = 0
GROUP_STAGGER_STEP_MM = 70

# --- SUBUNITS ---
SUBUNITS_PER_GROUP = 8
SUBUNIT_FAN_LENGTH = 60
SUBUNIT_PARALLEL_LENGTH = 240
SUBUNIT_FAN_SPREAD_DEG = 8
SUBUNIT_PARALLEL_ANGLE_DEG = 0

# --- LINE THICKNESS ---
LINE_MAIN = 3.0
LINE_GROUP = 1.8
LINE_SUBUNIT = 1.0

# ============================================================
# HEATSHRINK 1 (BREAKOUT 1)
# ============================================================

HEATSHRINK1_LENGTH_MM = 185      # <<< CHANGE LENGTH HERE
HEATSHRINK1_START_BEFORE_MM = (HEATSHRINK1_LENGTH_MM/2) - 17.5   

# Operator visibility (vertical exaggeration only)
HEATSHRINK1_DRAW_HEIGHT_MM = 36   # <<< CHANGE HEIGHT HERE if needed



# ============================================================
# HEATSHRINK 2 (SECOND STAGE)
# ============================================================

HEATSHRINK2_LENGTH_MM = 135          # <<< 50 mm shorter than HS1
HEATSHRINK2_START_BEFORE_MM = (HEATSHRINK2_LENGTH_MM/2) - 17.5   
# Operator visibility (vertical exaggeration only)
HEATSHRINK2_DRAW_HEIGHT_MM = 20 # <<< CHANGE HEIGHT HERE if needed


# ============================================================
# Aluminium Tube (SECOND STAGE)
# ============================================================

AL_TUBE_LENGTH_MM = 105          
AL_TUBE_START_BEFORE_MM = (AL_TUBE_LENGTH_MM/2) - 17.5      
# Operator visibility (vertical exaggeration only)
AL_TUBE_DRAW_HEIGHT_MM = 25 # <<< CHANGE HEIGHT HERE if needed


# ============================================================
# HELPERS
# ============================================================

def draw_line(c, x1, y1, x2, y2, width):
    c.setLineWidth(width)
    c.line(x1 * mm, y1 * mm, x2 * mm, y2 * mm)

def step(x, y, angle_deg, length_mm):
    a = math.radians(angle_deg)
    return (
        x + math.cos(a) * length_mm,
        y + math.sin(a) * length_mm
    )

# ============================================================
# CALIBRATION RULER
# ============================================================

def draw_ruler(c, start_x_mm, start_y_mm, length_mm=1000):
    c.setStrokeColor(colors.black)
    c.setLineWidth(0.8)

    c.line(
        start_x_mm * mm,
        start_y_mm * mm,
        (start_x_mm + length_mm) * mm,
        start_y_mm * mm
    )

    for i in range(0, length_mm + 1, 10):
        x = start_x_mm + i
        h = 8 if i % 100 == 0 else 6 if i % 50 == 0 else 4

        c.line(x * mm, start_y_mm * mm, x * mm, (start_y_mm + h) * mm)

        if i % 100 == 0:
            c.setFont("Helvetica", 7)
            c.drawCentredString(
                x * mm,
                (start_y_mm + h + 4) * mm,
                f"{i} mm"
            )

# ============================================================
# DRAW TEMPLATE
# ============================================================

def draw_template():
    c = canvas.Canvas(
        "harness_with_al_tube.pdf",
        pagesize=(PAGE_WIDTH, PAGE_HEIGHT)
    )

    base_x = MARGIN_MM + 70
    base_y = PAGE_HEIGHT_MM / 2

    # --------------------------------------------------------
    # MAIN CABLE
    # --------------------------------------------------------

    c.setStrokeColor(colors.black)
    draw_line(
        c, base_x, base_y,
        base_x + MAIN_LENGTH_MM, base_y,
        LINE_MAIN
    )

    breakout_x = base_x + MAIN_LENGTH_MM
    breakout_y = base_y

    # --------------------------------------------------------
    # HEATSHRINK 1 OUTLINE
    # --------------------------------------------------------

    hs1_start_x = breakout_x - HEATSHRINK1_START_BEFORE_MM
    hs1_bottom_y = base_y - (HEATSHRINK1_DRAW_HEIGHT_MM / 2)

    c.setLineWidth(1.2)
    c.rect(
        hs1_start_x * mm,
        hs1_bottom_y * mm,
        HEATSHRINK1_LENGTH_MM * mm,
        HEATSHRINK1_DRAW_HEIGHT_MM * mm
    )

    c.setFont("Helvetica", 8)
    c.drawCentredString(
        (hs1_start_x + HEATSHRINK1_LENGTH_MM / 2) * mm,
        (hs1_bottom_y + HEATSHRINK1_DRAW_HEIGHT_MM + 4) * mm,
        "Heatshrink 1"
    )



    # --------------------------------------------------------
    # HEATSHRINK 2 OUTLINE
    # --------------------------------------------------------

    hs2_start_x = breakout_x - HEATSHRINK2_START_BEFORE_MM
    hs2_bottom_y = base_y - (HEATSHRINK2_DRAW_HEIGHT_MM / 2)

    c.setLineWidth(1.2)
    c.rect(
        hs2_start_x * mm,
        hs2_bottom_y * mm,
        HEATSHRINK2_LENGTH_MM * mm,
        HEATSHRINK2_DRAW_HEIGHT_MM * mm
    )

    c.setFont("Helvetica", 8)
    c.drawCentredString(
        (hs2_start_x + HEATSHRINK2_LENGTH_MM / 2) * mm,
        (hs2_bottom_y + HEATSHRINK2_DRAW_HEIGHT_MM + 4) * mm,
        "Heatshrink 2"
    )

    # --------------------------------------------------------
    # ALUMINIUM TUBE OUTLINE
    # --------------------------------------------------------

    hs2_start_x = breakout_x - AL_TUBE_START_BEFORE_MM
    hs2_bottom_y = base_y - (AL_TUBE_DRAW_HEIGHT_MM / 2)

    c.setLineWidth(1.2)
    c.rect(
        hs2_start_x * mm,
        hs2_bottom_y * mm,
        AL_TUBE_LENGTH_MM * mm,
        AL_TUBE_DRAW_HEIGHT_MM * mm
    )

    c.setFont("Helvetica", 8)
    c.drawCentredString(
        (hs2_start_x + AL_TUBE_LENGTH_MM / 2) * mm,
        (hs2_bottom_y + AL_TUBE_DRAW_HEIGHT_MM + 4) * mm,
        "Aluminium Tube"
    )



    # --------------------------------------------------------
    # GROUP CABLES (STAGGERED)
    # --------------------------------------------------------

    group_ends = []
    mid = (GROUP_COUNT - 1) / 2

    for i in range(GROUP_COUNT):
        fan_angle = (mid - i) * GROUP_FAN_SPREAD_DEG

        fx, fy = step(breakout_x, breakout_y, fan_angle, GROUP_FAN_LENGTH)
        draw_line(c, breakout_x, breakout_y, fx, fy, LINE_GROUP)

        parallel_len = GROUP_PARALLEL_LENGTH - i * GROUP_STAGGER_STEP_MM
        px, py = step(fx, fy, 0, parallel_len)
        draw_line(c, fx, fy, px, py, LINE_GROUP)

        group_ends.append((px, py))

    # --------------------------------------------------------
    # SUBUNITS
    # --------------------------------------------------------

    for gx, gy in group_ends:
        mid_s = (SUBUNITS_PER_GROUP - 1) / 2

        for i in range(SUBUNITS_PER_GROUP):
            fan_angle = (i - mid_s) * SUBUNIT_FAN_SPREAD_DEG

            fx, fy = step(gx, gy, fan_angle, SUBUNIT_FAN_LENGTH)
            draw_line(c, gx, gy, fx, fy, LINE_SUBUNIT)

            px, py = step(fx, fy, 0, SUBUNIT_PARALLEL_LENGTH)
            draw_line(c, fx, fy, px, py, LINE_SUBUNIT)

    # --------------------------------------------------------
    # CALIBRATION RULER
    # --------------------------------------------------------

    draw_ruler(c, MARGIN_MM + 20, MARGIN_MM + 12, 1000)

    c.showPage()
    c.save()

# ============================================================
# RUN
# ============================================================

draw_template()