"""Generates the dashboard-style SVG panels for the GitHub profile README."""
import os

OUT = os.path.join(os.path.dirname(__file__), "assets")
os.makedirs(OUT, exist_ok=True)

BG = "#0B1220"      # page
PANEL = "#111A2E"   # tile
LINE = "#1E2A44"    # borders / grid
TXT = "#E6ECF8"
MUTED = "#8A97B4"
COBALT = "#3D6BFF"
COBALT_D = "#1F4FD8"
CORAL = "#FF6B5B"
SANS = "'Segoe UI','Helvetica Neue',Helvetica,Arial,sans-serif"
MONO = "SFMono-Regular,Consolas,'Liberation Mono',Menlo,monospace"

STYLE = f"""
<style>
  .sans{{font-family:{SANS}}} .mono{{font-family:{MONO}}}
  .grow{{transform-box:fill-box;transform-origin:left center;animation:grow 1.1s cubic-bezier(.2,.8,.2,1) both}}
  .rise{{transform-box:fill-box;transform-origin:center bottom;animation:rise .9s cubic-bezier(.2,.8,.2,1) both}}
  .fade{{animation:fade .8s ease-out both}}
  .draw{{stroke-dasharray:1200;animation:draw 2s ease-out both}}
  .pulse{{animation:pulse 2s ease-in-out infinite}}
  @keyframes grow{{from{{transform:scaleX(0)}}}}
  @keyframes rise{{from{{transform:scaleY(0)}}}}
  @keyframes fade{{from{{opacity:0}}}}
  @keyframes draw{{from{{stroke-dashoffset:1200}}}}
  @keyframes pulse{{50%{{opacity:.35}}}}
</style>"""


def svg(w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" role="img">{STYLE}'
            f'<rect width="{w}" height="{h}" rx="14" fill="{BG}"/>{body}</svg>')


def grid(w, h, step=24):
    lines = [f'<path d="M{x} 0V{h}" />' for x in range(step, w, step)]
    lines += [f'<path d="M0 {y}H{w}" />' for y in range(step, h, step)]
    return f'<g stroke="{LINE}" stroke-width="1" opacity=".45">{"".join(lines)}</g>'


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def chip(x, y, label, color=COBALT, fill=None):
    w = 22 + len(label) * 7.1
    fill = fill or "none"
    return (f'<rect x="{x}" y="{y}" width="{w:.0f}" height="24" rx="12" fill="{fill}" '
            f'stroke="{color}" stroke-opacity=".7"/>'
            f'<text x="{x + w / 2:.0f}" y="{y + 16}" text-anchor="middle" class="mono" '
            f'font-size="11.5" fill="{TXT}">{esc(label)}</text>'), w


def section_label(x, y, code, title):
    return (f'<text x="{x}" y="{y}" class="mono" font-size="11" fill="{CORAL}" '
            f'letter-spacing="1.5">{code}</text>'
            f'<text x="{x}" y="{y + 24}" class="sans" font-size="19" font-weight="700" '
            f'fill="{TXT}">{esc(title)}</text>')


# ---------------------------------------------------------------- header
def header():
    w, h = 900, 250
    b = [grid(w, h)]
    b.append(f'<rect x="0" y="0" width="{w}" height="34" rx="14" fill="{PANEL}"/>'
             f'<rect x="0" y="20" width="{w}" height="14" fill="{PANEL}"/>'
             f'<path d="M0 34H{w}" stroke="{LINE}"/>')
    for i, c in enumerate(["#FF5F57", "#FEBC2E", "#28C840"]):
        b.append(f'<circle cx="{22 + i * 18}" cy="17" r="5" fill="{c}"/>')
    b.append(f'<text x="{w / 2}" y="21" text-anchor="middle" class="mono" font-size="11.5" '
             f'fill="{MUTED}">pervej_hosen.pbix — Profile Overview</text>')
    b.append(f'<circle cx="{w - 70}" cy="17" r="4" fill="#28C840" class="pulse"/>'
             f'<text x="{w - 60}" y="21" class="mono" font-size="11" fill="{MUTED}">LIVE</text>')

    b.append(f'<g class="fade"><text x="40" y="78" class="mono" font-size="12" fill="{CORAL}" '
             f'letter-spacing="2">BUSINESS INTELLIGENCE · ANALYTICS ENGINEERING</text>'
             f'<text x="38" y="124" class="sans" font-size="44" font-weight="800" fill="{TXT}">'
             f'Pervej Hosen</text>'
             f'<text x="40" y="154" class="sans" font-size="16" fill="{MUTED}">'
             f'Sr. BI Developer turning raw data into decisions people trust.</text></g>')

    x = 40
    for label, col in [("Power BI", COBALT), ("SQL", COBALT), ("Snowflake", COBALT),
                       ("PL-300 Certified", CORAL), ("Dhaka · Remote", MUTED)]:
        c, cw = chip(x, 182, label, col)
        b.append(c)
        x += cw + 8

    # mini chart panel on the right
    px, py, pw, ph = 600, 58, 260, 160
    b.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="10" fill="{PANEL}" '
             f'stroke="{LINE}"/>'
             f'<text x="{px + 16}" y="{py + 24}" class="mono" font-size="10.5" fill="{MUTED}">'
             f'SCOPE · role by role</text>')
    vals = [1, 2, 3, 4, 5, 6]
    bw, gap, base = 26, 12, py + ph - 22
    for i, v in enumerate(vals):
        bh = 16 + v * 15
        bx = px + 22 + i * (bw + gap)
        col = CORAL if i == len(vals) - 1 else COBALT
        op = .45 + i * .1 if i < len(vals) - 1 else 1
        b.append(f'<rect class="rise" style="animation-delay:{i * .12:.2f}s" x="{bx}" '
                 f'y="{base - bh}" width="{bw}" height="{bh}" rx="4" fill="{col}" '
                 f'fill-opacity="{op:.2f}"/>')
    pts = " ".join(f"{px + 22 + i * (bw + gap) + bw / 2},{base - (16 + v * 15) - 8}"
                   for i, v in enumerate(vals))
    b.append(f'<polyline class="draw" points="{pts}" fill="none" stroke="{TXT}" '
             f'stroke-width="1.5" stroke-opacity=".55" stroke-linecap="round"/>')
    b.append(f'<path d="M{px + 16} {base}H{px + pw - 16}" stroke="{LINE}"/>')
    return svg(w, h, "".join(b))


# ---------------------------------------------------------------- KPI tiles
def kpis():
    w, h = 900, 132
    tiles = [("6", "Roles held", "sales → data → BI lead", COBALT),
             ("5", "Industries", "pharma · retail · finance …", COBALT),
             ("4", "Countries served", "US · UK · DE · AU — remote", COBALT),
             ("PL-300", "Microsoft certified", "Power BI Data Analyst", CORAL)]
    gap = 14
    tw = (w - gap * 3) / 4
    b = []
    for i, (val, lab, sub, col) in enumerate(tiles):
        x = i * (tw + gap)
        b.append(f'<g class="fade" style="animation-delay:{i * .12:.2f}s">'
                 f'<rect x="{x + .5:.1f}" y=".5" width="{tw - 1:.1f}" height="{h - 1}" rx="12" '
                 f'fill="{PANEL}" stroke="{LINE}"/>'
                 f'<rect x="{x + 18:.1f}" y="18" width="28" height="4" rx="2" fill="{col}"/>'
                 f'<text x="{x + 18:.1f}" y="68" class="sans" font-size="38" font-weight="800" '
                 f'fill="{TXT}">{val}</text>'
                 f'<text x="{x + 18:.1f}" y="92" class="sans" font-size="14" font-weight="600" '
                 f'fill="{TXT}">{lab}</text>'
                 f'<text x="{x + 18:.1f}" y="112" class="mono" font-size="11" fill="{MUTED}">'
                 f'{esc(sub)}</text></g>')
    # transparent outer bg for tiles
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" role="img">{STYLE}{"".join(b)}</svg>')


# ---------------------------------------------------------------- career
ROLES = [
    ("Sr. BI Developer", "Transparent Partners", "United States", "Consulting", True),
    ("Data Analytics Engineer", "Onwards Analytics", "Australia", "Mining & business improvement", False),
    ("BI Developer", "Instant Funding", "United Kingdom", "Prop trading", False),
    ("Business Intelligence Analyst", "Buddy & Selly", "Germany", "Circular fashion e-commerce", False),
    ("Associate Data Analyst", "Transcom Ltd", "Bangladesh", "Pharmaceutical", False),
    ("Assistant Officer, Sales & Distribution", "Transcom Ltd", "Bangladesh", "Pharmaceutical", False),
]


def career():
    w = 900
    top, row = 84, 56
    h = top + row * len(ROLES) + 30
    b = [grid(w, h), section_label(36, 42, "01 // CAREER", "Experience — most recent first")]
    b.append(f'<text x="{w - 36}" y="66" text-anchor="end" class="mono" font-size="11" '
             f'fill="{MUTED}">bar = scope of role</text>')
    track_x, track_w = 420, 440
    n = len(ROLES)
    for i, (title, co, country, ind, current) in enumerate(ROLES):
        y = top + i * row
        col = CORAL if current else COBALT
        frac = .38 + .62 * (n - 1 - i) / (n - 1)
        b.append(f'<path d="M36 {y + row - 4}H{w - 36}" stroke="{LINE}"/>')
        b.append(f'<circle cx="46" cy="{y + 18}" r="5" fill="{col}"/>')
        b.append(f'<text x="62" y="{y + 23}" class="sans" font-size="15" font-weight="700" '
                 f'fill="{TXT}">{esc(title)}</text>')
        b.append(f'<text x="62" y="{y + 42}" class="mono" font-size="11.5" fill="{MUTED}">'
                 f'{esc(co)} · {esc(country)}</text>')
        b.append(f'<rect x="{track_x}" y="{y + 10}" width="{track_w}" height="26" rx="6" '
                 f'fill="{PANEL}"/>')
        b.append(f'<rect class="grow" style="animation-delay:{i * .1:.2f}s" x="{track_x}" '
                 f'y="{y + 10}" width="{track_w * frac:.0f}" height="26" rx="6" fill="{col}" '
                 f'fill-opacity="{1 if current else .55 + .07 * (n - i):.2f}"/>')
        label = esc(ind) + ("  ● NOW" if current else "")
        b.append(f'<text x="{track_x + 12}" y="{y + 27}" class="mono" font-size="11.5" '
                 f'fill="#FFFFFF">{label}</text>')
    return svg(w, h, "".join(b))


# ---------------------------------------------------------------- toolkit
STACK = [
    ("VISUALIZE", ["Power BI", "DAX", "Looker Studio", "Excel"]),
    ("QUERY & MODEL", ["SQL", "Data Modeling", "Power Query"]),
    ("WAREHOUSE", ["Snowflake", "BigQuery"]),
    ("ANALYZE", ["Python", "GA4", "RFM Segmentation", "Predictive ML"]),
]


def toolkit():
    w = 900
    top, row = 84, 44
    h = top + row * len(STACK) + 16
    b = [grid(w, h), section_label(36, 42, "02 // TOOLKIT", "What I build with")]
    for i, (cat, tools) in enumerate(STACK):
        y = top + i * row
        b.append(f'<text x="36" y="{y + 17}" class="mono" font-size="11.5" fill="{MUTED}" '
                 f'letter-spacing="1.2">{esc(cat)}</text>')
        x = 190
        for j, t in enumerate(tools):
            hot = j == 0
            c, cw = chip(x, y, t, CORAL if hot else COBALT,
                         fill=COBALT_D if hot else None)
            b.append(c)
            x += cw + 8
        b.append(f'<path d="M36 {y + row - 8}H{w - 36}" stroke="{LINE}" stroke-dasharray="3 4"/>')
    return svg(w, h, "".join(b))


# ---------------------------------------------------------------- project cards
PROJECTS = [
    ("rfm", "RFM Segmentation", "Customer segments by recency, frequency & spend",
     ["SQL", "Snowflake", "Excel"], "scatter"),
    ("airbnb", "Airbnb Data Analysis", "Pricing & listing patterns explored in SQL",
     ["SQL", "Snowflake"], "bars"),
    ("bqml", "BigQuery + Python ML", "Modeling on BigQuery, reported in Looker Studio",
     ["BigQuery", "Python", "Looker"], "line"),
    ("ga4", "Google Merch Store", "E-commerce funnel & behavior from GA4",
     ["GA4", "Looker Studio"], "funnel"),
    ("hr", "HR Attrition Dashboard", "What drives employees to leave",
     ["Excel"], "donut"),
    ("superstore", "Super Store Sales", "Sales by region, category & segment",
     ["Excel"], "hbars"),
]


def glyph(kind, x, y):
    c, k = COBALT, CORAL
    if kind == "scatter":
        pts = [(8, 40), (18, 30), (26, 36), (34, 18), (44, 24), (50, 10), (14, 14), (40, 40)]
        return "".join(f'<circle cx="{x + a}" cy="{y + b_}" r="4" fill="{k if i in (3, 5) else c}"/>'
                       for i, (a, b_) in enumerate(pts))
    if kind == "bars":
        return "".join(f'<rect x="{x + i * 12}" y="{y + 48 - hh}" width="8" height="{hh}" rx="2" '
                       f'fill="{k if i == 2 else c}"/>' for i, hh in enumerate([20, 32, 44, 26, 14]))
    if kind == "line":
        return (f'<polyline points="{x},{y + 40} {x + 14},{y + 30} {x + 26},{y + 34} '
                f'{x + 40},{y + 14} {x + 56},{y + 6}" fill="none" stroke="{c}" stroke-width="3" '
                f'stroke-linecap="round" stroke-linejoin="round"/>'
                f'<circle cx="{x + 56}" cy="{y + 6}" r="4" fill="{k}"/>')
    if kind == "funnel":
        return "".join(f'<rect x="{x + i * 7}" y="{y + 4 + i * 12}" width="{56 - i * 14}" '
                       f'height="9" rx="2" fill="{k if i == 3 else c}" fill-opacity="{1 - i * .15}"/>'
                       for i in range(4))
    if kind == "donut":
        return (f'<circle cx="{x + 28}" cy="{y + 26}" r="20" fill="none" stroke="{c}" '
                f'stroke-width="9"/><circle cx="{x + 28}" cy="{y + 26}" r="20" fill="none" '
                f'stroke="{k}" stroke-width="9" stroke-dasharray="28 200" '
                f'transform="rotate(-90 {x + 28} {y + 26})"/>')
    if kind == "hbars":
        return "".join(f'<rect x="{x}" y="{y + 4 + i * 12}" width="{ww}" height="8" rx="2" '
                       f'fill="{k if i == 0 else c}"/>' for i, ww in enumerate([56, 42, 30, 18]))
    return ""


def card(slug, title, desc, tags, kind):
    w, h = 440, 132
    b = [f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="12" fill="{PANEL}" '
         f'stroke="{LINE}"/>',
         f'<rect x="0" y="22" width="4" height="34" rx="2" fill="{CORAL}"/>',
         f'<text x="22" y="40" class="sans" font-size="17" font-weight="700" fill="{TXT}">'
         f'{esc(title)}</text>',
         f'<text x="22" y="62" class="sans" font-size="12.5" fill="{MUTED}">{esc(desc)}</text>',
         glyph(kind, w - 84, 20)]
    x = 22
    for t in tags:
        c, cw = chip(x, 88, t)
        b.append(c)
        x += cw + 6
    b.append(f'<text x="{w - 22}" y="105" text-anchor="end" class="mono" font-size="11.5" '
             f'fill="{CORAL}">view repo →</text>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" role="img">{STYLE}<g class="fade">{"".join(b)}</g></svg>')


def projects_label():
    w, h = 900, 72
    return svg(w, h, grid(w, h) + section_label(36, 30, "03 // PROJECTS",
                                                "Selected work — click a card to open the repo"))


def footer():
    w, h = 900, 70
    b = [f'<path d="M36 18H{w - 36}" stroke="{LINE}"/>',
         f'<text x="{w / 2}" y="48" text-anchor="middle" class="mono" font-size="12.5" '
         f'fill="{MUTED}">-- data is only useful when someone makes a decision with it</text>']
    return svg(w, h, "".join(b))


files = {"header.svg": header(), "kpis.svg": kpis(), "career.svg": career(),
         "toolkit.svg": toolkit(), "projects.svg": projects_label(), "footer.svg": footer()}
for p in PROJECTS:
    files[f"card-{p[0]}.svg"] = card(*p)
for name, content in files.items():
    with open(os.path.join(OUT, name), "w") as f:
        f.write(content)
print("wrote", len(files), "files")
