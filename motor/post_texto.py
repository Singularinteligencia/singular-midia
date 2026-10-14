"""Carrossel 'post de texto' (estilo publicação de rede social): fundo preto, avatar, nome e texto."""
import sys
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, "/home/claude")
from brand import ORANGE
S = 2
W, H = 1080 * S, 1350 * S
FD = "/usr/share/fonts/truetype/google-fonts/"
F = lambda n, s: ImageFont.truetype(FD + n, int(s * S))
BRANCO, CINZA = (236, 236, 238), (125, 125, 132)
MX = 70 * S

def avatar():
    ref = Image.open("/mnt/user-data/outputs/singular_olho_rh-ia/1_card.png").convert("RGB")
    cx, cy, r = 290, 2279, 90
    a = ref.crop((cx - r, cy - r, cx + r, cy + r)).resize((104 * S, 104 * S), Image.LANCZOS)
    m = Image.new("L", a.size, 0); ImageDraw.Draw(m).ellipse([0, 0, a.width - 1, a.height - 1], fill=255)
    return a, m

def quebra(d, txt, fo, larg):
    out = []
    for par in txt.split("\n"):
        if not par.strip():
            out.append(""); continue
        cur = ""
        for w in par.split():
            t = (cur + " " + w).strip()
            if d.textlength(t, font=fo) <= larg or not cur: cur = t
            else: out.append(cur); cur = w
        out.append(cur)
    return out

def card(texto, n, total, saida, foto=None):
    img = Image.new("RGB", (W, H), (0, 0, 0)); d = ImageDraw.Draw(img)
    fo = F("Poppins-Regular.ttf", 41); lh = int(58 * S)
    linhas = quebra(d, texto, fo, W - 2 * MX)
    alt_txt = sum(lh if l else int(lh * 0.6) for l in linhas)
    alt_foto = 0
    if foto:
        fw = W - 2 * MX; ft = Image.open(foto).convert("RGB")
        fh = int(fw * 0.56); ft = ft.resize((fw, int(ft.height * fw / ft.width)), Image.LANCZOS)
        if ft.height > fh:
            o = (ft.height - fh) // 2; ft = ft.crop((0, o, fw, o + fh))
        alt_foto = ft.height + 50 * S
    bloco = 104 * S + 50 * S + alt_txt + alt_foto
    y = max(110 * S, (H - bloco) // 2)
    a, m = avatar()
    d.ellipse([MX - 5 * S, y - 5 * S, MX + 109 * S, y + 109 * S], fill=ORANGE)
    img.paste(a, (MX, y), m)
    d.text((MX + 132 * S, y + 14 * S), "Robert Santos", font=F("Poppins-Bold.ttf", 36), fill=BRANCO)
    d.text((MX + 132 * S, y + 60 * S), "@singularinteligencia", font=F("Poppins-Regular.ttf", 30), fill=CINZA)
    y += 104 * S + 50 * S
    for l in linhas:
        if l: d.text((MX, y), l, font=fo, fill=BRANCO); y += lh
        else: y += int(lh * 0.6)
    if foto:
        y += 30 * S
        lim = H - 90 * S - y
        if ft.height > lim:
            o = (ft.height - lim) // 2; ft = ft.crop((0, o, ft.width, o + lim))
        mk = Image.new("L", ft.size, 0); ImageDraw.Draw(mk).rounded_rectangle([0, 0, ft.width - 1, ft.height - 1], 28 * S, fill=255)
        img.paste(ft, (MX, y), mk)
    if n > 1:
        d.text((W - MX, 80 * S), f"{n}/{total}", font=F("Poppins-Regular.ttf", 30), fill=CINZA, anchor="ra")
    img.save(saida, quality=95)

TXT = [
"Há exatos 50 anos, Milton Friedman ganhava o Nobel de Economia.\n\nPoucos lembram que, antes disso, ele ajudou a criar o imposto descontado direto no salário.\n\nE é por isso que a sua folha de pagamento virou uma das maiores máquinas de arrecadação do país.",
"Em 1942, trabalhando no Tesouro americano, ele participou do desenho da retenção na fonte. A ideia era financiar a guerra sem esperar a declaração do ano seguinte.\n\nFuncionou tão bem que virou padrão no mundo inteiro. Anos depois, ele próprio reconheceu que a ferramenta ajudou o governo a crescer além do que ele defendia.\n\nAgora olha para a sua folha.",
"No Brasil, o imposto sai antes de o salário chegar.\n\nIR e INSS são descontados e recolhidos pela empresa, e o FGTS vai junto.\n\nO funcionário enxerga o líquido. A Receita enxerga o seu cadastro.\n\nQuem retém é a empresa. E quem responde pelo erro também.",
"E 2026 mudou a conta.\n\nCom a isenção do IR para quem ganha até R$ 5 mil, a retenção passou a ter um redutor no meio do cálculo.\n\nRubrica com incidência errada, dependente desatualizado ou pensão fora da base fazem esse redutor sair errado todo mês, sem dar erro nenhum na tela.",
"O que eu faria agora: conferir a retenção de outubro de uma amostra de funcionários contra a regra de 2026, antes do 13º e das férias de dezembro.\n\nFriedman criou a retenção para o governo não precisar esperar. Na sua folha, quem não pode esperar é a conferência.\n\nComenta aí: sua empresa já conferiu o IR da folha depois da isenção?",
]
if __name__ == "__main__":
    O = "/mnt/user-data/outputs/singular_friedman"
    for i, t in enumerate(TXT):
        card(t, i + 1, len(TXT), f"{O}/{i+1}.png", foto="/home/claude/fotos/holerite.png" if i == 0 else None)
    print("ok")
