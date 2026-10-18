#!/usr/bin/env python3
"""Generate the profile README and its SVG assets, in light and dark variants.

Edit the content below, then run from anywhere:

    python3 scripts/build.py

PROJECTS and STACK start empty: the README then shows a "going public soon"
card. Fill them in as repos go public and run the script again.
"""

import math
from pathlib import Path
from urllib.parse import quote
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
REPO = "mussetpro-ship-it/mussetpro-ship-it"
RAW = f"https://raw.githubusercontent.com/{REPO}/main/assets"

DISPLAY = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Arial Black', Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"

LIME = "#D7F7AA"
BLUE = "#305DFF"
INK = "#0A0A0A"

THEMES = {
    "light": {
        "card": LIME,       # banner background
        "panel": "#FFFFFF",  # other cards
        "edge": INK,
        "name": INK,
        "text": INK,
        "muted": "#4B5563",
        "highlight": BLUE,
        "chip_bg": INK,
        "chip_text": LIME,
        "block": "#FFFFFF",
        "block_shadow": INK,
    },
    "dark": {
        "card": "#0E1116",
        "panel": "#0E1116",
        "edge": LIME,
        "name": LIME,
        "text": "#E6EDF3",
        "muted": "#9BA3AF",
        "highlight": LIME,
        "chip_bg": LIME,
        "chip_text": INK,
        "block": "#161B22",
        "block_shadow": BLUE,
    },
}

# ---------------------------------------------------------------- content

NAME = "Musset"
KICKER = "GTM SYSTEMS · B2B"
TAGLINE_PREFIX = "I build GTM systems with "
TAGLINE_HIGHLIGHT = "Claude Code"
TAGLINE_END = "for B2B companies."
PIPELINE = ["signals", "enrich", "score", "route", "outreach"]
STICKER = "SHIPPED WITH CLAUDE CODE ✦ "

# (text, url, Simple Icons logo) rendered as badges under the banner.
LINKS = [
    ("@AI_for_salesrep", "https://x.com/AI_for_salesrep", "x"),
]

# Add one entry per public repo, for example:
# {
#     "slug": "lead-router",
#     "title": "Lead router",
#     "url": "https://github.com/mussetpro-ship-it/lead-router",
#     "lines": ["Routes inbound leads to the right rep in seconds,", "based on fit and intent signals."],
#     "tags": ["Claude Code", "HubSpot", "Python"],
# },
PROJECTS = []

# Tools, in the order they should appear, for example: ["Claude Code", "Clay", "HubSpot"].
STACK = []

# ---------------------------------------------------------------- helpers


def style_block(extra=""):
    return (
        "<style>"
        f".display {{ font-family: {DISPLAY}; }}"
        f".mono {{ font-family: {MONO}; }}"
        f"{extra}"
        "</style>"
    )


def svg(width, height, title, body):
    label = escape(title, {'"': "&quot;"})
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-label="{label}">\n'
        f"<title>{escape(title)}</title>\n{body}\n</svg>\n"
    )


def slab(x, y, w, h, fill, edge, shadow_color, shadow=8, radius=14, stroke=3):
    """A neo-brutalist block: flat fill, thick edge, hard offset shadow."""
    return (
        f'<rect x="{x + shadow:g}" y="{y + shadow:g}" width="{w:g}" height="{h:g}" rx="{radius}" fill="{shadow_color}"/>'
        f'<rect x="{x + stroke / 2:g}" y="{y + stroke / 2:g}" width="{w - stroke:g}" height="{h - stroke:g}" '
        f'rx="{radius - stroke / 2:g}" fill="{fill}" stroke="{edge}" stroke-width="{stroke}"/>'
    )


def chip_width(label, char_width=7.8, padding=28):
    # Monospace glyphs are ~0.6em wide, so the width is predictable.
    return round(len(label) * char_width + padding)


# ---------------------------------------------------------------- banner


def banner(t):
    w, h, shadow = 1200, 340, 12
    bx, bw, bh, step, top = 700, 270, 42, 53, 44
    cx, cy, r = 1090, 170, 62

    # Pipeline stages light up one after the other; the sticker ring spins.
    animation = (
        ".hit { opacity: 0; animation: hit 5s infinite both; }"
        "@keyframes hit { 0%, 100% { opacity: 0; } 4%, 16% { opacity: 1; } 24% { opacity: 0; } }"
        f".spin {{ animation: spin 24s linear infinite; transform-origin: {cx}px {cy}px; }}"
        "@keyframes spin { to { transform: rotate(360deg); } }"
        "@media (prefers-reduced-motion: reduce) { .hit, .spin { animation: none; } }"
    )
    chip_w = round(len(KICKER) * 9.3 + 32)

    body = [
        style_block(animation),
        slab(0, 0, w, h, t["card"], t["edge"], BLUE, shadow=shadow, radius=18),
        # Kicker chip
        f'<rect x="56" y="48" width="{chip_w}" height="34" rx="17" fill="{t["chip_bg"]}"/>',
        f'<text x="72" y="70" class="mono" font-size="13" font-weight="700" letter-spacing="1.5" '
        f'fill="{t["chip_text"]}">{escape(KICKER)}</text>',
        # Name and tagline
        f'<text x="48" y="198" class="display" font-size="120" font-weight="900" letter-spacing="-5" '
        f'fill="{t["name"]}">{escape(NAME)}</text>',
        f'<text x="56" y="252" class="display" font-size="24" font-weight="500" fill="{t["text"]}">'
        f'{escape(TAGLINE_PREFIX)}<tspan font-weight="800" fill="{t["highlight"]}">{escape(TAGLINE_HIGHLIGHT)}</tspan></text>',
        f'<text x="56" y="284" class="display" font-size="24" font-weight="500" fill="{t["text"]}">'
        f"{escape(TAGLINE_END)}</text>",
    ]

    # GTM pipeline
    for i, stage in enumerate(PIPELINE):
        y = top + i * step
        if i:
            body.append(
                f'<path d="M{bx + bw / 2:g} {y - step + bh + 5} V{y}" stroke="{t["edge"]}" stroke-width="2.5"/>'
            )
        body.append(slab(bx, y, bw, bh, t["block"], t["edge"], t["block_shadow"], shadow=5, radius=8, stroke=2.5))
        label = (
            f'<text x="{bx + 18}" y="{y + 27}" class="mono" font-size="13" font-weight="700" fill="{{num}}">0{i + 1}</text>'
            f'<text x="{bx + 52}" y="{y + 27}" class="mono" font-size="16" font-weight="700" fill="{{fg}}">{escape(stage)}</text>'
        )
        body.append(label.format(num=t["muted"], fg=t["text"]))
        body.append(
            f'<g class="hit" style="animation-delay: {i * 0.7:g}s">'
            f'<rect x="{bx + 1.25}" y="{y + 1.25}" width="{bw - 2.5}" height="{bh - 2.5}" rx="6.75" '
            f'fill="{BLUE}" stroke="{t["edge"]}" stroke-width="2.5"/>'
            + label.format(num=LIME, fg="#FFFFFF")
            + f'<text x="{bx + bw - 18}" y="{y + 28}" class="mono" font-size="18" font-weight="700" '
            f'text-anchor="end" fill="#FFFFFF">→</text></g>'
        )

    # Spinning sticker
    ring_r = 44
    body += [
        f'<circle cx="{cx + 4}" cy="{cy + 4}" r="{r}" fill="{t["edge"]}"/>',
        f'<circle cx="{cx}" cy="{cy}" r="{r - 1.5}" fill="{BLUE}" stroke="{t["edge"]}" stroke-width="3"/>',
        f'<path id="ring" d="M{cx - ring_r} {cy} a{ring_r} {ring_r} 0 1 1 {2 * ring_r} 0 '
        f'a{ring_r} {ring_r} 0 1 1 {-2 * ring_r} 0" fill="none"/>',
        f'<g class="spin"><text class="mono" font-size="11.5" font-weight="700" letter-spacing="2" fill="{LIME}">'
        f'<textPath href="#ring" textLength="{2 * math.pi * ring_r - 6:.0f}" lengthAdjust="spacing">'
        f"{escape(STICKER)}</textPath></text></g>",
        f'<path transform="translate({cx} {cy})" d="M0 -22 C3 -6 6 -3 22 0 C6 3 3 6 0 22 '
        f'C-3 6 -6 3 -22 0 C-6 -3 -3 -6 0 -22 Z" fill="{LIME}"/>',
    ]

    title = f"{NAME}. {TAGLINE_PREFIX}{TAGLINE_HIGHLIGHT} {TAGLINE_END}"
    return svg(w + shadow, h + shadow, title, "\n".join(body))


# ---------------------------------------------------------------- cards


def coming_soon(t):
    w, h, shadow = 860, 150, 8
    body = [
        style_block(
            ".blink { animation: blink 1.1s steps(1) infinite; }"
            "@keyframes blink { 50% { opacity: 0; } }"
            "@media (prefers-reduced-motion: reduce) { .blink { animation: none; } }"
        ),
        slab(0, 0, w, h, t["panel"], t["edge"], BLUE, shadow=shadow),
        f'<text x="32" y="46" class="mono" font-size="12" font-weight="700" letter-spacing="2" '
        f'fill="{t["highlight"]}">STATUS · IN PROGRESS</text>',
        f'<text x="30" y="94" class="display" font-size="36" font-weight="900" letter-spacing="-1" '
        f'fill="{t["name"]}">Repos going public soon'
        f'<tspan class="blink" fill="{BLUE}">_</tspan></text>',
        f'<text x="32" y="126" class="mono" font-size="14" fill="{t["muted"]}">'
        "Projects land here as soon as they ship.</text>",
    ]
    return svg(w + shadow, h + shadow, "Repos going public soon.", "\n".join(body))


def project_card(project, t):
    w, h, shadow = 860, 170, 8
    button = 56
    body = [
        style_block(),
        slab(0, 0, w, h, t["panel"], t["edge"], BLUE, shadow=shadow),
        # Initial block
        f'<rect x="28" y="30" width="86" height="86" rx="10" fill="{BLUE}" stroke="{t["edge"]}" stroke-width="2.5"/>',
        f'<text x="71" y="90" class="display" font-size="46" font-weight="900" text-anchor="middle" '
        f'fill="{LIME}">{escape(project["title"][:1].upper())}</text>',
        f'<text x="140" y="60" class="display" font-size="26" font-weight="800" fill="{t["name"]}">'
        f'{escape(project["title"])}</text>',
        # Open button
        f'<rect x="{w - 28 - button}" y="{(h - button) / 2:g}" width="{button}" height="{button}" rx="10" '
        f'fill="{LIME}" stroke="{t["edge"]}" stroke-width="2.5"/>',
        f'<text x="{w - 28 - button / 2:g}" y="{h / 2 + 10:g}" class="display" font-size="28" font-weight="900" '
        f'text-anchor="middle" fill="{INK}">→</text>',
    ]
    for i, line in enumerate(project["lines"]):
        body.append(
            f'<text x="140" y="{90 + i * 21}" class="display" font-size="15" fill="{t["text"]}">{escape(line)}</text>'
        )
    x = 140
    for tag in project["tags"]:
        width = chip_width(tag)
        body.append(
            f'<rect x="{x}" y="128" width="{width}" height="26" rx="13" fill="none" stroke="{t["edge"]}" stroke-width="2"/>'
            f'<text x="{x + width / 2:g}" y="145.5" class="mono" font-size="12" font-weight="700" '
            f'text-anchor="middle" fill="{t["text"]}">{escape(tag)}</text>'
        )
        x += width + 8
    summary = f'{project["title"]}: {" ".join(project["lines"])}'
    return svg(w + shadow, h + shadow, summary, "\n".join(body))


def stack_panel(t):
    w, gap, row_h, pad = 860, 12, 52, 4
    body = [style_block()]
    x, y = pad, pad
    for tool in STACK:
        width = chip_width(tool, char_width=8.4, padding=36)
        if x + width + 4 > w:
            x, y = pad, y + row_h
        body.append(slab(x, y, width, 40, t["block"], t["edge"], BLUE, shadow=4, radius=10, stroke=2.5))
        body.append(
            f'<text x="{x + width / 2:g}" y="{y + 26}" class="mono" font-size="14" font-weight="700" '
            f'text-anchor="middle" fill="{t["text"]}">{escape(tool)}</text>'
        )
        x += width + gap
    return svg(w, y + 48, "Stack: " + ", ".join(STACK), "\n".join(body))


# ---------------------------------------------------------------- readme


def picture(name, alt, indent=""):
    return (
        f"{indent}<picture>\n"
        f'{indent}  <source media="(prefers-color-scheme: dark)" srcset="{RAW}/{name}-dark.svg">\n'
        f'{indent}  <img alt="{escape(alt, {chr(34): "&quot;"})}" src="{RAW}/{name}-light.svg" width="100%">\n'
        f"{indent}</picture>"
    )


def badge(text, url, logo):
    # An empty label leaves only the logo on the dark side of the badge.
    value = quote(text.replace("-", "--").replace("_", "__"), safe="")
    src = (
        f"https://img.shields.io/badge/-{value}-{BLUE[1:]}"
        f"?style=for-the-badge&logo={logo}&logoColor=white&labelColor={INK[1:]}"
    )
    return f'<a href="{url}"><img alt="{escape(logo)} {escape(text)}" src="{src}"></a>'


def readme():
    parts = [
        picture("banner", f"{NAME}. {TAGLINE_PREFIX}{TAGLINE_HIGHLIGHT} {TAGLINE_END}"),
        '<p align="center">\n  ' + "\n  ".join(badge(*link) for link in LINKS) + "\n</p>",
        "## Projects",
    ]
    if PROJECTS:
        for project in PROJECTS:
            alt = f'{project["title"]}: {" ".join(project["lines"])}'
            parts.append(f'<a href="{project["url"]}">\n{picture("project-" + project["slug"], alt, "  ")}\n</a>')
    else:
        parts.append(picture("coming-soon", "Repos going public soon."))
    if STACK:
        parts += ["## Stack", picture("stack", "Stack: " + ", ".join(STACK))]
    return "\n\n".join(parts) + "\n"


# ---------------------------------------------------------------- build


def main(out_dir=ROOT / "assets", readme_path=ROOT / "README.md"):
    out_dir.mkdir(parents=True, exist_ok=True)
    for name, t in THEMES.items():
        (out_dir / f"banner-{name}.svg").write_text(banner(t))
        (out_dir / f"coming-soon-{name}.svg").write_text(coming_soon(t))
        for project in PROJECTS:
            (out_dir / f"project-{project['slug']}-{name}.svg").write_text(project_card(project, t))
        if STACK:
            (out_dir / f"stack-{name}.svg").write_text(stack_panel(t))
    readme_path.write_text(readme())
    print(f"Wrote {readme_path.name} and {len(list(out_dir.glob('*.svg')))} SVG files")


if __name__ == "__main__":
    main()
