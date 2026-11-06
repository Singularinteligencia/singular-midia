"""Stories 'Fim da 6x1: CNC e CNI no STF' (06/11/2026). Base visual: fim6x1_excecoes."""
import sys, os
sys.path.insert(0, "/home/claude")
from brand import *
from fim6x1 import rr, SURF, LINE
from fim6x1_excecoes import base, rodape, texto, SW, SH, KICK


def story1(path):
    img, d = base(KICK)
    y = 640
    for t, c in [("Comércio e", WHITE), ("indústria vão", WHITE), ("ao STF.", ORANGE)]:
        d.text((MARGIN, y), t, font=f(BOLD, 170), fill=c); y += 200
    y += 90
    itens = [
        ("As ações", "CNC (ADI 8041, relator Flávio Dino) e CNI questionam a transição da EC 141."),
        ("O pedido", "A CNC quer 42 horas só em outubro de 2027 e 40 horas em outubro de 2028. A CNI pede ao menos um ano a mais e proteção a contratos e normas coletivas já assinados."),
        ("Hoje", "O STF ainda não decidiu. Sem decisão, a emenda segue valendo: 42 horas em 16/12."),
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
    texto(d, y, "Fontes: CBIC e Agência O Globo (5/11).", size=50, fill=DIM, gap=72)
    rodape(d)
    img.save(path, quality=93)


def story2(path):
    img, d = base("E O SEU DP?")
    y = 640
    for t, c in [("Não planeje", WHITE), ("contando com", WHITE), ("o adiamento.", ORANGE)]:
        d.text((MARGIN, y), t, font=f(BOLD, 170), fill=c); y += 200
    y += 70
    itens = [
        "Trabalhe com a data da emenda: 16/12",
        "Confira com o sindicato as normas coletivas em vigor",
        "Cadastre jornadas e escalas no ponto e na folha",
        "Acompanhe o decreto previsto para 09/11",
    ]
    for i, t in enumerate(itens, 1):
        lines = wrap(d, t, f(REG, 60), SW - 2 * MARGIN - 280)
        h = max(170, 70 + len(lines) * 84)
        rr(d, [MARGIN, y, SW - MARGIN, y + h], fill=SURF, r=40)
        d.text((MARGIN + 60, y + h / 2), f"0{i}", font=f(BOLD, 52), fill=ORANGE, anchor="lm")
        yy = y + (h - len(lines) * 84) / 2
        for l in lines:
            d.text((MARGIN + 200, yy), l, font=f(REG, 60), fill=WHITE); yy += 84
        y += h + 30
    y += 40
    texto(d, y, "Se o STF mudar o prazo, a preparação continua útil. Se não mudar, você já está pronto.", size=62)
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
