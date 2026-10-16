"""Carrossel 'Fim da 6x1: emenda promulgada' (16/10/2026). Base visual: fim6x1.py."""
import sys, os
sys.path.insert(0, "/home/claude")
from brand import *
from fim6x1 import rr, titulo, par, SURF, SURF2, LINE

KICK = "FIM DA ESCALA 6X1"
TOTAL = 5


def num(d, i):
    kicker(d, KICK)
    d.text((W - MARGIN, MARGIN - 20), f"{i}/{TOTAL}", font=f(MED, 34), fill=DIM, anchor="ra")


def capa(d):
    kicker(d, KICK)
    y = 700
    y = titulo(d, y, [("É oficial.", WHITE), ("A 6x1 tem prazo para acabar.", ORANGE)], size=124, lh=146)
    y += 60
    y = par(d, y, "O Congresso promulgou nesta sexta, 16/10/2026, a Emenda Constitucional 141. A escala 5x2 começa em dois meses.", f(LIGHT, 54), GREY)
    d.text((MARGIN, H - 430), "arraste para o lado", font=f(REG, 42), fill=DIM)
    footer(d)


def calendario(d):
    num(d, 2)
    y = titulo(d, 430, [("O calendário", WHITE)], size=96, lh=112)
    y = par(d, y + 10, "Os prazos contam a partir da publicação da emenda no Diário Oficial.", f(LIGHT, 48), GREY)
    etapas = [("16/10/2026", "Promulgação da Emenda Constitucional 141.", False),
              ("PUBLICAÇÃO NO DOU", "Começa a contagem da transição.", False),
              ("DEZEMBRO DE 2026", "Dois meses depois: teto cai de 44h para 42h e a escala passa a ser 5x2, com duas folgas remuneradas.", True),
              ("DEZEMBRO DE 2027", "Mais 12 meses: teto chega a 40h semanais.", True)]
    y += 100; x = MARGIN + 30
    for i, (t, txt, on) in enumerate(etapas):
        d.ellipse([x - 26, y + 4, x + 26, y + 56], fill=ORANGE if on else (20, 20, 22), outline=ORANGE, width=6)
        tracked(d, (x + 80, y), t, f(BOLD, 50), ORANGE if on else WHITE, 6)
        yy = par(d, y + 80, txt, f(REG, 54), WHITE if on else GREY, maxw=W - 2 * MARGIN - 140, x=x + 80)
        nxt = max(y + 290, yy + 100)
        if i < len(etapas) - 1:
            d.line([(x, y + 70), (x, nxt - 10)], fill=LINE, width=6)
        y = nxt
    d.text((MARGIN, y + 20), "Sem redução de salário.", font=f(BOLD, 52), fill=WHITE)
    footer(d)


def regras(d):
    num(d, 3)
    y = titulo(d, 430, [("O que muda na prática", WHITE)], size=92, lh=108)
    itens = ["Até 8 horas por dia e duas folgas remuneradas por semana.",
             "As folgas não precisam ser seguidas. Uma delas, preferencialmente no domingo.",
             "Domingo trabalhado sem folga compensatória é pago em dobro.",
             "Compensação e banco de horas seguem valendo, conforme lei, acordo ou convenção.",
             "12x36 e regimes diferenciados continuam permitidos.",
             "Vale para os contratos atuais, sem perda de férias, 13º ou FGTS."]
    y += 90
    for t in itens:
        check(d, MARGIN, y + 14, size=52, thick=13)
        y = par(d, y, t, f(MED, 60), WHITE, maxw=W - 2 * MARGIN - 110, x=MARGIN + 110) + 80
    footer(d)


def sistema(d):
    num(d, 4)
    y = titulo(d, 430, [("O que o DP faz agora no ", WHITE), ("sistema de folha e ponto", ORANGE)], size=88, lh=106)
    itens = [("1", "Listar quem está hoje na 6x1 e nas 44h"),
             ("2", "Cadastrar as jornadas de 42h e os novos horários"),
             ("3", "Montar as escalas 5x2 e de revezamento"),
             ("4", "Revisar divisor (220 vira 210 nas 42h), extras, DSR e banco de horas"),
             ("5", "Enviar a alteração contratual de jornada ao eSocial (S-2206)")]
    y += 100
    for n, t in itens:
        d.ellipse([MARGIN, y, MARGIN + 104, y + 104], fill=ORANGE)
        d.text((MARGIN + 52, y + 52), n, font=f(BOLD, 52), fill=(20, 20, 22), anchor="mm")
        y = par(d, y + 14, t, f(MED, 60), WHITE, maxw=W - 2 * MARGIN - 150, x=MARGIN + 150) + 100
    footer(d)


def fecho(d):
    num(d, 5)
    y = titulo(d, 820, [("Dezembro está logo ali.", WHITE), ("Ajuste antes da folha virar.", ORANGE)], size=116, lh=138)
    par(d, y + 60, "A Singular revisa jornadas, escalas e eventos da sua folha para a transição.", f(LIGHT, 50), GREY)
    d.text((MARGIN, H - 450), "Sua empresa já começou a se preparar? Conta aqui.", font=f(MED, 44), fill=GREY)
    footer(d)


def story(path):
    SW, SH = 1080 * 2, 1920 * 2
    img = background().resize((SW, SH)); d = ImageDraw.Draw(img)
    tracked(d, (MARGIN, 520), KICK, f(BOLD, 44), ORANGE, 8)
    y = 760
    for t, c in [("É oficial.", WHITE), ("Emenda", WHITE), ("promulgada.", WHITE), ("5x2 em", ORANGE), ("dezembro.", ORANGE)]:
        d.text((MARGIN, y), t, font=f(BOLD, 170), fill=c); y += 200
    y += 80
    for l in wrap(d, "Emenda Constitucional 141, de 16/10/2026. Veja no post o calendário e o que ajustar na folha.", f(LIGHT, 64), SW - 2 * MARGIN):
        d.text((MARGIN, y), l, font=f(LIGHT, 64), fill=GREY); y += 92
    rr(d, [MARGIN, SH - 1000, SW - MARGIN, SH - 820], fill=ORANGE, r=90)
    d.text((SW / 2, SH - 910), "Novo post no perfil", font=f(BOLD, 70), fill=(20, 20, 22), anchor="mm")
    tracked(d, (SW / 2, SH - 560), "SINGULAR", f(BOLD, 80), ORANGE, 30, center=True)
    d.text((SW / 2, SH - 440), "@singularinteligencia", font=f(REG, 48), fill=DIM, anchor="ma")
    img.save(path, quality=93)


if __name__ == "__main__":
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    for i, fn in enumerate([capa, calendario, regras, sistema, fecho], 1):
        card(f"{out}/{i}.jpg", fn)
    story(f"{out}/story.jpg")
    print("ok")
