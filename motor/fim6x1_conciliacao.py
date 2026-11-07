"""Story 'Fim da 6x1: STF marca conciliação para 10/11' (07/11/2026). Base visual: fim6x1_stf."""
import sys, os
sys.path.insert(0, "/home/claude")
from brand import *
from fim6x1 import rr, SURF, LINE
from fim6x1_excecoes import base, rodape, texto, SW, SH, KICK


def story1(path):
    img, d = base(KICK)
    y = 640
    for t, c in [("STF marca", WHITE), ("conciliação", WHITE), ("para 10/11.", ORANGE)]:
        d.text((MARGIN, y), t, font=f(BOLD, 170), fill=c); y += 200
    y += 90
    itens = [
        ("A audiência", "Terça, 10/11, às 14h, na Primeira Turma do STF. Relator: ministro Flávio Dino."),
        ("Em discussão", "As ações da CNC (ADI 8041) e da CNI (ADI 8042), que pedem para adiar a transição da EC 141. Entidades de empregados e de empregadores foram convocadas."),
        ("Até lá", "Os pedidos de suspensão não foram decididos. Os prazos da emenda seguem valendo."),
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
    texto(d, y, "Fontes: Agência Brasil (5/11) e Rádio Peão Brasil (6/11).", size=50, fill=DIM, gap=72)
    rodape(d)
    img.save(path, quality=93)


if __name__ == "__main__":
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    story1(f"{out}/story1.jpg")
    from PIL import Image
    prev = sys.argv[2]
    os.makedirs(prev, exist_ok=True)
    Image.open(f"{out}/story1.jpg").resize((540, 960), Image.LANCZOS).save(f"{prev}/story1.jpg", quality=82)
