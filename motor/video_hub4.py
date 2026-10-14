"""Reels Singular v3: hub de inteligência com narração (voz B), trilha estilo
breaking news, telas de 'o que fazemos' e segmentos, e trocas de tela com impacto."""
import json
import math
import subprocess
import sys
import numpy as np
import soundfile as sf
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, "/home/claude")
from musica_news import gera, SR, BEAT

W, H, FPS = 1080, 1920, 30
ORANGE = (255, 93, 2)
WHITE = (255, 255, 255)
GREY = (176, 176, 181)
DIM = (120, 120, 126)
LINE = (78, 78, 86)
MG = 100
RNG = np.random.default_rng(21)

# ============================================================== tempos
# Sem narração: tudo amarrado à grade da trilha (120 bpm, tempo = 0,5 s, compasso = 2 s).
INICIO_MUS = 1.0
bt = lambda n: INICIO_MUS + n * BEAT          # n-ésimo tempo da música
TR = [bt(12), bt(28), bt(52), bt(68), bt(88), bt(104)]
TR_QUEM, TR_FAZ, TR_SEG, TR_MAPA, TR_IMP, TR_FIM = TR
VIRADAS_BRUTAS, FINAL_BRUTO = TR[:-1], TR[-1]
DUR = TR_FIM + 5.0

T_MENTES, T_NECES = bt(0), bt(4)
T_PONTE = bt(8)
T_QUEM = TR_QUEM + 0.5
T_RISCO = bt(16)
T_SOMOS = bt(20)
T_HUB = bt(22)
T_FAZ = TR_FAZ + 0.5
T_MOD = [bt(32), bt(36), bt(40), bt(44)]
T_SEGS = [bt(56 + i) for i in range(8)]
T_MIG0 = TR_MAPA + 0.05
T_MIG1 = bt(71)
T_ORIGEM = bt(72)
T_FIMPROP = bt(80)
T_NORTE = bt(80)
T_NOMES = [bt(92), bt(94), bt(96), bt(98)]
T_FIMHUB = bt(106)


def pulso(t):
    """Batida da trilha: 1 no bumbo, decai rápido. Antes da 1ª virada o bumbo
    cai só nos tempos 1 e 3; depois, em todos. Cabeça de compasso mais forte."""
    if t < INICIO_MUS or t > TR_FIM:
        return 0.0
    n = int((t - INICIO_MUS) / BEAT)
    if t < TR_QUEM and n % 2:
        n -= 1
    dt = t - bt(n)
    forca = 1.0 if n % 4 == 0 else 0.6
    return forca * math.exp(-dt * 9)


q8 = lambda x: INICIO_MUS + round((x - INICIO_MUS) / (BEAT / 2)) * (BEAT / 2)

# ============================================================== fontes
PF = "/usr/share/fonts/truetype/google-fonts/"
MF = "/usr/share/fonts/truetype/dejavu/"
_fc = {}


def fnt(c, s):
    if (c, s) not in _fc:
        _fc[(c, s)] = ImageFont.truetype(c, s)
    return _fc[(c, s)]


BOLD = lambda s: fnt(PF + "Poppins-Bold.ttf", s)
MED = lambda s: fnt(PF + "Poppins-Medium.ttf", s)
REG = lambda s: fnt(PF + "Poppins-Regular.ttf", s)
LIGHT = lambda s: fnt(PF + "Poppins-Light.ttf", s)
MONO = lambda s: fnt(MF + "DejaVuSansMono.ttf", s)
MONOB = lambda s: fnt(MF + "DejaVuSansMono-Bold.ttf", s)


# ============================================================ utilidades
def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease(p):
    p = clamp(p)
    return 1 - (1 - p) ** 3


def ease_in(p):
    p = clamp(p)
    return p ** 3


def ease_io(p):
    p = clamp(p)
    return 3 * p * p - 2 * p ** 3


def entrada(t, t0, dur=0.5, dist=40):
    p = ease((t - t0) / dur)
    return p, (1 - p) * dist


def janela(t, t0, t1, fade=0.35):
    if t < t0 - fade or t > t1 + fade:
        return 0.0
    return min(clamp((t - t0 + fade) / fade), clamp((t1 + fade - t) / fade))


def rgba(c, a):
    return (int(c[0]), int(c[1]), int(c[2]), int(255 * clamp(a)))


def digitado(txt, t, t0, cps=28):
    return txt[: int(max(0.0, t - t0) * cps)]


def tracked(d, xy, txt, fonte, cor, trk, centro=False):
    larg = sum(d.textlength(ch, font=fonte) + trk for ch in txt) - trk
    x, y = xy
    if centro:
        x -= larg / 2
    for ch in txt:
        d.text((x, y), ch, font=fonte, fill=cor)
        x += d.textlength(ch, font=fonte) + trk


# ================================================================ fundo
PAN = 160


def gera_fundo():
    LW, LH = W + PAN, H + PAN
    y, x = np.mgrid[0:LH, 0:LW]
    g = (x / LW) * 0.45 + (y / LH) * 0.55
    base = 13 + g * 19
    img = np.dstack([base, base, base + 3])
    dd = np.sqrt((x - LW * 0.10) ** 2 + (y - LH * 0.96) ** 2) / (LW * 1.15)
    halo = np.clip(1 - dd, 0, 1) ** 2.4 * 28
    img[:, :, 0] += halo
    img[:, :, 1] += halo * 0.34
    passo = 72
    img[((x % passo) < 1) | ((y % passo) < 1)] += 6
    img[((x % passo) < 3) & ((y % passo) < 3)] += 14
    img += np.random.default_rng(5).normal(0, 2.0, (LH, LW, 1))
    return Image.fromarray(np.clip(img, 0, 255).astype("uint8"), "RGB")


BG = gera_fundo()


def brilho_sprite(r, inten):
    s = 2 * r
    y, x = np.mgrid[0:s, 0:s]
    dd = np.sqrt((x - r + 0.5) ** 2 + (y - r + 0.5) ** 2) / r
    a = np.clip(1 - dd, 0, 1) ** 2.2 * 255 * inten
    arr = np.zeros((s, s, 4), dtype="uint8")
    arr[:, :, 0], arr[:, :, 1], arr[:, :, 2] = 255, 120, 30
    arr[:, :, 3] = a.astype("uint8")
    return Image.fromarray(arr, "RGBA")


GLOW = [brilho_sprite(34, (i + 1) / 10) for i in range(10)]


def cola_brilho(img, x, y, inten):
    if inten < 0.05:
        return
    sp = GLOW[min(9, int(inten * 10))]
    r = sp.width // 2
    xi, yi = int(x - r), int(y - r)
    if 0 <= xi and 0 <= yi and xi + sp.width <= W and yi + sp.height <= H:
        img.alpha_composite(sp, (xi, yi))


# ================================================================= mapa
def area(r):
    s = 0.0
    for i in range(len(r)):
        x1, y1 = r[i]
        x2, y2 = r[(i + 1) % len(r)]
        s += x1 * y2 - x2 * y1
    return s / 2


def centroide(r):
    a = area(r)
    cx = cy = 0.0
    for i in range(len(r)):
        x1, y1 = r[i]
        x2, y2 = r[(i + 1) % len(r)]
        c = x1 * y2 - x2 * y1
        cx += (x1 + x2) * c
        cy += (y1 + y2) * c
    return (cx / (6 * a), cy / (6 * a))


def carrega_mapa():
    g = json.load(open("/home/claude/geo_dados/br_states.json"))
    kx = math.cos(math.radians(-15.0))
    estados = []
    for ft in g["features"]:
        gt, co = ft["geometry"]["type"], ft["geometry"]["coordinates"]
        polys = co if gt == "MultiPolygon" else [co]
        estados.append((ft["id"], [[(lon * kx, -lat) for lon, lat in poly[0]] for poly in polys]))
    xs = [p[0] for _, an in estados for r in an for p in r]
    ys = [p[1] for _, an in estados for r in an for p in r]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    esc = min(860 / (x1 - x0), 740 / (y1 - y0))
    ox, oy = (W - (x1 - x0) * esc) / 2, 480
    proj = lambda p: ((p[0] - x0) * esc + ox, (p[1] - y0) * esc + oy)
    saida = []
    for uf, aneis in estados:
        pa = [[proj(p) for p in r] for r in aneis]
        saida.append((uf, pa, centroide(max(pa, key=lambda r: abs(area(r))))))
    bh = proj((-43.94 * kx, 19.92))
    caixa = (int(ox) - 10, oy - 10, int(ox + (x1 - x0) * esc) + 10, int(oy + (y1 - y0) * esc) + 10)
    return saida, bh, caixa


ESTADOS, BH, CAIXA = carrega_mapa()
UFS = [e[0] for e in ESTADOS]
AJ = {"RJ": (6, -4), "ES": (4, 0), "SE": (2, 2), "AL": (4, 2), "PB": (6, 0), "RN": (4, 2), "PE": (-10, 2),
      "SC": (6, 0), "AP": (0, 6), "PA": (0, 10)}
CENTROS = [(e[2][0] + AJ.get(e[0], (0, 0))[0], e[2][1] + AJ.get(e[0], (0, 0))[1]) for e in ESTADOS]

CX0, CY0, CX1, CY1 = CAIXA
MW, MH = CX1 - CX0, CY1 - CY0
CONTORNO = Image.new("RGBA", (W, H), (0, 0, 0, 0))
dc = ImageDraw.Draw(CONTORNO)
INDICE = Image.new("L", (MW, MH), 0)
di = ImageDraw.Draw(INDICE)
for i, (uf, aneis, _) in enumerate(ESTADOS):
    for r in aneis:
        if len(r) >= 3:
            di.polygon([(x - CX0, y - CY0) for x, y in r], fill=i + 1)
for uf, aneis, _ in ESTADOS:
    for r in aneis:
        if len(r) >= 3:
            dc.line(r + [r[0]], fill=(150, 150, 158, 150), width=2)
IDX = np.asarray(INDICE)


# ============================================================ sinapses
def aglomerado(cx, cy, n, rx, ry):
    pts = []
    while len(pts) < n:
        x, y = RNG.normal(cx, rx), RNG.normal(cy, ry)
        if all(math.hypot(x - a, y - b) > 58 for a, b in pts) and 140 < x < W - 140 and 900 < y < 1400:
            pts.append((x, y))
    return pts


NOS1 = aglomerado(330, 1150, 22, 120, 150) + aglomerado(750, 1150, 22, 120, 150)
N1 = len(NOS1)


def vizinhos(pts, k, faixa=None):
    ar = set()
    idxs = list(range(len(pts))) if faixa is None else faixa
    for i in idxs:
        ds = sorted((math.hypot(pts[i][0] - pts[j][0], pts[i][1] - pts[j][1]), j) for j in idxs if j != i)
        for _, j in ds[:k]:
            ar.add((min(i, j), max(i, j)))
    return sorted(ar)


AR_ESQ = vizinhos(NOS1, 3, list(range(0, 22)))
AR_DIR = vizinhos(NOS1, 3, list(range(22, 44)))
pares = sorted((math.hypot(NOS1[i][0] - NOS1[j][0], NOS1[i][1] - NOS1[j][1]), i, j)
               for i in range(22) for j in range(22, 44))
PONTES, usados = [], set()
for _, i, j in pares:
    if i not in usados and j not in usados:
        PONTES.append((i, j))
        usados |= {i, j}
    if len(PONTES) == 7:
        break


def agenda_pulsos(arestas, t0, t1, taxa, dur=(0.45, 0.8)):
    ag, t = [], t0
    while t < t1:
        t += RNG.exponential(1 / taxa)
        i, j = arestas[RNG.integers(len(arestas))]
        if RNG.random() < 0.5:
            i, j = j, i
        du = RNG.uniform(*dur)
        ag.append((q8(t + du) - du, i, j, du))
    return ag


PULSOS1 = (agenda_pulsos(AR_ESQ, 0.4, T_MIG0 + 0.3, 3.0) + agenda_pulsos(AR_DIR, 0.4, T_MIG0 + 0.3, 3.0)
           + agenda_pulsos(PONTES, T_PONTE + 0.3, T_MIG0 + 0.3, 3.5, (0.5, 0.75)))
MIGRAM = list(RNG.choice(N1, 27, replace=False))

NOS_MAPA = CENTROS + [BH]
NB = len(NOS_MAPA) - 1
AR_MAPA = set(vizinhos(NOS_MAPA, 3))
fora, dentro = set(range(len(NOS_MAPA))) - {NB}, {NB}
while fora:
    _, a, b = min((math.hypot(NOS_MAPA[a][0] - NOS_MAPA[b][0], NOS_MAPA[a][1] - NOS_MAPA[b][1]), a, b)
                  for a in dentro for b in fora)
    AR_MAPA.add((min(a, b), max(a, b)))
    dentro.add(b)
    fora.discard(b)
AR_MAPA = sorted(AR_MAPA)
adj = {i: [] for i in range(len(NOS_MAPA))}
for a, b in AR_MAPA:
    w = math.hypot(NOS_MAPA[a][0] - NOS_MAPA[b][0], NOS_MAPA[a][1] - NOS_MAPA[b][1])
    adj[a].append((b, w))
    adj[b].append((a, w))
dist = {i: float("inf") for i in adj}
pai = {}
dist[NB] = 0.0
pend = set(adj)
while pend:
    u = min(pend, key=lambda k: dist[k])
    pend.discard(u)
    for v, w in adj[u]:
        if dist[u] + w < dist[v]:
            dist[v], pai[v] = dist[u] + w, u
dmax = max(dist.values())
CHEGADA = {i: T_ORIGEM + 0.35 + (T_FIMPROP - T_ORIGEM - 0.35) * (dist[i] / dmax) for i in dist}
CHEGADA[NB] = T_ORIGEM
PROP = [(CHEGADA[pai[v]], pai[v], v, CHEGADA[v] - CHEGADA[pai[v]]) for v in pai]
PULSOS_MAPA = agenda_pulsos(AR_MAPA, T_FIMPROP + 0.2, TR_IMP + 0.6, 4.0, (0.5, 0.9))


def desenha_pulso(d, a, b, p, alfa, raio=6):
    for k in range(7):
        qq = p - k * 0.045
        if qq < 0 or qq > 1:
            continue
        x, y = a[0] + (b[0] - a[0]) * qq, a[1] + (b[1] - a[1]) * qq
        r = raio * (1 - k * 0.11)
        d.ellipse([x - r, y - r, x + r, y + r],
                  fill=rgba((255, 150, 70) if k == 0 else ORANGE, alfa * (1 - k / 7)))


def pos_no1(i, t):
    x, y = NOS1[i]
    x += 7 * math.sin(t * 0.6 + i)
    y += 7 * math.cos(t * 0.5 + i * 1.3)
    if i in MIGRAM and t > T_MIG0:
        k = MIGRAM.index(i)
        p = ease_io((t - T_MIG0) / (T_MIG1 - T_MIG0))
        cx, cy = CENTROS[k]
        x, y = x + (cx - x) * p, y + (cy - y) * p
    return x, y


def rede_cena1(lay, d, t):
    if t > T_MIG1 + 0.2:
        return
    base = clamp((t - 0.2) / 0.8)
    recuo = 1 - 0.72 * clamp((t - (TR_QUEM - 0.2)) / 0.6)
    texto_denso = janela(t, TR_FAZ, TR_MAPA - 0.1, fade=0.3)        # some atrás dos módulos e segmentos
    recuo *= 1 - 0.85 * texto_denso
    volta = clamp((t - TR_MAPA) / 0.3)                               # reacende para migrar ao mapa
    recuo = max(recuo, volta * 0.9)
    some = 1 - clamp((t - T_MIG0) / 0.9)
    a_rede = base * recuo
    pos = [pos_no1(i, t) for i in range(N1)]
    ilum_esq = clamp((t - T_MENTES) / 0.4) * (1 - 0.5 * clamp((t - T_MENTES - 0.8) / 1.0))
    ilum_dir = clamp((t - T_NECES) / 0.4) * (1 - 0.5 * clamp((t - T_NECES - 0.8) / 1.0))
    for (i, j) in AR_ESQ + AR_DIR:
        d.line([pos[i], pos[j]], fill=rgba(ORANGE, 0.20 * a_rede * some), width=2)
    pp = clamp((t - T_PONTE) / 0.9)
    for k, (i, j) in enumerate(PONTES):
        qq = clamp(pp * 1.6 - k * 0.09)
        if qq > 0:
            a, b = pos[i], pos[j]
            d.line([a, (a[0] + (b[0] - a[0]) * qq, a[1] + (b[1] - a[1]) * qq)],
                   fill=rgba(ORANGE, 0.42 * a_rede * some), width=2)
    energia = [0.0] * N1
    for (t0, i, j, du) in PULSOS1:
        p = (t - t0) / du
        if 0 <= p <= 1:
            desenha_pulso(d, pos[i], pos[j], p, 0.9 * a_rede * some)
        dt = t - (t0 + du)
        if 0 <= dt < 0.5:
            energia[j] = max(energia[j], 1 - dt / 0.5)
    for i in range(N1):
        x, y = pos[i]
        a_no = a_rede * (1.0 if i in MIGRAM else some)
        if a_no <= 0.01:
            continue
        luz = ilum_esq if i < 22 else ilum_dir
        e = max(energia[i] * some, luz * 0.8)
        cola_brilho(lay, x, y, a_no * (0.25 + 0.75 * max(e, 0.35 * pulso(t))))
        r = 5 + 3 * e
        d.ellipse([x - r, y - r, x + r, y + r], fill=rgba((255, 170, 100), a_no * (0.6 + 0.4 * e)))


def mapa_cena(lay, d, t):
    a = janela(t, T_MIG0 + 0.2, TR_IMP - 0.05, fade=0.5)
    if a <= 0.01:
        return
    lut = np.zeros(28, dtype="float32")
    for i in range(27):
        dt = t - CHEGADA[i]
        if dt >= 0:
            lut[i + 1] = 0.20 + 0.45 * math.exp(-dt * 2.2)
    arr = np.zeros((MH, MW, 4), dtype="uint8")
    arr[:, :, 0], arr[:, :, 1], arr[:, :, 2] = ORANGE
    arr[:, :, 3] = (lut[IDX] * 255 * a).astype("uint8")
    lay.alpha_composite(Image.fromarray(arr, "RGBA"), (CX0, CY0))
    cont = CONTORNO
    if a < 0.999:
        c = np.asarray(CONTORNO).copy()
        c[:, :, 3] = (c[:, :, 3] * a).astype("uint8")
        cont = Image.fromarray(c, "RGBA")
    lay.alpha_composite(cont)
    for (i, j) in AR_MAPA:
        if t >= min(CHEGADA[i], CHEGADA[j]):
            aa = 0.10 + 0.22 * clamp((t - max(CHEGADA[i], CHEGADA[j])) / 0.5)
            d.line([NOS_MAPA[i], NOS_MAPA[j]], fill=rgba(ORANGE, aa * a), width=2)
    for (t0, i, j, du) in PROP:
        p = (t - t0) / du
        if 0 <= p <= 1:
            desenha_pulso(d, NOS_MAPA[i], NOS_MAPA[j], p, a, raio=7)
    energia = {}
    for (t0, i, j, du) in PULSOS_MAPA:
        p = (t - t0) / du
        if 0 <= p <= 1:
            desenha_pulso(d, NOS_MAPA[i], NOS_MAPA[j], p, 0.8 * a, raio=5)
        dt = t - (t0 + du)
        if 0 <= dt < 0.5:
            energia[j] = max(energia.get(j, 0), 1 - dt / 0.5)
    for i, (x, y) in enumerate(NOS_MAPA):
        if i == NB:
            continue
        dt = t - CHEGADA[i]
        e = max(math.exp(-max(dt, 0) * 2.5) if dt >= 0 else 0, energia.get(i, 0))
        cola_brilho(lay, x, y, a * (0.2 + 0.8 * e) if dt >= 0 else a * 0.1)
        r = 5 + 3 * e
        d.ellipse([x - r, y - r, x + r, y + r],
                  fill=rgba((255, 170, 100), a * ((0.45 if dt >= 0 else 0.25) + 0.55 * max(e, 0.4 * pulso(t)))))
    bx, by = BH
    if t > T_ORIGEM - 0.01:
        for k in range(3):
            fase = (((t - INICIO_MUS) / BEAT) / 3 + k / 3) % 1
            rr = 10 + 70 * fase
            d.ellipse([bx - rr, by - rr, bx + rr, by + rr], outline=rgba(ORANGE, a * (1 - fase) * 0.8), width=2)
        cola_brilho(lay, bx, by, a)
        d.ellipse([bx - 8, by - 8, bx + 8, by + 8], fill=rgba(WHITE, a))
        if t > T_ORIGEM:
            d.text((bx + 18, by - 12), "BH", font=MONOB(22), fill=rgba(WHITE, a * clamp((t - T_ORIGEM) / 0.4)))


# ================================================================== HUD
def hud(d, t):
    a = clamp((t - 0.1) / 0.6) * (1 - clamp((t - (TR_FIM - 0.1)) / 0.4))
    if a <= 0:
        return
    pb = pulso(t)
    L, cor = int(38 + 14 * pb), rgba(ORANGE, (0.55 + 0.45 * pb) * a)
    for (x, y, sx, sy) in [(60, 252, 1, 1), (W - 60, 252, -1, 1), (60, 1648, 1, -1), (W - 60, 1648, -1, -1)]:
        d.line([(x, y), (x + sx * L, y)], fill=cor, width=3)
        d.line([(x, y), (x, y + sy * L)], fill=cor, width=3)
    d.text((MG, 272), "SINGULAR // HUB DE INTELIGÊNCIA", font=MONO(20), fill=rgba(DIM, a))
    pisca = 0.25 + 0.75 * pb
    d.ellipse([W - 220, 279, W - 208, 291], fill=rgba(ORANGE, a * pisca))
    d.text((W - 196, 272), "ONLINE", font=MONO(20), fill=rgba(DIM, a))
    d.line([(MG, 1610), (W - MG, 1610)], fill=rgba(LINE, a), width=2)
    d.line([(MG, 1610), (MG + (W - 2 * MG) * (t / DUR), 1610)], fill=rgba(ORANGE, a), width=2)
    d.text((MG, 1576), "@singularinteligencia", font=MONO(20), fill=rgba(DIM, a))
    d.text((W - MG, 1576), f"BPM 120 · {int((t - INICIO_MUS) // 2) + 1 if t > INICIO_MUS else 0:03d}", font=MONO(20), fill=rgba(DIM, a), anchor="ra")


def kicker(d, txt, t, t0, a):
    vis = digitado(txt, t, t0, 26)
    d.text((MG, 370), vis, font=MONOB(30), fill=rgba(ORANGE, a))
    if len(vis) < len(txt) or ((t - INICIO_MUS) % BEAT) < BEAT / 2:
        x = MG + d.textlength(vis, font=MONOB(30)) + 6
        d.rectangle([x, 374, x + 16, 404], fill=rgba(ORANGE, a * 0.9))


# ============================================================= cenas
def c_mote(d, t, a):
    kicker(d, "// NOSSO MOTE", t, T_MENTES - 0.4, a)
    p, dy = entrada(t, T_MENTES, 0.6)
    d.text((MG, 470 + dy), "Reunir as", font=BOLD(70), fill=rgba(WHITE, a * p))
    d.text((MG, 556 + dy), "melhores mentes", font=BOLD(70), fill=rgba(WHITE, a * p))
    p, dy = entrada(t, T_NECES, 0.6)
    d.text((MG, 642 + dy), "às maiores", font=BOLD(70), fill=rgba(ORANGE, a * p))
    d.text((MG, 728 + dy), "necessidades.", font=BOLD(70), fill=rgba(ORANGE, a * p))
    d.text((330, 1450), "MENTES", font=MONO(22), fill=rgba(GREY, a * clamp((t - T_MENTES - 0.2) / 0.5)), anchor="ma")
    d.text((750, 1450), "NECESSIDADES", font=MONO(22), fill=rgba(GREY, a * clamp((t - T_NECES - 0.2) / 0.5)), anchor="ma")


def c_quem(d, t, a):
    kicker(d, "// QUEM SOMOS", t, TR_QUEM + 0.05, a)
    p, dy = entrada(t, max(T_QUEM, TR_QUEM + 0.1), 0.55)
    f = MED(52)
    d.text((MG, 480 + dy), "Deixamos de ser só uma", font=f, fill=rgba(GREY, a * p))
    y1, y2 = 552, 624
    d.text((MG, y1 + dy), "consultoria em", font=f, fill=rgba(GREY, a * p))
    d.text((MG, y2 + dy), "softwares de gestão.", font=f, fill=rgba(GREY, a * p))
    for k, (txt, yy) in enumerate([("consultoria em", y1), ("softwares de gestão.", y2)]):
        qq = ease((t - T_RISCO - k * 0.35) / 0.45)
        if qq > 0:
            d.rectangle([MG - 6, yy + 38, MG + 6 + d.textlength(txt, font=f) * qq, yy + 44], fill=rgba(ORANGE, a))
    p, dy = entrada(t, T_SOMOS, 0.6)
    d.text((MG, 780 + dy), "Hoje, somos um", font=BOLD(80), fill=rgba(WHITE, a * p))
    p, dy = entrada(t, T_HUB, 0.6)
    d.text((MG, 878 + dy), "hub de", font=BOLD(96), fill=rgba(ORANGE, a * p))
    d.text((MG, 990 + dy), "inteligência.", font=BOLD(96), fill=rgba(ORANGE, a * p))


MODULOS = ["Folha de pagamento e eSocial", "Reforma tributária e fiscal",
           "Segurança e saúde no trabalho", "Infraestrutura, integrações e IA"]


def c_faz(d, t, a):
    kicker(d, "// O QUE FAZEMOS", t, TR_FAZ + 0.05, a)
    p, dy = entrada(t, max(T_FAZ - 0.1, TR_FAZ + 0.1), 0.55)
    d.text((MG, 470 + dy), "Onde a operação", font=BOLD(70), fill=rgba(WHITE, a * p))
    d.text((MG, 558 + dy), "costuma travar", font=BOLD(70), fill=rgba(WHITE, a * p))
    y = 740
    for i, txt in enumerate(MODULOS):
        ti = T_MOD[i]
        pi = ease((t - ti) / 0.45)
        if pi > 0.01:
            ai = a * pi
            ativo = clamp(1 - (t - ti - 0.2) / 1.2)
            borda = tuple(int(LINE[k] + (ORANGE[k] - LINE[k]) * ativo) for k in range(3))
            d.rounded_rectangle([MG, y, MG + (W - 2 * MG) * pi, y + 150], radius=14, outline=rgba(borda, ai), width=2)
            if pi > 0.6:
                d.text((MG + 32, y + 24), f"[0{i + 1}]", font=MONOB(28), fill=rgba(ORANGE, ai))
                ok = t > ti + 0.55
                d.text((W - MG - 30, y + 24), "● ATIVO" if ok else "○ CARREGANDO", font=MONO(22),
                       fill=rgba(ORANGE if ok else DIM, ai), anchor="ra")
                d.text((MG + 32, y + 72), digitado(txt, t, ti + 0.15, cps=46), font=MED(44), fill=rgba(WHITE, ai))
        y += 180


SEGMENTOS = ["Energia", "Marítimo e offshore", "Saúde", "Educação",
             "Mídia e comunicação", "Varejo", "Indústria", "Serviços"]


def c_seg(d, t, a):
    kicker(d, "// PARA QUEM FAZEMOS", t, TR_SEG + 0.05, a)
    p, dy = entrada(t, TR_SEG + 0.1, 0.55)
    d.text((MG, 470 + dy), "Oito segmentos,", font=BOLD(70), fill=rgba(WHITE, a * p))
    d.text((MG, 558 + dy), "uma mesma rotina", font=BOLD(70), fill=rgba(WHITE, a * p))
    y = 712
    for i, seg in enumerate(SEGMENTOS):
        pi, dx = entrada(t, T_SEGS[i], 0.4, dist=60)
        if pi > 0.01:
            ai = a * pi
            d.rounded_rectangle([MG + dx, y, W - MG + dx, y + 84], radius=12, outline=rgba(LINE, ai), width=2)
            d.text((MG + 30 + dx, y + 27), f"{i + 1:02d}", font=MONOB(26), fill=rgba(DIM, ai))
            d.text((MG + 104 + dx, y + 14), seg, font=MED(44), fill=rgba(WHITE, ai))
        y += 100


def contador(d, t, x, y, t0, t1, alvo, linhas, a):
    if t < t0 - 0.2:
        return
    nb = math.floor((t - t0) / (BEAT / 2)) / ((t1 - t0) / (BEAT / 2))
    v = alvo * ease_io(nb) if t < t1 else alvo
    pn = clamp((t - t0 + 0.2) / 0.4)
    d.text((x, y), f"+{int(round(v))}", font=MONOB(100), fill=rgba(ORANGE, a * pn))
    for j, l in enumerate(linhas):
        d.text((x, y + 124 + j * 44), l, font=BOLD(34), fill=rgba(WHITE, a * pn))


def c_mapa(d, t, a):
    kicker(d, "// DE NORTE A SUL", t, TR_MAPA + 0.05, a)
    contador(d, t, MG, 1248, T_ORIGEM, T_FIMPROP, 500, ["CNPJs confiam", "na Singular"], a)
    contador(d, t, MG + 450, 1248, bt(76), T_FIMPROP + 2 * BEAT, 10,
             ["experts com mais de", "10 anos de experiência"], a)
    if t > T_ORIGEM - 0.2:
        ok = sum(1 for i in range(27) if t >= CHEGADA[i])
        d.text((W - MG, 380), f"{ok:02d}/27 UFs", font=MONO(24), fill=rgba(GREY, a), anchor="ra")
    p, dy = entrada(t, T_NORTE + BEAT * 2, 0.6)
    d.line([(MG, 1478), (W - MG, 1478)], fill=rgba(LINE, a * p), width=2)
    d.text((MG, 1496 + dy), "Atendendo todo o Brasil, de norte a sul.", font=LIGHT(34), fill=rgba(GREY, a * p))


def c_imp(d, t, a):
    kicker(d, "// NA IMPRENSA", t, TR_IMP + 0.05, a)
    p, dy = entrada(t, TR_IMP + 0.1, 0.55)
    d.text((MG, 480 + dy), "Já citada em", font=BOLD(76), fill=rgba(WHITE, a * p))
    veiculos = [["Valor Econômico"], ["Pequenas Empresas", "& Grandes Negócios"], ["IstoÉ Tech"], ["Forbes"]]
    y = 680
    for k, linhas in enumerate(veiculos):
        pk, dk = entrada(t, T_NOMES[k], 0.5, dist=50)
        if pk > 0.01:
            alt = 70 * len(linhas)
            d.rectangle([MG + dk, y + 10, MG + 7 + dk, y + alt - 6], fill=rgba(ORANGE, a * pk))
            for j, l in enumerate(linhas):
                d.text((MG + 40 + dk, y + j * 70), l, font=BOLD(56), fill=rgba(WHITE, a * pk))
        y += 70 * len(linhas) + 46


def c_fim(d, t, a):
    p, dy = entrada(t, TR_FIM + 0.05, 0.9)
    tracked(d, (W / 2, 830 + dy), "SINGULAR", BOLD(96), rgba(ORANGE, a * p), 34 - 12 * p, centro=True)
    larg = 260 * ease((t - TR_FIM - 0.3) / 0.7)
    d.rectangle([W / 2 - larg / 2, 958, W / 2 + larg / 2, 964], fill=rgba(ORANGE, a))
    p2, dy2 = entrada(t, T_FIMHUB, 0.7)
    d.text((W / 2, 1000 + dy2), "hub de inteligência", font=LIGHT(46), fill=rgba(WHITE, a * p2), anchor="ma")
    p3, _ = entrada(t, T_FIMHUB + 2 * BEAT, 0.8)
    d.text((W / 2, 1420), "@singularinteligencia", font=REG(32), fill=rgba(DIM, a * p3), anchor="ma")


# (função, entra, sai). Sai/entra exatamente nas viradas, onde passa a faixa.
CENAS = [(c_mote, 0.6, TR_QUEM), (c_quem, TR_QUEM, TR_FAZ), (c_faz, TR_FAZ, TR_SEG),
         (c_seg, TR_SEG, TR_MAPA), (c_mapa, TR_MAPA, TR_IMP), (c_imp, TR_IMP, TR_FIM),
         (c_fim, TR_FIM, DUR + 1)]
SAIDA_DUR = 0.22      # saída rápida para a esquerda
ENTRADA_DUR = 0.45    # entrada pela direita


def compoe_textos(base, t):
    for func, t_in, t_out in CENAS:
        ini_saida = t_out - 0.18          # sai acelerando, escondida pela faixa
        if t < t_in or t > t_out + 0.02:
            continue
        dx, a = 0, 1.0
        if t_in > 1.0:
            e0 = t_in + 0.04              # entra depois que a faixa passou
            if t < e0:
                continue
            if t < e0 + ENTRADA_DUR:
                p = ease((t - e0) / ENTRADA_DUR)
                dx, a = int((1 - p) * 300), clamp(p * 1.5)
        else:
            a = clamp((t - t_in) / 0.4)
        if t > ini_saida:
            p = ease_io((t - ini_saida) / 0.2)
            dx, a = int(-p * 640), (1 - p) * a
        if a <= 0.01:
            continue
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        func(ImageDraw.Draw(lay), t, a)
        if dx > 0:
            base.alpha_composite(lay.crop((0, 0, W - dx, H)), (dx, 0))
        elif dx < 0:
            base.alpha_composite(lay.crop((-dx, 0, W, H)), (0, 0))
        else:
            base.alpha_composite(lay)


# ===================================================== trocas de tela
def transicao(img, t):
    """Faixa laranja inclinada, soco de zoom, tremor, flash e glitch nas viradas."""
    viradas = [tv for tv in TR if -0.25 <= t - tv <= 0.5]
    if not viradas:
        return img
    tv = viradas[0]
    u = t - tv
    # soco de zoom e tremor logo após o impacto
    if 0 <= u <= 0.45:
        k = 1 - u / 0.45
        esc = 1 + 0.07 * k ** 2
        nw, nh = int(W * esc), int(H * esc)
        sx = int(RNG.normal(0, 9 * k)) if u < 0.3 else 0
        sy = int(RNG.normal(0, 9 * k)) if u < 0.3 else 0
        g = img.resize((nw, nh), Image.BILINEAR)
        x0 = int(np.clip((nw - W) / 2 + sx, 0, nw - W))
        y0 = int(np.clip((nh - H) / 2 + sy, 0, nh - H))
        img = g.crop((x0, y0, x0 + W, y0 + H))
    # glitch: separa os canais de cor por alguns quadros
    if 0 <= u <= 0.12:
        r, g, b = img.split()
        desl = int(14 * (1 - u / 0.12))
        r = r.transform(img.size, Image.AFFINE, (1, 0, -desl, 0, 1, 0))
        b = b.transform(img.size, Image.AFFINE, (1, 0, desl, 0, 1, 0))
        img = Image.merge("RGB", (r, g, b))
    # flash
    if 0 <= u <= 0.16:
        fl = Image.new("RGB", img.size, (255, 236, 220))
        img = Image.blend(img, fl, 0.28 * (1 - u / 0.16))
    # faixa laranja varrendo da direita para a esquerda, centrada na virada
    p = (t - (tv - 0.22)) / 0.44
    if 0 <= p <= 1:
        d = ImageDraw.Draw(img)
        pe = ease_io(p)
        xc = W * 1.65 - pe * W * 2.3
        sk, lg = 360, 520
        d.polygon([(xc - lg / 2 + sk, 0), (xc + lg / 2 + sk, 0), (xc + lg / 2 - sk, H), (xc - lg / 2 - sk, H)],
                  fill=ORANGE)
        xt = xc + lg / 2 + 30
        d.polygon([(xt + sk, 0), (xt + 70 + sk, 0), (xt + 70 - sk, H), (xt - sk, H)], fill=(255, 150, 70))
        xd = xc - lg / 2 - 120
        d.polygon([(xd + sk, 0), (xd + 90 + sk, 0), (xd + 90 - sk, H), (xd - sk, H)], fill=(14, 14, 18))
    return img


# ================================================================ áudio
def audio(caminho):
    musica, viradas, final = gera(DUR, INICIO_MUS, VIRADAS_BRUTAS, FINAL_BRUTO)
    assert all(abs(a - b) < 1e-6 for a, b in zip(viradas + [final], TR)), "viradas fora de sincronia"
    n = int(DUR * SR)
    musica = np.pad(musica, (0, max(0, n - len(musica))))[:n]
    fade = int(0.8 * SR)
    musica[-fade:] *= np.linspace(1, 0, fade)
    sf.write(caminho, (0.95 * musica / np.max(np.abs(musica))).astype("float32"), SR)
    print("viradas:", TR)


# =============================================================== render
VID, AUD = "/home/claude/hub4_mudo.mp4", "/home/claude/hub4_audio.wav"
SAIDA = "/mnt/user-data/outputs/singular_reels_hub_inteligencia_v7_trilha.mp4"

if __name__ == "__main__":
    audio(AUD)
    total = int(DUR * FPS)
    proc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                             "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium",
                             "-crf", "19", "-pix_fmt", "yuv420p", VID], stdin=subprocess.PIPE)
    for n in range(total):
        t = n / FPS
        x0 = int(PAN * (0.15 + 0.7 * t / DUR))
        y0 = int(PAN * (0.85 - 0.7 * t / DUR))
        lay = BG.crop((x0, y0, x0 + W, y0 + H)).convert("RGBA")
        rede = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        dr = ImageDraw.Draw(rede)
        rede_cena1(rede, dr, t)
        mapa_cena(rede, dr, t)
        lay = Image.alpha_composite(lay, rede)
        topo = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        hud(ImageDraw.Draw(topo), t)
        lay = Image.alpha_composite(lay, topo)
        compoe_textos(lay, t)
        quadro = lay.convert("RGB")
        pb = pulso(t)
        if pb > 0.05 and not any(-0.3 <= t - tv <= 0.5 for tv in TR):
            e = 1 + 0.008 * pb
            g = quadro.resize((int(W * e), int(H * e)), Image.BILINEAR)
            ox, oy = (g.width - W) // 2, (g.height - H) // 2
            quadro = g.crop((ox, oy, ox + W, oy + H))
        quadro = transicao(quadro, t)
        proc.stdin.write(quadro.tobytes())
        if n % 300 == 0:
            print(f"  {n}/{total}", flush=True)
    proc.stdin.close()
    proc.wait()
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", VID, "-i", AUD, "-c:v", "copy",
                    "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", "-movflags", "+faststart", SAIDA], check=True)
    print("pronto:", SAIDA)
