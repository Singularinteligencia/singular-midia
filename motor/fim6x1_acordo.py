"""Stories 'Fim da 6x1: 42 horas em 5 dias e a norma coletiva' (nov/2026). Base visual: fim6x1_excecoes."""
import sys, os
sys.path.insert(0, "/home/claude")
from brand import *
from fim6x1 import rr, SURF, LINE
from fim6x1_excecoes import base, rodape, texto, SW, SH, KICK


def story1(path):
    img, d = base(KICK)
    y = 640
    for t, c in [("42 horas em", WHITE), ("5 dias pedem", WHITE), ("acordo coletivo.", ORANGE)]:
        d.text((MARGIN, y), t, font=f(BOLD, 170), fill=c); y += 200
    y += 90
    itens = [
        ("A conta", "42 horas em 5 dias dão 8h24 por dia. O limite diário segue em 8 horas."),
        ("A emenda", "Passar de 8 horas na etapa de 42 horas depende de convenção ou acordo coletivo (art. 7º da EC 141)."),
        ("Sem norma coletiva", "O teto prático fica em 40 horas já em dezembro, segundo a Fecomércio-DF."),
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
    texto(d, y, "Fontes: Metrópoles (1/11) e O Povo (29/10).", size=50, fill=DIM, gap=72)
    rodape(d)
    img.save(path, quality=93)


def story2(path):
    img, d = base("E O SEU DP?")
    y = 640
    for t, c in [("Decida antes", WHITE), ("de dezembro.", ORANGE)]:
        d.text((MARGIN, y), t, font=f(BOLD, 170), fill=c); y += 200
    y += 90
    itens = [
        "Pergunte ao sindicato se haverá convenção ou acordo",
        "Defina a jornada: 8h por dia ou 8h24 com norma coletiva",
        "Cadastre horários e escalas no sistema de ponto",
        "Revise o divisor e envie a alteração contratual no eSocial",
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
    texto(d, y, "Sem norma coletiva, o que passar de 8 horas no dia tende a contar como hora extra.", size=62)
    rodape(d, "Fale com a Singular")
    img.save(path, quality=93)


if __name__ == "__main__":
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    story1(f"{out}/story1.jpg")
    story2(f"{out}/story2.jpg")
    from PIL import Image
    prev = sys.argv[2]
    os.makedirs(prev, exist_ok=True)
    for n in ("story1", "story2"):
        Image.open(f"{out}/{n}.jpg").resize((540, 960), Image.LANCZOS).save(f"{prev}/{n}.jpg", quality=82)
