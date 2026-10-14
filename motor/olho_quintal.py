"""Olho do Especialista 14/10: Conheça o seu quintal (par do Reels do dia)."""
import os
import sys
from PIL import Image, ImageDraw

sys.path.insert(0, "/home/claude")
from brand import W, H, ORANGE, WHITE, GREY, DIM, MARGIN, BOLD, MED, REG, LIGHT, f, background, tracked, footer, wrap

SAIDA = "/mnt/user-data/outputs/singular_olho_quintal"
os.makedirs(SAIDA, exist_ok=True)

# avatar (mesmo do card anterior), recortado em círculo
ref = Image.open("/mnt/user-data/outputs/singular_olho_rh-ia/1_card.png").convert("RGB")
cx, cy, r = 290, 2279, 90
av = ref.crop((cx - r, cy - r, cx + r, cy + r))
mask = Image.new("L", av.size, 0)
ImageDraw.Draw(mask).ellipse([0, 0, 2 * r - 1, 2 * r - 1], fill=255)

ITENS = [
    ("Quanto custa, de verdade, cada colaborador?",
     "Salário é só o começo: encargos, benefícios, provisões e horas extras."),
    ("Quantas planilhas sustentam a operação?",
     "Cada planilha paralela é um processo que o sistema já deveria fazer."),
    ("O eSocial está em dia hoje?",
     "Pendência esquecida na fila de hoje vira multa amanhã."),
    ("Quem tem acesso a quê no sistema?",
     "Perfil de acesso desatualizado é risco de fraude e de vazamento."),
    ("Quanto do ERP você realmente usa?",
     "Módulo pago e parado é dinheiro guardado na gaveta."),
]

img = background()
d = ImageDraw.Draw(img)
tracked(d, (MARGIN, MARGIN - 26), "OLHO DO ESPECIALISTA", f(BOLD, 38), ORANGE, 8)
d.rectangle([MARGIN, MARGIN + 52, MARGIN + 110, MARGIN + 58], fill=ORANGE)

y = 380
d.text((MARGIN, y), "CONHEÇA O SEU QUINTAL", font=f(BOLD, 58), fill=ORANGE)
y += 90
for l in ["5 perguntas que todo", "gestor deveria responder"]:
    d.text((MARGIN, y), l, font=f(BOLD, 104), fill=WHITE)
    y += 118
y += 110

fn, fs = f(BOLD, 60), f(LIGHT, 45)
largura = W - MARGIN - (MARGIN + 110)
for k, (titulo, sub) in enumerate(ITENS):
    d.text((MARGIN, y), f"0{k + 1}", font=fn, fill=ORANGE)
    yy = y
    for l in wrap(d, titulo, fn, largura):
        d.text((MARGIN + 110, yy), l, font=fn, fill=WHITE)
        yy += 76
    for l in wrap(d, sub, fs, largura):
        d.text((MARGIN + 110, yy + 2), l, font=fs, fill=GREY)
        yy += 62
    y = yy + 104

# assinatura
ay = H - 520
d.ellipse([MARGIN - 7, ay - 7, MARGIN + 2 * r + 7, ay + 2 * r + 7], fill=ORANGE)
img.paste(av, (MARGIN, ay), mask)
d.text((MARGIN + 2 * r + 50, ay + 50), "Robert Santos", font=f(BOLD, 60), fill=WHITE)
d.text((MARGIN + 2 * r + 50, ay + 122), "Troubleshooter | Singular", font=f(REG, 44), fill=GREY)
footer(d)
img.save(f"{SAIDA}/1_card.png", quality=95)
print("ok", y)
