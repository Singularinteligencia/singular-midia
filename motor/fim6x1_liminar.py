"""Carrossel + story 'Fim da 6x1: liminar de Dino define regras da transição' (13/11/2026).
Base visual: fim6x1_promulgacao (cards) e fim6x1_excecoes (story)."""
import sys, os
sys.path.insert(0, "/home/claude")
from brand import *
from fim6x1 import rr, titulo, par, SURF, LINE
from fim6x1_excecoes import base, rodape, texto, SW, SH

KICK = "FIM DA 6X1 · STF"
TOTAL = 5


def num(d, i):
    kicker(d, KICK)
    d.text((W - MARGIN, MARGIN - 20), f"{i}/{TOTAL}", font=f(MED, 34), fill=DIM, anchor="ra")


def capa(d):
    kicker(d, KICK)
    y = 640
    y = titulo(d, y, [("42 horas em", WHITE), ("5 dias de 8h24.", ORANGE)], size=130, lh=152)
    y += 60
    y = par(d, y, "Liminar do ministro Flávio Dino, de 12/11/2026, mantém a escala 5x2 a partir de 16/12 e define regras para a transição.", f(LIGHT, 54), GREY)
    d.text((MARGIN, H - 430), "arraste para o lado", font=f(REG, 42), fill=DIM)
    footer(d)


def jornada(d):
    num(d, 2)
    y = titulo(d, 430, [("A jornada na transição", WHITE)], size=92, lh=108)
    # bloco 8h24 x 5
    y += 70
    bw = (W - 2 * MARGIN - 4 * 30) / 5
    for i, dia in enumerate(["SEG", "TER", "QUA", "QUI", "SEX"]):
        x0 = MARGIN + i * (bw + 30)
        rr(d, [x0, y, x0 + bw, y + 230], fill=ORANGE, r=36)
        d.text((x0 + bw / 2, y + 70), dia, font=f(BOLD, 40), fill=(20, 20, 22), anchor="mm")
        d.text((x0 + bw / 2, y + 155), "8h24", font=f(BOLD, 62), fill=(20, 20, 22), anchor="mm")
    y += 270
    d.text((MARGIN, y), "= 42 horas por semana, com duas folgas remuneradas", font=f(MED, 48), fill=WHITE)
    y += 140
    itens = ["Vale de 16/12/2026 a 15/12/2027, mesmo sem acordo ou convenção coletiva.",
             "Os 24 minutos além da 8ª hora não são pagos como hora extra nesse período.",
             "Depois disso, o teto cai para 40 horas semanais.",
             "Sem redução de salário, inclusive dos pisos."]
    for t in itens:
        check(d, MARGIN, y + 14, size=52, thick=13)
        y = par(d, y, t, f(MED, 58), WHITE, maxw=W - 2 * MARGIN - 110, x=MARGIN + 110) + 70
    footer(d)


def coletivo(d):
    num(d, 3)
    y = titulo(d, 430, [("Folgas e normas ", WHITE), ("coletivas", ORANGE)], size=96, lh=112)
    blocos = [("FOLGAS", "Sem limite semanal ou mensal para conceder os descansos. Acordo ou convenção define a distribuição, garantidos os dois repousos remunerados."),
              ("90 DIAS", "A partir de 16/12, prazo para renegociar contrapartidas de acordos e convenções. Sem negociação, ministérios podem editar portaria conjunta provisória."),
              ("180 DIAS", "Para adaptar contratos administrativos e para o Congresso regulamentar regimes diferenciados e regras de micro e pequenas empresas.")]
    y += 90
    for tag, t in blocos:
        lines = wrap(d, t, f(REG, 52), W - 2 * MARGIN - 120)
        h = 150 + len(lines) * 74
        rr(d, [MARGIN, y, W - MARGIN, y + h], fill=SURF, r=40)
        d.text((MARGIN + 60, y + 48), tag, font=f(BOLD, 44), fill=ORANGE)
        yy = y + 120
        for l in lines:
            d.text((MARGIN + 60, yy), l, font=f(REG, 52), fill=WHITE); yy += 74
        y += h + 44
    footer(d)


def sistema(d):
    num(d, 4)
    y = titulo(d, 430, [("O que o DP ajusta no ", WHITE), ("sistema de folha e ponto", ORANGE)], size=88, lh=106)
    itens = [("1", "Cadastrar o horário 5x2 de 8h24 por dia (42h semanais)"),
             ("2", "Parametrizar o ponto para não gerar extra nos 24 minutos até 15/12/2027"),
             ("3", "Revisar divisor (220 vira 210), DSR das duas folgas e banco de horas"),
             ("4", "Enviar a alteração de jornada ao eSocial (S-2206)"),
             ("5", "Acompanhar o referendo do plenário do STF")]
    y += 100
    for n, t in itens:
        d.ellipse([MARGIN, y, MARGIN + 104, y + 104], fill=ORANGE)
        d.text((MARGIN + 52, y + 52), n, font=f(BOLD, 52), fill=(20, 20, 22), anchor="mm")
        y = par(d, y + 14, t, f(MED, 58), WHITE, maxw=W - 2 * MARGIN - 150, x=MARGIN + 150) + 90
    footer(d)


def fecho(d):
    num(d, 5)
    y = titulo(d, 820, [("16/12 continua valendo.", WHITE), ("Agora com regra clara.", ORANGE)], size=112, lh=134)
    par(d, y + 60, "A decisão ainda será submetida ao plenário do STF. A Singular ajusta jornadas, escalas e eventos da sua folha para a transição.", f(LIGHT, 50), GREY)
    d.text((MARGIN, H - 450), "Sua empresa vai usar 8h24 ou outro desenho? Conta aqui.", font=f(MED, 44), fill=GREY)
    footer(d)


def story1(path):
    img, d = base("FIM DA 6X1 · STF")
    y = 620
    for t, c in [("42 horas", WHITE), ("em 5 dias", WHITE), ("de 8h24.", ORANGE)]:
        d.text((MARGIN, y), t, font=f(BOLD, 170), fill=c); y += 200
    y += 80
    itens = [
        ("A liminar", "Flávio Dino manteve a 5x2 em 16/12 e autorizou jornada diária de até 8h24 até 15/12/2027, sem hora extra nos 24 minutos."),
        ("Normas coletivas", "90 dias a partir de 16/12 para renegociar contrapartidas. Folgas sem limite semanal ou mensal, garantidos os dois repousos."),
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
    y += 20
    texto(d, y, "Decisão de 12/11, ainda vai a referendo do plenário. Fonte: STF.", size=50, fill=DIM, gap=72)
    rodape(d, "Novo post no perfil")
    img.save(path, quality=93)


if __name__ == "__main__":
    out, prev = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True); os.makedirs(prev, exist_ok=True)
    from PIL import Image
    for i, fn in enumerate([capa, jornada, coletivo, sistema, fecho], 1):
        card(f"{out}/{i}.jpg", fn)
        Image.open(f"{out}/{i}.jpg").resize((540, 675), Image.LANCZOS).save(f"{prev}/{i}.jpg", quality=82)
    story1(f"{out}/story1.jpg")
    Image.open(f"{out}/story1.jpg").resize((540, 960), Image.LANCZOS).save(f"{prev}/story1.jpg", quality=82)
    print("ok")
