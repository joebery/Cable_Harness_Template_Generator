import math
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor

# ============================================================
# PAGE SETUP
# ============================================================

PAGE_WIDTH_MM = 2523 
PAGE_HEIGHT_MM = 594
MARGIN_MM = 10

PAGE_WIDTH = PAGE_WIDTH_MM * mm
PAGE_HEIGHT = PAGE_HEIGHT_MM * mm

# ============================================================
# MAIN CABLE GEOMETRY
# ============================================================

MAIN_LENGTH_MM = 400
MAIN_CABLE_DIAMETER_MM = 20.4

# ============================================================
# GROUP GEOMETRY
# ============================================================

GROUP_COUNT = 6
GROUP_OD_MM = 10.7
GROUP_FAN_LENGTH = 550
GROUP_PARALLEL_LENGTH = 550
GROUP_FAN_SPREAD_DEG = 8
GROUP_STAGGER_STEP_MM = 70

# ============================================================
# LINE STYLES
# ============================================================

LINE_MAIN = 1.5
LINE_GROUP = 1.5
LINE_SUBUNIT = 1.5

# ============================================================
# BREAKOUT ELEMENT RECTANGLES
# ============================================================

BREAKOUT_RECT_COUNT = 7
BREAKOUT_RECT_HEIGHT_MM = 2
BREAKOUT_RECT_GAP_MM = 1

BREAKOUT_RECT_SHORT_LEN_MM = 25
BREAKOUT_RECT_LONG_LEN_MM = 106

BREAKOUT_RECT_EXTEND_LEN_MM = 110 - BREAKOUT_RECT_SHORT_LEN_MM
BREAKOUT_RECT_EXTEND_HEIGHT_MM = 2.3

BREAKOUT_RECT_COLORS = [
    "#FFFFFF",
    "#9E9E9E",
    "#8B6B00",
    "#000000",
    "#00A651",
    "#FFD200",
    "#6EC1FF",
]

# ============================================================
# BREAKOUT 1: HEATSHRINK & TUBE
# ============================================================

BREAKOUT1_INTERNAL_GAP = 25

BREAKOUT1_HS1_LENGTH_MM = 185
BREAKOUT1_HS1_DRAW_HEIGHT_MM = 40

BREAKOUT1_HS2_LENGTH_MM = 135
BREAKOUT1_HS2_DRAW_HEIGHT_MM = 32

BREAKOUT1_AL_TUBE_LENGTH_MM = 105
BREAKOUT1_AL_TUBE_DRAW_HEIGHT_MM = 35

# ============================================================
# BREAKOUT 2: HEATSHRINK 
# ============================================================

BREAKOUT2_INTERNAL_GAP = 10

BREAKOUT2_HS1_LENGTH_MM = 145




# ============================================================
# SUBUNIT BLOCK GEOMETRY (NEW)
# ============================================================

SUBUNIT_COUNT = 8
SUBUNIT_SLOT_HEIGHT_MM = 5
SUBUNIT_SLOT_GAP_MM = 0
SUBUNIT_BLOCK_LENGTH_MM = 700
SUBUNIT_BLOCK_PADDING_MM = 1.5

# ============================================================
# HELPERS
# ============================================================

def draw_line(c, x1, y1, x2, y2, width):
    c.setLineWidth(width)
    c.line(x1 * mm, y1 * mm, x2 * mm, y2 * mm)

def step(x, y, angle_deg, length_mm):
    a = math.radians(angle_deg)
    return x + math.cos(a) * length_mm, y + math.sin(a) * length_mm

def draw_rotated_rect(c, x, y, length_mm, height_mm, angle_deg, stroke_width):
    c.saveState()
    c.translate(x * mm, y * mm)
    c.rotate(angle_deg)
    c.setLineWidth(stroke_width)
    c.setStrokeColor(colors.black)
    c.setFillColor(colors.white)
    c.rect(
        0,
        -(height_mm / 2) * mm,
        length_mm * mm,
        height_mm * mm,
        stroke=1,
        fill=0
    )
    c.restoreState()

# ============================================================
# DRAW TEMPLATE
# ============================================================

def draw_template():
    c = canvas.Canvas(
        "harness_breakout2.pdf",
        pagesize=(PAGE_WIDTH, PAGE_HEIGHT)
    )

    base_x = MARGIN_MM + 70
    base_y = PAGE_HEIGHT_MM / 2

    # --------------------------------------------------------
    # MAIN CABLE
    # --------------------------------------------------------

    c.setLineWidth(LINE_MAIN)
    c.setStrokeColor(colors.black)
    c.rect(
        base_x * mm,
        (base_y - MAIN_CABLE_DIAMETER_MM / 2) * mm,
        MAIN_LENGTH_MM * mm,
        MAIN_CABLE_DIAMETER_MM * mm,
        stroke=1,
        fill=0
    )

    breakout_x = base_x + MAIN_LENGTH_MM
    breakout_y = base_y

    # --------------------------------------------------------
    # CUT / BREAKOUT LINE
    # --------------------------------------------------------

    c.setDash(3, 3)
    c.line(
        breakout_x * mm,
        (base_y - 60) * mm,
        breakout_x * mm,
        (base_y + 60) * mm
    )
    c.setDash()
    c.drawString(
        (breakout_x + 4) * mm,
        (base_y + 64) * mm,
        "CUT / BREAKOUT POINT"
    )

    # --------------------------------------------------------
    # BREAKOUT ELEMENT RECTANGLES
    # --------------------------------------------------------

    total_stack_height = (
        BREAKOUT_RECT_COUNT * BREAKOUT_RECT_HEIGHT_MM +
        (BREAKOUT_RECT_COUNT - 1) * BREAKOUT_RECT_GAP_MM
    )

    stack_bottom_y = base_y - total_stack_height / 2
    middle_index = BREAKOUT_RECT_COUNT // 2

    for i in range(BREAKOUT_RECT_COUNT):
        rect_y = stack_bottom_y + i * (
            BREAKOUT_RECT_HEIGHT_MM + BREAKOUT_RECT_GAP_MM
        )

        rect_len = (
            BREAKOUT_RECT_LONG_LEN_MM
            if i == middle_index else
            BREAKOUT_RECT_SHORT_LEN_MM
        )

        c.setFillColor(HexColor(BREAKOUT_RECT_COLORS[i]))
        c.rect(
            breakout_x * mm,
            rect_y * mm,
            rect_len * mm,
            BREAKOUT_RECT_HEIGHT_MM * mm,
            stroke=1,
            fill=1
        )

        if i != middle_index:
            ext_y = rect_y + (
                (BREAKOUT_RECT_HEIGHT_MM - BREAKOUT_RECT_EXTEND_HEIGHT_MM) / 2
            )
            c.setFillColor(colors.white)
            c.rect(
                (breakout_x + rect_len) * mm,
                ext_y * mm,
                BREAKOUT_RECT_EXTEND_LEN_MM * mm,
                BREAKOUT_RECT_EXTEND_HEIGHT_MM * mm,
                stroke=1,
                fill=0
            )

    # --------------------------------------------------------
    # HEATSHRINK + TUBE
    # --------------------------------------------------------
    BREAKOUT1_HS1_START_BEFORE = (BREAKOUT1_HS1_LENGTH_MM / 2) - (BREAKOUT1_INTERNAL_GAP/2)
    hs1_x = breakout_x - BREAKOUT1_HS1_START_BEFORE
    c.rect(
        hs1_x * mm,
        (base_y - BREAKOUT1_HS1_DRAW_HEIGHT_MM / 2) * mm,
        BREAKOUT1_HS1_LENGTH_MM * mm,
        BREAKOUT1_HS1_DRAW_HEIGHT_MM * mm,
        stroke=1,
        fill=0
    )
    BREAKOUT1_HS2_START_BEFORE_MM = (BREAKOUT1_HS2_LENGTH_MM / 2) - (BREAKOUT1_INTERNAL_GAP/2)
    hs2_x = breakout_x - BREAKOUT1_HS2_START_BEFORE_MM
    c.rect(
        hs2_x * mm,
        (base_y - BREAKOUT1_HS2_DRAW_HEIGHT_MM / 2) * mm,
        BREAKOUT1_HS2_LENGTH_MM * mm,
        BREAKOUT1_HS2_DRAW_HEIGHT_MM * mm,
        stroke=1,
        fill=0
    )
    BREAKOUT1_AL_TUBE_START_BEFORE_MM = (BREAKOUT1_AL_TUBE_LENGTH_MM / 2) - (BREAKOUT1_INTERNAL_GAP/2)
    al_x = breakout_x - BREAKOUT1_AL_TUBE_START_BEFORE_MM
    c.rect(
        al_x * mm,
        (base_y - BREAKOUT1_AL_TUBE_DRAW_HEIGHT_MM / 2) * mm,
        BREAKOUT1_AL_TUBE_LENGTH_MM * mm,
        BREAKOUT1_AL_TUBE_DRAW_HEIGHT_MM * mm,
        stroke=1,
        fill=0
    )

    # --------------------------------------------------------
    # GROUPS (OD 10.7 FULL ENVELOPE)
    # --------------------------------------------------------

    fan_start_x = hs1_x + BREAKOUT1_HS1_LENGTH_MM
    fan_start_y = base_y
    group_ends = []
    mid = (GROUP_COUNT - 1) / 2

    for i in range(GROUP_COUNT):
        angle = (mid - i) * GROUP_FAN_SPREAD_DEG

        fx, fy = step(fan_start_x, fan_start_y, angle, GROUP_FAN_LENGTH)

        draw_rotated_rect(
            c, fan_start_x, fan_start_y,
            GROUP_FAN_LENGTH, GROUP_OD_MM,
            angle, LINE_GROUP
        )

        parallel_len = GROUP_PARALLEL_LENGTH - i * GROUP_STAGGER_STEP_MM
        c.rect(
            fx * mm,
            (fy - GROUP_OD_MM / 2) * mm,
            parallel_len * mm,
            GROUP_OD_MM * mm,
            stroke=1,
            fill=0
        )

        group_ends.append((fx + parallel_len, fy))

    # --------------------------------------------------------
    # SUBUNIT BLOCKS (8‑SLOT, NO FAN‑OUT)
    # --------------------------------------------------------

    for gx, gy in group_ends:
        slots_height = (
            SUBUNIT_COUNT * SUBUNIT_SLOT_HEIGHT_MM +
            (SUBUNIT_COUNT - 1) * SUBUNIT_SLOT_GAP_MM
        )

        
        block_height = slots_height + 2 * SUBUNIT_BLOCK_PADDING_MM
        block_bottom_y = gy - (block_height / 2)

        # Outer block
        c.setLineWidth(0.6)

        # Internal slots
        c.setLineWidth(0.9)

        slot_y = block_bottom_y + SUBUNIT_BLOCK_PADDING_MM
        for i in range(SUBUNIT_COUNT):
            c.rect(
                gx * mm,
                (slot_y + i * (SUBUNIT_SLOT_HEIGHT_MM + SUBUNIT_SLOT_GAP_MM)) * mm,
                SUBUNIT_BLOCK_LENGTH_MM * mm,
                SUBUNIT_SLOT_HEIGHT_MM * mm,
                stroke=1,
                fill=0
            )

        
        # ----------------------------------------------------
        # BREAKOUT 2 – HEATSHRINK 1
        # ----------------------------------------------------
        # Heatshrink applied around the group→subunit transition.
        # Anchored to Breakout 2 (end of groups).
        # Dimensions are parametric to support future changes.
        # ----------------------------------------------------

        
        BREAKOUT2_HS1_START_BEFORE_MM = (BREAKOUT2_HS1_LENGTH_MM/2)-(BREAKOUT2_INTERNAL_GAP/2)
        breakout2_x = gx  # Breakout 2 = end of groups (defined in Step 3)

        hs2_1_start_x = breakout2_x - BREAKOUT2_HS1_START_BEFORE_MM
        hs2_1_bottom_y = block_bottom_y  # same vertical envelope as subunit block

        c.setStrokeColor(colors.black)
        c.setFillColor(colors.white)
        c.setLineWidth(1.0)

        c.rect(
            hs2_1_start_x * mm,
            hs2_1_bottom_y * mm,
            BREAKOUT2_HS1_LENGTH_MM * mm,
            block_height * mm,
            stroke=1,
            fill=0
        )

        # ----------------------------------------------------
        # CUT & LABEL REFERENCE LINES (RELATIVE TO SUBUNIT BLOCK)
        # ----------------------------------------------------

        block_end_x = gx + SUBUNIT_BLOCK_LENGTH_MM

        # ==============================
        # CUT HERE LINE (50 mm to right)
        # ==============================

        cut_line_x = block_end_x + 50

        c.setDash(4, 4)
        c.setLineWidth(1.0)

        c.line(
            cut_line_x * mm,
            block_bottom_y * mm,
            cut_line_x * mm,
            (block_bottom_y + block_height) * mm
        )

        c.setDash()
        c.setFillColor(colors.black)
        c.setFont("Helvetica", 8)

        c.drawCentredString(
            cut_line_x * mm,
            (block_bottom_y + block_height + 6) * mm,
            "CUT HERE"
        )

        # ==============================
        # LEG LABEL PLACEMENT (LEFT SIDE)
        # ==============================

        label_line_1_x = block_end_x - 200
        label_line_2_x = label_line_1_x - 25

        c.setDash(2, 3)
        c.setLineWidth(0.9)

        # First label reference line
        c.line(
            label_line_1_x * mm,
            block_bottom_y * mm,
            label_line_1_x * mm,
            (block_bottom_y + block_height) * mm
        )

        # Second label reference line (25 mm left)
        c.line(
            label_line_2_x * mm,
            block_bottom_y * mm,
            label_line_2_x * mm,
            (block_bottom_y + block_height) * mm
        )

        c.setDash()

        c.setFont("Helvetica", 8)
        c.drawCentredString(
            (label_line_2_x + 12.5) * mm,
            (block_bottom_y + block_height + 6) * mm,
            "LEG LABEL PLACEMENT"
        )


    c.showPage()
    c.save()

# ============================================================
# RUN
# ============================================================

draw_template()