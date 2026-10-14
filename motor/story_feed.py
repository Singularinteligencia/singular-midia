"""Story 9:16 'novo no feed' com a capa do post, no padrão Singular."""
import sys, numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "/home/claude")
from brand import ORANGE, WHITE, GREY, DIM, BOLD, MED, REG, LIGHT, f, tracked
W, H = 1080, 1920
def fundo():
    y, x = np.mgrid[0:H, 0:W]
    g = (x / W) * 0.45 + (y / H) * 0.55
    base = 16 + g * 22
    img = np.dstack([base, base, base + 2])
    d = np.sqrt((x - W * 0.12) ** 2 + (y - H * 0.95) ** 2) / (W * 1.2)
    halo = np.clip(1 - d, 0, 1) ** 2.6 * 30
    img[:, :, 0] += halo; img[:, :, 1] += halo * 0.34
    img = img + np.random.normal(0, 2.4, (H, W, 1))
    return Image.fromarray(np.clip(img, 0, 255).astype("uint8"), "RGB")
def story(capa, kick, titulo, saida, rotulo="NOVO NO FEED"):
    img = fundo(); d = ImageDraw.Draw(img)
    tracked(d, (90, 250), rotulo, f(BOLD, 34), ORANGE, 8)
    d.rectangle([90, 304, 190, 309], fill=ORANGE)
    y = 360
    fo = f(BOLD, 64)
    for txt, cor in titulo:
        palavras, cur = txt.split(), ""
        for w_ in palavras:
            t = (cur + " " + w_).strip()
            if d.textlength(t, font=fo) <= W - 180 or not cur: cur = t
            else: d.text((90, y), cur, font=fo, fill=cor); y += 78; cur = w_
        if cur: d.text((90, y), cur, font=fo, fill=cor); y += 78
    c = Image.open(capa).convert("RGB"); disp = (H - 330) - (y + 50) - 110; larg = min(760, int(disp * c.width / c.height)); c = c.resize((larg, int(c.height * larg / c.width)), Image.LANCZOS)
    x0, y0 = (W - larg) // 2, y + 50
    sombra = Image.new("L", (W, H), 0); ImageDraw.Draw(sombra).rounded_rectangle([x0 + 10, y0 + 24, x0 + larg + 10, y0 + c.height + 24], 28, fill=150)
    img.paste((0, 0, 0), (0, 0), sombra.filter(ImageFilter.GaussianBlur(28)))
    m = Image.new("L", c.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, c.width - 1, c.height - 1], 24, fill=255)
    img.paste(c, (x0, y0), m)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([x0, y0, x0 + larg - 1, y0 + c.height - 1], 24, outline=ORANGE, width=4)
    yb = y0 + c.height + 70
    d.text((W / 2, yb), "Toque no perfil para ver o post completo", font=f(REG, 36), fill=GREY, anchor="ma")
    tracked(d, (W / 2, H - 230), "SINGULAR", f(BOLD, 48), ORANGE, 20, center=True)
    d.text((W / 2, H - 165), "@singularinteligencia", font=f(REG, 30), fill=DIM, anchor="ma")
    img.save(saida, quality=92)
if __name__ == "__main__":
    O = "/home/claude/singular-midia/posts"
    story(f"{O}/2026-10-15-cadastro/1_capa.jpg", "", [("Outubro é o mês", WHITE), ("de arrumar o cadastro.", ORANGE)], f"{O}/2026-10-15-cadastro/story.jpg")
    story(f"{O}/2026-10-20-alerta/1_capa.jpg", "", [("INSS e FGTS não batem?", WHITE), ("A causa está na folha.", ORANGE)], f"{O}/2026-10-20-alerta/story.jpg", "ALERTA DA OPERAÇÃO")
    story(f"{O}/2026-10-22-13o/1_capa.jpg", "", [("13º: primeira parcela", WHITE), ("vence em 30/11.", ORANGE)], f"{O}/2026-10-22-13o/story.jpg")
