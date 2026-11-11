"""Story 'Fim da 6x1: o que saiu da audiência no STF' (11/11/2026). Base visual: fim6x1_decreto."""
import sys, os
sys.path.insert(0, "/home/claude")
from brand import *
from fim6x1 import rr, SURF, LINE
from fim6x1_excecoes import base, rodape, texto, SW, SH, KICK


def story1(path):
    img, d = base(KICK)
    y = 600
    for t, c in [("Dino mantém", WHITE), ("as 42 horas", WHITE), ("em 16/12.", ORANGE)]:
        d.text((MARGIN, y), t, font=f(BOLD, 160), fill=c); y += 190
    y += 80
    itens = [
        ("A audiência", "Na conciliação de 10/11, o ministro Flávio Dino disse que o calendário da EC 141 não muda: 42 horas semanais em 16/12 e 40 horas em dezembro de 2027."),
        ("Sem salto para 40h", "Mesmo sem acordo coletivo, não há cenário de redução direta de 44 para 40 horas em dezembro."),
        ("O que pode flexibilizar", "Dino sinalizou que convenção coletiva poderá ampliar o prazo de compensação das folgas. A decisão formal ainda será publicada."),
    ]
    for tag, t in itens:
        lines = wrap(d, t, f(REG, 56), SW - 2 * MARGIN - 120)
        h = 150 + len(lines) * 80
        rr(d, [MARGIN, y, SW - MARGIN, y + h], fill=SURF, r=40)
        d.text((MARGIN + 60, y + 50), tag.upper(), font=f(BOLD, 44), fill=ORANGE)
        yy = y + 120
        for l in lines:
            d.text((MARGIN + 60, yy), l, font=f(REG, 56), fill=WHITE); yy += 80
        y += h + 40
    y += 30
    texto(d, y, "Fontes: Metrópoles e Agência Brasil (10/11).", size=50, fill=DIM, gap=72)
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
