#!/usr/bin/env python3
"""Generate the SVG cards and link pills used in README.md.

Edit CONTENT below, then run:  python3 scripts/build-cards.py
Output goes to assets/ (one dark and one light file per image).
"""
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets"

# ---------------------------------------------------------------- content

ABOUT = {
    "title": "About & Engineering Focus",
    "tag": "TypeScript Ecosystem",
    "intro": "Full-stack developer owning products end to end within the modern TypeScript ecosystem.",
    "items": [
        ("End-to-end delivery:", "taking features from design mockup to production — UI, API, database and infrastructure."),
        ("Web & Mobile:", "building web apps and cross-platform mobile apps backed by reusable design systems."),
        ("Backend & Integrations:", "designing modular services, webhook integrations and solid relational data models."),
    ],
}

SNAPSHOT = {
    "title": "Snapshot",
    "rows": [
        ("Experience", "Since 2023", None),
        ("Education", "M.S. in CS · NURE (2025)", None),
        ("Location", "Kharkiv, UA (Remote)", None),
        ("Languages", "UA native · EN B1", None),
        ("Focus", "Full-Stack & Mobile", "blue"),
    ],
}

STACK = {
    "title": "Curated Production Stack",
    "rows": [
        ("Core", [("TypeScript", "blue"), ("JavaScript", "yellow")]),
        ("Web & Mobile", [("Next.js", "blue"), ("React", "cyan"), ("React Native", "cyan"), ("Expo", "purple"), ("Tailwind", "teal")]),
        ("Backend", [("NestJS", "red"), ("Elysia.js", "pink"), ("Node.js", "green"), ("Express", "yellow")]),
        ("Data", [("PostgreSQL", "indigo"), ("MySQL", "indigo"), ("Prisma", "cyan"), ("Drizzle", "amber")]),
        ("Cloud & Infra", [("AWS (S3/CloudFront)", "amber"), ("Docker", "sky"), ("CI/CD", "sky")]),
    ],
}

PRINCIPLES = {
    "title": "Craft & Engineering Mindset",
    "items": [
        "Turning ambitious, visually-refined designs into fluid digital products.",
        "Deconstructing complex problems into clean, reusable primitives.",
        "Obsessing over performance and resilience — from interface to cloud.",
    ],
}

# (slug, label, dark-theme color, light-theme color)
LINKS = [
    ("portfolio", "Portfolio", "#e6edf3", "#1f2328"),
    ("resume", "Resume", "#3fb950", "#1a7f37"),
    ("linkedin", "LinkedIn", "#4493f8", "#0a66c2"),
    ("telegram", "Telegram", "#3db5f0", "#0b84c6"),
    ("email", "Email", "#f47067", "#d1242f"),
]

# ---------------------------------------------------------------- theme

THEMES = {
    "dark": {
        "page": "#0d1117", "card": "#161b22", "border": "#30363d", "fg": "#e6edf3", "muted": "#8b949e",
        "blue": "#60a5fa", "purple": "#c084fc", "green": "#34d399", "cyan": "#22d3ee",
        "teal": "#2dd4bf", "red": "#f87171", "pink": "#f472b6", "yellow": "#facc15",
        "indigo": "#818cf8", "amber": "#fbbf24", "sky": "#38bdf8",
    },
    "light": {
        "page": "#ffffff", "card": "#f6f8fa", "border": "#d0d7de", "fg": "#1f2328", "muted": "#656d76",
        "blue": "#2563eb", "purple": "#9333ea", "green": "#059669", "cyan": "#0891b2",
        "teal": "#0d9488", "red": "#dc2626", "pink": "#db2777", "yellow": "#a16207",
        "indigo": "#4f46e5", "amber": "#b45309", "sky": "#0284c7",
    },
}

SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"

# ---------------------------------------------------------------- layout

W = 880          # viewBox width of a card row
GAP = 16
PAD = 24
RADIUS = 16
WIDE = (W - GAP) * 7 // 12
NARROW = W - GAP - WIDE

BODY = 14        # sans body size
LINE = 22        # body line height
MONO_SIZE = 12.5
MONO_CHAR = 0.6  # monospace advance in em (SF Mono, Menlo, Consolas ≈ 0.55–0.6)


def text_width(s, size, bold=False):
    """Conservative width estimate for proportional sans text."""
    narrow, semi, wide = set("ijlI.,:;'|!·()"), set("frt -/"), set("mwMW@")
    em = 0.0
    for ch in s:
        if ch in narrow:
            em += 0.27
        elif ch in semi:
            em += 0.36
        elif ch in wide:
            em += 0.86
        elif ch.isupper():
            em += 0.68
        else:
            em += 0.56
    return em * size * (1.06 if bold else 1.0) * 1.04  # headroom for Segoe UI / Noto


def wrap(words, width, size, first_offset=0.0):
    lines, cur, offset = [], "", first_offset
    for w in words:
        trial = f"{cur} {w}".strip()
        if cur and offset + text_width(trial, size) > width:
            lines.append(cur)
            cur, offset = w, 0.0
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines


def card(x, w, h, t):
    return (f'<rect x="{x + .5}" y=".5" width="{w - 1}" height="{h - 1}" rx="{RADIUS}" '
            f'fill="{t["card"]}" stroke="{t["border"]}"/>')


def title(x, y, label, color):
    return (f'<text x="{x}" y="{y}" font-family="{MONO}" font-size="12" font-weight="700" '
            f'letter-spacing="1.4" fill="{color}">{escape(label.upper())}</text>')


def about_card(x, t):
    w, inner = WIDE, WIDE - 2 * PAD
    out, y = [], PAD + 14
    out.append(title(x + PAD, y, ABOUT["title"], t["blue"]))
    tag_w = len(ABOUT["tag"]) * 11 * MONO_CHAR + 16
    tx = x + w - PAD - tag_w
    out.append(f'<rect x="{tx}" y="{y - 15}" width="{tag_w}" height="21" rx="6" fill="{t["blue"]}" fill-opacity=".12"/>')
    out.append(f'<text x="{tx + 8}" y="{y - 1}" font-family="{MONO}" font-size="11" fill="{t["blue"]}">{escape(ABOUT["tag"])}</text>')
    y += 30
    for line in wrap(ABOUT["intro"].split(), inner, BODY):
        out.append(f'<text x="{x + PAD}" y="{y}" font-family="{SANS}" font-size="{BODY}" fill="{t["muted"]}">{escape(line)}</text>')
        y += LINE
    y += 8
    indent = 16
    for lead, rest in ABOUT["items"]:
        lead_w = text_width(lead + " ", BODY, bold=True)
        lines = wrap(rest.split(), inner - indent, BODY, first_offset=lead_w)
        out.append(f'<circle cx="{x + PAD + 3}" cy="{y - 5}" r="2" fill="{t["muted"]}"/>')
        out.append(f'<text x="{x + PAD + indent}" y="{y}" font-family="{SANS}" font-size="{BODY}">'
                   f'<tspan font-weight="600" fill="{t["fg"]}">{escape(lead)}</tspan>'
                   f'<tspan fill="{t["muted"]}"> {escape(lines[0])}</tspan></text>')
        for line in lines[1:]:
            y += LINE
            out.append(f'<text x="{x + PAD + indent}" y="{y}" font-family="{SANS}" font-size="{BODY}" fill="{t["muted"]}">{escape(line)}</text>')
        y += LINE + 8
    return out, y - 8 - LINE + PAD + 6


def snapshot_card(x, t):
    w = NARROW
    out, y = [], PAD + 14
    out.append(title(x + PAD, y, SNAPSHOT["title"], t["purple"]))
    y += 34
    for label, value, accent in SNAPSHOT["rows"]:
        out.append(f'<text x="{x + PAD}" y="{y}" font-family="{SANS}" font-size="{BODY}" fill="{t["muted"]}">{escape(label)}</text>')
        out.append(f'<text x="{x + w - PAD}" y="{y}" text-anchor="end" font-family="{MONO}" font-size="13" '
                   f'font-weight="600" fill="{t[accent] if accent else t["fg"]}">{escape(value)}</text>')
        y += 32
    return out, y - 32 + PAD + 6


def stack_card(x, t):
    w, label_w = WIDE, 118
    out, y = [], PAD + 14
    out.append(title(x + PAD, y, STACK["title"], t["blue"]))
    y += 34
    char = MONO_SIZE * MONO_CHAR
    max_x = x + w - PAD
    for label, tokens in STACK["rows"]:
        out.append(f'<text x="{x + PAD}" y="{y}" font-family="{SANS}" font-size="{BODY}" font-weight="600" fill="{t["fg"]}">{escape(label)}</text>')
        cx = x + PAD + label_w
        for i, (tok, color) in enumerate(tokens):
            sep = "," if i < len(tokens) - 1 else ""
            need = (len(tok) + len(sep)) * char
            if cx + need > max_x:
                cx, y = x + PAD + label_w, y + LINE
            out.append(f'<text x="{cx:.1f}" y="{y}" font-family="{MONO}" font-size="{MONO_SIZE}" fill="{t[color]}">{escape(tok)}'
                       f'<tspan fill="{t["muted"]}">{sep}</tspan></text>')
            cx += need + char
        y += 30
    return out, y - 30 + PAD + 6


def principles_card(x, t):
    w, indent = NARROW, 16
    inner = w - 2 * PAD - indent
    out, y = [], PAD + 14
    out.append(title(x + PAD, y, PRINCIPLES["title"], t["green"]))
    y += 34
    for item in PRINCIPLES["items"]:
        out.append(f'<circle cx="{x + PAD + 3}" cy="{y - 5}" r="2.5" fill="{t["green"]}"/>')
        for line in wrap(item.split(), inner, BODY):
            out.append(f'<text x="{x + PAD + indent}" y="{y}" font-family="{SANS}" font-size="{BODY}" fill="{t["fg"]}">{escape(line)}</text>')
            y += LINE
        y += 8
    return out, y - 8 - LINE + PAD + 6


def row(left_fn, right_fn, t):
    l_items, l_h = left_fn(0, t)
    r_items, r_h = right_fn(WIDE + GAP, t)
    h = int(max(l_h, r_h))
    return [card(0, WIDE, h, t), card(WIDE + GAP, NARROW, h, t), *l_items, *r_items], h


def cards(t, alt):
    top, top_h = row(about_card, snapshot_card, t)
    bottom, bottom_h = row(stack_card, principles_card, t)
    body = [*top, f'<g transform="translate(0 {top_h + GAP})">', *bottom, "</g>"]
    return svg(W, top_h + GAP + bottom_h, body, alt)


def svg(w, h, body, alt):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="{escape(alt, {chr(34): "&quot;"})}">\n<title>{escape(alt)}</title>\n'
            + "\n".join(body) + "\n</svg>\n")


def mix(color, base, amount):
    """Blend color over base, so pills stay opaque and readable on any page background."""
    c, b = (tuple(int(h[i:i + 2], 16) for i in (1, 3, 5)) for h in (color, base))
    return "#" + "".join(f"{round(cv * amount + bv * (1 - amount)):02x}" for cv, bv in zip(c, b))


def pill(label, color, t):
    size, h = 13, 30
    w = round(14 + 8 + 8 + len(label) * size * MONO_CHAR + 14)
    body = [
        f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="8" fill="{mix(color, t["page"], .14)}" stroke="{mix(color, t["page"], .5)}"/>',
        f'<circle cx="18" cy="{h / 2}" r="4" fill="{color}"/>',
        f'<text x="30" y="{h / 2 + 4.5}" font-family="{MONO}" font-size="{size}" font-weight="600" fill="{t["fg"]}">{escape(label)}</text>',
    ]
    return svg(w, h, body, label)


def main():
    OUT.mkdir(exist_ok=True)
    about_alt = "About: " + ABOUT["intro"] + " " + " ".join(f"{a} {b}" for a, b in ABOUT["items"])
    snap_alt = "Snapshot: " + "; ".join(f"{a}: {b}" for a, b, _ in SNAPSHOT["rows"])
    stack_alt = "Stack: " + "; ".join(f"{a}: {', '.join(n for n, _ in toks)}" for a, toks in STACK["rows"])
    princ_alt = "Mindset: " + " ".join(PRINCIPLES["items"])
    for name, t in THEMES.items():
        (OUT / f"cards-{name}.svg").write_text(cards(t, " ".join([about_alt, snap_alt, stack_alt, princ_alt])))
        for slug, label, dark, light in LINKS:
            (OUT / f"link-{slug}-{name}.svg").write_text(pill(label, dark if name == "dark" else light, t))
    print(f"wrote {len(list(OUT.glob('*.svg')))} files to {OUT.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
