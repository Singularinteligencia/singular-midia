"""Story 'Fim da 6x1: decreto adiado' (10/11/2026). Base visual: fim6x1_conciliacao."""
import sys, os
sys.path.insert(0, "/home/claude")
from brand import *
from fim6x1 import rr, SURF, LINE
from fim6x1_excecoes import base, rodape, texto, SW, SH, KICK


def story1(path):
    img, d = base(KICK)
    y = 640
    for t, c in [("Decreto da 6x1", WHITE), ("fica para", WHITE), ("depois.", ORANGE)]:
        d.text((MARGIN, y), t, font=f(BOLD, 160), fill=c); y += 190
    y += 90
    itens = [
        ("O que houve", "O decreto que regulamenta o fim da 6x1 era esperado para segunda, 9/11. O texto foi concluído pelos ministérios, mas ainda não foi aprovado pelo presidente."),
        ("Nova previsão", "Sem data exata. A publicação deve ocorrer depois da viagem de Lula à Turquia (COP31) e às Filipinas."),
        ("Para o DP", "A EC 141 já está promulgada e o decreto vem para detalhar as regras. Siga preparando escalas e jornadas no sistema de ponto e folha."),
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
    texto(d, y, "Fontes: CNN Brasil e Exame (9/11).", size=50, fill=DIM, gap=72)
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
