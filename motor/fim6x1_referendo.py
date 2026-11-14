"""Story 'Fim da 6x1: STF tem 4 votos para manter a liminar de Dino' (14/11/2026). Base visual: fim6x1_audiencia."""
import sys, os
sys.path.insert(0, "/home/claude")
from brand import *
from fim6x1 import rr, SURF, LINE
from fim6x1_excecoes import base, rodape, texto, SW, SH


def story1(path):
    img, d = base("FIM DA 6X1 · STF")
    y = 600
    for t, c in [("4 votos para", WHITE), ("manter a regra", WHITE), ("de transição.", ORANGE)]:
        d.text((MARGIN, y), t, font=f(BOLD, 160), fill=c); y += 190
    y += 80
    itens = [
        ("O placar", "No plenário virtual, Flávio Dino, Alexandre de Moraes, Cármen Lúcia e Gilmar Mendes votaram para referendar a liminar. Nenhum voto contrário até agora."),
        ("O prazo", "A votação vai até segunda-feira, 16/11, às 11h. Ministros ainda podem votar, pedir vista ou destaque."),
        ("O que está em jogo", "42 horas em 16/12, jornada de até 8h24 em 5 dias sem hora extra nos 24 minutos e 90 dias para renegociar acordos e convenções."),
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
    texto(d, y, "Fontes: Correio Braziliense, CNN Brasil e Metrópoles (13/11).", size=50, fill=DIM, gap=72)
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
