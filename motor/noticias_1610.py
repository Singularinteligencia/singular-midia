"""Notícias da semana 16/10: carrossel no padrão Singular."""
import sys
from PIL import ImageDraw
sys.path.insert(0, "/home/claude")
from brand import W, H, ORANGE, WHITE, GREY, DIM, MARGIN, BOLD, MED, REG, LIGHT, f, background, tracked, footer, wrap
OUT = "/mnt/user-data/outputs/singular_16-10_noticias"
KICK = "NOTÍCIAS DA SEMANA"

def topo(d, pag=None):
    tracked(d, (MARGIN, MARGIN - 26), KICK, f(BOLD, 38), ORANGE, 8)
    d.rectangle([MARGIN, MARGIN + 52, MARGIN + 110, MARGIN + 58], fill=ORANGE)
    if pag: d.text((W - MARGIN, MARGIN - 20), pag, font=f(MED, 34), fill=DIM, anchor="ra")

def bloco(d, txt, fo, cor, y, lh, larg=W - 2 * MARGIN):
    for l in wrap(d, txt, fo, larg):
        d.text((MARGIN, y), l, font=fo, fill=cor); y += lh
    return y

def capa():
    img = background(); d = ImageDraw.Draw(img); topo(d)
    y = 760
    for t, c in [("Quatro mudanças", WHITE), ("que chegam", WHITE), ("na sua rotina.", ORANGE)]:
        d.text((MARGIN, y), t, font=f(BOLD, 136), fill=c); y += 156
    y += 60
    bloco(d, "Simples Nacional, reforma tributária, eSocial e 13º: o que mudou nesta semana e o que fazer com isso.", f(LIGHT, 54), GREY, y, 76)
    d.text((MARGIN, H - 430), "arraste para o lado", font=f(REG, 42), fill=DIM)
    footer(d); img.save(f"{OUT}/1_capa.png", quality=95)

def item(n, tag, titulo, corpo, acao, nome):
    img = background(); d = ImageDraw.Draw(img); topo(d, f"{n}/6")
    L = W - 2 * MARGIN
    ft, fc, fa = f(BOLD, 112), f(LIGHT, 56), f(MED, 58)
    h = 110 + len(wrap(d, titulo, ft, L)) * 132 + 60 + len(wrap(d, corpo, fc, L)) * 82 + 110 + 100 + len(wrap(d, acao, fa, L)) * 82
    y = max(420, (H - 120 - h) // 2)
    tracked(d, (MARGIN, y), tag, f(BOLD, 46), ORANGE, 6); y += 110
    y = bloco(d, titulo, ft, WHITE, y, 132) + 60
    y = bloco(d, corpo, fc, GREY, y, 82) + 70
    d.rectangle([MARGIN, y, MARGIN + 110, y + 6], fill=ORANGE); y += 40
    d.text((MARGIN, y), "O QUE FAZER", font=f(BOLD, 40), fill=ORANGE)
    bloco(d, acao, fa, WHITE, y + 100, 82)
    footer(d); img.save(f"{OUT}/{nome}.png", quality=95)

def fecho():
    img = background(); d = ImageDraw.Draw(img); topo(d, "6/6")
    y = 860
    for t, c in [("Qual desses", WHITE), ("pega a sua", WHITE), ("empresa?", ORANGE)]:
        d.text((MARGIN, y), t, font=f(BOLD, 128), fill=c); y += 148
    y += 70
    bloco(d, "Conta nos comentários. E se precisar ajustar o sistema para alguma dessas mudanças, fale com a Singular pelo link da bio.", f(LIGHT, 52), GREY, y, 76)
    footer(d); img.save(f"{OUT}/6_fecho.png", quality=95)

capa()
item(2, "SIMPLES NACIONAL", "A opção para 2027 fechou ontem, 15/10.",
     "Quem quer recolher IBS e CBS pelo regime regular, o chamado Simples híbrido, ainda tem até 30 de outubro. É a mesma data limite para regularizar pendências.",
     "Confirmar com a contabilidade se a opção foi aceita e qual regime vale em 2027.", "2_simples")
item(3, "REFORMA TRIBUTÁRIA", "Faltam 77 dias para a CBS.",
     "O TCU tem até 30/10 para calcular a alíquota de referência; depois o Senado fixa o número. As alíquotas do Imposto Seletivo só devem ir ao Congresso após 25/10.",
     "Revisar cadastro de produtos e serviços agora, sem esperar a alíquota final.", "3_reforma")
item(4, "ESOCIAL", "Próxima etapa da NT 07/2026 em 26/10.",
     "A nota técnica que mexe em leiautes e validações segue escalonada: depois vêm 23/11, 14/12 e 18/01/2027.",
     "Confirmar a versão do sistema antes de cada virada e testar em produção restrita.", "4_esocial")
item(5, "13º SALÁRIO", "A segunda parcela sai até sexta, 18/12.",
     "Em 2026 o dia 20/12 cai num domingo, então o pagamento precisa ser antecipado. A primeira parcela continua até segunda, 30/11.",
     "Ajustar o calendário de pagamento e provisionar o caixa das duas parcelas.", "5_13o")
fecho()
print("ok")
