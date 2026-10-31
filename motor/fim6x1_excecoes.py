"""Stories 'Fim da 6x1: exceções em discussão' (31/10/2026). Base visual: fim6x1_promulgacao.story."""
import sys, os
sys.path.insert(0, "/home/claude")
from brand import *
from fim6x1 import rr, SURF, LINE

SW, SH = 1080 * 2, 1920 * 2
KICK = "FIM DA 6X1 · ATUALIZAÇÃO"


def base(kick):
    img = background().resize((SW, SH)); d = ImageDraw.Draw(img)
    tracked(d, (MARGIN, 420), kick, f(BOLD, 44), ORANGE, 8)
    return img, d


def rodape(d, cta=None):
    if cta:
        rr(d, [MARGIN, SH - 1000, SW - MARGIN, SH - 820], fill=ORANGE, r=90)
        d.text((SW / 2, SH - 910), cta, font=f(BOLD, 70), fill=(20, 20, 22), anchor="mm")
    tracked(d, (SW / 2, SH - 560), "SINGULAR", f(BOLD, 80), ORANGE, 30, center=True)
    d.text((SW / 2, SH - 440), "@singularinteligencia", font=f(REG, 48), fill=DIM, anchor="ma")


def texto(d, y, t, size=64, fill=GREY, font=LIGHT, gap=92):
    for l in wrap(d, t, f(font, size), SW - 2 * MARGIN):
        d.text((MARGIN, y), l, font=f(font, size), fill=fill); y += gap
    return y


def story1(path):
    img, d = base(KICK)
    y = 640
    for t, c in [("Exceções à", WHITE), ("5x2 entram", WHITE), ("na pauta.", ORANGE)]:
        d.text((MARGIN, y), t, font=f(BOLD, 170), fill=c); y += 200
    y += 90
    itens = [
        ("Senado", "PEC paralela para jornadas especiais, como embarcados, aeroviários e caminhoneiros. Coleta de assinaturas prevista para 3/11."),
        ("Governo", "Ministério do Trabalho prepara decreto com a lista de exceções."),
    ]
    for tag, t in itens:
        lines = wrap(d, t, f(REG, 58), SW - 2 * MARGIN - 120)
        h = 150 + len(lines) * 84
        rr(d, [MARGIN, y, SW - MARGIN, y + h], fill=SURF, r=40)
        d.text((MARGIN + 60, y + 50), tag.upper(), font=f(BOLD, 44), fill=ORANGE)
        yy = y + 120
        for l in lines:
            d.text((MARGIN + 60, yy), l, font=f(REG, 58), fill=WHITE); yy += 84
        y += h + 40
    y += 30
    texto(d, y, "Nada disso foi protocolado ou publicado ainda. Fontes: Exame, IstoÉ Dinheiro e CNN Brasil (28 a 30/10).", size=50, fill=DIM, gap=72)
    rodape(d)
    img.save(path, quality=93)


def story2(path):
    img, d = base("E O SEU DP?")
    y = 640
    for t, c in [("O calendário", WHITE), ("não mudou.", ORANGE)]:
        d.text((MARGIN, y), t, font=f(BOLD, 170), fill=c); y += 200
    y += 90
    itens = [
        "A emenda promulgada em 16/10 segue valendo",
        "Dezembro: teto de 42 horas e escala 5x2",
        "Um ano depois: teto de 40 horas",
        "Exceções, se vierem, ajustam casos específicos",
    ]
    for i, t in enumerate(itens, 1):
        lines = wrap(d, t, f(MED, 60), SW - 2 * MARGIN - 230)
        h = 90 + len(lines) * 86
        rr(d, [MARGIN, y, SW - MARGIN, y + h], fill=SURF, r=40)
        d.text((MARGIN + 60, y + h / 2), f"0{i}", font=f(BOLD, 52), fill=ORANGE, anchor="lm")
        yy = y + 45
        for l in lines:
            d.text((MARGIN + 200, yy), l, font=f(MED, 60), fill=WHITE); yy += 86
        y += h + 34
    y += 50
    texto(d, y, "Escalas, jornada no ponto e alterações contratuais no eSocial: comece agora.", size=62)
    rodape(d, "Fale com a Singular")
    img.save(path, quality=93)


if __name__ == "__main__":
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    story1(f"{out}/story1.jpg"); story2(f"{out}/story2.jpg")
    print("ok")
