from PIL import Image, ImageDraw, ImageFont
import numpy as np

W, H = 2160, 2700
ORANGE = (255, 93, 2)
WHITE = (255, 255, 255)
GREY = (168, 168, 172)
DIM = (120, 120, 124)
MARGIN = 190

FD = "/usr/share/fonts/truetype/google-fonts/"
BOLD, MED, REG, LIGHT = "Poppins-Bold.ttf", "Poppins-Medium.ttf", "Poppins-Regular.ttf", "Poppins-Light.ttf"


def f(name, size):
    return ImageFont.truetype(FD + name, size)


def background():
    y, x = np.mgrid[0:H, 0:W]
    g = (x / W) * 0.45 + (y / H) * 0.55
    base = 16 + g * 22
    img = np.dstack([base, base, base + 2])
    d = np.sqrt((x - W * 0.12) ** 2 + (y - H * 0.95) ** 2) / (W * 0.95)
    halo = np.clip(1 - d, 0, 1) ** 2.6 * 26
    img[:, :, 0] += halo
    img[:, :, 1] += halo * 0.34
    img[:, :, 2] += halo * 0.02
    img = img + np.random.normal(0, 2.4, (H, W, 1))
    return Image.fromarray(np.clip(img, 0, 255).astype("uint8"), "RGB")


def tracked(draw, xy, text, font, fill, tracking, center=False):
    total = sum(draw.textlength(c, font=font) + tracking for c in text) - tracking
    x, y = xy
    if center:
        x -= total / 2
    for c in text:
        draw.text((x, y), c, font=font, fill=fill)
        x += draw.textlength(c, font=font) + tracking
    return total


def wrap(draw, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if draw.textlength(t, font=font) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def footer(draw, page=None):
    tracked(draw, (W / 2, H - 300), "SINGULAR", f(BOLD, 60), ORANGE, 26, center=True)
    draw.text((W / 2, H - 208), "@singularinteligencia", font=f(REG, 36), fill=DIM, anchor="ma")
    if page:
        draw.text((W - MARGIN, MARGIN - 20), page, font=f(MED, 34), fill=DIM, anchor="ra")


def kicker(draw, text):
    tracked(draw, (MARGIN, MARGIN - 26), text, f(BOLD, 38), ORANGE, 8)
    draw.rectangle([MARGIN, MARGIN + 52, MARGIN + 110, MARGIN + 58], fill=ORANGE)


def check(draw, x, y, size=46, color=ORANGE, thick=12):
    draw.line([(x, y + size * 0.55), (x + size * 0.36, y + size * 0.92)], fill=color, width=thick)
    draw.line([(x + size * 0.36, y + size * 0.92), (x + size, y + size * 0.08)], fill=color, width=thick)


def card(path, build):
    img = background()
    build(ImageDraw.Draw(img))
    img.save(path, quality=95)


def capa_faixa(foto, kick, linhas, sub=None, arraste=True, corte=1430,
               fx=0.50, fy=0.40, fonte=96, lh=114, saida=None):
    """Padrão Singular de capa com foto: imagem intacta em cima,
    filete laranja e bloco escuro com o texto embaixo."""
    img = background()
    im = Image.open(foto).convert("RGB")
    r = max(W / im.width, corte / im.height)
    im = im.resize((int(im.width * r), int(im.height * r)), Image.LANCZOS)
    left = int((im.width - W) * fx)
    top = int((im.height - corte) * fy)
    img.paste(im.crop((left, top, left + W, top + corte)), (0, 0))

    d = ImageDraw.Draw(img)
    d.rectangle([0, corte, W, corte + 10], fill=ORANGE)

    y = corte + 110
    tracked(d, (MARGIN, y), kick, f(BOLD, 38), ORANGE, 8)
    y += 120

    fb = f(BOLD, fonte)
    for texto, cor in linhas:
        if texto is None:
            y += 60
            continue
        for l in wrap(d, texto, fb, W - 2 * MARGIN):
            d.text((MARGIN, y), l, font=fb, fill=cor)
            y += lh

    if sub:
        y += 50
        for l in wrap(d, sub, f(LIGHT, 50), W - 2 * MARGIN):
            d.text((MARGIN, y), l, font=f(LIGHT, 50), fill=GREY)
            y += 70

    if arraste:
        d.text((MARGIN, H - 430), "arraste para o lado", font=f(REG, 42), fill=DIM)
    footer(d)
    if saida:
        img.save(saida, quality=95)
    return img
