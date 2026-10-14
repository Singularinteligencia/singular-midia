"""Motor de Reels curtos no leiaute Singular (fundo escuro, HUD, laranja de destaque).
Cada Reels é uma lista de cenas; tudo cai na grade da trilha (120 bpm)."""
import math
import subprocess
import sys
import numpy as np
import soundfile as sf
from PIL import Image, ImageDraw, ImageOps

sys.path.insert(0, "/home/claude")
import video_hub4 as m
from video_hub4 import (W, H, FPS, ORANGE, WHITE, GREY, DIM, LINE, MG, BOLD, MED, REG, LIGHT, MONO, MONOB,
                        clamp, ease, ease_io, entrada, rgba, tracked)
from musica_reels import gera, SR, BEAT

CHK = lambda s: m.fnt("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", s)
FONTES = {"b": BOLD, "m": MED, "r": REG, "l": LIGHT}


def back_ease(p, s=1.6):
    p = clamp(p) - 1
    return 1 + (s + 1) * p ** 3 + s * p ** 2


def letras(d, txt, fonte, x, y, t, t0, cor, a, ancora="l", passo=0.018):
    if t < t0 or a <= 0.01:
        return
    asc, desc = fonte.getmetrics()
    alt = asc + desc + 16
    larg = d.textlength(txt, font=fonte)
    x0 = x - larg / 2 if ancora == "m" else x
    cam = Image.new("RGBA", (int(larg) + 40, alt), (0, 0, 0, 0))
    dc = ImageDraw.Draw(cam)
    cx = 20
    for k, ch in enumerate(txt):
        p = back_ease((t - t0 - k * passo) / 0.32)
        dy = (1 - p) * alt
        if -alt < dy < alt:
            dc.text((cx, 8 + dy), ch, font=fonte, fill=rgba(cor, a))
        cx += dc.textlength(ch, font=fonte)
    d._image.alpha_composite(cam, (int(x0 - 20), int(y - 8)))


def quebra(d, txt, fonte, larg):
    ws, ls, cur = txt.split(), [], ""
    for w_ in ws:
        tt = (cur + " " + w_).strip()
        if d.textlength(tt, font=fonte) <= larg or not cur:
            cur = tt
        else:
            ls.append(cur)
            cur = w_
    if cur:
        ls.append(cur)
    return ls


class Reels:
    """cenas: lista de dicts
       {"beats": n, "kick": "// TEXTO", "linhas": [(beat, texto, tamanho, cor, peso)], "y": 470,
        "itens": [(beat, texto)], "numero": (beat, "30/11", legenda)}
       A última cena é sempre o cartão final da Singular (gerado aqui)."""

    def __init__(self, cenas, fim_frase, fim_sub="hub de inteligência", pb=False, calmo=False, ini=0.6):
        self.cenas, self.fim_frase, self.fim_sub, self.pb, self.calmo = cenas, fim_frase, fim_sub, pb, calmo
        self.INI = ini
        self.bt = lambda n: ini + n * BEAT
        acc, self.inicios = 0, []
        for c in cenas:
            self.inicios.append(self.bt(acc))
            acc += c["beats"]
        self.TR_FIM = self.bt(acc)
        self.TR = self.inicios[1:] + [self.TR_FIM]
        self.DUR = self.TR_FIM + 4.5
        m.INICIO_MUS, m.TR, m.TR_FIM, m.DUR = ini, self.TR, self.TR_FIM, self.DUR
        m.TR_QUEM = self.TR[0]
        m.pulso = self.pulso
        cenas_m = []
        for k, c in enumerate(cenas):
            t1 = self.inicios[k + 1] if k + 1 < len(cenas) else self.TR_FIM
            cenas_m.append((self._cena(c, self.inicios[k]), max(0.3, self.inicios[k]) if k else 0.3, t1))
        cenas_m.append((self.c_fim, self.TR_FIM, self.DUR + 1))
        m.CENAS = cenas_m

    def pulso(self, t):
        if t < self.INI or t > self.TR_FIM + 0.2:
            return 0.0
        n = int((t - self.INI) / BEAT)
        if self.calmo and n % 2:
            n -= 1
        return (1.0 if n % 4 == 0 else 0.6) * math.exp(-(t - self.bt(n)) * 9)

    def _cena(self, c, t0):
        def f(d, t, a):
            if c.get("kick"):
                m.kicker(d, c["kick"], t, t0 + 0.05, a)
            y = c.get("y", 540)
            for b, txt, tam, cor, peso in c.get("linhas", []):
                if txt is None:
                    y += tam
                    continue
                fonte = FONTES[peso](tam)
                for ln in quebra(d, txt, fonte, W - 2 * MG):
                    letras(d, ln, fonte, MG, y, t, t0 + b * BEAT + 0.06, cor, a, passo=0.014 if tam < 70 else 0.018)
                    y += int(tam * 1.2)
            if c.get("numero"):
                b, num, leg = c["numero"]
                p, dy = entrada(t, t0 + b * BEAT, 0.45, 60)
                esc = 1 + 0.04 * self.pulso(t)
                fo = BOLD(int(230 * esc))
                d.text((MG, y + 40 + dy), num, font=fo, fill=rgba(ORANGE, a * p))
                y += 330
                if leg:
                    letras(d, leg, LIGHT(48), MG, y, t, t0 + b * BEAT + 0.3, GREY, a)
                    y += 80
            itens = c.get("itens", [])
            if itens:
                y += 30
                for k, (b, txt) in enumerate(itens):
                    ti = t0 + b * BEAT
                    if t < ti:
                        y += 118
                        continue
                    p = back_ease((t - ti) / 0.3)
                    cx, cy = MG, y + 10
                    s = 44 * p
                    d.line([(cx, cy + s * 0.55), (cx + s * 0.36, cy + s * 0.92)], fill=rgba(ORANGE, a), width=9)
                    d.line([(cx + s * 0.36, cy + s * 0.92), (cx + s, cy + s * 0.08)], fill=rgba(ORANGE, a), width=9)
                    fo = MED(54)
                    ls = quebra(d, txt, fo, W - 2 * MG - 70)
                    for j, ln in enumerate(ls):
                        letras(d, ln, fo, MG + 80, y + j * 66, t, ti + 0.04, WHITE, a, passo=0.01)
                    y += 66 * len(ls) + 70
        return f

    def c_fim(self, d, t, a):
        T = self.TR_FIM
        y = 540
        for k, ln in enumerate(self.fim_frase):
            cor = WHITE if k == 0 else ORANGE
            letras(d, ln, MED(52), W / 2, y, t, T + 0.05 + k * 0.3, cor, a, ancora="m", passo=0.012)
            y += 66
        p, dy = entrada(t, T + 1.0, 0.8)
        tracked(d, (W / 2, 790 + dy), "SINGULAR", BOLD(96), rgba(ORANGE, a * p), 34 - 12 * p, centro=True)
        p2, dy2 = entrada(t, T + 1.5, 0.6)
        d.text((W / 2, 956 + dy2), self.fim_sub, font=LIGHT(46), fill=rgba(WHITE, a * p2), anchor="ma")
        p3, _ = entrada(t, T + 2.2, 0.7)
        d.text((W / 2, 1080), "@singularinteligencia", font=REG(32), fill=rgba(DIM, a * p3), anchor="ma")

    def palco(self, d, t):
        """Equalizador discreto na parte de baixo, batendo com a trilha."""
        a = clamp((t - 0.2) / 0.6) * (1 - clamp((t - (self.TR_FIM - 0.2)) / 0.4))
        if a <= 0:
            return
        pb = self.pulso(t)
        n = 28
        larg = (W - 2 * MG) / n
        for i in range(n):
            ph = math.sin(i * 0.9 + t * 3.1) * 0.5 + 0.5
            h = 18 + 120 * ph * (0.35 + 0.65 * pb) * (0.6 + 0.4 * math.sin(i * 0.37))
            x = MG + i * larg
            cor = ORANGE if i % 7 == int(t * 2) % 7 else LINE
            d.rectangle([x + 4, 1500 - h, x + larg - 4, 1500], fill=rgba(cor, a * (0.9 if cor == ORANGE else 0.7)))

    def transicao(self, img, t):
        for tv in self.TR:
            u = t - tv
            if -0.2 <= u <= 0.35:
                if 0 <= u <= 0.3:
                    e = 1 + 0.025 * (1 - u / 0.3) ** 2
                    g = img.resize((int(W * e), int(H * e)), Image.BILINEAR)
                    ox, oy = (g.width - W) // 2, (g.height - H) // 2
                    img = g.crop((ox, oy, ox + W, oy + H))
                pp = ease_io((u + 0.2) / 0.5)
                y = int(180 + pp * (H - 360))
                arr = np.asarray(img).astype("float32")
                yy = np.arange(H, dtype="float32")[:, None]
                glow = np.exp(-((yy - y) / 26) ** 2) * 0.35 + np.exp(-((yy - y) / 2.2) ** 2) * 0.9
                k = (glow * math.sin(math.pi * clamp((u + 0.2) / 0.55)))[..., None]
                arr = arr * (1 - k) + np.array(ORANGE, dtype="float32") * k
                img = Image.fromarray(np.clip(arr, 0, 255).astype("uint8"), "RGB")
                break
        return img

    def quadro(self, t):
        x0 = int(m.PAN * (0.15 + 0.7 * t / self.DUR))
        y0 = int(m.PAN * (0.85 - 0.7 * t / self.DUR))
        lay = m.BG.crop((x0, y0, x0 + W, y0 + H)).convert("RGBA")
        topo = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        dt = ImageDraw.Draw(topo)
        self.palco(dt, t)
        m.hud(dt, t)
        lay = Image.alpha_composite(lay, topo)
        m.compoe_textos(lay, t)
        q = lay.convert("RGB")
        pb = self.pulso(t)
        if pb > 0.05 and not any(-0.3 <= t - tv <= 0.5 for tv in self.TR):
            e = 1 + 0.006 * pb
            g = q.resize((int(W * e), int(H * e)), Image.BILINEAR)
            ox, oy = (g.width - W) // 2, (g.height - H) // 2
            q = g.crop((ox, oy, ox + W, oy + H))
        q = self.transicao(q, t)
        if self.pb:
            q = ImageOps.grayscale(q).point(lambda v: min(255, int(v * 1.6)) if v > 110 else v).convert("RGB")
        return q

    def render(self, saida, previa=None):
        if previa:
            for s in previa:
                self.quadro(s).save(f"/tmp/claude-0/prev_{s}.png")
            return
        vid, aud = saida + ".mudo.mp4", saida + ".wav"
        mus = gera(self.DUR, self.INI, self.TR[:-1], self.TR_FIM, calmo=self.calmo)
        sf.write(aud, 0.95 * mus, SR)
        proc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                                 "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium",
                                 "-crf", "20", "-pix_fmt", "yuv420p", vid], stdin=subprocess.PIPE)
        for n in range(int(self.DUR * FPS)):
            proc.stdin.write(self.quadro(n / FPS).tobytes())
        proc.stdin.close()
        proc.wait()
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", vid, "-i", aud, "-c:v", "copy",
                        "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", "-c:a", "aac", "-b:a", "192k",
                        "-shortest", "-movflags", "+faststart", saida], check=True)
        print("pronto:", saida, round(self.DUR, 1))
