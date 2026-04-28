import math
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.platypus import Table, TableStyle


# ============================================================
# DEV TOOLS
# ============================================================
OUTPUT_MODE = "A4"      # options: "A4" or "FULL"


# ============================================================
# DESCRIPTION
# ============================================================


DESCRIPTION_LINES = [
    "Breakout 1 & Breakout 2 harness",
    "Units: millimetres (mm)",
    "Reference layout – 1:1 scale",
] # You can add more lines if you want

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
# BREAKOUT 1 TABLE CONFIGURATION
# ============================================================

BO1_TABLE_OFFSET_Y_MM = 100       # distance below Breakout 1 assembly
BO1_TABLE_WIDTH_MM = 160          # overall table width
BO1_TABLE_ROW_HEIGHT_MM = 10

BO1_TABLE_TITLE = "BREAKOUT 1 ASSEMBLY"

BO1_TABLE_DATA = [
    ["Main Cable", "18.4mm / 576F"],
    ["Heat Shrink Tube 1", "HEATSHRINK 38mm ADHESIVE"],
    ["Aluminum Tube", "Aluminum Break-out 10.5cm"],
    ["Heat Shrink Tube 2", "Heatshrink 1inch Black D"],
    ["Subunits", "Cable sub-units in colored tubes"],
    ["Outer Tubing", "Tube (OD:8.5, ID:5.9)"],
    ["Strength Member", "Black central strength member 4.7mm"],
]

# ============================================================
# BREAKOUT 2 TABLE CONFIGURATION
# ============================================================

BO2_TABLE_GAP_MM = 70     # gap below BO1 table
BO2_TABLE_WIDTH_MM = 200
BO2_TABLE_ROW_HEIGHT_MM = 10

BO2_TABLE_TITLE = "BREAKOUT 2 ASSEMBLY"

BO2_TABLE_DATA = [
    ["Tubing", "Tube (OD:8.5, ID:5.9)"],
    ["Heat Shrink Tube 1", "HEATSHRINK 19mm ADHESIVE"],
    ["Breakout Boot", "Rubber Breakout Boot 6cm"],
    ["Heat Shrink Tube 2", "Heatshrink 1inch Black D"],
    ["Furcation Tube", "3mm Furcation Tube"],
]



# ============================================================
# MAIN CABLE GEOMETRY
# ============================================================
MAIN_VERTICAL_OFFSET_MM = +10 # +UP -DOWN 
MAIN_LENGTH_MM = 400
MAIN_CABLE_DIAMETER_MM = 20.4
MAIN_CABLE_FILL_COLOR = HexColor("#FFD200")  

# ============================================================
# GROUP GEOMETRY
# ============================================================

GROUP_COUNT = 6
GROUP_OD_MM = 10.7
GROUP_FAN_LENGTH = 520 
GROUP_PARALLEL_LENGTH = 580
GROUP_FAN_SPREAD_DEG = 9.8
GROUP_STAGGER_STEP_MM = 70

"""""
QUICK NOTE 
I HAVE TAKEN THE HEATSHRINK LENGTH FROM THE BREAKPOINT TO THE END 
OFF OF THE PARALLEL LENGTH SO THE DIMENTIONS ARE SOUND
"""""
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
BREAKOUT1_HS1_DESCRIPTION = 'HS1'

BREAKOUT1_HS2_LENGTH_MM = 135
BREAKOUT1_HS2_DRAW_HEIGHT_MM = 32
BREAKOUT1_HS2_DESCRIPTION = 'HS2'

BREAKOUT1_AL_TUBE_LENGTH_MM = 105
BREAKOUT1_AL_TUBE_DRAW_HEIGHT_MM = 35
BREAKOUT1_AL_TUBE_DESCRIPTION = 'AL TUBE'




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


GROUP_PARALLEL_LENGTH = GROUP_PARALLEL_LENGTH - (BREAKOUT1_HS1_LENGTH_MM / 2) + (BREAKOUT1_INTERNAL_GAP / 2) #()+() = 105

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

BREAKOUT2_HS1_DESCRIPTION = "HS1"
BREAKOUT2_HS1_LENGTH_MM = 145

BREAKOUT2_HS2_DESCRIPTION = "HS2"
BREAKOUT2_HS2_LENGTH_MM = 35

BREAKOUT2_BOOT_DESCRIPTION = "BOOT"
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



def draw_canvas_table(c, x_mm, y_mm, title, data, width_mm, row_height_mm):
    """
    Draws a titled table onto a canvas.
    Bottom-left anchored at (x_mm, y_mm).
    """

    col_count = len(data[0])
    col_widths = [width_mm / col_count] * col_count

    table = Table(
        data,
        colWidths=[w * mm for w in col_widths],
        rowHeights=[row_height_mm * mm] * len(data)
    )

    table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.8, colors.black),
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("FONT", (0, 0), (-1, -1), "Helvetica", 8),
    ]))

    # Title
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(colors.black)
    c.drawCentredString(
        (x_mm + width_mm / 2) * mm,
        (y_mm + row_height_mm * len(data) + 6) * mm,
        title
    )

    table.wrapOn(c, 0, 0)
    table.drawOn(c, x_mm * mm, y_mm * mm)


def draw_rotated_label(c, x_mm, y_mm, text, angle_deg=90):
    """
    Draws rotated text centred at (x_mm, y_mm).
    """
    c.saveState()
    c.setFillColor(colors.black)
    c.translate(x_mm * mm, y_mm * mm)
    c.rotate(angle_deg)
    c.setFont("Helvetica-Bold", 9)
   

    # Draw centred text at origin after transform
    c.drawCentredString(0, -10, text)

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

def draw_full_harness(c, x_offset_mm=0, y_offset_mm=0):
    c.saveState()
    c.translate(-x_offset_mm * mm, -y_offset_mm * mm)


    base_x = MARGIN_MM + 70
    base_y = (PAGE_HEIGHT_MM / 2) + MAIN_VERTICAL_OFFSET_MM

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
    c.setStrokeColor(colors.black)
    c.setFillColor(MAIN_CABLE_FILL_COLOR)

    c.rect(
        base_x * mm,
        (base_y - MAIN_CABLE_DIAMETER_MM / 2) * mm,
        MAIN_LENGTH_MM * mm,
        MAIN_CABLE_DIAMETER_MM * mm,
        stroke=1,
        fill=1
    )

    breakout1_x = base_x + MAIN_LENGTH_MM


    # --------------------------------------------------------
    # BREAKOUT 1 CUT / BREAKOUT POINT (MATCH BO2 STYLE)
    # --------------------------------------------------------

    bo1_block_bottom_y = base_y - (BREAKOUT1_HS1_DRAW_HEIGHT_MM / 2)
    bo1_block_height   = BREAKOUT1_HS1_DRAW_HEIGHT_MM

    c.saveState()

    c.setLineWidth(1.0)
    c.setDash(3, 3)
    c.setStrokeColor(colors.black)

    c.line(
        breakout1_x * mm,
        bo1_block_bottom_y * mm,
        breakout1_x * mm,
        (bo1_block_bottom_y + bo1_block_height + 5) * mm
    )

    c.setDash()
    c.setFont("Helvetica", 7)
    c.setFillColor(colors.black)

    c.drawCentredString(
        breakout1_x * mm,
        (bo1_block_bottom_y + bo1_block_height + 6) * mm,
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
    # BREAKOUT 1 COMPONENT LABELS 
    # --------------------------------------------------------

    label_y = base_y  # cable centreline

    draw_rotated_label(
        c,
        x_mm=hs1_x,
        y_mm=label_y,
        text=BREAKOUT1_HS1_DESCRIPTION,  # e.g. "HS1"
        angle_deg=90
    )

    draw_rotated_label(
        c,
        x_mm=hs2_x,
        y_mm=label_y,
        text=BREAKOUT1_HS2_DESCRIPTION,  # e.g. "HS2"
        angle_deg=90
    )

    draw_rotated_label(
        c,
        x_mm=al_x,
        y_mm=label_y,
        text=BREAKOUT1_AL_TUBE_DESCRIPTION,  # e.g. "AL TUBE"
        angle_deg=90
    )

    # ========================
    # BREAKOUT 1 INFORMATION TABLE (CENTERED ON HS1)
    # ========================

    # Centre of Breakout 1 assembly (HS1)
    hs1_center_x = hs1_x + (BREAKOUT1_HS1_LENGTH_MM / 2)

    bo1_table_x = hs1_center_x - (BO1_TABLE_WIDTH_MM / 2)
    bo1_table_y = base_y - BO1_TABLE_OFFSET_Y_MM

    draw_canvas_table(
        c=c,
        x_mm=bo1_table_x,
        y_mm=bo1_table_y,
        title=BO1_TABLE_TITLE,
        data=BO1_TABLE_DATA,
        width_mm=BO1_TABLE_WIDTH_MM,
        row_height_mm=BO1_TABLE_ROW_HEIGHT_MM
    )

    # Height of BO1 table
    bo1_table_height_mm = BO1_TABLE_ROW_HEIGHT_MM * len(BO1_TABLE_DATA)


    # ========================
    # BREAKOUT 2 INFORMATION TABLE
    # (STACKED UNDER BO1, CENTRED ON BREAKOUT 1 ASSEMBLY)
    # ========================

    bo2_table_x = hs1_center_x - (BO2_TABLE_WIDTH_MM / 2)

    bo2_table_y = (
        bo1_table_y
        - bo1_table_height_mm
        - BO2_TABLE_GAP_MM
    )

    draw_canvas_table(
        c=c,
        x_mm=bo2_table_x,
        y_mm=bo2_table_y,
        title=BO2_TABLE_TITLE,
        data=BO2_TABLE_DATA,
        width_mm=BO2_TABLE_WIDTH_MM,
        row_height_mm=BO2_TABLE_ROW_HEIGHT_MM
    )




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
        # BREAKOUT 2 CUT / BREAKOUT POINT
        # ========================

        c.saveState()

        c.setLineWidth(1.0)
        c.setDash(3, 3)
        c.setStrokeColor(colors.black)

        c.line(
            breakout2_x * mm,
            block_bottom_y * mm,
            breakout2_x * mm,
            (block_bottom_y + block_height + 5) * mm
        )

        c.setDash()
        c.setFont("Helvetica", 7)
        c.setFillColor(colors.black)

        c.drawCentredString(
            breakout2_x * mm,
            (block_bottom_y + block_height + 6) * mm,
            "CUT / BREAKOUT POINT"
        )

        c.restoreState()

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
        # BREAKOUT 2 COMPONENT LABELS
        # ========================

        label_y = gy  # center of this leg

        draw_rotated_label(
            c,
            x_mm=hs1_x,
            y_mm=label_y,
            text=BREAKOUT2_HS1_DESCRIPTION,
            angle_deg=90
        )

        draw_rotated_label(
            c,
            x_mm=hs2_x,
            y_mm=label_y,
            text=BREAKOUT2_HS2_DESCRIPTION,
            angle_deg=90
        )

        draw_rotated_label(
            c,
            x_mm=boot_x,
            y_mm=label_y,
            text=BREAKOUT2_BOOT_DESCRIPTION,
            angle_deg=90
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
        # SUBUNIT COLOURED END BLOCK (EXTENDED)
        # ========================

        EXTRA_LEN_MM = 25     # +20 mm to the right
        EXTRA_HEIGHT_MM = 25  # +20 mm total (10 up + 10 down)

        coloured_block_x = subunit_block_start_x + main_subunit_length_mm

        c.setLineWidth(0.9)
        c.setStrokeColor(colors.black)
        c.setFillColor(HexColor(SUBUNIT_COLOURED_END_COLOR))

        c.rect(
            coloured_block_x * mm,
            (block_bottom_y - EXTRA_HEIGHT_MM / 2) * mm,
            (SUBUNIT_COLOURED_END_LENGTH_MM + EXTRA_LEN_MM) * mm,
            (block_height + EXTRA_HEIGHT_MM) * mm,
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

    
        draw_credit_footer(
            c,
            x_mm=MARGIN_MM + 2,
            y_mm=MARGIN_MM + 6
        )

    c.restoreState()

        # --------------------------------------------------------
        # BOTTOM REFERENCE RULER (mm)
        # --------------------------------------------------------

     
def draw_full_size_pdf():
    """
    Generates a single full-size PDF (actual dimensions).
    Used for development and quick testing.
    """
    c = canvas.Canvas(
        "harness_FULL_SIZE.pdf",
        pagesize=(PAGE_WIDTH_MM * mm, PAGE_HEIGHT_MM * mm)
    )

    draw_full_harness(c, x_offset_mm=0)
    c.showPage()
    c.save()

    # --------------------------------------------------------
    # RULER 
    # --------------------------------------------------------

    draw_credit_footer(
        c,
        x_mm=MARGIN_MM + 2,
        y_mm=MARGIN_MM + 6
    )




# ============================================================
# RUN
# ============================================================

def draw_template():
    from math import ceil

    A4_WIDTH_MM = 297
    A4_HEIGHT_MM = 210

    tiles_x = ceil(PAGE_WIDTH_MM / A4_WIDTH_MM)
    tiles_y = ceil(PAGE_HEIGHT_MM / A4_HEIGHT_MM)

    c = canvas.Canvas(
        "harness_A4_TILED.pdf",
        pagesize=(A4_WIDTH_MM * mm, A4_HEIGHT_MM * mm)
    )

    page_num = 1

    for y_index in range(tiles_y):
        for x_index in range(tiles_x):

            x_offset_mm = x_index * A4_WIDTH_MM
            y_offset_mm = y_index * A4_HEIGHT_MM

            c.saveState()
            clip_path = c.beginPath()
            clip_path.rect(0, 0, A4_WIDTH_MM * mm, A4_HEIGHT_MM * mm)
            c.clipPath(clip_path, stroke=0, fill=0)

            c.setFont("Helvetica", 8)
            c.drawString(
                10 * mm,
                (A4_HEIGHT_MM - 10) * mm,
                f"A4 TILE {page_num} ({x_index+1},{y_index+1})"
            )

            draw_full_harness(
                c,
                x_offset_mm=x_offset_mm,
                y_offset_mm=y_offset_mm
            )

            c.restoreState()
            c.showPage()
            page_num += 1

    c.save()




# ============================================================
# RUN
# ============================================================

if OUTPUT_MODE == "FULL":
    draw_full_size_pdf()
elif OUTPUT_MODE == "A4":
    draw_template()
else:
    raise ValueError("Unknown OUTPUT_MODE") #HELLO
#IF THE ERROR BRINGS YOU DOWN HERE GO TO THE TOP AND SELECT A4 OR FULL