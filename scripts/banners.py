"""Banners animados de cada projeto e a faixa de stack rolando (ticker).

Uso: python scripts/banners.py   (escreve em assets/banners/ e assets/ticker.svg)
"""
import math
from pathlib import Path

from build_assets import LOOP_CSS
from theme import C, e, svg, text_w

OUT = Path(__file__).resolve().parent.parent / "assets"

AZUL, AMARELO, LARANJA, ROXO, ROSA, VERDE, CIANO = ("#118DFF", "#F2C811", "#E66C37", "#9B7BFF", "#E044A7",
                                                     "#1AAB40", "#13BFCF")

CSS = LOOP_CSS + """
  .spin{transform-box:fill-box;transform-origin:50% 50%;animation:spin 6s linear infinite;}
  .spinr{transform-box:fill-box;transform-origin:50% 50%;animation:spin 4s linear infinite reverse;}
  @keyframes spin{to{transform:rotate(360deg)}}
  .flow{animation:flow 1s linear infinite;}
  @keyframes flow{to{stroke-dashoffset:-24}}
  .loopdraw{stroke-dasharray:400;stroke-dashoffset:400;animation:loopdraw 5s ease-in-out infinite;}
  @keyframes loopdraw{0%{stroke-dashoffset:400}45%,85%{stroke-dashoffset:0}100%{stroke-dashoffset:-400}}
  .band{animation:band 5s ease-in-out infinite;}
  @keyframes band{0%,30%{opacity:0}50%,85%{opacity:.35}100%{opacity:0}}
  .fill{transform-box:fill-box;transform-origin:0 50%;animation:fill 3.2s ease-in-out infinite;}
  @keyframes fill{0%{transform:scaleX(0)}70%,100%{transform:scaleX(1)}}
  .cell{animation:cell 4s ease-in-out infinite both;}
  @keyframes cell{0%{opacity:.08}25%,80%{opacity:.95}100%{opacity:.08}}
  .pop{transform-box:fill-box;transform-origin:50% 50%;animation:pop 2.4s ease-in-out infinite;}
  @keyframes pop{0%,100%{transform:scale(1)}50%{transform:scale(1.12)}}
  .ticker{animation:ticker var(--d) linear infinite;}
  @keyframes ticker{to{transform:translateX(var(--w))}}
"""


def _ajusta(texto, tamanho, largura, bold=True):
    return min(tamanho, tamanho * largura / max(text_w(texto, tamanho, bold), 1))


def _quebra(texto, tamanho, largura):
    linhas, atual = [], ""
    for p in texto.split():
        teste = f"{atual} {p}".strip()
        if text_w(teste, tamanho) > largura and atual:
            linhas.append(atual)
            atual = p
        else:
            atual = teste
    return linhas + [atual]


def _chip(x, y, t, cor, h=24, size=12):
    w = text_w(t, size) + 22
    return (f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{h}" rx="{h / 2}" fill="{C["card2"]}" stroke="{C["line2"]}"/>'
            f'<text x="{x + w / 2:.1f}" y="{y + h / 2 + size * .36:.1f}" font-size="{size}" fill="{C["text2"]}" '
            f'text-anchor="middle">{e(t)}</text>'), w


# ------------------------------------------------------------------ decorações (mini visuais animados)
def deco_forecast(x, y, w, h, cor):
    pts = []
    for i in range(24):
        v = .5 + .28 * math.sin(i / 1.6) + .1 * math.sin(i * 1.7)
        pts.append((x + 12 + i * (w * .58) / 23, y + h - 12 - v * (h - 30)))
    hist = " ".join(f"{a:.1f},{b:.1f}" for a, b in pts)
    x0, y0 = pts[-1]
    fut = [(x0 + (k + 1) * (w * .34) / 8, y0 - 6 * math.sin(k / 2) - k * 1.2) for k in range(8)]
    linha = f"{x0:.1f},{y0:.1f} " + " ".join(f"{a:.1f},{b:.1f}" for a, b in fut)
    sup = [(a, b - 4 - k * 2.2) for k, (a, b) in enumerate(fut)]
    inf = [(a, b + 4 + k * 2.2) for k, (a, b) in enumerate(fut)]
    banda = f"{x0:.1f},{y0:.1f} " + " ".join(f"{a:.1f},{b:.1f}" for a, b in sup) + " " + \
            " ".join(f"{a:.1f},{b:.1f}" for a, b in reversed(inf))
    return (f'<polyline points="{hist}" fill="none" stroke="{AMARELO}" stroke-width="2" opacity=".85"/>'
            f'<polygon points="{banda}" fill="{cor}" class="band"/>'
            f'<polyline points="{linha}" fill="none" stroke="{cor}" stroke-width="2.6" stroke-linecap="round" class="loopdraw"/>'
            f'<line x1="{x0:.1f}" y1="{y + 8}" x2="{x0:.1f}" y2="{y + h - 8}" stroke="{C["dim"]}" stroke-dasharray="3 3"/>'
            f'<text x="{x0 + 6:.1f}" y="{y + 18}" font-size="10" fill="{C["muted"]}">previsão</text>')


def deco_pipeline(x, y, w, h, cor):
    nomes = ["API", "ETL", "DuckDB", "Painel"]
    passo = (w - 40) / (len(nomes) - 1)
    cy = y + h / 2
    b = [f'<path d="M{x + 20} {cy}H{x + w - 20}" stroke="{C["line2"]}" stroke-width="2"/>',
         f'<path d="M{x + 20} {cy}H{x + w - 20}" stroke="{cor}" stroke-width="2.5" stroke-dasharray="5 7" class="flow"/>']
    for i, n in enumerate(nomes):
        nx = x + 20 + i * passo
        b.append(f'<g class="pop" style="animation-delay:{i * .6:.1f}s"><circle cx="{nx:.1f}" cy="{cy}" r="13" '
                 f'fill="{C["chrome"]}" stroke="{cor}" stroke-width="2"/><circle cx="{nx:.1f}" cy="{cy}" r="4.5" fill="{cor}"/></g>'
                 f'<text x="{nx:.1f}" y="{cy + 30}" font-size="10.5" fill="{C["muted"]}" text-anchor="middle">{n}</text>')
    b.append(f'<circle r="4" fill="{AMARELO}"><animateMotion dur="2.4s" repeatCount="indefinite" '
             f'path="M{x + 20} {cy}H{x + w - 20}"/></circle>')
    return "".join(b)


def deco_riscos(x, y, w, h, cor):
    cores = ["#1AAB40", "#1AAB40", AMARELO, AMARELO, LARANJA, "#D64550", LARANJA, AMARELO, "#1AAB40", LARANJA, "#D64550", AMARELO]
    n = len(cores)
    bw = (w - 24) / n
    b = []
    for i, c in enumerate(cores):
        hh = 18 + (i * 37 % 50)
        b.append(f'<g class="eq" style="animation-delay:{i * .17:.2f}s"><rect x="{x + 12 + i * bw:.1f}" y="{y + h - 10 - hh}" '
                 f'width="{bw * .7:.1f}" height="{hh}" rx="2" fill="{c}" opacity=".9"/></g>')
    b.append(f'<path d="M{x + 10} {y + h - 9}H{x + w - 10}" stroke="{C["line2"]}"/>')
    return "".join(b)


def _engrenagem(cx, cy, r, dentes, cor, classe):
    pts = []
    for k in range(dentes * 2):
        ang = math.pi * k / dentes
        rr = r if k % 2 == 0 else r * .78
        for d in (-.18, .18):
            a = ang + d * math.pi / dentes
            pts.append(f"{cx + rr * math.cos(a):.1f},{cy + rr * math.sin(a):.1f}")
    return (f'<g class="{classe}"><polygon points="{" ".join(pts)}" fill="{C["chrome"]}" stroke="{cor}" stroke-width="2"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r * .32:.1f}" fill="{C["page"]}" stroke="{cor}" stroke-width="2"/></g>')


def deco_engrenagens(x, y, w, h, cor):
    return (_engrenagem(x + w * .30, y + h * .52, 30, 10, cor, "spin") +
            _engrenagem(x + w * .30 + 50, y + h * .52 - 16, 19, 8, AMARELO, "spinr") +
            f'<text x="{x + w * .62:.1f}" y="{y + h * .42:.1f}" font-size="12" font-weight="700" fill="{C["text"]}">SAP GUI</text>'
            f'<text x="{x + w * .62:.1f}" y="{y + h * .42 + 17:.1f}" font-size="10.5" fill="{C["muted"]}">robô em execução</text>'
            f'<circle cx="{x + w * .62 - 9:.1f}" cy="{y + h * .42 - 4:.1f}" r="3.5" fill="#1AAB40" class="pulse"/>')


def deco_play(x, y, w, h, cor):
    cx, cy = x + 46, y + h / 2
    b = [f'<circle cx="{cx}" cy="{cy}" r="26" fill="none" stroke="{cor}" stroke-width="2" class="breath"/>',
         f'<g class="pop"><circle cx="{cx}" cy="{cy}" r="19" fill="{cor}"/>'
         f'<path d="M{cx - 6} {cy - 9}l15 9-15 9z" fill="#201F1E"/></g>']
    for i in range(9):
        hh = 12 + (i * 23 % 40)
        b.append(f'<g class="eq" style="animation-delay:{i * .21:.2f}s"><rect x="{x + 96 + i * 24}" y="{y + h - 10 - hh}" '
                 f'width="15" height="{hh}" rx="2" fill="{[cor, AMARELO, AZUL][i % 3]}" opacity=".9"/></g>')
    return "".join(b)


def deco_progresso(x, y, w, h, cor):
    return (f'<rect x="{x + 8}" y="{y + h / 2 - 7}" width="{w - 16}" height="14" rx="7" fill="{C["card2"]}"/>'
            f'<rect x="{x + 8}" y="{y + h / 2 - 7}" width="{w - 16}" height="14" rx="7" fill="{cor}" class="fill"/>'
            f'<text x="{x + w - 8}" y="{y + h / 2 - 14}" font-size="11" font-weight="700" fill="{C["text"]}" text-anchor="end">100%</text>'
            f'<text x="{x + 8}" y="{y + h / 2 - 14}" font-size="10.5" fill="{C["muted"]}">10 rodadas</text>')


def deco_planilha(x, y, w, h, cor):
    cols, rows = 7, 4
    cw, ch = (w - 16) / cols, (h - 16) / rows
    b = []
    for r in range(rows):
        for c in range(cols):
            fill = C["line"] if r == 0 else cor
            b.append(f'<rect x="{x + 8 + c * cw:.1f}" y="{y + 8 + r * ch:.1f}" width="{cw - 3:.1f}" height="{ch - 3:.1f}" rx="2" '
                     f'fill="{fill}" class="cell" style="animation-delay:{(r * cols + c) * .09:.2f}s"/>')
    return "".join(b)


DECOS = {"forecast": deco_forecast, "pipeline": deco_pipeline, "riscos": deco_riscos, "engrenagens": deco_engrenagens,
         "play": deco_play, "progresso": deco_progresso, "planilha": deco_planilha}


def _defs(cor):
    return (f'<radialGradient id="glow" cx="0" cy="0" r="1"><stop offset="0" stop-color="{cor}" stop-opacity=".30"/>'
            f'<stop offset="1" stop-color="{cor}" stop-opacity="0"/></radialGradient>'
            f'<linearGradient id="sweepg" x1="0" x2="1"><stop offset="0" stop-color="{cor}" stop-opacity="0"/>'
            f'<stop offset=".5" stop-color="{cor}"/><stop offset="1" stop-color="{cor}" stop-opacity="0"/></linearGradient>')


def _titulo(x, y, titulo, size, cor):
    if ":" in titulo:
        a, b = titulo.split(":", 1)
        return (f'<text x="{x}" y="{y}" font-size="{size:.1f}" font-weight="800" fill="{C["text"]}">{e(a)}:'
                f'<tspan fill="{cor}">{e(b)}</tspan></text>')
    return f'<text x="{x}" y="{y}" font-size="{size:.1f}" font-weight="800" fill="{C["text"]}">{e(titulo)}</text>'


def _kpis(x, y, w, h, kpis, cor, gap=8, vsize=22):
    out = []
    kw = (w - gap * (len(kpis) - 1)) / len(kpis)
    for i, (v, l) in enumerate(kpis):
        kx = x + i * (kw + gap)
        vs = _ajusta(v, vsize, kw - 20)
        out.append(f'<g class="up" style="animation-delay:{.5 + i * .15:.2f}s">'
                   f'<rect x="{kx:.1f}" y="{y}" width="{kw:.1f}" height="{h}" rx="6" fill="{C["chrome"]}" stroke="{C["line"]}"/>'
                   f'<rect x="{kx:.1f}" y="{y}" width="{kw:.1f}" height="2.5" rx="1.2" fill="{cor}"/>'
                   f'<text x="{kx + 12:.1f}" y="{y + h * .52:.1f}" font-size="{vs:.1f}" font-weight="800" fill="{C["text"]}">{e(v)}</text>'
                   f'<text x="{kx + 12:.1f}" y="{y + h * .52 + 17:.1f}" font-size="10.5" fill="{C["muted"]}">{e(l)}</text></g>')
    return "".join(out)


def _moldura(W, H, cor, idx, categoria, tile=66, x0=28, y0=28):
    return [f'<clipPath id="c"><rect width="{W}" height="{H}" rx="12"/></clipPath><g clip-path="url(#c)">',
            f'<rect width="{W}" height="{H}" fill="{C["page"]}"/>',
            f'<circle cx="0" cy="0" r="{W * .45:.0f}" fill="url(#glow)" class="breath"/>',
            f'<rect width="{W}" height="3" fill="{cor}" opacity=".9"/>',
            f'<rect class="sweep" x="0" y="{H - 3}" width="300" height="3" fill="url(#sweepg)"/>',
            f'<rect x="{x0}" y="{y0}" width="{tile}" height="{tile}" rx="12" fill="{C["chrome"]}" stroke="{cor}" stroke-opacity=".75"/>',
            f'<rect x="{x0 - 4}" y="{y0 - 4}" width="{tile + 8}" height="{tile + 8}" rx="15" fill="none" stroke="{cor}" '
            f'stroke-opacity=".5" class="breath"/>',
            f'<text x="{x0 + tile / 2}" y="{y0 + tile / 2 + tile * .16:.1f}" font-size="{tile * .4:.0f}" font-weight="800" '
            f'fill="{cor}" text-anchor="middle" class="mono">{idx:02d}</text>']


def _categoria(x, y, texto, cor):
    w = text_w(texto, 11, True) * 1.18 + 34
    return (f'<rect x="{x}" y="{y}" width="{w:.0f}" height="24" rx="12" fill="{cor}" fill-opacity=".14" stroke="{cor}" stroke-opacity=".55"/>'
            f'<circle cx="{x + 13}" cy="{y + 12}" r="4" fill="{cor}" class="pulse"/>'
            f'<text x="{x + 24}" y="{y + 16}" font-size="11" font-weight="700" fill="{cor}" letter-spacing="1.6">{e(texto)}</text>')


def banner(idx, categoria, titulo, sub, chips, kpis, deco, cor):
    W, H = 1200, 214
    b = _moldura(W, H, cor, idx, categoria)
    b.append(f'<g class="up">{_categoria(116, 30, categoria, cor)}</g>')
    b.append(f'<g class="up" style="animation-delay:.15s">{_titulo(116, 92, titulo, _ajusta(titulo, 30, 690), cor)}</g>')
    b.append(f'<text x="116" y="122" font-size="{_ajusta(sub, 14.5, 690, False):.1f}" fill="{C["text2"]}" class="fade" '
             f'style="animation-delay:.3s">{e(sub)}</text>')
    x = 116
    for i, t in enumerate(chips):
        c, w = _chip(x, 146, t, cor)
        if x + w > 812:
            break
        b.append(f'<g class="float" style="animation-delay:{i * .4:.1f}s">{c}</g>')
        x += w + 7
    b.append(f'<rect x="836" y="24" width="336" height="92" rx="8" fill="{C["chrome"]}" stroke="{C["line"]}"/>')
    b.append(DECOS[deco](836, 24, 336, 92, cor))
    b.append(_kpis(836, 126, 336, 62, kpis, cor))
    b.append('</g>')
    b.append(f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="12" fill="none" stroke="{C["line"]}"/>')
    return svg(W, H, "\n".join(b), f"Projeto {idx:02d} · {categoria} · {titulo}: {sub}", css=CSS, defs=_defs(cor))


def banner_meio(idx, categoria, titulo, sub, kpis, deco, cor):
    W, H = 600, 236
    b = _moldura(W, H, cor, idx, categoria, tile=56, x0=24, y0=24)
    b.append(f'<g class="up">{_categoria(96, 24, categoria, cor)}</g>')
    b.append(f'<g class="up" style="animation-delay:.15s">{_titulo(96, 74, titulo, _ajusta(titulo, 23, 360), cor)}</g>')
    for i, linha in enumerate(_quebra(sub, 13, 552)[:2]):
        b.append(f'<text x="24" y="{108 + i * 19}" font-size="13" fill="{C["text2"]}" class="fade" '
                 f'style="animation-delay:.3s">{e(linha)}</text>')
    b.append(f'<rect x="468" y="20" width="110" height="62" rx="8" fill="{C["chrome"]}" stroke="{C["line"]}"/>')
    b.append(DECOS[deco](468, 20, 110, 62, cor))
    b.append(_kpis(24, 152, 552, 60, kpis, cor, vsize=21))
    b.append('</g>')
    b.append(f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="12" fill="none" stroke="{C["line"]}"/>')
    return svg(W, H, "\n".join(b), f"Projeto {idx:02d} · {categoria} · {titulo}: {sub}", css=CSS, defs=_defs(cor))


def ticker():
    itens = ["Python", "SQL", "Estatística", "Machine Learning", "XGBoost", "SARIMA", "Power BI", "DAX", "Power Query",
             "Pentaho PDI", "Oracle SQL", "PostgreSQL", "MySQL", "DuckDB", "pandas", "scikit-learn", "statsmodels",
             "Streamlit", "SAP GUI Scripting", "VBA", "Playwright", "Java", "C#", ".NET", "HTML", "CSS", "JavaScript",
             "Docker", "AWS", "GitHub Actions"]
    cores = [AMARELO, AZUL, LARANJA, ROXO, ROSA, VERDE, CIANO]
    W, H = 1200, 52
    partes, x = [], 0.0
    for i, t in enumerate(itens):
        w = text_w(t, 13.5, True) + 40
        cor = cores[i % len(cores)]
        partes.append(f'<rect x="{x:.1f}" y="10" width="{w:.1f}" height="32" rx="16" fill="{C["chrome"]}" stroke="{C["line2"]}"/>'
                      f'<circle cx="{x + 16:.1f}" cy="26" r="4" fill="{cor}"/>'
                      f'<text x="{x + 26:.1f}" y="30.7" font-size="13.5" font-weight="600" fill="{C["text"]}">{e(t)}</text>')
        x += w + 10
    um = "".join(partes)
    b = [f'<clipPath id="c"><rect width="{W}" height="{H}" rx="10"/></clipPath><g clip-path="url(#c)">',
         f'<rect width="{W}" height="{H}" fill="{C["page"]}"/>',
         f'<g class="ticker" style="--w:-{x:.1f}px;--d:{x / 45:.0f}s"><g>{um}</g><g transform="translate({x:.1f} 0)">{um}</g></g>',
         f'<rect width="90" height="{H}" fill="url(#fadeL)"/><rect x="{W - 90}" width="90" height="{H}" fill="url(#fadeR)"/>',
         '</g>',
         f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="10" fill="none" stroke="{C["line"]}"/>']
    defs = (f'<linearGradient id="fadeL" x1="0" x2="1"><stop offset="0" stop-color="{C["page"]}"/>'
            f'<stop offset="1" stop-color="{C["page"]}" stop-opacity="0"/></linearGradient>'
            f'<linearGradient id="fadeR" x1="0" x2="1"><stop offset="0" stop-color="{C["page"]}" stop-opacity="0"/>'
            f'<stop offset="1" stop-color="{C["page"]}"/></linearGradient>')
    return svg(W, H, "\n".join(b), "Stack: " + ", ".join(itens), css=CSS, defs=defs)


# ------------------------------------------------------------------ hackathons
def hackathon_2026():
    W, H = 1200, 330
    OURO, PRATA, BRONZE = "#F2C811", "#C9CED6", "#D08A4E"
    b = [f'<clipPath id="c"><rect width="{W}" height="{H}" rx="12"/></clipPath><g clip-path="url(#c)">',
         f'<rect width="{W}" height="{H}" fill="{C["page"]}"/>',
         f'<circle cx="150" cy="165" r="420" fill="url(#glow)" class="breath"/>',
         f'<rect width="{W}" height="3" fill="url(#pbi)"/>',
         f'<rect class="sweep" x="0" y="{H - 3}" width="300" height="3" fill="url(#sweepg)"/>']
    # medalha com raios girando
    raios = "".join(f'<path d="M150 165 L{150 + 125 * math.cos(math.radians(a - 4)):.1f} {165 + 125 * math.sin(math.radians(a - 4)):.1f} '
                    f'L{150 + 125 * math.cos(math.radians(a + 4)):.1f} {165 + 125 * math.sin(math.radians(a + 4)):.1f}Z" '
                    f'fill="{OURO}" opacity=".10"/>' for a in range(0, 360, 20))
    b.append(f'<g class="spin" style="animation-duration:24s">{raios}</g>')
    b.append(f'<circle cx="150" cy="165" r="92" fill="none" stroke="{OURO}" stroke-width="2" stroke-dasharray="4 7" class="spinr" '
             f'style="animation-duration:30s"/>')
    b.append(f'<g class="pop" style="animation-duration:3.2s"><circle cx="150" cy="165" r="76" fill="url(#medalha)"/>'
             f'<circle cx="150" cy="165" r="62" fill="#2A2210" stroke="{OURO}" stroke-width="2.5"/>'
             f'<text x="150" y="186" font-size="62" font-weight="800" fill="{OURO}" text-anchor="middle">4º</text>'
             f'<text x="150" y="212" font-size="11" font-weight="700" fill="{OURO}" text-anchor="middle" letter-spacing="3">LUGAR</text></g>')
    for i, (dx, dy) in enumerate([(-70, -80), (78, -64), (-84, 60), (86, 74), (0, -112)]):
        b.append(f'<circle cx="{150 + dx}" cy="{165 + dy}" r="2.6" fill="{OURO}" class="pulse" style="animation-delay:{i * .4:.1f}s"/>')
    # texto central
    x0 = 300
    b.append(f'<g class="up">{_categoria(x0, 36, "HACKATHON DE IA · 2026", OURO)}</g>')
    b.append(f'<g class="up" style="animation-delay:.15s">{_titulo(x0, 98, "HackaEmb 2026: 4º lugar entre 14 times", _ajusta("HackaEmb 2026: 4º lugar entre 14 times", 32, 515), OURO)}</g>')
    b.append(f'<text x="{x0}" y="130" font-size="13.5" fill="{C["text2"]}" class="fade" style="animation-delay:.3s">'
             f'5 dias de maratona · cerca de 140 colaboradores · 14 equipes multidisciplinares</text>')
    b.append(f'<g class="up" style="animation-delay:.45s">'
             f'<rect x="{x0}" y="152" width="510" height="108" rx="8" fill="{C["chrome"]}" stroke="{C["line"]}"/>'
             f'<rect x="{x0}" y="152" width="4" height="108" rx="2" fill="{OURO}"/>'
             f'<text x="{x0 + 20}" y="180" font-size="16" font-weight="800" fill="{C["text"]}">ConformAI'
             f'<tspan font-size="12.5" font-weight="400" fill="{C["muted"]}">  ·  time PacNine</tspan></text>'
             f'<text x="{x0 + 20}" y="204" font-size="13" fill="{C["text2"]}">Orienta o registro de não conformidades: visão computacional</text>'
             f'<text x="{x0 + 20}" y="222" font-size="13" fill="{C["text2"]}">avalia as fotos e a IA sugere os campos obrigatórios.</text>'
             f'<text x="{x0 + 20}" y="246" font-size="13" fill="{C["text"]}"><tspan fill="{OURO}" font-weight="700">Meu papel:</tspan>'
             f' dados e integração da IA com documentos (RAG)</text></g>')
    x = x0
    for i, t in enumerate(["Visão computacional", "RAG", "IA", "Pitch para banca"]):
        c, w = _chip(x, 278, t, OURO)
        b.append(f'<g class="float" style="animation-delay:{i * .5:.1f}s">{c}</g>')
        x += w + 7
    # painel de classificação
    px, py, pw, ph = 842, 30, 330, 270
    b.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="10" fill="{C["chrome"]}" stroke="{C["line"]}"/>')
    b.append(f'<text x="{px + 18}" y="{py + 30}" font-size="14" font-weight="700" fill="{C["text"]}">Classificação final</text>'
             f'<text x="{px + 18}" y="{py + 48}" font-size="11" fill="{C["muted"]}">14 times · avaliação da banca</text>')
    for k in range(14):
        col, lin = k % 7, k // 7
        cx, cy = px + 34 + col * 44, py + 84 + lin * 60
        cor = {0: OURO, 1: PRATA, 2: BRONZE}.get(k, C["line2"])
        if k == 3:
            b.append(f'<circle cx="{cx}" cy="{cy}" r="21" fill="none" stroke="{OURO}" stroke-width="2" class="breath"/>'
                     f'<circle cx="{cx}" cy="{cy}" r="16" fill="{OURO}" class="pop"/>'
                     f'<text x="{cx}" y="{cy + 5}" font-size="13" font-weight="800" fill="#201F1E" text-anchor="middle">4</text>')
        else:
            b.append(f'<g class="fade" style="animation-delay:{.2 + k * .06:.2f}s"><circle cx="{cx}" cy="{cy}" r="15" fill="{cor}" '
                     f'opacity="{1 if k < 3 else .55}"/><text x="{cx}" y="{cy + 4.5}" font-size="12" font-weight="700" '
                     f'fill="{"#201F1E" if k < 3 else C["muted"]}" text-anchor="middle">{k + 1}</text></g>')
    b.append(f'<text x="{px + 166}" y="{py + 117}" font-size="11" fill="{OURO}" text-anchor="middle" font-weight="700">'
             f'▲ PacNine</text>')
    gy = py + 206
    b.append(f'<text x="{px + 18}" y="{gy}" font-size="12" fill="{C["muted"]}">colocação</text>'
             f'<text x="{px + pw - 18}" y="{gy}" font-size="20" font-weight="800" fill="{C["text"]}" text-anchor="end">4º de 14</text>')
    seg = (pw - 36 - 13 * 3) / 14
    for k in range(14):
        cor = {0: OURO, 1: PRATA, 2: BRONZE, 3: OURO}.get(k, C["card2"])
        b.append(f'<rect x="{px + 18 + k * (seg + 3):.1f}" y="{gy + 12}" width="{seg:.1f}" height="12" rx="3" fill="{cor}" '
                 f'opacity="{1 if k < 4 else .9}" class="cell" style="animation-delay:{k * .12:.2f}s"/>')
    b.append(f'<text x="{px + pw - 18}" y="{gy + 46}" font-size="11" fill="{C["muted"]}" text-anchor="end">'
             f'top 4 · <tspan fill="{OURO}" font-weight="700">quase no pódio</tspan></text>')
    b.append('</g>')
    b.append(f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="12" fill="none" stroke="{C["line"]}"/>')
    defs = _defs(OURO) + (f'<radialGradient id="medalha"><stop offset="0" stop-color="#FFE27A"/>'
                          f'<stop offset="1" stop-color="#C67A0A"/></radialGradient>')
    return svg(W, H, "\n".join(b), "HackaEmb 2026: 4º lugar entre 14 times com o ConformAI, time PacNine",
               css=CSS, defs=defs)


def _foto_b64(caminho, largura, altura):
    from carousel import jpeg_b64
    return jpeg_b64(Path(caminho), largura, altura)


FOTO_CSS = ".kb{transform-box:fill-box;transform-origin:50% 45%;animation:kb 18s ease-in-out infinite alternate;}" \
           "@keyframes kb{from{transform:scale(1)}to{transform:scale(1.07) translate(-1%,1%)}}"


def foto_2026(caminho):
    W, iw = 1200, 1176
    ih = round(iw * 591 / 1052)
    H = ih + 24
    OURO = "#F2C811"
    d = _foto_b64(caminho, round(iw * 1.15), round(ih * 1.15))
    b = [f'<clipPath id="ft"><rect x="12" y="12" width="{iw}" height="{ih}" rx="10"/></clipPath>',
         f'<rect width="{W}" height="{H}" rx="14" fill="{C["page"]}"/>',
         f'<g clip-path="url(#ft)"><image class="kb" x="12" y="12" width="{iw}" height="{ih}" href="data:image/jpeg;base64,{d}"/>'
         f'<rect x="12" y="{12 + ih - 150}" width="{iw}" height="150" fill="url(#sombra)"/>'
         f'<rect class="sweep" x="12" y="12" width="260" height="{ih}" fill="url(#brilho)" opacity=".12"/></g>',
         f'<g class="up" style="animation-delay:.3s">'
         f'<text x="44" y="{ih - 46}" font-size="30" font-weight="800" fill="#FFFFFF">Time PacNine</text>'
         f'<text x="44" y="{ih - 18}" font-size="15" fill="#E6E6E6">HackaEmb 2026 · ConformAI · 5 dias de maratona</text></g>',
         f'<g class="pop" style="animation-duration:3s"><rect x="{W - 252}" y="{ih - 86}" width="208" height="56" rx="28" '
         f'fill="#1B1A19" fill-opacity=".85" stroke="{OURO}" stroke-width="2"/>'
         f'<circle cx="{W - 220}" cy="{ih - 58}" r="17" fill="url(#medalha)"/>'
         f'<text x="{W - 220}" y="{ih - 52}" font-size="15" font-weight="800" fill="#2A2210" text-anchor="middle">4º</text>'
         f'<text x="{W - 193}" y="{ih - 61}" font-size="15" font-weight="800" fill="{OURO}">4º LUGAR</text>'
         f'<text x="{W - 193}" y="{ih - 43}" font-size="11.5" fill="#E6E6E6">entre 14 times</text></g>',
         f'<rect x="12" y="12" width="{iw}" height="{ih}" rx="10" fill="none" stroke="{OURO}" stroke-opacity=".55" '
         f'stroke-width="2" class="breath"/>']
    defs = ('<linearGradient id="sombra" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity="0"/>'
            '<stop offset="1" stop-color="#000" stop-opacity=".78"/></linearGradient>'
            '<linearGradient id="brilho" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
            '<stop offset=".5" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
            '<radialGradient id="medalha"><stop offset="0" stop-color="#FFE27A"/><stop offset="1" stop-color="#C67A0A"/></radialGradient>')
    return svg(W, H, "\n".join(b), "Foto do time PacNine no HackaEmb 2026, 4º lugar entre 14 times", css=CSS + FOTO_CSS, defs=defs)


def hackathon_2025(caminho):
    W, H = 1200, 430
    cor = AZUL
    fw, fh = 540, 404
    d = _foto_b64(caminho, round(fw * 1.4), round(fh * 1.4))
    b = [f'<clipPath id="c"><rect width="{W}" height="{H}" rx="12"/></clipPath><g clip-path="url(#c)">',
         f'<rect width="{W}" height="{H}" fill="{C["page"]}"/>',
         f'<circle cx="{W}" cy="0" r="520" fill="url(#glow)" class="breath"/>',
         f'<rect width="{W}" height="3" fill="{cor}"/>',
         f'<rect class="sweep" x="0" y="{H - 3}" width="300" height="3" fill="url(#sweepg)"/>',
         f'<clipPath id="ft"><rect x="13" y="13" width="{fw}" height="{fh}" rx="10"/></clipPath>',
         f'<g clip-path="url(#ft)"><image class="kb" x="13" y="13" width="{fw}" height="{fh}" href="data:image/jpeg;base64,{d}"/>'
         f'<rect x="13" y="{13 + fh - 90}" width="{fw}" height="90" fill="url(#sombra)"/></g>',
         f'<text x="34" y="{fh - 14}" font-size="20" font-weight="800" fill="#FFFFFF" class="up">Time Kai7en</text>',
         f'<rect x="13" y="13" width="{fw}" height="{fh}" rx="10" fill="none" stroke="{cor}" stroke-opacity=".6" stroke-width="2" class="breath"/>']
    x0 = 590
    b.append(f'<g class="up">{_categoria(x0, 30, "HACKATHON DE IA · 2025", cor)}</g>')
    b.append(f'<text x="{x0}" y="100" font-size="34" font-weight="800" fill="{C["text"]}" class="up" style="animation-delay:.1s">HackaEmb 2025</text>')
    b.append(f'<text x="{x0}" y="136" font-size="22" font-weight="800" fill="{cor}" class="up" style="animation-delay:.2s">'
             f'Agentes de IA para Simplificação</text>')
    for i, linha in enumerate(_quebra("Minha primeira competição de programação: no time Kai7en, pensamos em como a "
                                      "tecnologia pode simplificar processos complexos do dia a dia, deixando as rotinas "
                                      "mais intuitivas e democratizando o conhecimento.", 14, 580)):
        b.append(f'<text x="{x0}" y="{172 + i * 21}" font-size="14" fill="{C["text2"]}" class="fade" style="animation-delay:.35s">{e(linha)}</text>')
    b.append(_kpis(x0, 262, 586, 62, [("1ª", "participação"), ("40 h", "de maratona"), ("5", "dias · 15 a 19/09")], cor))
    x = x0
    for i, t in enumerate(["Agentes de IA", "Trabalho em equipe", "Pitch", "Innovation Month"]):
        c, w = _chip(x, 346, t, cor)
        b.append(f'<g class="float" style="animation-delay:{i * .5:.1f}s">{c}</g>')
        x += w + 7
    b.append('</g>')
    b.append(f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="12" fill="none" stroke="{C["line"]}"/>')
    defs = _defs(cor) + ('<linearGradient id="sombra" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity="0"/>'
                         '<stop offset="1" stop-color="#000" stop-opacity=".75"/></linearGradient>')
    return svg(W, H, "\n".join(b), "HackaEmb 2025, Agentes de IA para Simplificação: primeira participação, time Kai7en, "
                                  "5 dias e 40 horas de maratona", css=CSS + FOTO_CSS, defs=defs)


PROJETOS = {
    "01-previsao-inflacao": banner(
        1, "CIÊNCIA DE DADOS · ESTATÍSTICA", "Previsão de Inflação: Estatística vs. Machine Learning",
        "22 anos de IPCA, testes de hipótese e 6 modelos disputando um backtest fora da amostra",
        ["Python", "statsmodels", "SciPy", "scikit-learn", "XGBoost", "pytest"],
        [("6", "modelos"), ("36", "meses de backtest"), ("IC 95%", "na previsão")], "forecast", AZUL),
    "02-pipeline-bcb": banner(
        2, "ENGENHARIA DE DADOS · ETL", "Do Banco Central ao Dashboard: Pipeline ETL",
        "API oficial → modelo estrela no DuckDB → checagens de qualidade → painel no estilo Power BI",
        ["Python", "SQL", "DuckDB", "pandas", "Streamlit", "GitHub Actions"],
        [("6", "séries oficiais"), ("852", "linhas no fato"), ("19 s", "pipeline completo")], "pipeline", AMARELO),
    "03-epidemiological-forecaster": banner(
        3, "MACHINE LEARNING · TCC NOTA 10", "Epidemiological Forecaster: Dengue Bairro a Bairro",
        "4 modelos XGBoost preveem o risco de 1 a 4 semanas à frente nos 94 bairros do Recife",
        ["Python", "XGBoost", "PostgreSQL", "FastAPI", "Streamlit", "Plotly"],
        [("10", "nota do TCC"), ("> 85%", "F1-Macro (1 semana)"), ("> 95%", "acurácia (1 semana)")], "riscos", LARANJA),
    "04-rpa-sap": banner(
        4, "RPA · EM PRODUÇÃO", "Robôs Corporativos: SAP no Piloto Automático",
        "Python e VBA operando SAP GUI, Outlook, OCR de PDFs e Oracle SQL nas rotinas de Supply Chain",
        ["SAP GUI Scripting", "Python", "VBA", "Oracle SQL", "OCR", "HTML/CSS/JS"],
        [("SAP", "GUI Scripting"), ("OCR", "de PDFs"), ("E-mail", "automático")], "engrenagens", ROXO),
    "05-auto-videos": banner(
        5, "AUTOMAÇÃO + DADOS", "auto-videos: Fábrica de Vídeos Guiada por KPIs",
        "Roteiro, narração e render no GitHub Actions; a Central de KPIs escolhe os próximos temas",
        ["Python", "ffmpeg", "SQLite", "Streamlit", "YouTube API", "GitHub Actions"],
        [("4", "canais no YouTube"), ("467", "vídeos publicados"), ("6 h", "coleta de KPIs")], "play", ROSA),
    "06-rpa-challenge": banner_meio(
        6, "RPA · DESAFIO", "RPA Challenge: 70 Campos em 0,7 s",
        "Playwright e openpyxl preenchendo 10 formulários cujos campos mudam de lugar a cada envio",
        [("100%", "de acerto"), ("70/70", "campos"), ("0,7 s", "execução")], "progresso", VERDE),
    "07-robo-catalogo": banner_meio(
        7, "RPA · RELATÓRIOS", "Robô de Catálogo: do Site ao Excel",
        "Navega 50 categorias, consolida 1.000 itens e entrega Excel com gráficos nativos e e-mail",
        [("1.000", "itens"), ("50", "categorias"), ("24 s", "ponta a ponta")], "planilha", CIANO),
}


def main():
    (OUT / "banners").mkdir(parents=True, exist_ok=True)
    for nome, conteudo in PROJETOS.items():
        (OUT / "banners" / f"{nome}.svg").write_text(conteudo, encoding="utf-8")
        print("ok", nome)
    (OUT / "ticker.svg").write_text(ticker(), encoding="utf-8")
    (OUT / "banners" / "hackaemb-2026.svg").write_text(hackathon_2026(), encoding="utf-8")
    fotos = Path(__file__).resolve().parent.parent / "fotos"
    if (fotos / "time-2026.jpg").exists():
        (OUT / "banners" / "hackaemb-2026-foto.svg").write_text(foto_2026(fotos / "time-2026.jpg"), encoding="utf-8")
        (OUT / "banners" / "hackaemb-2025.svg").write_text(hackathon_2025(fotos / "time-2025.jpg"), encoding="utf-8")
    print("ok ticker")


if __name__ == "__main__":
    main()
