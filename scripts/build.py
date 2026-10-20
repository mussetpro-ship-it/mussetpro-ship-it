#!/usr/bin/env python3
"""Generate the profile README and its SVG assets, in light and dark variants.

    python3 scripts/build.py                                          # README.md and assets/, as set below
    python3 scripts/build.py --style paper --activity pillars --out /tmp/look   # another look, elsewhere

The look follows trytikt.com: Manrope, graphite text, Electric Blue, flat surfaces, thin lines, lime as a
highlighter. The font is embedded in each image (Manrope, SIL Open Font License, scripts/fonts/OFL.txt),
since GitHub shows README images without loading web fonts; scripts/fonts/manrope-metrics.json holds its
glyph widths, so text is measured, not guessed.

The activity chart reads data/contributions.json, written by scripts/fetch_contributions.py,
which .github/workflows/profile.yml runs every day.
"""

import argparse
import base64
import json
from collections import OrderedDict
from datetime import date, timedelta
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
REPO = "mussetpro-ship-it/mussetpro-ship-it"
RAW = f"https://raw.githubusercontent.com/{REPO}/main/assets"
W = 1200

FONT = "Manrope, -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif"
METRICS = json.loads((ROOT / "scripts" / "fonts" / "manrope-metrics.json").read_text())

# ---------------------------------------------------------------- content

STYLE = "electric"
ACTIVITY = "zoom"  # zoom: the last 12 weeks, day by day · skyline: one tower per week · pillars: one per month

NAME = "Maxime Musset"
# The headline of the X profile, word for word. The highlight goes on the third part.
HEADLINE = ("Helping B2B turn Likes & Comments", "into ", "leads that convert", ".")
SUBLINE = "I build GTM systems with Claude Code."
FLOW = ["Likes & comments", "Checked against your ICP", "Warm leads", "Your outreach tool"]
FLOW_HOT = 2

# The networks, shown under the header as their logos in rounded squares: (slug, name, url, background, mark).
# The marks are the networks' own logos, as drawn by Simple Icons, on a 24-unit grid.
LINKS = [
    ("x", "X", "https://x.com/AI_for_salesrep", "#000000",
     "M18.901 1.153h3.68l-8.04 9.19L24 22.846h-7.406l-5.8-7.584-6.638 7.584H.474l8.6-9.83L0 1.154h7.594l5.243 6.932Z"
     "M17.61 20.644h2.039L6.486 3.24H4.298Z"),
    ("linkedin", "LinkedIn", "https://www.linkedin.com/in/maxime-musset/", "#0A66C2",
     "M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561"
     "h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 "
     "0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452z"),
]

TIKT = {
    "url": "https://trytikt.com",
    "logo": ROOT / "scripts" / "brand" / "tikt-logo.png",
    # The category line of trytikt.com, validated.
    "title": "Turn LinkedIn engagement into warm leads.",
    "button": "trytikt.com",
}

PROJECTS = [
    {
        "slug": "gtm-os",
        "url": "https://github.com/mussetpro-ship-it/gtm-os",
        "kicker": "OPEN SOURCE · AGENT SKILL",
        "title": "GTM OS",
        "lines": ["The go-to-market memory your agents read first,", "and that tells them when it goes stale."],
        "tags": ["Claude Code", "Codex", "Hermes Agent", "Node.js"],
        "layers": ["Context", "Skills", "Orchestration", "Integrations"],
        "hot": 2,
    },
]

# ---------------------------------------------------------------- styles

INK, BLUE, SKY, LIME, PAPER, LINE = "#1A1A1E", "#305CFF", "#84A6FF", "#B8FA4E", "#F5F5F6", "#DEDFE6"
WHITE = "#FFFFFF"

CARD_LIGHT = {
    "card": WHITE, "edge": LINE, "text": INK, "muted": "#64646F", "accent": BLUE, "button": BLUE,
    "button_text": WHITE, "chip": LINE, "layer": PAPER, "layer_edge": LINE, "hot": BLUE, "hot_text": WHITE,
    "ramp": ["#E9EAEE", "#95AFFF", "#6D8BFF", "#4466F0", "#2140C9"], "callout": INK, "callout_text": WHITE,
}
CARD_DARK = {
    "card": INK, "edge": "#2E2E36", "text": WHITE, "muted": "#A1A1AA", "accent": SKY, "button": BLUE,
    "button_text": WHITE, "chip": "#41414B", "layer": "#25252C", "layer_edge": "#3A3A44", "hot": BLUE,
    "hot_text": WHITE, "ramp": ["#2A2A31", "#24346E", "#2B49B8", BLUE, SKY], "callout": WHITE, "callout_text": INK,
}

HEADER_PAPER_LIGHT = {
    "bg": WHITE, "edge": LINE, "pattern": "#EDEDF1", "text": INK, "muted": "#64646F", "accent": BLUE,
    "highlight": None, "node": PAPER, "node_edge": LINE, "node_text": INK, "hot": BLUE, "hot_text": WHITE, "dot": BLUE,
}
HEADER_PAPER_DARK = {
    "bg": INK, "edge": "#2E2E36", "pattern": "#232329", "text": WHITE, "muted": "#A1A1AA", "accent": SKY,
    "highlight": None, "node": "#25252C", "node_edge": "#3A3A44", "node_text": WHITE, "hot": BLUE, "hot_text": WHITE,
    "dot": SKY,
}
HEADER_ELECTRIC = {
    "bg": BLUE, "edge": BLUE, "pattern": "#4A71FF", "text": WHITE, "muted": "#D6E0FF", "accent": INK,
    "highlight": LIME, "node": "#4A71FF", "node_edge": "#7E99FF", "node_text": WHITE, "hot": WHITE, "hot_text": BLUE,
    "dot": LIME,
}
HEADER_GRAPHITE = {
    "bg": INK, "edge": INK, "pattern": "#2A2A31", "text": WHITE, "muted": "#A1A1AA", "accent": SKY,
    "highlight": None, "node": "#25252C", "node_edge": "#3A3A44", "node_text": WHITE, "hot": BLUE, "hot_text": WHITE,
    "dot": SKY,
}

STYLES = {
    "paper": {"light": (HEADER_PAPER_LIGHT, CARD_LIGHT), "dark": (HEADER_PAPER_DARK, CARD_DARK)},
    "electric": {"light": (HEADER_ELECTRIC, CARD_LIGHT), "dark": (HEADER_ELECTRIC, CARD_DARK)},
    "graphite": {"light": (HEADER_GRAPHITE, CARD_DARK), "dark": (HEADER_GRAPHITE, CARD_DARK)},
}

# ---------------------------------------------------------------- helpers


def font_faces():
    faces = []
    for weight in (500, 700, 800):
        data = base64.b64encode((ROOT / "scripts" / "fonts" / f"manrope-{weight}.woff").read_bytes()).decode()
        faces.append(f"@font-face {{ font-family: Manrope; font-weight: {weight}; src: url(data:font/woff;base64,{data}) format('woff'); }}")
    return "".join(faces)


FACES = None


def style_block(extra=""):
    global FACES
    FACES = FACES or font_faces()
    return f"<style>{FACES} text {{ font-family: {FONT}; }} {extra}</style>"


def svg(width, height, title, body):
    label = escape(title, {'"': "&quot;"})
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-label="{label}">\n'
        f"<title>{escape(title)}</title>\n{body}\n</svg>\n"
    )


def text(x, y, content, size, weight=500, fill=INK, anchor=None, spacing=None, raw=False):
    extra = (f' text-anchor="{anchor}"' if anchor else "") + (f' letter-spacing="{spacing}"' if spacing is not None else "")
    return f'<text x="{x:g}" y="{y:g}" font-size="{size}" font-weight="{weight}" fill="{fill}"{extra}>{content if raw else escape(content)}</text>'


def width_of(label, size, weight=500, spacing=0):
    widths = METRICS[str(weight)]
    return sum(widths.get(c, 0.6) * size + spacing for c in label)


def chip(x, y, label, edge, fill_text, size=13, height=30, spacing=1.2):
    w = width_of(label, size, 700, spacing) + 28
    return (
        f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{height}" rx="{height / 2:g}" fill="none" stroke="{edge}" stroke-width="1.5"/>'
        + text(x + w / 2, y + height / 2 + size * 0.36, label, size, 700, fill_text, "middle", spacing)
    ), w


def card(h, t):
    return f'<rect x="1" y="1" width="{W - 2}" height="{h - 2}" rx="22" fill="{t["card"]}" stroke="{t["edge"]}" stroke-width="1.5"/>'


def shade(color, factor):
    r, g, b = (int(color[i : i + 2], 16) for i in (1, 3, 5))
    return "#" + "".join(f"{max(0, min(255, round(c * factor))):02X}" for c in (r, g, b))


def poly(points, fill):
    return f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in points)}" fill="{fill}"/>'


def prism(footprint, height, color):
    """A block standing on a four-corner footprint: the side faces turned toward the viewer, then the top."""
    top = [(x, y - height) for x, y in footprint]
    cx = sum(x for x, _ in top) / 4
    cy = sum(y for _, y in top) / 4
    shapes = []
    for k in range(4):
        p, q = top[k], top[(k + 1) % 4]
        nx, ny = q[1] - p[1], p[0] - q[0]
        if nx * ((p[0] + q[0]) / 2 - cx) + ny * ((p[1] + q[1]) / 2 - cy) < 0:
            nx, ny = -nx, -ny
        if ny > 0.01 and height > 0.5:
            light = 0.86 if nx < 0 else 0.68
            shapes.append(poly([p, q, (q[0], q[1] + height), (p[0], p[1] + height)], shade(color, light)))
    shapes.append(poly(top, color))
    return shapes


def footprint(origin, u, v, i, j, fill_u=0.84, fill_v=0.84):
    """The four corners of cell (i, j) on a grid whose axes are the vectors u and v."""
    ox = origin[0] + (i + (1 - fill_u) / 2) * u[0] + (j + (1 - fill_v) / 2) * v[0]
    oy = origin[1] + (i + (1 - fill_u) / 2) * u[1] + (j + (1 - fill_v) / 2) * v[1]
    a = (u[0] * fill_u, u[1] * fill_u)
    b = (v[0] * fill_v, v[1] * fill_v)
    return [(ox, oy), (ox + a[0], oy + a[1]), (ox + a[0] + b[0], oy + a[1] + b[1]), (ox + b[0], oy + b[1])]


def callout(x, y, label, t):
    """A small dark tag above a point, joined to it by a thin line."""
    w = width_of(label, 14, 700) + 22
    return (
        f'<line x1="{x:.1f}" y1="{y - 4:.1f}" x2="{x:.1f}" y2="{y - 30:.1f}" stroke="{t["callout"]}" stroke-width="1.5"/>'
        f'<rect x="{x - w / 2:.1f}" y="{y - 58:.1f}" width="{w:.1f}" height="28" rx="8" fill="{t["callout"]}"/>'
        + text(x, y - 39, label, 14, 700, t["callout_text"], "middle")
    )


def short_date(d):
    return f"{d:%b} {d.day}"


# ---------------------------------------------------------------- header


def header(h_t):
    h = 340
    top, step, nh, nw, nx = 52, 62, 46, 330, 816
    path_x = nx + 26
    flow_path = f"M{path_x} {top + nh / 2} V{top + (len(FLOW) - 1) * step + nh / 2}"
    animation = (
        f".dot {{ offset-path: path('{flow_path}'); animation: run 3.6s ease-in-out infinite; }}"
        "@keyframes run { 0% { offset-distance: 0%; opacity: 0; } 8% { opacity: 1; } 85% { opacity: 1; } 100% { offset-distance: 100%; opacity: 0; } }"
        "@media (prefers-reduced-motion: reduce) { .dot { display: none; } }"
    )
    body = [
        style_block(animation),
        '<defs><clipPath id="c"><rect x="0" y="0" width="1200" height="340" rx="24"/></clipPath>'
        f'<pattern id="p" width="28" height="28" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.6" fill="{h_t["pattern"]}"/></pattern></defs>',
        f'<rect x="1" y="1" width="{W - 2}" height="{h - 2}" rx="24" fill="{h_t["bg"]}" stroke="{h_t["edge"]}" stroke-width="2"/>',
        f'<rect x="0" y="0" width="{W}" height="{h}" fill="url(#p)" clip-path="url(#c)"/>',
        text(52, 128, NAME, 72, 800, h_t["text"], spacing=-2.5),
    ]
    first, lead, hot, end = HEADLINE
    size, spacing = 30, -0.4
    body.append(text(56, 194, first, size, 500, h_t["text"], spacing=spacing))
    if h_t["highlight"]:
        # A highlighter stroke behind the words and their full stop, which turns dark with them.
        hot, end = hot + end, ""
        x = 56 + width_of(lead, size, 500, spacing)
        w = width_of(hot, size, 800, spacing)
        body.append(f'<rect x="{x - 5:.1f}" y="{240 - 26}" width="{w + 9:.1f}" height="36" rx="7" fill="{h_t["highlight"]}"/>')
    second = f'{escape(lead)}<tspan font-weight="800" fill="{h_t["accent"]}">{escape(hot)}</tspan>{escape(end)}'
    body.append(text(56, 240, second, size, 500, h_t["text"], spacing=spacing, raw=True))
    body.append(text(56, 292, SUBLINE, 18, 500, h_t["muted"]))

    body.append(f'<path d="{flow_path}" stroke="{h_t["node_edge"]}" stroke-width="2" stroke-dasharray="3 5" fill="none"/>')
    for i, label in enumerate(FLOW):
        y = top + i * step
        hot_node = i == FLOW_HOT
        fill, edge, fg = (h_t["hot"], h_t["hot"], h_t["hot_text"]) if hot_node else (h_t["node"], h_t["node_edge"], h_t["node_text"])
        body.append(f'<rect x="{nx}" y="{y}" width="{nw}" height="{nh}" rx="13" fill="{fill}" stroke="{edge}" stroke-width="1.5"/>')
        body.append(f'<circle cx="{path_x}" cy="{y + nh / 2}" r="5" fill="{fg}" opacity="{1 if hot_node else 0.55}"/>')
        body.append(text(nx + 46, y + 29, label, 17, 700, fg, spacing=-0.2))
        body.append(text(nx + nw - 18, y + 29, f"0{i + 1}", 13, 700, fg, "end", 1))
    body.append(f'<circle class="dot" r="6" fill="{h_t["dot"]}"/>')
    return svg(W, h, f"{NAME}. {first} {''.join(HEADLINE[1:])} {SUBLINE}", "\n".join(body))


# ---------------------------------------------------------------- TIKT


def tikt_card(t):
    h = 184
    logo = base64.b64encode(TIKT["logo"].read_bytes()).decode()
    body = [
        style_block(),
        card(h, t),
        '<defs><clipPath id="l"><rect x="40" y="40" width="104" height="104" rx="24"/></clipPath></defs>',
        f'<image href="data:image/png;base64,{logo}" x="40" y="40" width="104" height="104" clip-path="url(#l)"/>',
        text(178, 86, "TIKT", 36, 800, t["text"], spacing=-1),
        text(178, 128, TIKT["title"], 27, 700, t["text"], spacing=-0.6),
    ]
    label = TIKT["button"] + " →"
    bw = width_of(label, 17, 700) + 44
    bx = W - 40 - bw
    body.append(f'<rect x="{bx:g}" y="66" width="{bw:g}" height="52" rx="14" fill="{t["button"]}"/>')
    body.append(text(bx + bw / 2, 98, label, 17, 700, t["button_text"], "middle"))
    return svg(W, h, f'TIKT. {TIKT["title"]}', "\n".join(body))


# ---------------------------------------------------------------- projects


def project_card(project, t):
    h = 300
    body = [style_block(), card(h, t)]
    body.append(text(48, 66, project["kicker"], 13, 700, t["accent"], spacing=1.6))
    body.append(text(46, 124, project["title"], 52, 800, t["text"], spacing=-1.8))
    for i, line in enumerate(project["lines"]):
        body.append(text(48, 166 + i * 28, line, 20, 500, t["muted"]))
    x = 48
    for tag in project["tags"]:
        piece, w = chip(x, 226, tag, t["chip"], t["text"], 13, 32)
        body.append(piece)
        x += w + 10
    # The four layers, the orchestration lit: the layer this skill adds.
    lx, lw, lh, top = 760, 392, 44, 46
    for i, layer in enumerate(project["layers"]):
        y = top + i * 54
        hot = i == project["hot"]
        fill, edge, fg = (t["hot"], t["hot"], t["hot_text"]) if hot else (t["layer"], t["layer_edge"], t["text"])
        body.append(f'<rect x="{lx}" y="{y}" width="{lw}" height="{lh}" rx="12" fill="{fill}" stroke="{edge}" stroke-width="1.5"/>')
        body.append(text(lx + 20, y + 28, f"0{i + 1}", 13, 700, fg if hot else t["muted"], spacing=1))
        body.append(text(lx + 56, y + 28, layer, 17, 700, fg, spacing=-0.2))
    body.append(text(lx + lw, top + 4 * 54 + 22, "View on GitHub →", 15, 700, t["accent"], "end"))
    summary = f'{project["title"]}: {" ".join(project["lines"])} Works in {", ".join(project["tags"][:3])}.'
    return svg(W, h, summary, "\n".join(body))


# ---------------------------------------------------------------- activity, in 3D


def streaks(days):
    longest = run = 0
    for _, count, _ in days:
        run = run + 1 if count else 0
        longest = max(longest, run)
    current = 0
    tail = days[:-1] if days and not days[-1][1] else days  # today may not have started yet
    for _, count, _ in reversed(tail):
        if not count:
            break
        current += 1
    return longest, current


def stats_block(t, data, days):
    longest, current = streaks(days)
    best = max(days, key=lambda d: d[1])
    total = f'{data["total"]:,}'
    out = [
        text(48, 66, "GITHUB ACTIVITY", 13, 700, t["accent"], spacing=1.6),
        text(46, 132, total, 64, 800, t["text"], spacing=-2),
        text(48 + width_of(total, 64, 800, -2) + 14, 132, "contributions in the last year", 22, 500, t["muted"]),
    ]
    stats = [("Longest streak", f"{longest} days"), ("Current streak", f"{current} days"), ("Most in a day", str(best[1]))]
    for i, (label, value) in enumerate(stats):
        x = 48 + i * 180
        out.append(text(x, 184, label, 14, 700, t["muted"], spacing=0.2))
        out.append(text(x, 218, value, 28, 800, t["text"], spacing=-0.8))
    summary = (
        f'GitHub activity: {data["total"]} contributions in the last year. Longest streak {longest} days, '
        f"current streak {current} days, most in a day {best[1]}."
    )
    return out, summary


def ramp_level(value, peak):
    return 0 if not value else 1 + min(3, int(4 * value / (peak + 1)))


def legend(x, y, t, label_less="Less", label_more="More"):
    out = [text(x, y + 13, label_less, 13, 700, t["muted"])]
    x += width_of(label_less, 13, 700) + 10
    for color in t["ramp"] + [LIME]:
        out.append(f'<rect x="{x:.1f}" y="{y}" width="16" height="16" rx="4" fill="{color}"/>')
        x += 21
    out.append(text(x + 4, y + 13, label_more, 13, 700, t["muted"]))
    return out


def activity_zoom(t, data, days):
    """The last 12 weeks, one block per day."""
    weeks = data["weeks"][-12:]
    levels = {"NONE": 0, "FIRST_QUARTILE": 1, "SECOND_QUARTILE": 2, "THIRD_QUARTILE": 3, "FOURTH_QUARTILE": 4}
    s = 27
    u, v = (0.866 * s, -0.5 * s), (0.866 * s, 0.5 * s)  # weeks rise to the right, days fall to the right
    origin, tallest, h = (676, 372), 150, 520
    peak = max(d[1] for week in weeks for d in week) or 1
    best = max((d for week in weeks for d in week), key=lambda d: d[1])
    stats, summary = stats_block(t, data, days)
    body = [style_block(), card(h, t), *stats]
    cells = []
    for i, week in enumerate(weeks):
        for day_str, count, level in week:
            j = date.fromisoformat(day_str).isoweekday() % 7  # Sunday first, as on GitHub
            cells.append((i, j, day_str, count, levels.get(level, 0)))
    tag = None
    for i, j, day_str, count, level in sorted(cells, key=lambda c: c[0] * u[1] + c[1] * v[1]):
        height = 2 if not count else 8 + tallest * (count / peak) ** 0.75
        color = LIME if day_str == best[0] and count else t["ramp"][level]
        corners = footprint(origin, u, v, i, j)
        body += prism(corners, height, color)
        if day_str == best[0] and count:
            cx = sum(x for x, _ in corners) / 4
            cy = sum(y for _, y in corners) / 4 - height
            tag = callout(cx, cy - 4, f"{count} on {short_date(date.fromisoformat(day_str))}", t)
    seen = set()
    for i, week in enumerate(weeks):
        last = date.fromisoformat(week[0][0]) + timedelta(days=6)
        if (last.year, last.month) in seen:
            continue
        seen.add((last.year, last.month))
        x = origin[0] + (i + 0.5) * u[0] + 7.5 * v[0]
        y = origin[1] + (i + 0.5) * u[1] + 7.5 * v[1] + 18
        body.append(text(x, y, last.strftime("%b"), 13, 700, t["muted"]))
    if tag:
        body.append(tag)
    body.append(text(48, h - 92, "The last 12 weeks, day by day", 15, 700, t["text"]))
    body += legend(48, h - 70, t)
    body.append(text(W - 48, h - 28, "Updated every day", 13, 500, t["muted"], "end"))
    return svg(W, h, summary + " Chart: the last 12 weeks, one block per day.", "\n".join(body))


def activity_skyline(t, data, days):
    """The whole year, one tower per week."""
    weeks = data["weeks"]
    totals = [sum(d[1] for d in week) for week in weeks]
    u, v = (18.4, -3.4), (-26.0, 19.0)
    origin, tallest, h = (164, 450), 160, 520
    peak = max(totals) or 1
    best = totals.index(peak)
    stats, summary = stats_block(t, data, days)
    body = [style_block(), card(h, t), *stats]
    tag = None
    # The ground: one flat band under the whole year, so empty weeks read as empty, not as noise.
    sx, sy = origin[0] + 0.1 * u[0] + 0.05 * v[0], origin[1] + 0.1 * u[1] + 0.05 * v[1]
    ax, ay = u[0] * (len(weeks) - 0.2), u[1] * (len(weeks) - 0.2)
    body += prism([(sx, sy), (sx + ax, sy + ay), (sx + ax + v[0] * 0.9, sy + ay + v[1] * 0.9), (sx + v[0] * 0.9, sy + v[1] * 0.9)], 3, t["ramp"][0])
    for i in sorted(range(len(weeks)), key=lambda i: i * u[1]):
        value = totals[i]
        if not value:
            continue
        height = 8 + tallest * (value / peak) ** 0.8
        color = LIME if i == best and value else t["ramp"][ramp_level(value, peak)]
        corners = footprint(origin, u, v, i, 0, 0.8, 0.9)
        body += prism([(x, y - 3) for x, y in corners], height, color)
        if i == best and value:
            cx = sum(x for x, _ in corners) / 4
            cy = sum(y for _, y in corners) / 4 - height
            tag = callout(cx, cy - 4, f"{value} in the week of {short_date(date.fromisoformat(weeks[i][0][0]))}", t)
    seen = set()
    for i, week in enumerate(weeks):
        last = date.fromisoformat(week[0][0]) + timedelta(days=6)
        if (last.year, last.month) in seen or i == 0:
            seen.add((last.year, last.month))
            continue
        seen.add((last.year, last.month))
        x = origin[0] + (i + 0.4) * u[0] + v[0]
        y = origin[1] + (i + 0.4) * u[1] + v[1] + 24
        body.append(text(x, y, last.strftime("%b"), 13, 700, t["muted"]))
    if tag:
        body.append(tag)
    body.append(text(W - 48, h - 52, "One tower per week", 13, 700, t["text"], "end"))
    body.append(text(W - 48, h - 30, "Updated every day", 13, 500, t["muted"], "end"))
    return svg(W, h, summary + " Chart: one tower per week over the last year.", "\n".join(body))


def activity_pillars(t, data, days):
    """The last 12 months, one pillar per month, its count on top."""
    months = OrderedDict()
    for day_str, count, _ in days:
        months.setdefault(day_str[:7], 0)
        months[day_str[:7]] += count
    keys = list(months)[-12:]
    values = [months[k] for k in keys]
    u, v = (82.0, -15.0), (-26.0, 19.0)
    origin, tallest, h = (166, 438), 190, 512
    peak = max(values) or 1
    best = values.index(peak)
    stats, summary = stats_block(t, data, days)
    body = [style_block(), card(h, t), *stats]
    labels = []
    for i in sorted(range(len(keys)), key=lambda i: i * u[1]):
        value = values[i]
        height = 4 if not value else 10 + tallest * (value / peak) ** 0.8
        color = LIME if i == best and value else t["ramp"][ramp_level(value, peak)]
        corners = footprint(origin, u, v, i, 0, 0.7, 0.9)
        body += prism(corners, height, color)
        cx = sum(x for x, _ in corners) / 4
        cy = sum(y for _, y in corners) / 4
        if value:
            labels.append(text(cx, cy - height - 14, f"{value:,}", 18, 800, t["text"], "middle", -0.4))
        month = date.fromisoformat(keys[i] + "-01").strftime("%b")
        labels.append(text(cx + v[0] * 0.2, cy + v[1] * 0.75 + 22, month, 13, 700, t["muted"], "middle"))
    body += labels
    body.append(text(W - 48, h - 52, "One pillar per month", 13, 700, t["text"], "end"))
    body.append(text(W - 48, h - 30, "Updated every day", 13, 500, t["muted"], "end"))
    return svg(W, h, summary + " Chart: one pillar per month over the last year.", "\n".join(body))


ACTIVITY_VIEWS = {"zoom": activity_zoom, "skyline": activity_skyline, "pillars": activity_pillars}


# ---------------------------------------------------------------- readme


def picture(name, alt, base, indent=""):
    return (
        f"{indent}<picture>\n"
        f'{indent}  <source media="(prefers-color-scheme: dark)" srcset="{base}/{name}-dark.svg">\n'
        f'{indent}  <img alt="{escape(alt, {chr(34): "&quot;"})}" src="{base}/{name}-light.svg" width="100%">\n'
        f"{indent}</picture>"
    )


def icon(background, mark):
    # A rounded square with the network's mark in white; a thin edge keeps a black square visible on dark pages.
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 48 48">'
        f'<rect x="0.75" y="0.75" width="46.5" height="46.5" rx="11" fill="{background}" stroke="#3A3A44" stroke-opacity="0.35" stroke-width="1.5"/>'
        f'<path transform="translate(12 12)" d="{mark}" fill="#FFFFFF"/></svg>\n'
    )


def icon_link(slug, name, url, base):
    return f'<a href="{url}"><img alt="{escape(name)}" src="{base}/icon-{slug}.svg" width="40" height="40"></a>'


def readme(base):
    first, lead, hot, end = HEADLINE
    parts = [
        picture("header", f"{NAME}. {first} {lead}{hot}{end}", base),
        '<p align="center">\n  ' + "\n  &nbsp;\n  ".join(icon_link(slug, name, url, base) for slug, name, url, _, _ in LINKS) + "\n</p>",
        "## About",
        f'<a href="{TIKT["url"]}">\n' + picture("tikt", f'TIKT. {TIKT["title"]}', base, "  ") + "\n</a>",
        "## Projects",
    ]
    for project in PROJECTS:
        alt = f'{project["title"]}: {" ".join(project["lines"])}'
        parts.append(f'<a href="{project["url"]}">\n{picture("project-" + project["slug"], alt, base, "  ")}\n</a>')
    parts += [
        "## Activity",
        picture("activity", "GitHub activity over the last year, in 3D", base),
        '<p align="center"><sub>Building TIKT in public. The fastest way to reach me is '
        '<a href="https://www.linkedin.com/in/maxime-musset/">LinkedIn</a> or '
        '<a href="https://x.com/AI_for_salesrep">X</a>.</sub></p>',
    ]
    return "\n\n".join(parts) + "\n"


# ---------------------------------------------------------------- build


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--style", default=STYLE, choices=sorted(STYLES))
    parser.add_argument("--activity", default=ACTIVITY, choices=sorted(ACTIVITY_VIEWS))
    parser.add_argument("--out", type=Path, default=ROOT)
    args = parser.parse_args()
    out_dir = args.out / "assets"
    out_dir.mkdir(parents=True, exist_ok=True)
    data = json.loads((ROOT / "data" / "contributions.json").read_text())
    days = [day for week in data["weeks"] for day in week]
    for mode, (h_t, t) in STYLES[args.style].items():
        (out_dir / f"header-{mode}.svg").write_text(header(h_t))
        (out_dir / f"tikt-{mode}.svg").write_text(tikt_card(t))
        for project in PROJECTS:
            (out_dir / f"project-{project['slug']}-{mode}.svg").write_text(project_card(project, t))
        (out_dir / f"activity-{mode}.svg").write_text(ACTIVITY_VIEWS[args.activity](t, data, days))
    for slug, _, _, background, mark in LINKS:
        (out_dir / f"icon-{slug}.svg").write_text(icon(background, mark))
    (args.out / "README.md").write_text(readme(RAW))
    print(f"{args.style}, {args.activity}: wrote README.md and {len(list(out_dir.glob('*.svg')))} SVG files in {args.out}")


if __name__ == "__main__":
    main()
