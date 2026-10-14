"""Capa do Alerta 20/10 com foto gerada no Canva (padrão faixa sólida)."""
import sys; sys.path.insert(0, "/home/claude")
from brand import *
from PIL import ImageDraw
img = capa_faixa("/home/claude/fotos/alerta_dp_noite.png", "",
    [("INSS e FGTS não batem na", WHITE), ("DCTFWeb e no FGTS Digital?", ORANGE)],
    sub="Vimos isso em vários fechamentos este ano. Quase sempre a causa está na folha, não na guia.",
    corte=1430, fy=0.35, fonte=100, lh=120)
d = ImageDraw.Draw(img)
x, y = MARGIN, 1430 + 104
d.polygon([(x, y + 46), (x + 26, y), (x + 52, y + 46)], fill=ORANGE)
d.rectangle([x + 23, y + 14, x + 29, y + 32], fill=(20, 20, 22))
d.rectangle([x + 23, y + 36, x + 29, y + 41], fill=(20, 20, 22))
tracked(d, (x + 74, y + 2), "ALERTA DA OPERAÇÃO", f(BOLD, 38), ORANGE, 8)
img.save("/mnt/user-data/outputs/singular_20-10_alerta/1_capa.png", quality=95)
