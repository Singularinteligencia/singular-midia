"""Carrossel 'Fim da escala 6x1' (16/10/2026): padrão Singular, painéis comparativos e exemplos de escala."""
import sys, os
sys.path.insert(0, "/home/claude")
from brand import *

SURF = (34, 34, 38)      # painel escuro
SURF2 = (46, 46, 52)
LINE = (70, 70, 76)
KICK = "FIM DA ESCALA 6X1"
TOTAL = 6


def rr(d, box, fill=None, outline=None, r=44, w=4):
    d.rounded_rectangle(box, r, fill=fill, outline=outline, width=w)


def titulo(d, y, partes, size=104, lh=124, maxw=W - 2 * MARGIN):
    """partes: lista de (texto, cor) numa frase; quebra preservando cor por palavra."""
    fb = f(BOLD, size)
    lines = []
    for k, (t, c) in enumerate(partes):
        cur, cw = [], 0
        if k and not partes[k - 1][0].endswith((".", "?", "!")) and lines:
            cur = lines.pop(); cw = sum(d.textlength(w_ + " ", font=fb) for w_, _ in cur)
        for w_ in t.split():
            ww = d.textlength(w_ + " ", font=fb)
            if cw + ww > maxw + d.textlength(" ", font=fb) and cur:
                lines.append(cur); cur, cw = [], 0
            cur.append((w_, c)); cw += ww
        if cur: lines.append(cur)
    for ln in lines:
        x = MARGIN
        for w_, c in ln:
            d.text((x, y), w_, font=fb, fill=c); x += d.textlength(w_ + " ", font=fb)
        y += lh
    return y


def par(d, y, txt, font, fill, maxw=W - 2 * MARGIN, lh=None, x=MARGIN):
    lh = lh or int(font.size * 1.42)
    for l in wrap(d, txt, font, maxw):
        d.text((x, y), l, font=font, fill=fill); y += lh
    return y


def dias(d, x, y, on, size=74, gap=12):
    """fileira SEG..DOM com dias ativos em laranja."""
    nomes = ["SEG", "TER", "QUA", "QUI", "SEX", "SÁB", "DOM"]
    for i, n in enumerate(nomes):
        bx = x + i * (size + gap)
        if i in on:
            rr(d, [bx, y, bx + size, y + size * 0.62], fill=ORANGE, r=12)
            d.text((bx + size / 2, y + size * 0.31), n, font=f(BOLD, 22), fill=(20, 20, 22), anchor="mm")
        else:
            rr(d, [bx, y, bx + size, y + size * 0.62], outline=LINE, r=12, w=3)
            d.text((bx + size / 2, y + size * 0.31), n, font=f(MED, 22), fill=DIM, anchor="mm")
    return y + size * 0.62


def capa(d):
    kicker(d, KICK)
    y = 760
    y = titulo(d, y, [("A 6x1 acabou no Senado.", WHITE), ("Sua folha está pronta para o 5x2?", ORANGE)], size=120, lh=142)
    y += 50
    y = par(d, y, "PEC aprovada em 14/10/2026 por 75 votos a 1. Agora vai à promulgação.", f(LIGHT, 52), GREY)
    d.text((MARGIN, H - 430), "arraste para o lado", font=f(REG, 42), fill=DIM)
    footer(d)


def comparativo(d):
    kicker(d, KICK); d.text((W - MARGIN, MARGIN - 20), "2/6", font=f(MED, 34), fill=DIM, anchor="ra")
    y = titulo(d, 430, [("O que muda na jornada", WHITE)], size=88, lh=104)
    top, bh = y + 70, 900
    gw = (W - 2 * MARGIN - 60) / 2
    for i, (lab, big, linhas, dark) in enumerate([
        ("COMO É HOJE", "6x1", ["44h semanais", "6 dias de trabalho", "1 folga por semana"], False),
        ("COMO VAI FICAR", "5x2", ["40h semanais", "5 dias de trabalho", "2 folgas remuneradas"], True)]):
        x0 = MARGIN + i * (gw + 60)
        rr(d, [x0, top, x0 + gw, top + bh], fill=SURF2 if dark else SURF, outline=ORANGE if dark else LINE, w=5 if dark else 3)
        tracked(d, (x0 + gw / 2, top + 90), lab, f(BOLD, 36), ORANGE if dark else GREY, 8, center=True)
        d.text((x0 + gw / 2, top + 330), big, font=f(BOLD, 250), fill=ORANGE if dark else WHITE, anchor="mm")
        yy = top + 560
        for k, l in enumerate(linhas):
            d.text((x0 + gw / 2, yy), l, font=f(BOLD if k == 0 else REG, 60 if k == 0 else 46), fill=WHITE if k == 0 else GREY, anchor="ma")
            yy += 100 if k == 0 else 74
    y = top + bh + 90
    for t in ["Sem redução de salário.", "Uma das folgas preferencialmente aos domingos.", "Até 8 horas por dia, com compensação por acordo ou convenção."]:
        check(d, MARGIN, y + 6, size=44, thick=11)
        y = par(d, y, t, f(MED, 48), WHITE, maxw=W - 2 * MARGIN - 90, x=MARGIN + 90) + 26
    footer(d)


def transicao(d):
    kicker(d, KICK); d.text((W - MARGIN, MARGIN - 20), "3/6", font=f(MED, 34), fill=DIM, anchor="ra")
    y = titulo(d, 430, [("Não vira tudo de uma vez", WHITE)], size=88, lh=104)
    y = par(d, y + 20, "As regras valem a partir da promulgação e publicação da emenda, em duas etapas.", f(LIGHT, 48), GREY)
    etapas = [("PROMULGAÇÃO", "Congresso publica a emenda. Começa a contagem.", False),
              ("2º MÊS", "Teto cai de 44h para 42h e a escala passa a ser 5x2, com duas folgas remuneradas.", True),
              ("14º MÊS", "Teto chega a 40h semanais.", True)]
    y += 90; x = MARGIN + 30
    for i, (t, txt, on) in enumerate(etapas):
        d.ellipse([x - 26, y - 26 + 30, x + 26, y + 26 + 30], fill=ORANGE if on else (20, 20, 22), outline=ORANGE, width=6)
        if i < len(etapas) - 1:
            d.line([(x, y + 62), (x, y + 300)], fill=LINE, width=6)
        tracked(d, (x + 80, y), t, f(BOLD, 44), ORANGE, 6)
        par(d, y + 74, txt, f(REG, 46), WHITE, maxw=W - 2 * MARGIN - 140, x=x + 80)
        y += 330
    rr(d, [MARGIN, y + 10, W - MARGIN, y + 300], fill=SURF, outline=LINE, w=3, r=36)
    par(d, y + 60, "Cláusulas de acordos coletivos que contrariem as novas regras perdem validade. Profissionais com nível superior e salário acima de 2,5 vezes o teto do INSS ficam de fora.", f(REG, 40), GREY, maxw=W - 2 * MARGIN - 120, x=MARGIN + 60)
    footer(d)


def exemplos(d):
    kicker(d, KICK); d.text((W - MARGIN, MARGIN - 20), "4/6", font=f(MED, 34), fill=DIM, anchor="ra")
    y = titulo(d, 430, [("Como fica na prática", WHITE)], size=88, lh=104)
    y = par(d, y + 10, "Exemplos de escala 5x2 para negócios diferentes.", f(LIGHT, 46), GREY)
    cards = [
        ("ESCRITÓRIO", "segunda a sexta", [("", [0, 1, 2, 3, 4], "08h às 17h")]),
        ("LOJA", "segunda a sábado", [("Equipe A", [0, 1, 2, 3, 4], "09h às 18h"), ("Equipe B", [1, 2, 3, 4, 5], "09h às 18h")]),
        ("SUPERMERCADO", "todos os dias", [("Equipe A", [0, 1, 2, 3, 4], "07h às 16h"), ("Equipe B", [2, 3, 4, 5, 6], "13h às 22h")]),
        ("POSTO 24H", "três turnos com revezamento", [("Manhã", None, "06h às 14h"), ("Tarde", None, "14h às 22h"), ("Noite", None, "22h às 06h")]),
    ]
    top = y + 60; gw = (W - 2 * MARGIN - 50) / 2; ch = 640
    for i, (nome, sub, linhas) in enumerate(cards):
        x0 = MARGIN + (i % 2) * (gw + 50); y0 = top + (i // 2) * (ch + 50)
        rr(d, [x0, y0, x0 + gw, y0 + ch], fill=SURF, outline=LINE, w=3, r=36)
        d.text((x0 + 50, y0 + 50), nome, font=f(BOLD, 50), fill=WHITE)
        d.text((x0 + 50, y0 + 118), sub, font=f(REG, 34), fill=GREY)
        yy = y0 + 200
        for lab, on, hora in linhas:
            if on is not None:
                if lab:
                    d.text((x0 + 50, yy), lab, font=f(MED, 30), fill=GREY); yy += 46
                dias(d, x0 + 50, yy, on, size=78, gap=10); yy += 64
                d.text((x0 + 50, yy), hora + "  ·  1h de intervalo", font=f(MED, 34), fill=ORANGE); yy += 70
            else:
                d.text((x0 + 50, yy), lab, font=f(MED, 34), fill=GREY)
                d.text((x0 + gw - 50, yy), hora, font=f(BOLD, 40), fill=ORANGE, anchor="ra"); yy += 112
    footer(d)


def folha(d):
    kicker(d, KICK); d.text((W - MARGIN, MARGIN - 20), "5/6", font=f(MED, 34), fill=DIM, anchor="ra")
    y = titulo(d, 430, [("O que ajustar no ", WHITE), ("sistema de folha e ponto", ORANGE)], size=88, lh=106)
    itens = ["Jornadas e horários contratuais de cada funcionário",
             "Escalas de revezamento e equipes A e B",
             "Divisor de horas: de 220 para 200 na jornada de 40h",
             "Base de horas extras, DSR e adicional noturno",
             "Banco de horas e regras de compensação",
             "Alteração contratual de jornada enviada ao eSocial",
             "Convenção coletiva revisada com o sindicato"]
    y += 90
    for t in itens:
        check(d, MARGIN, y + 6, size=46, thick=12)
        y = par(d, y, t, f(MED, 50), WHITE, maxw=W - 2 * MARGIN - 100, x=MARGIN + 100) + 46
    footer(d)


def fecho(d):
    kicker(d, KICK); d.text((W - MARGIN, MARGIN - 20), "6/6", font=f(MED, 34), fill=DIM, anchor="ra")
    y = titulo(d, 800, [("Ajuste o cadastro antes da vigência.", WHITE), ("E não recalcule a folha depois.", ORANGE)], size=112, lh=134)
    par(d, y + 60, "A Singular revisa jornadas, escalas e eventos da sua folha para a transição.", f(LIGHT, 50), GREY)
    d.text((MARGIN, H - 450), "Sua empresa ainda trabalha na 6x1? Conta aqui.", font=f(MED, 44), fill=GREY)
    footer(d)


def story(path):
    from PIL import Image as I
    SW, SH = 1080 * 2, 1920 * 2
    img = background().resize((SW, SH))
    d = ImageDraw.Draw(img)
    tracked(d, (MARGIN, 520), KICK, f(BOLD, 44), ORANGE, 8)
    y = 760
    for t, c in [("A 6x1 acabou", WHITE), ("no Senado.", WHITE), ("E agora,", ORANGE), ("sua folha?", ORANGE)]:
        d.text((MARGIN, y), t, font=f(BOLD, 170), fill=c); y += 200
    y += 80
    for l in wrap(d, "Jornada de 40h e escala 5x2, em etapas, depois da promulgação. Veja no post o que muda e o que ajustar.", f(LIGHT, 64), SW - 2 * MARGIN):
        d.text((MARGIN, y), l, font=f(LIGHT, 64), fill=GREY); y += 92
    rr(d, [MARGIN, SH - 1000, SW - MARGIN, SH - 820], fill=ORANGE, r=90)
    d.text((SW / 2, SH - 910), "Novo post no perfil", font=f(BOLD, 70), fill=(20, 20, 22), anchor="mm")
    tracked(d, (SW / 2, SH - 560), "SINGULAR", f(BOLD, 80), ORANGE, 30, center=True)
    d.text((SW / 2, SH - 440), "@singularinteligencia", font=f(REG, 48), fill=DIM, anchor="ma")
    img.save(path, quality=93)


def story_lista(path, kick, tit, itens, rodape):
    SW, SH = 1080 * 2, 1920 * 2
    img = background().resize((SW, SH)); d = ImageDraw.Draw(img)
    tracked(d, (MARGIN, 460), kick, f(BOLD, 44), ORANGE, 8)
    y = 640
    for t, c in tit:
        d.text((MARGIN, y), t, font=f(BOLD, 140), fill=c); y += 168
    y += 110
    for num, t in itens:
        if num:
            d.ellipse([MARGIN, y, MARGIN + 110, y + 110], fill=ORANGE)
            d.text((MARGIN + 55, y + 55), num, font=f(BOLD, 56), fill=(20, 20, 22), anchor="mm")
        else:
            check(d, MARGIN + 10, y + 20, size=70, thick=16)
        yy = y + 12
        for l in wrap(d, t, f(MED, 66), SW - 2 * MARGIN - 170):
            d.text((MARGIN + 170, yy), l, font=f(MED, 66), fill=WHITE); yy += 90
        y = max(y + 150, yy + 60)
    d.text((MARGIN, SH - 1000), rodape, font=f(REG, 56), fill=GREY)
    tracked(d, (SW / 2, SH - 560), "SINGULAR", f(BOLD, 80), ORANGE, 30, center=True)
    d.text((SW / 2, SH - 440), "@singularinteligencia", font=f(REG, 48), fill=DIM, anchor="ma")
    img.save(path, quality=93)


if __name__ == "__main__":
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    for i, fn in enumerate([capa, comparativo, transicao, exemplos, folha, fecho], 1):
        card(f"{out}/{i}.jpg", fn)
    story(f"{out}/story.jpg")
    story_lista(f"{out}/story2.jpg", "FIM DA 6X1: COMO SE PREPARAR", [("Comece pela", WHITE), ("folha e ponto.", ORANGE)],
        [("", "Liste quem trabalha na 6x1 hoje"), ("", "Desenhe as novas escalas 5x2"), ("", "Atualize jornadas no sistema"), ("", "Revise divisor, extras e DSR"), ("", "Envie a alteração de jornada ao eSocial")],
        "Checklist completo no post de ontem.")
    story_lista(f"{out}/story3.jpg", "FIM DA 6X1: O CALENDÁRIO", [("Não muda", WHITE), ("de uma vez.", ORANGE)],
        [("1", "Promulgação e publicação da emenda"), ("2", "2º mês: 42h semanais e escala 5x2"), ("3", "14º mês: 40h semanais")],
        "Sem redução de salário.")
    print("ok")
