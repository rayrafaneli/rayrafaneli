"""Gera os SVGs estáticos do perfil (cabeçalho, abas, seções, DAX, matriz de stack, rodapé).

Uso: python scripts/build_assets.py   (escreve em assets/)
"""
from pathlib import Path

from theme import C, DATA, chip, e, logo, svg, text_w, visual_icons

OUT = Path(__file__).resolve().parent.parent / "assets"

PAGES = [("sobre", "Sobre"), ("stack", "Stack"), ("projetos", "Projetos"),
         ("metricas", "Métricas"), ("contato", "Contato")]


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
    b.append(f'<rect x="1078" y="45" width="104" height="22" rx="4" fill="url(#pbi)"/>'
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
    focos = ["Business Intelligence", "Engenharia de dados", "Automação (RPA)", "Desenvolvimento"]
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
             f'RELATÓRIO DE PERFIL · DESENVOLVIMENTO BI</text>')
    b.append(f'<text x="98" y="184" font-size="48" font-weight="800" fill="{C["text"]}" letter-spacing="-.5" class="up">Raywã Rafaneli</text>')
    b.append('<clipPath id="type"><rect x="96" y="198" width="0" height="34">'
             '<animate attributeName="width" from="0" to="540" dur="2.4s" begin=".5s" fill="freeze"/></rect></clipPath>')
    b.append(f'<text x="100" y="222" font-size="19" fill="{C["text2"]}" clip-path="url(#type)">'
             f'Desenvolvedor BI · Análise de Dados &amp; Automação</text>')
    b.append(f'<text x="100" y="252" font-size="14" fill="{C["muted"]}" class="fade" style="animation-delay:1.2s">'
             f'<tspan fill="{C["yellow"]}">●</tspan> Embraer · Supply Chain · desde abr/2025</text>')
    x = 100
    for i, t in enumerate(["Power BI", "DAX", "Power Query", "SQL", "Python"]):
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
    etapas = ["Extrair", "Tratar", "Modelar", "Visualizar", "Decidir"]
    hs = [34, 54, 76, 96, 116]
    pts = []
    for i, (lab, h) in enumerate(zip(etapas, hs)):
        bx = vx + 30 + i * 54
        b.append(f'<rect class="bar" style="animation-delay:{.6 + i * .12:.2f}s" x="{bx}" y="{base - h}" width="32" '
                 f'height="{h}" rx="2" fill="url(#barg)"/>')
        b.append(f'<text x="{bx + 16}" y="{base + 16}" font-size="9.5" fill="{C["muted"]}" text-anchor="middle">{lab}</text>')
        pts.append((bx + 16, base - h - 12))
    b.append(f'<polyline class="draw" points="{" ".join(f"{a},{c}" for a, c in pts)}" fill="none" stroke="{DATA[0]}" '
             f'stroke-width="2.4" stroke-linejoin="round" stroke-linecap="round"/>')
    for i, (a, c) in enumerate(pts):
        b.append(f'<circle class="fade" style="animation-delay:{1.6 + i * .2:.2f}s" cx="{a}" cy="{c}" r="3.6" '
                 f'fill="{C["page"]}" stroke="{DATA[0]}" stroke-width="2"/>')

    # cartões de KPI
    cards = [("Embraer", "Dados &amp; Automação", "Supply Chain · desde 2025", C["yellow"]),
             ("12", "certificações", "Power BI · BI · SQL · Python", DATA[0]),
             ("10", "nota no TCC", "Machine Learning com XGBoost", DATA[1]),
             ("2027", "Ciência da Computação", "bacharelado · UNIP", DATA[2])]
    for i, (big, l1, l2, cor) in enumerate(cards):
        cx = 100 + i * 216
        b.append(f'<g class="up" style="animation-delay:{.9 + i * .15:.2f}s">'
                 f'<rect x="{cx}" y="330" width="198" height="150" rx="6" fill="{C["chrome"]}" stroke="{C["line"]}"/>'
                 f'<rect x="{cx}" y="330" width="198" height="3" rx="1.5" fill="{cor}"/>'
                 f'<text x="{cx + 20}" y="392" font-size="36" font-weight="800" fill="{C["text"]}">{big}</text>'
                 f'<text x="{cx + 20}" y="426" font-size="13" font-weight="600" fill="{C["text2"]}">{l1}</text>'
                 f'<text x="{cx + 20}" y="448" font-size="11.5" fill="{C["muted"]}">{l2}</text></g>')

    # barra inferior: abas de página + zoom
    b.append(f'<rect y="520" width="{W}" height="40" fill="{C["chrome"]}"/><rect y="520" width="{W}" height="1" fill="{C["line"]}"/>')
    x = 60
    for i, (_, nome) in enumerate(PAGES):
        w = text_w(nome, 12.5, True) + 30
        if i == 0:
            b.append(f'<rect x="{x}" y="525" width="{w:.0f}" height="30" rx="4" fill="{C["card2"]}"/>'
                     f'<rect x="{x + 10}" y="551" width="{w - 20:.0f}" height="2.5" rx="1.2" fill="{C["yellow"]}"/>')
        b.append(f'<text x="{x + w / 2:.0f}" y="545" font-size="12.5" text-anchor="middle" '
                 f'fill="{C["text"] if i == 0 else C["muted"]}"{" font-weight=" + chr(34) + "600" + chr(34) if i == 0 else ""}>{e(nome)}</text>')
        x += w + 6
    b.append(f'<text x="{x + 8:.0f}" y="546" font-size="17" fill="{C["muted"]}">+</text>')
    b.append(f'<text x="880" y="545" font-size="11.5" fill="{C["muted"]}">Página 1 de {len(PAGES)}</text>')
    b.append(f'<path d="M990 540h8" stroke="{C["muted"]}" stroke-width="1.4"/>'
             f'<rect x="1008" y="539" width="100" height="2" rx="1" fill="{C["line2"]}"/>'
             f'<circle cx="1058" cy="540" r="5" fill="{C["text"]}"/>'
             f'<path d="M1118 540h8M1122 536v8" stroke="{C["muted"]}" stroke-width="1.4"/>'
             f'<text x="1140" y="545" font-size="11.5" fill="{C["muted"]}">100%</text>')
    b.append('</g>')
    b.append(f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="12" fill="none" stroke="{C["line"]}"/>')
    return svg(W, H, "\n".join(b), "Relatório de perfil no estilo Power BI: Raywã Rafaneli, Desenvolvedor BI, "
                                  "Análise de Dados e Automação na Embraer")


# ------------------------------------------------------------------ abas (navegação)
def tab(num, nome):
    w = int(text_w(nome, 15, True) + 74)
    b = (f'<rect x=".5" y=".5" width="{w - 1}" height="43" rx="8" fill="{C["chrome"]}" stroke="{C["line"]}"/>'
         f'<text x="18" y="27" font-size="12" font-weight="700" fill="{C["yellow"]}" class="mono">{num:02d}</text>'
         f'<text x="44" y="27.5" font-size="15" font-weight="600" fill="{C["text"]}">{e(nome)}</text>'
         f'<rect x="16" y="38" width="{w - 32}" height="3" rx="1.5" fill="url(#pbi)"/>')
    return svg(w, 44, b, nome)


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
        b.append(f'<rect class="bar" style="animation-delay:{.2 + i * .1:.1f}s" x="{1010 + i * 14}" y="{70 - h}" width="9" '
                 f'height="{h}" rx="1.5" fill="url(#barg)" opacity="{.45 + i * .11:.2f}"/>')
    b.append(visual_icons(1100, 32))
    b.append('</g>')
    b.append(f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="10" fill="none" stroke="{C["line"]}"/>')
    defs = (f'<linearGradient id="shine" x1="0" x2="1"><stop offset="0" stop-color="{C["yellow"]}" stop-opacity="0"/>'
            f'<stop offset=".5" stop-color="{C["yellow"]}"/><stop offset="1" stop-color="{C["yellow"]}" stop-opacity="0"/>'
            f'</linearGradient>')
    return svg(W, H, "\n".join(b), f"Página {num} · {titulo}", defs=defs)


# ------------------------------------------------------------------ editor DAX
KW, STR, VAR, TBL, COL, OP, CMT = "#569CD6", "#CE9178", "#DCDCAA", "#4EC9B0", "#9CDCFE", "#D4D4D4", "#6A9955"
DAX = [
    [("-- quem sou eu, em uma medida", CMT)],
    [("DEFINE", KW)],
    [("    MEASURE ", KW), ("Perfil", TBL), ("[Raywã]", COL), (" =", OP)],
    [("        VAR ", KW), ("Cargo", VAR), ("    = ", OP), ('"Análise de Dados e Automação"', STR)],
    [("        VAR ", KW), ("Empresa", VAR), ("  = ", OP), ('"Embraer"', STR)],
    [("        VAR ", KW), ("Area", VAR), ("     = ", OP), ('"Supply Chain"', STR)],
    [("        VAR ", KW), ("Foco", VAR), ("     = ", OP), ('"Business Intelligence"', STR)],
    [("        VAR ", KW), ("Stack", VAR), ("    = ", OP), ('"Power BI · DAX · SQL · Python"', STR)],
    [("        RETURN", KW)],
    [("            ", OP), ("Cargo", VAR), (' & ', OP), ('" @ "', STR), (" & ", OP), ("Empresa", VAR)],
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
             f'<text x="32" y="{ry + 84}" font-size="13" fill="{C["text"]}">Análise de Dados e Automação @ Embraer</text>'
             f'<rect x="{W - 46}" y="{ry + 72}" width="2" height="15" fill="{C["yellow"]}" class="pulse"/></g>')
    b.append('</g>')
    b.append(f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="10" fill="none" stroke="{C["line"]}"/>')
    return svg(W, H, "\n".join(b), "Consulta DAX que descreve o perfil: Análise de Dados e Automação na Embraer, "
                                  "Supply Chain, foco em Business Intelligence, stack Power BI, DAX, SQL e Python")


# ------------------------------------------------------------------ matriz de stack
CTX = {"Trabalho": "#1AAB40", "Projetos": DATA[0], "Estudo": C["yellow"]}
STACK = [
    ("BI & Visualização", ["Power BI", "DAX", "Power Query (M)", "Metabase"], ["Trabalho"]),
    ("Dados & ETL", ["SQL", "Oracle", "Pentaho PDI", "Pandas", "Modelagem de dados"], ["Trabalho"]),
    ("Automação (RPA)", ["Python", "VBA", "SAP GUI Scripting", "SMTP"], ["Trabalho"]),
    ("Desenvolvimento", ["ASP.NET", "VB.NET", "FastAPI", "Streamlit", "APIs REST"], ["Trabalho", "Projetos"]),
    ("Cloud & DevOps", ["Docker", "AWS", "Git", "GitHub Actions", "SQLite"], ["Projetos"]),
    ("IA & Machine Learning", ["XGBoost", "Visão computacional", "LLMs"], ["Projetos"]),
    ("Governança", ["Governança de dados", "LGPD", "Lean"], ["Trabalho", "Estudo"]),
    ("Estudando agora", ["SQL Server", "Azure SQL", "Apache Spark"], ["Estudo"]),
]


def stack():
    W = 1200
    top, rh = 112, 50
    H = top + len(STACK) * rh + 62
    b = [f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="10" fill="{C["page"]}" stroke="{C["line"]}"/>',
         f'<text x="28" y="40" font-size="16" font-weight="700" fill="{C["text"]}">Matriz de competências</text>',
         f'<text x="28" y="60" font-size="12" fill="{C["muted"]}">Ferramentas por área e onde eu uso cada uma</text>',
         visual_icons(1100, 30),
         f'<text x="52" y="98" font-size="12.5" font-weight="700" fill="{C["text2"]}">Área</text>',
         f'<text x="300" y="98" font-size="12.5" font-weight="700" fill="{C["text2"]}">Ferramentas</text>',
         f'<text x="964" y="98" font-size="12.5" font-weight="700" fill="{C["text2"]}">Onde uso</text>',
         f'<rect x="20" y="{top - 1}" width="{W - 40}" height="1.5" fill="{C["yellow"]}" opacity=".8"/>']
    for i, (area, tools, ctx) in enumerate(STACK):
        y = top + i * rh
        g = ['<g>']
        if i % 2:
            g.append(f'<rect x="20" y="{y + .5}" width="{W - 40}" height="{rh}" fill="#232221"/>')
        g.append(f'<rect x="32" y="{y + 20}" width="10" height="10" rx="2" fill="{(DATA + [C["yellow"]])[i % 9]}"/>'
                 f'<text x="52" y="{y + 30}" font-size="14" font-weight="600" fill="{C["text"]}">{e(area)}</text>')
        x = 300
        for t in tools:
            c, w = chip(x, y + 12, t, size=12.5)
            g.append(c)
            x += w + 8
        x = 964
        for c in ctx:
            g.append(f'<circle cx="{x + 6}" cy="{y + 25}" r="6" fill="{CTX[c]}"/>'
                     f'<text x="{x + 18}" y="{y + 29.5}" font-size="12.5" fill="{C["text2"]}">{c}</text>')
            x += text_w(c, 12.5) + 36
        g.append(f'<rect x="20" y="{y + rh}" width="{W - 40}" height="1" fill="{C["line"]}" opacity=".6"/></g>')
        b.append("".join(g))
    ly = H - 26
    x = 28
    for nome, cor in [("Trabalho (Embraer)", CTX["Trabalho"]), ("Projetos pessoais e acadêmicos", CTX["Projetos"]),
                      ("Estudo / curso", CTX["Estudo"])]:
        b.append(f'<circle cx="{x + 5}" cy="{ly - 4}" r="5" fill="{cor}"/>'
                 f'<text x="{x + 16}" y="{ly}" font-size="12" fill="{C["muted"]}">{e(nome)}</text>')
        x += text_w(nome, 12) + 44
    return svg(W, H, "\n".join(b), "Matriz de competências: " + "; ".join(
        f"{a}: {', '.join(t)}" for a, t, _ in STACK))


# ------------------------------------------------------------------ dashboard confidencial
def confidencial():
    W, H = 1200, 540
    b = [f'<clipPath id="c"><rect width="{W}" height="{H}" rx="12"/></clipPath><g clip-path="url(#c)">',
         f'<rect width="{W}" height="{H}" fill="{C["bg"]}"/>',
         f'<rect width="{W}" height="40" fill="{C["chrome"]}"/>', logo(18, 13),
         f'<text x="48" y="26" font-size="13" font-weight="600" fill="{C["text"]}">painel-corporativo.pbix'
         f'<tspan fill="{C["muted"]}" font-weight="400"> — Supply Chain · Embraer</tspan></text>',
         f'<rect x="1046" y="10" width="138" height="21" rx="10.5" fill="#3A1E1E" stroke="#D64550"/>'
         f'<text x="1115" y="25" font-size="11" font-weight="700" fill="#F28B8B" text-anchor="middle" letter-spacing="1">CONFIDENCIAL</text>',
         '<g filter="url(#blur)">']
    # esqueleto do dashboard
    for i in range(4):
        x = 28 + i * 290
        b.append(f'<rect x="{x}" y="62" width="274" height="96" rx="6" fill="{C["chrome"]}"/>'
                 f'<rect x="{x + 18}" y="84" width="110" height="10" rx="5" fill="#3E3C3A"/>'
                 f'<rect x="{x + 18}" y="106" width="{150 - i * 18}" height="26" rx="6" fill="{[C["yellow"], DATA[0], DATA[1], DATA[2]][i]}" opacity=".55"/>')
    b.append(f'<rect x="28" y="176" width="710" height="336" rx="6" fill="{C["chrome"]}"/>')
    hs = [120, 180, 150, 210, 170, 240, 200, 260, 190, 230, 280, 250]
    for i, h in enumerate(hs):
        b.append(f'<rect x="{60 + i * 56}" y="{488 - h}" width="34" height="{h}" rx="3" fill="url(#barg)" opacity=".7"/>')
    b.append(f'<polyline points="{" ".join(f"{77 + i * 56},{470 - h * .9:.0f}" for i, h in enumerate(hs))}" '
             f'fill="none" stroke="{DATA[0]}" stroke-width="4"/>')
    b.append(f'<rect x="756" y="176" width="416" height="336" rx="6" fill="{C["chrome"]}"/>')
    for i in range(8):
        y = 206 + i * 36
        b.append(f'<rect x="776" y="{y}" width="120" height="12" rx="6" fill="#3E3C3A"/>'
                 f'<rect x="916" y="{y}" width="{70 + (i * 37) % 160}" height="12" rx="6" fill="{DATA[i % 4]}" opacity=".6"/>')
    b.append('</g>')
    # aviso
    b.append(f'<rect class="sweep" x="0" y="0" width="240" height="{H}" fill="url(#shine)" opacity=".06"/>')
    b.append(f'<g class="up" style="animation-delay:.3s">'
             f'<rect x="330" y="186" width="540" height="190" rx="12" fill="{C["bg"]}" fill-opacity=".93" stroke="{C["yellow"]}" stroke-opacity=".55"/>'
             f'<rect x="586" y="226" width="28" height="22" rx="4" fill="url(#pbi)"/>'
             f'<path d="M591 226v-6a9 9 0 0 1 18 0v6" fill="none" stroke="{C["yellow"]}" stroke-width="3.2"/>'
             f'<circle cx="600" cy="236" r="3" fill="#201F1E"/>'
             f'<text x="600" y="286" font-size="24" font-weight="800" fill="{C["text"]}" text-anchor="middle">Conteúdo confidencial</text>'
             f'<text x="600" y="316" font-size="14.5" fill="{C["text2"]}" text-anchor="middle">'
             f'Dashboards de Supply Chain em Power BI e Metabase</text>'
             f'<text x="600" y="344" font-size="13" fill="{C["muted"]}" text-anchor="middle">'
             f'Telas e dados ficam fora do GitHub por compliance.</text></g>')
    b.append('</g>')
    b.append(f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="12" fill="none" stroke="{C["line"]}"/>')
    defs = ('<filter id="blur" x="-5%" y="-5%" width="110%" height="110%"><feGaussianBlur stdDeviation="5"/></filter>'
            f'<linearGradient id="shine" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
            f'<stop offset=".5" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>')
    return svg(W, H, "\n".join(b), "Dashboard corporativo de Supply Chain desfocado, com o aviso: conteúdo confidencial",
               defs=defs)


# ------------------------------------------------------------------ rodapé
def rodape():
    W, H = 1200, 64
    b = [f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="10" fill="{C["chrome"]}" stroke="{C["line"]}"/>',
         logo(22, 23),
         f'<text x="54" y="38" font-size="15" font-weight="700" fill="{C["text"]}">Obrigado pela visita!</text>',
         f'<text x="600" y="37" font-size="12" fill="{C["muted"]}" text-anchor="middle">'
         f'Página {len(PAGES)} de {len(PAGES)} · relatório de perfil · rayrafaneli</text>',
         f'<circle cx="930" cy="32" r="4.5" fill="#1AAB40" class="pulse"/>'
         f'<text x="942" y="37" font-size="12" fill="{C["muted"]}">dados atualizados</text>',
         f'<path d="M1062 32h8" stroke="{C["muted"]}" stroke-width="1.4"/>'
         f'<rect x="1078" y="31" width="64" height="2" rx="1" fill="{C["line2"]}"/>'
         f'<circle cx="1110" cy="32" r="5" fill="{C["text"]}"/>'
         f'<path d="M1150 32h8M1154 28v8" stroke="{C["muted"]}" stroke-width="1.4"/>']
    return svg(W, H, "\n".join(b), "Obrigado pela visita!")


def main():
    files = {"header.svg": header(), "dax.svg": dax(), "stack.svg": stack(),
             "confidencial.svg": confidencial(), "footer.svg": rodape()}
    subs = {"sobre": "quem sou", "stack": "ferramentas", "projetos": "portfólio",
            "metricas": "github", "contato": "vamos conversar"}
    titulos = {"sobre": "Sobre mim", "stack": "Stack & competências", "projetos": "Projetos em destaque",
               "metricas": "Métricas do GitHub", "contato": "Contato"}
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
