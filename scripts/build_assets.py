"""Gera os SVGs estáticos do perfil (cabeçalho, abas, seções, DAX, matriz de stack, rodapé).

Uso: python scripts/build_assets.py   (escreve em assets/)
"""
from pathlib import Path

from theme import C, DATA, chip, e, logo, svg, text_w, visual_icons

OUT = Path(__file__).resolve().parent.parent / "assets"

PAGES = [("sobre", "Sobre"), ("hackathons", "Hackathons"), ("stack", "Stack"), ("dados", "Dados & ML"), ("rpa", "Automação & RPA"),
         ("metricas", "Métricas"), ("contato", "Contato")]

LOOP_CSS = """
  .eq{transform-box:fill-box;transform-origin:50% 100%;animation:eq 2.6s ease-in-out infinite alternate;}
  @keyframes eq{0%{transform:scaleY(1)}35%{transform:scaleY(.55)}70%{transform:scaleY(1.08)}100%{transform:scaleY(.8)}}
  .breath{animation:breath 3.2s ease-in-out infinite;}
  @keyframes breath{0%,100%{opacity:.55}50%{opacity:1}}
  .caret{animation:caret 1s steps(1) infinite;}
  @keyframes caret{50%{opacity:0}}
  .float{animation:float 5s ease-in-out infinite;}
  @keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-3px)}}
  .shine{transform-box:fill-box;animation:shine 3.6s ease-in-out infinite;}
  @keyframes shine{0%{transform:translateX(-120%)}60%,100%{transform:translateX(320%)}}
"""


# ------------------------------------------------------------------ cabeçalho
def header():
    W, H = 1200, 560
    b = []
    b.append(f'<clipPath id="win"><rect width="{W}" height="{H}" rx="12"/></clipPath>')
    b.append('<g clip-path="url(#win)">')
    b.append(f'<rect width="{W}" height="{H}" fill="{C["bg"]}"/>')

    # barra de título
    b.append(f'<rect width="{W}" height="72" fill="{C["chrome"]}"/>')
    b.append(logo(18, 13))
    b.append(f'<text x="48" y="26" font-size="13" fill="{C["text"]}" font-weight="600">rayrafaneli.pbix'
             f'<tspan fill="{C["muted"]}" font-weight="400"> — Relatório de perfil</tspan></text>')
    b.append(f'<rect x="470" y="8" width="260" height="24" rx="4" fill="{C["bg"]}" stroke="{C["line"]}"/>'
             f'<circle cx="486" cy="19" r="4.5" fill="none" stroke="{C["muted"]}" stroke-width="1.4"/>'
             f'<path d="M489.5 22.5l3.5 3.5" stroke="{C["muted"]}" stroke-width="1.4" stroke-linecap="round"/>'
             f'<text x="500" y="24.5" font-size="12" fill="{C["dim"]}">Pesquisar</text>')
    b.append(f'<g stroke="{C["muted"]}" stroke-width="1.3" fill="none">'
             f'<path d="M1084 20h11"/><rect x="1124" y="14" width="11" height="11"/>'
             f'<path d="M1164 14l11 11M1175 14l-11 11"/></g>')

    # faixa de abas da faixa de opções
    tabs = [("Arquivo", 20), ("Página Inicial", 84), ("Inserir", 190), ("Modelagem", 250),
            ("Exibir", 338), ("Otimizar", 394), ("Ajuda", 466)]
    for name, x in tabs:
        active = name == "Página Inicial"
        b.append(f'<text x="{x}" y="60" font-size="12.5" fill="{C["text"] if active else C["muted"]}"'
                 f'{" font-weight=" + chr(34) + "600" + chr(34) if active else ""}>{e(name)}</text>')
    b.append(f'<rect x="84" y="67" width="{text_w("Página Inicial", 12.5, True):.0f}" height="3" rx="1.5" fill="{C["yellow"]}"/>')
    b.append(f'<rect x="1074" y="41" width="112" height="30" rx="7" fill="none" stroke="{C["yellow"]}" stroke-width="1.5" class="breath"/>'
             f'<rect x="1078" y="45" width="104" height="22" rx="4" fill="url(#pbi)"/>'
             f'<path d="M1093 61v-8m-3.5 3.5L1093 53l3.5 3.5M1088 63h10" stroke="#201F1E" stroke-width="1.5" fill="none" '
             f'stroke-linecap="round" stroke-linejoin="round"/>'
             f'<text x="1106" y="60.5" font-size="12" font-weight="700" fill="#201F1E">Publicar</text>')
    b.append(f'<rect y="72" width="{W}" height="1" fill="{C["line"]}"/>')

    # trilho esquerdo (Relatório, Tabela, Modelo, DAX)
    b.append(f'<rect y="73" width="48" height="447" fill="{C["chrome"]}"/>'
             f'<rect x="48" y="73" width="1" height="447" fill="{C["line"]}"/>')
    b.append(f'<rect x="0" y="86" width="48" height="34" fill="{C["card2"]}"/><rect x="0" y="86" width="3" height="34" fill="{C["yellow"]}"/>')
    m = C["muted"]
    b.append(f'<g fill="{C["text"]}"><rect x="15" y="105" width="4" height="8"/><rect x="22" y="99" width="4" height="14"/>'
             f'<rect x="29" y="94" width="4" height="19"/></g>')
    b.append(f'<g fill="none" stroke="{m}" stroke-width="1.4"><rect x="15" y="134" width="18" height="16"/>'
             f'<path d="M15 140h18M15 145h18M21 134v16"/>'
             f'<rect x="14" y="173" width="7" height="6"/><rect x="27" y="173" width="7" height="6"/><rect x="20" y="186" width="7" height="6"/>'
             f'<path d="M21 176h6M24 179v7"/></g>')
    b.append(f'<text x="24" y="232" font-size="12" font-weight="700" fill="{m}" text-anchor="middle" class="mono">DAX</text>')

    # painel de filtros (direita)
    px = 990
    b.append(f'<rect x="{px}" y="73" width="210" height="447" fill="{C["chrome"]}"/>'
             f'<rect x="{px}" y="73" width="1" height="447" fill="{C["line"]}"/>')
    b.append(f'<text x="{px + 16}" y="100" font-size="14" font-weight="700" fill="{C["text"]}">Filtros</text>'
             f'<path d="M{px + 180} 92l5 5-5 5M{px + 186} 92l5 5-5 5" stroke="{m}" stroke-width="1.3" fill="none"/>')
    b.append(f'<rect x="{px + 14}" y="114" width="182" height="26" rx="4" fill="{C["bg"]}" stroke="{C["line2"]}"/>'
             f'<circle cx="{px + 28}" cy="126" r="4.5" fill="none" stroke="{m}" stroke-width="1.3"/>'
             f'<path d="M{px + 31.5} 129.5l3.5 3.5" stroke="{m}" stroke-width="1.3" stroke-linecap="round"/>'
             f'<text x="{px + 42}" y="131" font-size="11.5" fill="{C["dim"]}">Pesquisar</text>')
    b.append(f'<text x="{px + 16}" y="166" font-size="11" fill="{m}">Filtros nesta página</text>')
    b.append(f'<rect x="{px + 14}" y="176" width="182" height="146" rx="4" fill="{C["card2"]}"/>'
             f'<text x="{px + 26}" y="198" font-size="12" font-weight="700" fill="{C["text"]}">Foco de atuação</text>')
    focos = ["Engenharia de dados", "Ciência de dados", "Business Intelligence", "Automação (RPA)"]
    for i, f in enumerate(focos):
        y = 214 + i * 24
        b.append(f'<g class="fade" style="animation-delay:{1.6 + i * .15:.2f}s">'
                 f'<rect x="{px + 26}" y="{y}" width="13" height="13" rx="2.5" fill="{C["yellow"]}"/>'
                 f'<path d="M{px + 29} {y + 6.8}l2.6 2.6 4.6-5.2" stroke="#201F1E" stroke-width="1.7" fill="none" '
                 f'stroke-linecap="round" stroke-linejoin="round"/>'
                 f'<text x="{px + 46}" y="{y + 11}" font-size="11.5" fill="{C["text2"]}">{e(f)}</text></g>')
    for i, (t, v) in enumerate([("Local", "Jacareí · SP · Brasil"), ("Idiomas", "Português · Inglês avançado")]):
        y = 334 + i * 76
        b.append(f'<rect x="{px + 14}" y="{y}" width="182" height="64" rx="4" fill="{C["card2"]}"/>'
                 f'<text x="{px + 26}" y="{y + 24}" font-size="12" font-weight="700" fill="{C["text"]}">{e(t)}</text>'
                 f'<text x="{px + 26}" y="{y + 46}" font-size="11.5" fill="{C["muted"]}">{e(v)}</text>')

    # página do relatório
    b.append(f'<rect x="72" y="92" width="894" height="408" rx="6" fill="{C["page"]}" stroke="#33312F"/>')
    b.append(f'<text x="100" y="132" font-size="11" font-weight="700" fill="{C["yellow"]}" letter-spacing="2.5">'
             f'RELATÓRIO DE PERFIL · ENGENHARIA &amp; CIÊNCIA DE DADOS</text>')
    b.append(f'<text x="98" y="184" font-size="48" font-weight="800" fill="{C["text"]}" letter-spacing="-.5" class="up">Raywã Rafaneli</text>')
    # subtítulo que alterna entre 3 frases (efeito de digitação com SMIL)
    frases = ["Engenharia de dados · ETL · SQL · Python", "Ciência de dados · estatística · previsão",
              "Business Intelligence · Power BI · DAX", "Automação · RPA · SAP"]
    seg, tot = 3.6, 3.6 * len(frases)
    kt = f"0;{1.0 / tot:.4f};{3.0 / tot:.4f};{3.4 / tot:.4f};1"
    for i, fr in enumerate(frases):
        base = 560 if i == 0 else 0
        b.append(f'<clipPath id="type{i}"><rect x="96" y="198" width="{base}" height="34">'
                 f'<animate attributeName="width" values="0;560;560;0;0" keyTimes="{kt}" dur="{tot}s" '
                 f'begin="{i * seg}s" repeatCount="indefinite"/></rect></clipPath>'
                 f'<g clip-path="url(#type{i})"><text x="100" y="222" font-size="19" fill="{C["text2"]}">{fr}</text>'
                 f'<rect x="{104 + text_w(fr.replace("&amp;", "&"), 19):.0f}" y="205" width="2.5" height="22" '
                 f'fill="{C["yellow"]}" class="caret"/></g>')
    b.append(f'<text x="100" y="252" font-size="14" fill="{C["muted"]}" class="fade" style="animation-delay:1.2s">'
             f'<tspan fill="{C["yellow"]}">●</tspan> Jacareí, SP · dados de ponta a ponta, do ETL à previsão</text>')
    x = 100
    for i, t in enumerate(["Python", "SQL", "Estatística", "Machine Learning", "Power BI"]):
        first = i == 0
        g, w = chip(x, 270, t, fill="url(#pbi)" if first else None, stroke=C["yellow"] if first else None,
                    color="#201F1E" if first else None, bold=first)
        b.append(f'<g class="up" style="animation-delay:{1.3 + i * .12:.2f}s">{g}</g>')
        x += w + 8

    # visual combinado (colunas + linha): etapas do trabalho
    vx, vy = 640, 112
    b.append(f'<rect x="{vx}" y="{vy}" width="306" height="194" rx="6" fill="{C["chrome"]}" stroke="{C["line"]}"/>')
    b.append(f'<text x="{vx + 16}" y="{vy + 25}" font-size="13" font-weight="700" fill="{C["text"]}">Do dado à decisão</text>'
             f'<text x="{vx + 16}" y="{vy + 42}" font-size="10.5" fill="{C["muted"]}">etapas do meu trabalho</text>')
    b.append(visual_icons(vx + 220, vy + 14))
    base = vy + 160
    for gy in (base - 40, base - 80, base - 120):
        b.append(f'<path d="M{vx + 16} {gy}H{vx + 290}" stroke="#302F2E" stroke-dasharray="3 4"/>')
    b.append(f'<path d="M{vx + 16} {base}H{vx + 290}" stroke="{C["line2"]}"/>')
    etapas = ["Extrair", "Tratar", "Modelar", "Prever", "Decidir"]
    hs = [34, 54, 76, 96, 116]
    pts = []
    for i, (lab, h) in enumerate(zip(etapas, hs)):
        bx = vx + 30 + i * 54
        b.append(f'<g class="eq" style="animation-delay:{2 + i * .35:.2f}s"><rect class="bar" '
                 f'style="animation-delay:{.6 + i * .12:.2f}s" x="{bx}" y="{base - h}" width="32" '
                 f'height="{h}" rx="2" fill="url(#barg)"/></g>')
        b.append(f'<text x="{bx + 16}" y="{base + 16}" font-size="9.5" fill="{C["muted"]}" text-anchor="middle">{lab}</text>')
        pts.append((bx + 16, base - h - 12))
    b.append(f'<polyline class="draw" points="{" ".join(f"{a},{c}" for a, c in pts)}" fill="none" stroke="{DATA[0]}" '
             f'stroke-width="2.4" stroke-linejoin="round" stroke-linecap="round"/>')
    for i, (a, c) in enumerate(pts):
        b.append(f'<circle class="fade" style="animation-delay:{1.6 + i * .2:.2f}s" cx="{a}" cy="{c}" r="3.6" '
                 f'fill="{C["page"]}" stroke="{DATA[0]}" stroke-width="2"/>')
    trilha = "M" + " L".join(f"{a},{c}" for a, c in pts)
    b.append(f'<circle r="5" fill="{C["yellow"]}" opacity="0"><animateMotion dur="3.2s" begin="2.8s" '
             f'repeatCount="indefinite" path="{trilha}"/><animate attributeName="opacity" values="0;1;1;0" '
             f'keyTimes="0;.1;.85;1" dur="3.2s" begin="2.8s" repeatCount="indefinite"/></circle>')

    # cartões de KPI
    cards = [("4º", "lugar no HackaEmb 2026", "entre 14 times · 2 hackathons", C["yellow"]),
             ("12", "certificações", "Power BI avançado · SQL · Python", DATA[0]),
             ("10", "nota no TCC", "predição com Machine Learning", DATA[1]),
             ("2027", "Ciência da Computação", "bacharelado · UNIP", DATA[2])]
    for i, (big, l1, l2, cor) in enumerate(cards):
        cx = 100 + i * 216
        b.append(f'<g class="up" style="animation-delay:{.9 + i * .15:.2f}s">'
                 f'<rect x="{cx}" y="330" width="198" height="150" rx="6" fill="{C["chrome"]}" stroke="{C["line"]}"/>'
                 f'<rect x="{cx}" y="330" width="198" height="3" rx="1.5" fill="{cor}"/>'
                 f'<text x="{cx + 20}" y="392" font-size="36" font-weight="800" fill="{C["text"]}">{big}</text>'
                 f'<text x="{cx + 20}" y="426" font-size="13" font-weight="600" fill="{C["text2"]}">{l1}</text>'
                 f'<text x="{cx + 20}" y="448" font-size="11.5" fill="{C["muted"]}">{l2}</text></g>')
    # brilho que passa pelos cartões
    clip = "".join(f'<rect x="{100 + i * 216}" y="330" width="198" height="150" rx="6"/>' for i in range(4))
    b.append(f'<defs><clipPath id="cardsclip">{clip}</clipPath><linearGradient id="glint" x1="0" x2="1">'
             f'<stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".08"/>'
             f'<stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient></defs>'
             f'<g clip-path="url(#cardsclip)"><rect class="shine" style="animation-delay:2.5s" x="100" y="330" width="260" '
             f'height="150" fill="url(#glint)"/></g>')

    # barra inferior: abas de página que avançam sozinhas + zoom
    b.append(f'<rect y="520" width="{W}" height="40" fill="{C["chrome"]}"/><rect y="520" width="{W}" height="1" fill="{C["line"]}"/>')
    n, passo = len(PAGES), 2.6
    dur = n * passo
    kts = ";".join(f"{k / n:.4f}" for k in range(n))
    xs, ws = [], []
    x = 60
    for _, nome in PAGES:
        w = text_w(nome, 12.5, True) + 30
        xs.append(x)
        ws.append(w)
        x += w + 6
    b.append(f'<rect x="{xs[0]}" y="525" width="{ws[0]:.0f}" height="30" rx="4" fill="{C["card2"]}">'
             f'<animate attributeName="x" values="{";".join(f"{v:.0f}" for v in xs)}" keyTimes="{kts}" calcMode="discrete" dur="{dur}s" repeatCount="indefinite"/>'
             f'<animate attributeName="width" values="{";".join(f"{v:.0f}" for v in ws)}" keyTimes="{kts}" calcMode="discrete" dur="{dur}s" repeatCount="indefinite"/></rect>')
    b.append(f'<rect x="{xs[0] + 10}" y="551" width="{ws[0] - 20:.0f}" height="2.5" rx="1.2" fill="{C["yellow"]}">'
             f'<animate attributeName="x" values="{";".join(f"{v + 10:.0f}" for v in xs)}" keyTimes="{kts}" calcMode="discrete" dur="{dur}s" repeatCount="indefinite"/>'
             f'<animate attributeName="width" values="{";".join(f"{v - 20:.0f}" for v in ws)}" keyTimes="{kts}" calcMode="discrete" dur="{dur}s" repeatCount="indefinite"/></rect>')
    for i, (_, nome) in enumerate(PAGES):
        vis = ";".join("1" if k == i else "0" for k in range(n))
        b.append(f'<text x="{xs[i] + ws[i] / 2:.0f}" y="545" font-size="12.5" text-anchor="middle" fill="{C["muted"]}">{e(nome)}</text>'
                 f'<text x="{xs[i] + ws[i] / 2:.0f}" y="545" font-size="12.5" text-anchor="middle" fill="{C["text"]}" '
                 f'font-weight="600" opacity="{1 if i == 0 else 0}"><animate attributeName="opacity" values="{vis}" '
                 f'keyTimes="{kts}" calcMode="discrete" dur="{dur}s" repeatCount="indefinite"/>{e(nome)}</text>'
                 f'<text x="880" y="545" font-size="11.5" fill="{C["muted"]}" opacity="{1 if i == 0 else 0}">'
                 f'<animate attributeName="opacity" values="{vis}" keyTimes="{kts}" calcMode="discrete" dur="{dur}s" '
                 f'repeatCount="indefinite"/>Página {i + 1} de {n}</text>')
    b.append(f'<text x="{x + 8:.0f}" y="546" font-size="17" fill="{C["muted"]}">+</text>')
    b.append(f'<path d="M990 540h8" stroke="{C["muted"]}" stroke-width="1.4"/>'
             f'<rect x="1008" y="539" width="100" height="2" rx="1" fill="{C["line2"]}"/>'
             f'<circle cx="1058" cy="540" r="5" fill="{C["text"]}"/>'
             f'<path d="M1118 540h8M1122 536v8" stroke="{C["muted"]}" stroke-width="1.4"/>'
             f'<text x="1140" y="545" font-size="11.5" fill="{C["muted"]}">100%</text>')
    b.append('</g>')
    b.append(f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="12" fill="none" stroke="{C["line"]}"/>')
    return svg(W, H, "\n".join(b), "Relatório de perfil no estilo Power BI: Raywã Rafaneli, Desenvolvedor BI, "
                                  "engenharia e ciência de dados", css=LOOP_CSS)


# ------------------------------------------------------------------ abas (navegação)
def tab(num, nome):
    w = int(text_w(nome, 15, True) + 74)
    b = (f'<clipPath id="c"><rect width="{w}" height="44" rx="8"/></clipPath>'
         f'<rect x=".5" y=".5" width="{w - 1}" height="43" rx="8" fill="{C["chrome"]}" stroke="{C["line"]}"/>'
         f'<text x="18" y="27" font-size="12" font-weight="700" fill="{C["yellow"]}" class="mono">{num:02d}</text>'
         f'<text x="44" y="27.5" font-size="15" font-weight="600" fill="{C["text"]}">{e(nome)}</text>'
         f'<rect x="16" y="38" width="{w - 32}" height="3" rx="1.5" fill="url(#pbi)" class="breath" '
         f'style="animation-delay:{num * .4:.1f}s"/>'
         f'<g clip-path="url(#c)"><rect class="shine" style="animation-delay:{num * .45:.2f}s" x="0" y="0" width="{w * .35:.0f}" '
         f'height="44" fill="url(#glint)"/></g>')
    defs = ('<linearGradient id="glint" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
            '<stop offset=".5" stop-color="#fff" stop-opacity=".09"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>')
    return svg(w, 44, b, nome, css=LOOP_CSS, defs=defs)


# ------------------------------------------------------------------ cabeçalhos de seção
def section(num, titulo, sub):
    W, H = 1200, 96
    b = [f'<clipPath id="c"><rect width="{W}" height="{H}" rx="10"/></clipPath><g clip-path="url(#c)">',
         f'<rect width="{W}" height="{H}" fill="{C["page"]}"/>',
         f'<rect width="6" height="{H}" fill="url(#pbi)"/>',
         f'<rect class="sweep" x="0" y="{H - 3}" width="260" height="3" fill="url(#shine)"/>',
         f'<text x="34" y="36" font-size="11.5" font-weight="700" fill="{C["yellow"]}" letter-spacing="3">'
         f'PÁGINA {num:02d} · {e(sub.upper())}</text>',
         f'<text x="32" y="74" font-size="30" font-weight="800" fill="{C["text"]}">{e(titulo)}</text>']
    # mini visual decorativo à direita
    hs = [14, 24, 18, 32, 26, 40]
    for i, h in enumerate(hs):
        b.append(f'<g class="eq" style="animation-delay:{1.2 + i * .23:.2f}s"><rect class="bar" style="animation-delay:{.2 + i * .1:.1f}s" '
                 f'x="{1000 + i * 14}" y="{70 - h}" width="9" height="{h}" rx="1.5" fill="url(#barg)" opacity="{.45 + i * .11:.2f}"/></g>')
    b.append(f'<path d="M1000 74H1083" stroke="{C["line2"]}"/>')
    b.append(visual_icons(1100, 32))
    b.append(f'<circle cx="{W - 22}" cy="{H - 20}" r="3.5" fill="#1AAB40" class="pulse"/>')
    b.append('</g>')
    b.append(f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="10" fill="none" stroke="{C["line"]}"/>')
    defs = (f'<linearGradient id="shine" x1="0" x2="1"><stop offset="0" stop-color="{C["yellow"]}" stop-opacity="0"/>'
            f'<stop offset=".5" stop-color="{C["yellow"]}"/><stop offset="1" stop-color="{C["yellow"]}" stop-opacity="0"/>'
            f'</linearGradient>')
    return svg(W, H, "\n".join(b), f"Página {num} · {titulo}", defs=defs, css=LOOP_CSS)


# ------------------------------------------------------------------ editor DAX
KW, STR, VAR, TBL, COL, OP, CMT = "#569CD6", "#CE9178", "#DCDCAA", "#4EC9B0", "#9CDCFE", "#D4D4D4", "#6A9955"
DAX = [
    [("-- quem sou eu, em uma medida", CMT)],
    [("DEFINE", KW)],
    [("    MEASURE ", KW), ("Perfil", TBL), ("[Raywã]", COL), (" =", OP)],
    [("        VAR ", KW), ("Area", VAR), ("       = ", OP), ('"Engenharia & Ciência de Dados"', STR)],
    [("        VAR ", KW), ("Stack", VAR), ("      = ", OP), ('"Python · SQL · Estatística · Power BI"', STR)],
    [("        VAR ", KW), ("Extra", VAR), ("      = ", OP), ('"RPA"', STR)],
    [("        VAR ", KW), ("Hackathons", VAR), (" = ", OP), ("2", "#B5CEA8")],
    [("        VAR ", KW), ("Destaque", VAR), ("   = ", OP), ('"4º lugar · HackaEmb 2026"', STR)],
    [("        RETURN", KW)],
    [("            ", OP), ("Area", VAR), (' & ', OP), ('" + "', STR), (" & ", OP), ("Extra", VAR)],
    [("EVALUATE", KW)],
    [("    { ", OP), ("[Raywã]", COL), (" }", OP)],
]


def dax():
    W, H = 600, 420
    b = [f'<clipPath id="c"><rect width="{W}" height="{H}" rx="10"/></clipPath><g clip-path="url(#c)">',
         f'<rect width="{W}" height="{H}" fill="#1E1E1E"/>',
         f'<rect width="{W}" height="40" fill="{C["chrome"]}"/>', logo(16, 13, .9),
         f'<text x="44" y="25" font-size="12.5" fill="{C["muted"]}">Exibição de consulta DAX</text>',
         f'<rect x="196" y="8" width="96" height="32" rx="4" fill="#1E1E1E"/>'
         f'<rect x="196" y="8" width="96" height="2.5" fill="{C["yellow"]}"/>'
         f'<text x="244" y="29" font-size="12" fill="{C["text"]}" text-anchor="middle">perfil.dax</text>',
         f'<rect x="494" y="9" width="90" height="23" rx="4" fill="none" stroke="{C["yellow"]}"/>'
         f'<path d="M507 15v11l9-5.5z" fill="{C["yellow"]}"/>'
         f'<text x="524" y="25" font-size="12" font-weight="600" fill="{C["yellow"]}">Executar</text>']
    y0, lh = 70, 21
    for i, toks in enumerate(DAX):
        y = y0 + i * lh
        spans = "".join(f'<tspan fill="{c}">{e(t)}</tspan>' for t, c in toks)
        b.append(f'<g class="fade" style="animation-delay:{.3 + i * .16:.2f}s">'
                 f'<text x="38" y="{y}" font-size="12.5" fill="#6E7681" text-anchor="end" class="mono">{i + 1}</text>'
                 f'<text x="54" y="{y}" font-size="13" class="mono" xml:space="preserve">{spans}</text></g>')
    # resultado
    ry = y0 + len(DAX) * lh + 4
    d = .3 + len(DAX) * .16 + .3
    b.append(f'<g class="up" style="animation-delay:{d:.2f}s">'
             f'<rect x="0" y="{ry}" width="{W}" height="1" fill="{C["line"]}"/>'
             f'<text x="20" y="{ry + 26}" font-size="12" font-weight="700" fill="{C["text"]}">Resultados</text>'
             f'<text x="96" y="{ry + 26}" font-size="11" fill="{C["muted"]}">1 linha · 0,08 s</text>'
             f'<rect x="20" y="{ry + 38}" width="{W - 40}" height="26" fill="{C["chrome"]}"/>'
             f'<text x="32" y="{ry + 55}" font-size="12" font-weight="600" fill="{C["text2"]}">[Raywã]</text>'
             f'<rect x="20" y="{ry + 64}" width="{W - 40}" height="30" fill="#232221" stroke="{C["line"]}"/>'
             f'<text x="32" y="{ry + 84}" font-size="13" fill="{C["text"]}">Engenharia &amp; Ciência de Dados + RPA</text>'
             f'<rect x="{W - 46}" y="{ry + 72}" width="2" height="15" fill="{C["yellow"]}" class="caret"/></g>')
    b.append('</g>')
    b.append(f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="10" fill="none" stroke="{C["line"]}"/>')
    return svg(W, H, "\n".join(b), "Consulta DAX que descreve o perfil: engenharia e ciência de dados, "
                                  "stack Python, SQL, estatística e Power BI, RPA em SAP e 4º lugar no HackaEmb 2026", css=LOOP_CSS)


# ------------------------------------------------------------------ matriz de stack
CTX = {"Trabalho": "#1AAB40", "Projetos": DATA[0], "Estudo": C["yellow"]}
STACK = [
    ("Ciência de dados & estatística", ["Estatística inferencial", "Testes de hipótese", "Séries temporais", "SARIMA",
                                        "Regressão", "Previsão (forecasting)", "Validação walk-forward"], ["Projetos"]),
    ("Machine Learning & IA", ["XGBoost", "Scikit-learn", "statsmodels", "SciPy", "Visão computacional", "LLMs", "Jupyter"],
     ["Projetos"]),
    ("Engenharia de dados & ETL", ["SQL", "Pandas", "NumPy", "Pentaho PDI", "Modelagem dimensional", "APIs de dados",
                                   "Qualidade de dados"], ["Trabalho", "Projetos"]),
    ("Bancos de dados", ["Oracle SQL", "PostgreSQL", "MySQL", "SQL Server", "DuckDB", "SQLite"], ["Trabalho", "Projetos"]),
    ("BI & visualização", ["Power BI (avançado)", "DAX", "Power Query (M)", "Metabase", "Streamlit", "Plotly",
                           "Matplotlib", "Seaborn"], ["Trabalho", "Projetos"]),
    ("Automação & RPA", ["SAP ERP", "SAP GUI Scripting", "Python", "VBA", "Outlook (pywin32)", "OCR de PDFs",
                         "Playwright", "Excel (openpyxl)", "SMTP"], ["Trabalho", "Projetos"]),
    ("Linguagens", ["Python", "SQL", "Java", "C#", "VB.NET", "VBA", "JavaScript"], ["Trabalho", "Projetos"]),
    ("Web & .NET", ["HTML5", "CSS3 (Flexbox, Grid)", "SVG", ".NET", "ASP.NET", "FastAPI", "Java (sockets, Maven)"],
     ["Trabalho", "Projetos"]),
    ("Cloud, DevOps & testes", ["Docker", "AWS", "Git", "GitHub Actions", "CI/CD", "pytest"], ["Projetos"]),
    ("Bots & integrações", ["Telegram Bot API", "YouTube Data API", "APIs REST"], ["Projetos"]),
    ("Governança & processos", ["Governança de dados", "LGPD", "Lean", "Supply Chain"], ["Trabalho"]),
    ("Cursos & estudando", ["SAP S/4HANA", "Azure SQL", "Apache Spark"], ["Estudo"]),
]


def stack():
    W = 1200
    x0, xmax, top, lh = 300, 935, 112, 36
    linhas = []  # (área, [(x, y_rel, nome)], ctx, altura)
    for area, tools, ctx in STACK:
        x, yrel, itens = x0, 0, []
        for t in tools:
            w = text_w(t, 12.5) + 26
            if x + w > xmax:
                x, yrel = x0, yrel + lh
            itens.append((x, yrel, t))
            x += w + 8
        linhas.append((area, itens, ctx, yrel + 50))
    H = top + sum(h for *_, h in linhas) + 62
    b = [f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="10" fill="{C["page"]}" stroke="{C["line"]}"/>',
         f'<text x="28" y="40" font-size="16" font-weight="700" fill="{C["text"]}">Matriz de competências</text>',
         f'<text x="28" y="60" font-size="12" fill="{C["muted"]}">Ferramentas por área e onde eu uso cada uma</text>',
         visual_icons(1100, 30),
         f'<text x="52" y="98" font-size="12.5" font-weight="700" fill="{C["text2"]}">Área</text>',
         f'<text x="300" y="98" font-size="12.5" font-weight="700" fill="{C["text2"]}">Ferramentas</text>',
         f'<text x="964" y="98" font-size="12.5" font-weight="700" fill="{C["text2"]}">Onde uso</text>',
         f'<rect x="20" y="{top - 1}" width="{W - 40}" height="1.5" fill="{C["yellow"]}" opacity=".8"/>']
    y = top
    k = 0
    cores = DATA + [C["yellow"], "#1AAB40", "#13BFCF"]
    for i, (area, itens, ctx, h) in enumerate(linhas):
        g = [f'<g class="up" style="animation-delay:{.15 + i * .09:.2f}s">']
        if i % 2:
            g.append(f'<rect x="20" y="{y + .5}" width="{W - 40}" height="{h}" fill="#232221"/>')
        g.append(f'<rect x="32" y="{y + 20}" width="10" height="10" rx="2" fill="{cores[i % len(cores)]}"/>'
                 f'<text x="52" y="{y + 30}" font-size="14" font-weight="600" fill="{C["text"]}">{e(area)}</text>')
        for x, yrel, t in itens:
            c, _ = chip(x, y + 12 + yrel, t, size=12.5)
            g.append(f'<g class="float" style="animation-delay:{(k * .37) % 5:.2f}s">{c}</g>')
            k += 1
        x = 964
        for c in ctx:
            g.append(f'<circle cx="{x + 6}" cy="{y + 25}" r="6" fill="{CTX[c]}" class="breath" '
                     f'style="animation-delay:{i * .3:.1f}s"/>'
                     f'<text x="{x + 18}" y="{y + 29.5}" font-size="12.5" fill="{C["text2"]}">{c}</text>')
            x += text_w(c, 12.5) + 36
        g.append(f'<rect x="20" y="{y + h}" width="{W - 40}" height="1" fill="{C["line"]}" opacity=".6"/></g>')
        b.append("".join(g))
        y += h
    ly = H - 26
    x = 28
    for nome, cor in [("Trabalho", CTX["Trabalho"]), ("Projetos pessoais e acadêmicos", CTX["Projetos"]),
                      ("Estudo / curso", CTX["Estudo"])]:
        b.append(f'<circle cx="{x + 5}" cy="{ly - 4}" r="5" fill="{cor}"/>'
                 f'<text x="{x + 16}" y="{ly}" font-size="12" fill="{C["muted"]}">{e(nome)}</text>')
        x += text_w(nome, 12) + 44
    return svg(W, H, "\n".join(b), "Matriz de competências: " + "; ".join(
        f"{a}: {', '.join(t)}" for a, t, _ in STACK), css=LOOP_CSS)


# ------------------------------------------------------------------ rodapé
def rodape():
    W, H = 1200, 64
    b = [f'<clipPath id="c"><rect width="{W}" height="{H}" rx="10"/></clipPath>',
         f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="10" fill="{C["chrome"]}" stroke="{C["line"]}"/>',
         f'<g clip-path="url(#c)"><rect class="sweep" x="0" y="{H - 3}" width="300" height="3" fill="url(#shine)"/></g>',
         f'<g class="float">{logo(22, 23)}</g>',
         f'<text x="54" y="38" font-size="15" font-weight="700" fill="{C["text"]}">Obrigado pela visita!</text>',
         f'<text x="600" y="37" font-size="12" fill="{C["muted"]}" text-anchor="middle">'
         f'Página {len(PAGES)} de {len(PAGES)} · relatório de perfil · rayrafaneli</text>',
         f'<circle cx="910" cy="32" r="4.5" fill="#1AAB40" class="pulse"/>'
         f'<text x="922" y="37" font-size="12" fill="{C["muted"]}">dados atualizados todo dia</text>',
         f'<path d="M1080 32h8" stroke="{C["muted"]}" stroke-width="1.4"/>'
         f'<rect x="1096" y="31" width="52" height="2" rx="1" fill="{C["line2"]}"/>'
         f'<circle cx="1122" cy="32" r="5" fill="{C["text"]}">'
         f'<animate attributeName="cx" values="1104;1140;1104" dur="6s" repeatCount="indefinite"/></circle>'
         f'<path d="M1158 32h8M1162 28v8" stroke="{C["muted"]}" stroke-width="1.4"/>']
    defs = (f'<linearGradient id="shine" x1="0" x2="1"><stop offset="0" stop-color="{C["yellow"]}" stop-opacity="0"/>'
            f'<stop offset=".5" stop-color="{C["yellow"]}"/><stop offset="1" stop-color="{C["yellow"]}" stop-opacity="0"/>'
            f'</linearGradient>')
    return svg(W, H, "\n".join(b), "Obrigado pela visita!", css=LOOP_CSS, defs=defs)


def fluxo_rpa():
    """Fluxo típico das automações corporativas, com dados correndo pelas setas."""
    W, H = 1200, 250
    etapas = [("E-mail & PDFs", "Outlook · OCR", DATA[0]), ("Python", "regras de negócio", C["yellow"]),
              ("SAP ERP", "GUI Scripting", DATA[1]), ("Oracle SQL", "consulta e cruzamento", DATA[2]),
              ("Excel", "relatórios", "#1AAB40"), ("Painel & e-mail", "HTML · CSS · JS", DATA[3])]
    b = [f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="10" fill="{C["page"]}" stroke="{C["line"]}"/>',
         f'<text x="28" y="38" font-size="16" font-weight="700" fill="{C["text"]}">Como meus robôs corporativos trabalham</text>',
         f'<text x="28" y="58" font-size="12" fill="{C["muted"]}">fluxo típico das automações em produção · Python e VBA</text>',
         visual_icons(1100, 28)]
    n, w, h, y = len(etapas), 160, 96, 104
    gap = (W - 56 - n * w) / (n - 1)
    xs = [28 + i * (w + gap) for i in range(n)]
    for i in range(n - 1):
        x1, x2 = xs[i] + w, xs[i + 1]
        b.append(f'<path d="M{x1 + 4} {y + h / 2}H{x2 - 8}" stroke="{C["line2"]}" stroke-width="2"/>'
                 f'<path d="M{x1 + 4} {y + h / 2}H{x2 - 8}" stroke="{C["yellow"]}" stroke-width="2.5" '
                 f'stroke-dasharray="6 10" class="flow"/>'
                 f'<path d="M{x2 - 10} {y + h / 2 - 5}l6 5-6 5" stroke="{C["yellow"]}" stroke-width="2" fill="none"/>')
    for i, (titulo, sub, cor) in enumerate(etapas):
        x = xs[i]
        b.append(f'<g class="up" style="animation-delay:{.15 + i * .15:.2f}s">'
                 f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{C["chrome"]}" stroke="{C["line"]}"/>'
                 f'<rect x="{x}" y="{y}" width="{w}" height="3" rx="1.5" fill="{cor}"/>'
                 f'<circle cx="{x + 22}" cy="{y + 32}" r="7" fill="{cor}" class="breath" style="animation-delay:{i * .5:.1f}s"/>'
                 f'<text x="{x + 38}" y="{y + 37}" font-size="14.5" font-weight="700" fill="{C["text"]}">{e(titulo)}</text>'
                 f'<text x="{x + 16}" y="{y + 70}" font-size="12" fill="{C["muted"]}">{e(sub)}</text></g>')
    b.append(f'<text x="28" y="{H - 22}" font-size="12" fill="{C["muted"]}">Exemplos: consultas e atualizações em transações '
             f'do SAP, leitura de grids, extração de dados de documentos e e-mails automáticos com o status.</text>')
    css = LOOP_CSS + ".flow{animation:flow 1.1s linear infinite;}@keyframes flow{to{stroke-dashoffset:-32}}"
    return svg(W, H, "\n".join(b), "Fluxo das automações: e-mail e PDFs, Python, SAP ERP, Oracle SQL, Excel e painel/e-mail",
               css=css)


def main():
    files = {"header.svg": header(), "dax.svg": dax(), "stack.svg": stack(), "footer.svg": rodape(),
             "fluxo-rpa.svg": fluxo_rpa()}
    subs = {"sobre": "quem sou", "hackathons": "competições de programação", "stack": "ferramentas", "dados": "engenharia, estatística e ml", "rpa": "robôs e automações",
            "metricas": "github", "contato": "vamos conversar"}
    titulos = {"sobre": "Sobre mim", "hackathons": "Hackathons & conquistas", "stack": "Stack & competências", "dados": "Engenharia & ciência de dados",
               "rpa": "Automação & RPA", "metricas": "Métricas do GitHub", "contato": "Contato"}
    for i, (slug, nome) in enumerate(PAGES, 1):
        files[f"tabs/{slug}.svg"] = tab(i, nome)
        files[f"sections/{slug}.svg"] = section(i, titulos[slug], subs[slug])
    for nome, conteudo in files.items():
        p = OUT / nome
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(conteudo, encoding="utf-8")
        print("ok", p.relative_to(OUT.parent))


if __name__ == "__main__":
    main()
