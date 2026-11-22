"""Paleta e helpers compartilhados pelos SVGs do perfil (tema Power BI, modo escuro)."""
from html import escape

FONT = ("'Segoe UI','Segoe UI Variable',system-ui,-apple-system,BlinkMacSystemFont,"
        "'Helvetica Neue',Arial,sans-serif")
MONO = "'Cascadia Code','Cascadia Mono',Consolas,'SFMono-Regular',Menlo,monospace"

C = {
    "bg": "#161514",       # fundo do canvas
    "chrome": "#252423",   # barras e painéis
    "page": "#1F1E1D",     # página do relatório
    "card": "#292827",     # visuais
    "card2": "#2D2C2B",
    "line": "#3B3A39",
    "line2": "#4A4846",
    "text": "#F3F2F1",
    "text2": "#D2D0CE",
    "muted": "#A19F9D",
    "dim": "#7A7876",
    "yellow": "#F2C811",
    "amber": "#E8A317",
    "orange": "#C67A0A",
}
# Cores padrão dos visuais do Power BI
DATA = ["#118DFF", "#E66C37", "#744EC2", "#E044A7", "#12239E", "#6B007B", "#D9B300", "#D64550"]

DEFS = f"""
  <linearGradient id="pbi" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{C['yellow']}"/><stop offset="1" stop-color="{C['amber']}"/>
  </linearGradient>
  <linearGradient id="barg" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{C['yellow']}"/><stop offset="1" stop-color="{C['orange']}"/>
  </linearGradient>"""

BASE_CSS = f"""
  text{{font-family:{FONT};}}
  .mono{{font-family:{MONO};}}
  .bar{{transform-box:fill-box;transform-origin:50% 100%;animation:grow 1.1s cubic-bezier(.2,.8,.2,1) both;}}
  @keyframes grow{{from{{transform:scaleY(0)}}to{{transform:scaleY(1)}}}}
  .up{{animation:up .7s ease-out both;}}
  @keyframes up{{from{{opacity:0;transform:translateY(10px)}}to{{opacity:1;transform:translateY(0)}}}}
  .fade{{animation:fade .6s ease-out both;}}
  @keyframes fade{{from{{opacity:0}}to{{opacity:1}}}}
  .draw{{stroke-dasharray:900;stroke-dashoffset:900;animation:draw 1.8s ease-out 1.1s forwards;}}
  @keyframes draw{{to{{stroke-dashoffset:0}}}}
  .pulse{{animation:pulse 2s ease-in-out infinite;}}
  @keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:.35}}}}
  .sweep{{animation:sweep 4.5s ease-in-out infinite;}}
  @keyframes sweep{{0%{{transform:translateX(-300px)}}100%{{transform:translateX(1500px)}}}}
"""


def e(s):
    return escape(str(s), quote=True)


def svg(w, h, body, label, css="", defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="{e(label)}">\n<title>{e(label)}</title>\n'
            f'<defs>{DEFS}{defs}\n<style>{BASE_CSS}{css}</style>\n</defs>\n{body}\n</svg>\n')


def logo(x, y, s=1.0):
    """Ícone de três barras amarelas (tema BI)."""
    bars = [(0, 9, 8), (7, 4, 13), (14, -1, 18)]
    return "".join(
        f'<rect x="{x + bx * s:.1f}" y="{y + by * s:.1f}" width="{5 * s:.1f}" height="{bh * s:.1f}" '
        f'rx="{1.4 * s:.1f}" fill="url(#pbi)"/>' for bx, by, bh in bars)


def text_w(s, size, bold=False):
    """Largura aproximada de um texto (sans), com folga para fontes de fallback."""
    w = 0.0
    for ch in str(s):
        if ch in "il.,:;|!'·": w += 0.30
        elif ch in "fjtrI()[] ": w += 0.38
        elif ch in "mwMW@": w += 0.88
        elif ch.isupper() or ch.isdigit(): w += 0.64
        else: w += 0.55
    return w * size * (1.06 if bold else 1.0)


def chip(x, y, label, size=12.5, fill=None, stroke=None, color=None, h=26, bold=False):
    fill = fill or C["card2"]
    stroke = stroke or C["line2"]
    color = color or C["text"]
    w = text_w(label, size, bold) + 26
    weight = ' font-weight="600"' if bold else ''
    return (f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{h}" rx="{h / 2}" fill="{fill}" stroke="{stroke}"/>'
            f'<text x="{x + w / 2:.1f}" y="{y + h / 2 + size * 0.36:.1f}" font-size="{size}" fill="{color}" '
            f'text-anchor="middle"{weight}>{e(label)}</text>'), w


def visual_icons(x, y, color=None):
    """Ícones do cabeçalho de um visual: filtro, modo foco e '...'."""
    c = color or C["dim"]
    return (f'<g fill="none" stroke="{c}" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round">'
            f'<path d="M{x} {y}h12l-4.5 5.5v4.5l-3-1.5v-3z"/>'
            f'<path d="M{x + 26} {y + 4}v-4h4M{x + 38} {y}h4v4M{x + 42} {y + 8}v4h-4M{x + 30} {y + 12}h-4v-4"/>'
            f'</g><g fill="{c}"><circle cx="{x + 56}" cy="{y + 6}" r="1.5"/><circle cx="{x + 62}" cy="{y + 6}" r="1.5"/>'
            f'<circle cx="{x + 68}" cy="{y + 6}" r="1.5"/></g>')
