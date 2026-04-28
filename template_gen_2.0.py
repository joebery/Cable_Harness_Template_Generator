import math
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor

# ============================================================
# DESCRIPTION
# ============================================================


DESCRIPTION_LINES = [
    "Breakout 1 & Breakout 2 harness",
    "Units: millimetres (mm)",
    "Reference layout – 1:1 scale",
]

DESCRIPTION_TITLE = 'Cable Template Test'

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
LINE_SUBUNIT = 1.0


# ============================================================
# BREAKOUT 1: HEATSHRINK & TUBE
# ============================================================

BREAKOUT1_INTERNAL_GAP = 25

BREAKOUT1_HS1_LENGTH_MM = 185 # Should be the biggest heatshrink
BREAKOUT1_HS1_DRAW_HEIGHT_MM = 40

BREAKOUT1_HS2_LENGTH_MM = 135
BREAKOUT1_HS2_DRAW_HEIGHT_MM = 32

BREAKOUT1_AL_TUBE_LENGTH_MM = 105
BREAKOUT1_AL_TUBE_DRAW_HEIGHT_MM = 35



# Derived offsets DO NOT CHANGE
###These are so the heatshrinks are anchored to the breakoutpoint,
### taking into account for the internal gap
BREAKOUT1_HS1_START_BEFORE_MM = (
    (BREAKOUT1_HS1_LENGTH_MM / 2) - (BREAKOUT1_INTERNAL_GAP / 2) #=80
)

BREAKOUT1_HS2_START_BEFORE_MM = (
    (BREAKOUT1_HS2_LENGTH_MM / 2) - (BREAKOUT1_INTERNAL_GAP / 2) #=55
)

BREAKOUT1_AL_TUBE_START_BEFORE_MM = (
    (BREAKOUT1_AL_TUBE_LENGTH_MM / 2) - (BREAKOUT1_INTERNAL_GAP / 2)#=40 
)

# ============================================================
# BREAKOUT 1 ELEMENT RECTANGLES
# ============================================================

BREAKOUT_RECT_COUNT = 7
BREAKOUT_RECT_HEIGHT_MM = 2
BREAKOUT_RECT_GAP_MM = 1

BREAKOUT_RECT_SHORT_LEN_MM = 25 # this is the length of the coloured rectangles
BREAKOUT_RECT_LONG_LEN_MM = 90 # this is the length of the support member

BREAKOUT_RECT_EXTEND_LEN_MM = ( # Length of the (no fill) extention rectangles
    BREAKOUT1_HS1_START_BEFORE_MM + BREAKOUT1_INTERNAL_GAP #So they go to the end of the biggest heatshrink 
    ) - BREAKOUT_RECT_SHORT_LEN_MM 

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
# BREAKOUT 2: HEATSHRINK
# ============================================================

BREAKOUT2_INTERNAL_GAP = 10
BREAKOUT2_HS1_LENGTH_MM = 145

BREAKOUT2_HS2_LENGTH_MM = 35

BREAKOUT2_BREAKOUT_BOOT_LENGTH_MM = 60

# Derived offsets DO NOT CHANGE
BREAKOUT2_HS1_START_BEFORE_MM = (
    (BREAKOUT2_HS1_LENGTH_MM / 2) - (BREAKOUT2_INTERNAL_GAP / 2)
)

BREAKOUT2_HS2_START_BEFORE_MM = (
    (BREAKOUT2_HS2_LENGTH_MM / 2) - (BREAKOUT2_INTERNAL_GAP / 2)
)

BREAKOUT2_BREAKOUT_BOOT_START_BEFORE_MM = (
    (BREAKOUT2_BREAKOUT_BOOT_LENGTH_MM / 2) - (BREAKOUT2_INTERNAL_GAP / 2)
)

# ============================================================
# SUBUNIT BLOCK GEOMETRY
# ============================================================

SUBUNIT_COUNT = 8
SUBUNIT_SLOT_HEIGHT_MM = 5
SUBUNIT_SLOT_GAP_MM = 0
SUBUNIT_BLOCK_LENGTH_MM = 700
SUBUNIT_BLOCK_PADDING_MM = 1.5

# ============================================================
# SUBUNIT BLOCK CONFIGURATION
# ============================================================

SUBUNIT_COLOURED_END_LENGTH_MM = 60   # length of coloured section at right end
SUBUNIT_COLOURED_END_COLOR = "#EEFF00"  # user-defined (example: light blue)

# ============================================================
# HELPERS
# ============================================================

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

def draw_mm_ruler(c, start_x_mm, start_y_mm, length_mm, label_step_mm=50):
    """
    Draw a horizontal millimetre ruler.
    - Major ticks every 10 mm
    - Label every `label_step_mm`
    """
    c.saveState()

    c.setLineWidth(0.8)
    c.setStrokeColor(colors.black)
    c.setFont("Helvetica", 7)

    # Main ruler line
    c.line(
        start_x_mm * mm,
        start_y_mm * mm,
        (start_x_mm + length_mm) * mm,
        start_y_mm * mm
    )

    for i in range(0, length_mm + 1, 10):
        x = start_x_mm + i

        # Tick height
        if i % label_step_mm == 0:
            tick_h = 7   # major
        else:
            tick_h = 4   # minor

        c.line(
            x * mm,
            start_y_mm * mm,
            x * mm,
            (start_y_mm + tick_h) * mm
        )

        # Number labels
        if i % label_step_mm == 0:
            c.drawCentredString(
                x * mm,
                (start_y_mm + tick_h + 3) * mm,
                f"{i} mm"
            )

    c.restoreState()


def draw_title_and_description(c, x_mm, y_mm, title, description_lines):
    """
    Draw title and multi-line description at a fixed position.
    """
    c.saveState()

    # Title
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(colors.black)
    c.drawString(x_mm * mm, y_mm * mm, title)

    # Description lines
    c.setFont("Helvetica", 9)
    text_y = y_mm - 14

    for line in description_lines:
        c.drawString(x_mm * mm, text_y * mm, line)
        text_y -= 10

    c.restoreState()

import base64

def draw_credit_footer(c, x_mm, y_mm):
    """
    Draw an obfuscated credit footer at a fixed position.
    """
    c.saveState()

    _credit_b64 = "dGVtcGxhdGUgYnkgam9zZXBoIGJlcnk="
    credit_text = base64.b64decode(_credit_b64).decode("utf-8")

    c.setFont("Helvetica-Oblique", 7)
    c.setFillColor(colors.grey)

    c.drawString(x_mm * mm, y_mm * mm, credit_text)

    c.restoreState()


# ============================================================
# DRAW TEMPLATE
# ============================================================

def draw_template():
    c = canvas.Canvas("harness_v2_coloured_end.pdf", pagesize=(PAGE_WIDTH, PAGE_HEIGHT))

    base_x = MARGIN_MM + 70
    base_y = PAGE_HEIGHT_MM / 2

    # --------------------------------------------------------
    # TITLE & DESCRIPTION (TOP LEFT)
    # --------------------------------------------------------

    

    draw_title_and_description(
        c,
        x_mm=MARGIN_MM + 2,
        y_mm=PAGE_HEIGHT_MM - MARGIN_MM - 6,
        title= DESCRIPTION_TITLE,
        description_lines=DESCRIPTION_LINES
    )


    # --------------------------------------------------------
    # BOTTOM REFERENCE RULER (mm)
    # --------------------------------------------------------

    draw_mm_ruler(
        c,
        start_x_mm=MARGIN_MM + 70,   # align with main cable start
        start_y_mm=MARGIN_MM + 10,   # bottom margin
        length_mm=PAGE_WIDTH_MM - (MARGIN_MM * 2) - 70,
        label_step_mm=100            # label every 100 mm
    )

    # --------------------------------------------------------
    # MAIN CABLE
    # --------------------------------------------------------

    c.setLineWidth(LINE_MAIN)
    c.rect(
        base_x * mm,
        (base_y - MAIN_CABLE_DIAMETER_MM / 2) * mm,
        MAIN_LENGTH_MM * mm,
        MAIN_CABLE_DIAMETER_MM * mm,
        stroke=1,
        fill=0
    )

    breakout1_x = base_x + MAIN_LENGTH_MM

    # --------------------------------------------------------
    # BREAKOUT 1 CUT LINE (FIXED REFERENCE)
    # --------------------------------------------------------

    breakout1_x = base_x + MAIN_LENGTH_MM

    c.saveState()  # protect dash/font state

    c.setLineWidth(1.0)
    c.setDash(3, 3)

    c.line(
        breakout1_x * mm,
        (base_y - 60) * mm,
        breakout1_x * mm,
        (base_y + 60) * mm
    )

    c.setDash()
    c.setFont("Helvetica", 8)

    c.drawString(
        (breakout1_x + 4) * mm,
        (base_y + 66) * mm,
        "CUT / BREAKOUT POINT"
    )

    c.restoreState()



    # --------------------------------------------------------
    # BREAKOUT 1 ELEMENT RECTANGLES
    # --------------------------------------------------------

    total_stack_height = (
        BREAKOUT_RECT_COUNT * BREAKOUT_RECT_HEIGHT_MM +
        (BREAKOUT_RECT_COUNT - 1) * BREAKOUT_RECT_GAP_MM
    )

    stack_bottom_y = base_y - total_stack_height / 2
    middle_index = BREAKOUT_RECT_COUNT // 2

    for i in range(BREAKOUT_RECT_COUNT):
        ry = stack_bottom_y + i * (BREAKOUT_RECT_HEIGHT_MM + BREAKOUT_RECT_GAP_MM)
        length = BREAKOUT_RECT_LONG_LEN_MM if i == middle_index else BREAKOUT_RECT_SHORT_LEN_MM

        c.setFillColor(HexColor(BREAKOUT_RECT_COLORS[i]))
        c.rect(
            breakout1_x * mm,
            ry * mm,
            length * mm,
            BREAKOUT_RECT_HEIGHT_MM * mm,
            stroke=1,
            fill=1
        )

        if i != middle_index:
            ext_y = ry + (BREAKOUT_RECT_HEIGHT_MM - BREAKOUT_RECT_EXTEND_HEIGHT_MM) / 2
            c.setFillColor(colors.white)
            c.rect(
                (breakout1_x + length) * mm,
                ext_y * mm,
                BREAKOUT_RECT_EXTEND_LEN_MM * mm,
                BREAKOUT_RECT_EXTEND_HEIGHT_MM * mm,
                stroke=1,
                fill=0
            )

    # --------------------------------------------------------
    # BREAKOUT 1 HEATSHRINK / TUBE
    # --------------------------------------------------------

    hs1_x = breakout1_x - BREAKOUT1_HS1_START_BEFORE_MM
    hs2_x = breakout1_x - BREAKOUT1_HS2_START_BEFORE_MM
    al_x  = breakout1_x - BREAKOUT1_AL_TUBE_START_BEFORE_MM

    c.rect(hs1_x*mm, (base_y-BREAKOUT1_HS1_DRAW_HEIGHT_MM/2)*mm,
           BREAKOUT1_HS1_LENGTH_MM*mm, BREAKOUT1_HS1_DRAW_HEIGHT_MM*mm, stroke=1, fill=0)

    c.rect(hs2_x*mm, (base_y-BREAKOUT1_HS2_DRAW_HEIGHT_MM/2)*mm,
           BREAKOUT1_HS2_LENGTH_MM*mm, BREAKOUT1_HS2_DRAW_HEIGHT_MM*mm, stroke=1, fill=0)

    c.rect(al_x*mm, (base_y-BREAKOUT1_AL_TUBE_DRAW_HEIGHT_MM/2)*mm,
           BREAKOUT1_AL_TUBE_LENGTH_MM*mm, BREAKOUT1_AL_TUBE_DRAW_HEIGHT_MM*mm, stroke=1, fill=0)

    # --------------------------------------------------------
    # GROUPS
    # --------------------------------------------------------

    fan_start_x = hs1_x + BREAKOUT1_HS1_LENGTH_MM
    group_ends = []
    mid = (GROUP_COUNT - 1) / 2

    for i in range(GROUP_COUNT):
        angle = (mid - i) * GROUP_FAN_SPREAD_DEG
        fx, fy = step(fan_start_x, base_y, angle, GROUP_FAN_LENGTH)

        draw_rotated_rect(c, fan_start_x, base_y,
                          GROUP_FAN_LENGTH, GROUP_OD_MM, angle, LINE_GROUP)

        parallel_len = GROUP_PARALLEL_LENGTH - i * GROUP_STAGGER_STEP_MM
        c.rect(
            fx * mm,
            (fy - GROUP_OD_MM/2) * mm,
            parallel_len * mm,
            GROUP_OD_MM * mm,
            stroke=1,
            fill=0
        )

        group_ends.append((fx + parallel_len, fy))



 # --------------------------------------------------------
# BREAKOUT 2 + SUBUNIT BLOCK (HEATSHRINKS + BOOT + SUBUNITS)
# --------------------------------------------------------

    for gx, gy in group_ends:

        # ========================
        # BREAKOUT 2 ANCHOR
        # ========================
        # Structural transition: end of groups
        breakout2_x = gx

        # ========================
        # SHARED VERTICAL ENVELOPE
        # ========================
        slots_height = (
            SUBUNIT_COUNT * SUBUNIT_SLOT_HEIGHT_MM +
            (SUBUNIT_COUNT - 1) * SUBUNIT_SLOT_GAP_MM
        )

        block_height = slots_height + 2 * SUBUNIT_BLOCK_PADDING_MM
        block_bottom_y = gy - (block_height / 2)

        # ========================
        # BREAKOUT 2 – HEATSHRINK 1
        # ========================
        hs1_x = breakout2_x - BREAKOUT2_HS1_START_BEFORE_MM

        c.setLineWidth(1.0)
        c.setStrokeColor(colors.black)
        c.setFillColor(colors.white)

        c.rect(
            hs1_x * mm,
            block_bottom_y * mm,
            BREAKOUT2_HS1_LENGTH_MM * mm,
            block_height * mm,
            stroke=1,
            fill=0
        )

        # ========================
        # BREAKOUT 2 – HEATSHRINK 2
        # ========================
        hs2_x = breakout2_x - BREAKOUT2_HS2_START_BEFORE_MM

        c.rect(
            hs2_x * mm,
            block_bottom_y * mm,
            BREAKOUT2_HS2_LENGTH_MM * mm,
            block_height * mm,
            stroke=1,
            fill=0
        )

        # ========================
        # BREAKOUT 2 – BREAKOUT BOOT
        # ========================
        boot_x = breakout2_x - BREAKOUT2_BREAKOUT_BOOT_START_BEFORE_MM

        c.rect(
            boot_x * mm,
            block_bottom_y * mm,
            BREAKOUT2_BREAKOUT_BOOT_LENGTH_MM * mm,
            block_height * mm,
            stroke=1,
            fill=0
        )

        # ========================
        # SUBUNIT BLOCK START
        # ========================
        # Subunits begin AFTER Breakout 2 coverage
        subunit_block_start_x = (
            breakout2_x
            + (BREAKOUT2_HS1_LENGTH_MM / 2)
            + (BREAKOUT2_INTERNAL_GAP / 2)
        )

        # ========================
        # SUBUNIT SLOTS (MAIN BLOCK – UNCOLOURED)
        # ========================

        main_subunit_length_mm = (
            SUBUNIT_BLOCK_LENGTH_MM - SUBUNIT_COLOURED_END_LENGTH_MM
        )

        slot_y = block_bottom_y + SUBUNIT_BLOCK_PADDING_MM
        c.setLineWidth(0.9)

        for i in range(SUBUNIT_COUNT):
            c.rect(
                subunit_block_start_x * mm,
                (slot_y + i * (SUBUNIT_SLOT_HEIGHT_MM + SUBUNIT_SLOT_GAP_MM)) * mm,
                main_subunit_length_mm * mm,
                SUBUNIT_SLOT_HEIGHT_MM * mm,
                stroke=1,
                fill=0
            )

        # ========================
        # SUBUNIT COLOURED END BLOCK
        # ========================

        coloured_block_x = subunit_block_start_x + main_subunit_length_mm

        c.setLineWidth(0.9)
        c.setStrokeColor(colors.black)
        c.setFillColor(HexColor(SUBUNIT_COLOURED_END_COLOR))

        c.rect(
            coloured_block_x * mm,
            block_bottom_y * mm,
            SUBUNIT_COLOURED_END_LENGTH_MM * mm,
            block_height * mm,
            stroke=1,
            fill=1
        )


        # ==============================
        # LEG LABEL PLACEMENT (LEFT SIDE)
        # ==============================

        block_end_x = subunit_block_start_x + SUBUNIT_BLOCK_LENGTH_MM  # ✅ FIX

        label_line_1_x = block_end_x - 200
        label_line_2_x = label_line_1_x - 25

        c.saveState()  # protect dash/font state

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
        c.setFillColor(colors.black)
        c.setFont("Helvetica", 8)

        c.drawCentredString(
            (label_line_2_x + 12.5) * mm,
            (block_bottom_y + block_height + 6) * mm,
            "LEG LABEL PLACEMENT"
        )

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

        c.restoreState()

        # --------------------------------------------------------
        # BOTTOM REFERENCE RULER (mm)
        # --------------------------------------------------------

     

# --------------------------------------------------------
#SHOW PAGE
# --------------------------------------------------------

    draw_credit_footer(
        c,
        x_mm=MARGIN_MM + 2,
        y_mm=MARGIN_MM + 6
    )

    c.showPage()
    c.save()

# ============================================================
# RUN
# ============================================================

draw_template()