"""Alerta da Operação #01 (20/10): diferenças de INSS e FGTS na DCTFWeb e no FGTS Digital."""
import os
import sys
from PIL import ImageDraw

sys.path.insert(0, "/home/claude")
from brand import (W, H, ORANGE, WHITE, GREY, DIM, MARGIN, BOLD, MED, REG, LIGHT, f, background, tracked,
                   footer, wrap, check)

SAIDA = "/mnt/user-data/outputs/singular_20-10_alerta"
os.makedirs(SAIDA, exist_ok=True)


def selo(d, pagina=None):
    """Selo do pilar: triângulo de alerta + 'ALERTA DA OPERAÇÃO' com filete."""
    x, y = MARGIN, MARGIN - 30
    d.polygon([(x, y + 46), (x + 26, y), (x + 52, y + 46)], fill=ORANGE)
    d.rectangle([x + 23, y + 14, x + 29, y + 32], fill=(20, 20, 22))
    d.rectangle([x + 23, y + 36, x + 29, y + 41], fill=(20, 20, 22))
    tracked(d, (x + 74, y + 2), "ALERTA DA OPERAÇÃO", f(BOLD, 38), ORANGE, 8)
    d.rectangle([MARGIN, MARGIN + 52, MARGIN + 110, MARGIN + 58], fill=ORANGE)
    if pagina:
        d.text((W - MARGIN, MARGIN - 20), pagina, font=f(MED, 34), fill=DIM, anchor="ra")


def bloco(d, linhas, y, fonte, lh, larg=W - 2 * MARGIN):
    for txt, cor in linhas:
        for l in wrap(d, txt, fonte, larg):
            d.text((MARGIN, y), l, font=fonte, fill=cor)
            y += lh
    return y


def salva(img, nome):
    img.save(f"{SAIDA}/{nome}", quality=95)


# 1. capa
img = background()
d = ImageDraw.Draw(img)
selo(d)
y = 700
y = bloco(d, [("INSS e FGTS", WHITE), ("não batem na", WHITE), ("DCTFWeb e no", ORANGE), ("FGTS Digital?", ORANGE)],
          y, f(BOLD, 136), 156)
y += 70
bloco(d, [("Vimos isso em vários fechamentos este ano. Quase sempre a causa está na folha, não na guia.", GREY)],
      y, f(LIGHT, 54), 76)
d.text((MARGIN, H - 430), "arraste para o lado", font=f(REG, 42), fill=DIM)
footer(d)
salva(img, "1_capa.png")

# 2. de onde vem a diferença
CAUSAS = [
    ("Rubrica com incidência errada",
     "A base do INSS e do FGTS sai do eSocial pela incidência de cada rubrica. Um código errado muda o valor sem ninguém ver."),
    ("13º e reflexos fora do lugar",
     "O 13º tem incidência própria, e o reflexo no aviso-prévio indenizado tem outra. Misturar as duas gera diferença."),
    ("Dissídio e retroativos",
     "Diferenças salariais têm regra própria de competência. Lançadas no mês errado, as bases deixam de bater."),
    ("Folha recalculada depois do envio",
     "Ajuste feito depois de transmitir a remuneração, sem retransmitir o evento, deixa a folha e o eSocial diferentes."),
    ("Rescisão no começo do mês",
     "Desligamento entre os dias 1 e 9 antecipa o prazo do FGTS do mês anterior, que segue o prazo rescisório."),
]
img = background()
d = ImageDraw.Draw(img)
selo(d, "2/4")
d.text((MARGIN, 360), "De onde a diferença", font=f(BOLD, 92), fill=WHITE)
d.text((MARGIN, 466), "costuma vir", font=f(BOLD, 92), fill=ORANGE)
y = 690
for k, (t, s) in enumerate(CAUSAS):
    d.text((MARGIN, y), f"0{k + 1}", font=f(BOLD, 58), fill=ORANGE)
    yy = y
    for l in wrap(d, t, f(BOLD, 58), W - 2 * MARGIN - 120):
        d.text((MARGIN + 120, yy), l, font=f(BOLD, 58), fill=WHITE)
        yy += 72
    for l in wrap(d, s, f(LIGHT, 42), W - 2 * MARGIN - 120):
        d.text((MARGIN + 120, yy + 4), l, font=f(LIGHT, 42), fill=GREY)
        yy += 58
    y = yy + 62
footer(d)
salva(img, "2_causas.png")

# 3. como evitar
PASSOS = [
    "Conferir as bases de INSS e FGTS do eSocial contra a folha antes de fechar",
    "Revisar a incidência de toda rubrica nova ou alterada",
    "Retransmitir os eventos depois de qualquer recálculo",
    "Lançar dissídio e retroativos na competência correta",
    "Acompanhar os prazos: FGTS no dia 20 e, na rescisão, em até 10 dias",
]
img = background()
d = ImageDraw.Draw(img)
selo(d, "3/4")
d.text((MARGIN, 360), "Como evitar", font=f(BOLD, 92), fill=WHITE)
d.text((MARGIN, 466), "no próximo fechamento", font=f(BOLD, 92), fill=ORANGE)
y = 720
for p in PASSOS:
    check(d, MARGIN, y + 8, size=50, thick=12)
    yy = y
    for l in wrap(d, p, f(MED, 54), W - 2 * MARGIN - 110):
        d.text((MARGIN + 100, yy), l, font=f(MED, 54), fill=WHITE)
        yy += 70
    y = yy + 64
footer(d)
salva(img, "3_como_evitar.png")

# 4. fecho
img = background()
d = ImageDraw.Draw(img)
selo(d, "4/4")
y = 820
y = bloco(d, [("Esse alerta nasceu", WHITE), ("da nossa operação.", WHITE)], y, f(BOLD, 116), 136)
y += 60
y = bloco(d, [("Se a sua guia não bate,", ORANGE), ("a gente encontra o porquê.", ORANGE)], y, f(BOLD, 84), 104)
y += 70
bloco(d, [("Salve este post para usar no próximo fechamento e fale com a Singular pelo link da bio.", GREY)],
      y, f(LIGHT, 50), 72)
footer(d)
salva(img, "4_fecho.png")
print("ok")
