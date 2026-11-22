"""Gera um SVG animado (carrossel) a partir de prints de um painel: janela estilo Power BI,
troca de página com fade, abas de página e barra de progresso sincronizadas.

Uso (local, precisa de Pillow):
    python scripts/carousel.py saida.svg "Título" "subtítulo" "Aba 1=print1.png" "Aba 2=print2.png" ...
"""
import base64
import io
import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from theme import C, e, logo, svg, text_w  # noqa: E402

W, PAD, TOP, BOT = 1200, 12, 46, 44
IW = W - 2 * PAD
SEG = 4.5      # segundos por página
FADE = 0.7


def jpeg_b64(caminho: Path, largura: int, altura: int) -> str:
    im = Image.open(caminho).convert("RGB")
    alvo = altura / largura
    if im.height / im.width > alvo:  # corta embaixo para manter a proporção
        im = im.crop((0, 0, im.width, round(im.width * alvo)))
    im = im.resize((largura, altura), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=80, optimize=True, progressive=True)
    return base64.b64encode(buf.getvalue()).decode()


def carrossel(destino: Path, titulo: str, sub: str, paginas: list[tuple[str, Path]], ih: int = 720) -> None:
    n = len(paginas)
    T = n * SEG
    p, f = 100 / n, FADE / T * 100
    H = TOP + ih + PAD + BOT
    css = (f"@keyframes show{{0%{{opacity:0}}{f:.2f}%{{opacity:1}}{p:.2f}%{{opacity:1}}{p + f:.2f}%{{opacity:0}}100%{{opacity:0}}}}"
           f".sl{{opacity:0;animation:show {T}s linear infinite both;}}"
           f"@keyframes prog{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}"
           f".prog{{transform-box:fill-box;transform-origin:0 50%;animation:prog {SEG}s linear infinite;}}")
    b = [f'<clipPath id="win"><rect width="{W}" height="{H}" rx="12"/></clipPath>',
         f'<clipPath id="img"><rect x="{PAD}" y="{TOP}" width="{IW}" height="{ih}" rx="6"/></clipPath>',
         '<g clip-path="url(#win)">',
         f'<rect width="{W}" height="{H}" fill="{C["bg"]}"/>',
         f'<rect width="{W}" height="{TOP - 6}" fill="{C["chrome"]}"/>', logo(18, 13),
         f'<text x="48" y="26" font-size="14" font-weight="700" fill="{C["text"]}">{e(titulo)}'
         f'<tspan fill="{C["muted"]}" font-weight="400" font-size="13"> — {e(sub)}</tspan></text>',
         f'<circle cx="{W - 96}" cy="21" r="4.5" fill="#1AAB40" class="pulse"/>'
         f'<text x="{W - 86}" y="25.5" font-size="12" fill="{C["muted"]}">{n} páginas</text>']
    imgs = [jpeg_b64(c, round(IW * 1.2), round(ih * 1.2)) for _, c in paginas]
    b.append('<g clip-path="url(#img)">')
    b.append(f'<image x="{PAD}" y="{TOP}" width="{IW}" height="{ih}" href="data:image/jpeg;base64,{imgs[0]}"/>')
    for i, d in enumerate(imgs):
        b.append(f'<image class="sl" style="animation-delay:{i * SEG}s" x="{PAD}" y="{TOP}" width="{IW}" height="{ih}" '
                 f'href="data:image/jpeg;base64,{d}"/>')
    b.append('</g>')
    # barra inferior: abas de página sincronizadas + progresso
    by = TOP + ih + PAD
    b.append(f'<rect y="{by - 2}" width="{W}" height="{BOT + 2}" fill="{C["chrome"]}"/>')
    b.append(f'<rect class="prog" x="0" y="{by - 2}" width="{W}" height="2.5" fill="url(#pbi)"/>')
    x = 20
    for i, (nome, _) in enumerate(paginas):
        w = text_w(nome, 12.5, True) + 30
        b.append(f'<text x="{x + w / 2:.0f}" y="{by + 26}" font-size="12.5" fill="{C["muted"]}" text-anchor="middle">{e(nome)}</text>')
        b.append(f'<g class="sl" style="animation-delay:{i * SEG}s">'
                 f'<rect x="{x}" y="{by + 6}" width="{w:.0f}" height="30" rx="4" fill="{C["card2"]}"/>'
                 f'<rect x="{x + 10}" y="{by + 32}" width="{w - 20:.0f}" height="2.5" rx="1.2" fill="{C["yellow"]}"/>'
                 f'<text x="{x + w / 2:.0f}" y="{by + 26}" font-size="12.5" font-weight="600" fill="{C["text"]}" '
                 f'text-anchor="middle">{e(nome)}</text></g>')
        x += w + 6
    b.append(f'<text x="{W - 20}" y="{by + 26}" font-size="11.5" fill="{C["muted"]}" text-anchor="end">'
             f'troca de página a cada {SEG:g} s</text>')
    b.append('</g>')
    b.append(f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="12" fill="none" stroke="{C["line"]}"/>')
    rotulo = f"{titulo}: " + ", ".join(nome for nome, _ in paginas)
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(svg(W, H, "\n".join(b), rotulo, css=css), encoding="utf-8")
    print(f"ok {destino} {destino.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    out, titulo, sub, *pags = sys.argv[1:]
    carrossel(Path(out), titulo, sub, [(a.split("=", 1)[0], Path(a.split("=", 1)[1])) for a in pags])
