"""Gera assets de métricas do GitHub no estilo de uma página de relatório do Power BI.

Uso: GH_TOKEN=... GH_USER=rayrafaneli python scripts/metrics.py dist/metrics.svg
Só biblioteca padrão (roda no GitHub Actions sem instalar nada).
Com um token pessoal (secret METRICS_TOKEN) entram também os repositórios privados
nas linguagens e no total de repositórios; com o GITHUB_TOKEN padrão, só os públicos.
"""
import json
import os
import sys
import urllib.request
from collections import OrderedDict
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from theme import C, DATA, e, svg, text_w, visual_icons  # noqa: E402

MESES = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]

QUERY = """
query($login: String!) {
  user(login: $login) {
    createdAt
    contributionsCollection {
      totalCommitContributions
      restrictedContributionsCount
      contributionCalendar { totalContributions weeks { contributionDays { date contributionCount } } }
    }
    repositories(ownerAffiliations: OWNER, isFork: false, first: 100) {
      totalCount
      nodes { languages(first: 10, orderBy: {field: SIZE, direction: DESC}) { edges { size node { name } } } }
    }
  }
}"""


def gql(token, login):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": login}}).encode(),
        headers={"Authorization": f"bearer {token}", "User-Agent": "profile-metrics"})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    if "errors" in data:
        raise SystemExit(f"GraphQL: {data['errors']}")
    return data["data"]["user"]


def resumo(u):
    days = [(date.fromisoformat(d["date"]), d["contributionCount"])
            for w in u["contributionsCollection"]["contributionCalendar"]["weeks"] for d in w["contributionDays"]]
    days.sort()
    hoje = days[-1][0]
    # sequência atual (hoje sem commit ainda não quebra a sequência)
    atual, i = 0, len(days) - 1
    if days[i][1] == 0:
        i -= 1
    while i >= 0 and days[i][1] > 0:
        atual += 1
        i -= 1
    maior = run = 0
    for _, c in days:
        run = run + 1 if c else 0
        maior = max(maior, run)
    # últimos 12 meses, mês a mês
    meses = OrderedDict()
    ref = date(hoje.year, hoje.month, 1)
    for k in range(11, -1, -1):
        y, m = ref.year, ref.month - k
        while m <= 0:
            m += 12
            y -= 1
        meses[(y, m)] = 0
    for d, c in days:
        if (d.year, d.month) in meses:
            meses[(d.year, d.month)] += c
    ativos = sum(1 for _, c in days if c)
    langs = {}
    for repo in u["repositories"]["nodes"]:
        for edge in repo["languages"]["edges"]:
            langs[edge["node"]["name"]] = langs.get(edge["node"]["name"], 0) + edge["size"]
    return {
        "total": u["contributionsCollection"]["contributionCalendar"]["totalContributions"],
        "atual": atual, "maior": maior, "ativos": ativos, "repos": u["repositories"]["totalCount"],
        "meses": meses, "langs": sorted(langs.items(), key=lambda kv: -kv[1]),
    }


def fmt(n):
    return f"{n:,}".replace(",", ".")


def render(r, quando):
    W, H = 1200, 600
    b = [f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="10" fill="{C["page"]}" stroke="{C["line"]}"/>']
    # cartões de KPI
    kpis = [(fmt(r["total"]), "contribuições", "últimos 12 meses", C["yellow"]),
            (f'{r["maior"]}', "dias seguidos (recorde)", f'sequência atual: {r["atual"]} dia{"s" if r["atual"] != 1 else ""}', DATA[0]),
            (f'{r["ativos"]}', "dias com commits", "no último ano", DATA[1]),
            (f'{r["repos"]}', "repositórios", "projetos no GitHub", DATA[2])]
    for i, (v, l1, l2, cor) in enumerate(kpis):
        x = 24 + i * 292
        b.append(f'<g class="up" style="animation-delay:{.1 + i * .12:.2f}s">'
                 f'<rect x="{x}" y="24" width="276" height="124" rx="6" fill="{C["chrome"]}" stroke="{C["line"]}"/>'
                 f'<rect x="{x}" y="24" width="276" height="3" rx="1.5" fill="{cor}"/>'
                 f'<text x="{x + 22}" y="86" font-size="40" font-weight="800" fill="{C["text"]}">{e(v)}</text>'
                 f'<text x="{x + 22}" y="114" font-size="13.5" font-weight="600" fill="{C["text2"]}">{e(l1)}</text>'
                 f'<text x="{x + 22}" y="133" font-size="11.5" fill="{C["muted"]}">{e(l2)}</text></g>')

    # colunas: contribuições por mês
    cx, cy, cw, ch = 24, 166, 740, 410
    b.append(f'<rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" rx="6" fill="{C["chrome"]}" stroke="{C["line"]}"/>'
             f'<text x="{cx + 20}" y="{cy + 30}" font-size="14" font-weight="700" fill="{C["text"]}">Contribuições por mês</text>'
             f'<text x="{cx + 20}" y="{cy + 48}" font-size="11.5" fill="{C["muted"]}">commits, pull requests e issues</text>')
    b.append(visual_icons(cx + cw - 90, cy + 20))
    vals = list(r["meses"].values())
    mx = max(vals + [4])
    passo = next(m * 10 ** k for k in range(7) for m in (1, 2, 5) if m * 10 ** k * 4 >= mx * 1.08)
    teto = passo * 4
    px0, py0, pw, ph = cx + 56, cy + 360, cw - 80, 270
    for k in range(5):
        y = py0 - ph * k / 4
        b.append(f'<path d="M{px0} {y:.1f}H{px0 + pw}" stroke="{"#4A4846" if k == 0 else "#302F2E"}"'
                 f'{"" if k == 0 else " stroke-dasharray=" + chr(34) + "3 4" + chr(34)}/>'
                 f'<text x="{px0 - 10}" y="{y + 4:.1f}" font-size="10.5" fill="{C["dim"]}" text-anchor="end">{fmt(int(teto * k / 4))}</text>')
    slot = pw / len(vals)
    bw = slot * .58
    pts = []
    for i, ((ano, mes), v) in enumerate(r["meses"].items()):
        h = ph * v / teto
        x = px0 + i * slot + (slot - bw) / 2
        last = i == len(vals) - 1
        b.append(f'<rect class="bar" style="animation-delay:{.3 + i * .07:.2f}s" x="{x:.1f}" y="{py0 - h:.1f}" '
                 f'width="{bw:.1f}" height="{max(h, .01):.1f}" rx="2" fill="url(#barg)"{"" if last else " opacity=" + chr(34) + ".9" + chr(34)}/>')
        if v:
            b.append(f'<text class="fade" style="animation-delay:{1 + i * .07:.2f}s" x="{x + bw / 2:.1f}" y="{py0 - h - 8:.1f}" '
                     f'font-size="11" font-weight="600" fill="{C["text2"]}" text-anchor="middle">{fmt(v)}</text>')
        rot = MESES[mes - 1] + (f"/{str(ano)[2:]}" if mes == 1 or i == 0 else "")
        b.append(f'<text x="{x + bw / 2:.1f}" y="{py0 + 20}" font-size="11" fill="{C["muted"]}" text-anchor="middle">{rot}</text>')
        pts.append((x + bw / 2, py0 - h))
    # linha de média móvel (3 meses)
    mm = []
    for i in range(len(vals)):
        janela = vals[max(0, i - 2): i + 1]
        mm.append((pts[i][0], py0 - ph * (sum(janela) / len(janela)) / teto))
    b.append(f'<polyline class="draw" points="{" ".join(f"{a:.1f},{c:.1f}" for a, c in mm)}" fill="none" '
             f'stroke="{DATA[0]}" stroke-width="2.4" stroke-linejoin="round" stroke-linecap="round"/>')
    b.append(f'<rect x="{cx + cw - 250}" y="{cy + 40}" width="10" height="10" rx="2" fill="url(#barg)"/>'
             f'<text x="{cx + cw - 234}" y="{cy + 49}" font-size="11" fill="{C["muted"]}">contribuições</text>'
             f'<path d="M{cx + cw - 146} {cy + 45}h14" stroke="{DATA[0]}" stroke-width="2.4"/>'
             f'<text x="{cx + cw - 126}" y="{cy + 49}" font-size="11" fill="{C["muted"]}">média 3 meses</text>')

    # rosca: linguagens
    dx, dy, dw, dh = 780, 166, 396, 410
    b.append(f'<rect x="{dx}" y="{dy}" width="{dw}" height="{dh}" rx="6" fill="{C["chrome"]}" stroke="{C["line"]}"/>'
             f'<text x="{dx + 20}" y="{dy + 30}" font-size="14" font-weight="700" fill="{C["text"]}">Linguagens</text>'
             f'<text x="{dx + 20}" y="{dy + 48}" font-size="11.5" fill="{C["muted"]}">% do código nos repositórios</text>')
    langs = r["langs"]
    total = sum(v for _, v in langs) or 1
    top5 = [(n, v) for n, v in langs[:5] if v / total >= .01]
    resto = total - sum(v for _, v in top5)
    fatias = top5 + ([("Outras", resto)] if resto / total >= .005 else [])
    cores = [C["yellow"], DATA[0], DATA[1], DATA[2], DATA[3], "#605E5C"]
    import math
    ox, oy, R, rr = dx + 120, dy + 200, 92, 58
    ang = -math.pi / 2
    for i, (n, v) in enumerate(fatias):
        frac = v / total
        a2 = ang + frac * 2 * math.pi
        large = 1 if frac > .5 else 0
        p = lambda a, rad: (ox + rad * math.cos(a), oy + rad * math.sin(a))  # noqa: E731
        (x1, y1), (x2, y2) = p(ang, R), p(a2 - 1e-4, R)
        (x3, y3), (x4, y4) = p(a2 - 1e-4, rr), p(ang, rr)
        b.append(f'<path class="fade" style="animation-delay:{.4 + i * .12:.2f}s" d="M{x1:.2f} {y1:.2f}A{R} {R} 0 {large} 1 {x2:.2f} {y2:.2f}'
                 f'L{x3:.2f} {y3:.2f}A{rr} {rr} 0 {large} 0 {x4:.2f} {y4:.2f}Z" fill="{cores[i]}" stroke="{C["chrome"]}" stroke-width="2"/>')
        ly = dy + 122 + i * 30
        b.append(f'<g class="fade" style="animation-delay:{.6 + i * .12:.2f}s">'
                 f'<rect x="{dx + 236}" y="{ly - 9}" width="10" height="10" rx="2" fill="{cores[i]}"/>'
                 f'<text x="{dx + 252}" y="{ly}" font-size="12" fill="{C["text2"]}">{e(n)}</text>'
                 f'<text x="{dx + dw - 18}" y="{ly}" font-size="12" font-weight="600" fill="{C["text"]}" text-anchor="end">'
                 f'{frac * 100:.0f}%</text></g>')
        ang = a2
    if langs:
        b.append(f'<text x="{ox}" y="{oy - 4}" font-size="22" font-weight="800" fill="{C["text"]}" text-anchor="middle">{len(langs)}</text>'
                 f'<text x="{ox}" y="{oy + 16}" font-size="11" fill="{C["muted"]}" text-anchor="middle">linguagens</text>')
    b.append(f'<circle cx="{dx + 26}" cy="{dy + dh - 26}" r="4" fill="#1AAB40" class="pulse"/>'
             f'<text x="{dx + 38}" y="{dy + dh - 22}" font-size="11" fill="{C["muted"]}">atualizado em {quando}</text>')
    return svg(W, H, "\n".join(b), f"Métricas do GitHub: {r['total']} contribuições nos últimos 12 meses, "
                                  f"sequência atual de {r['atual']} dias, {r['repos']} repositórios")


def main():
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "dist/metrics.svg")
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    login = os.environ.get("GH_USER", "rayrafaneli")
    r = resumo(gql(token, login))
    brt = datetime.now(timezone.utc) - timedelta(hours=3)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(r, brt.strftime("%d/%m/%Y")), encoding="utf-8")
    print(f"ok {out}: {r['total']} contribuições, {r['repos']} repos, {len(r['langs'])} linguagens")


if __name__ == "__main__":
    main()
