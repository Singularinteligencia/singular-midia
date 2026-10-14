"""Trilha sintetizada no estilo vinheta de telejornal (breaking news).
Ré menor, 120 bpm, ostinato em semicolcheias, bateria, metais e impactos."""
import numpy as np
from scipy.signal import butter, sosfilt

SR = 48000
BPM = 120
BEAT = 60 / BPM
S16 = BEAT / 4
RNG = np.random.default_rng(42)

HZ = {"D2": 73.42, "Bb1": 58.27, "C2": 65.41, "D3": 146.83, "F3": 174.61, "A3": 220.0,
      "Bb2": 116.54, "C3": 130.81, "E3": 164.81, "G3": 196.0}
ACORDES = [("D2", ["D3", "F3", "A3"]), ("D2", ["D3", "F3", "A3"]),
           ("Bb1", ["Bb2", "D3", "F3"]), ("C2", ["C3", "E3", "G3"])]
PADRAO = [2, 0, 1, 0, 2, 0, 1, 0, 2, 0, 1, 2, 1, 0, 1, 0]   # índices no acorde, 16 passos


def lp(x, fc, ordem=2):
    return sosfilt(butter(ordem, fc, "low", fs=SR, output="sos"), x)


def hp(x, fc, ordem=2):
    return sosfilt(butter(ordem, fc, "high", fs=SR, output="sos"), x)


def bp(x, f1, f2):
    return sosfilt(butter(2, [f1, f2], "band", fs=SR, output="sos"), x)


def serra(freq, dur, corte, dets=(0.0,)):
    n = int(dur * SR)
    t = np.arange(n) / SR
    out = np.zeros(n, dtype="float64")
    for dt in dets:
        f = freq * (1 + dt)
        hmax = int(min(40, 11000 / f))
        for h in range(1, hmax + 1):
            peso = (1 / h) * np.exp(-(h * f) / corte)
            out += peso * np.sin(2 * np.pi * h * f * t + RNG.uniform(0, 6.28) * (dt != 0))
    return out / len(dets)


def env(n, ataque, decai):
    t = np.arange(n) / SR
    return np.minimum(1, t / max(ataque, 1e-4)) * np.exp(-t * decai)


def bumbo(vol):
    n = int(0.45 * SR)
    t = np.arange(n) / SR
    f = 45 + 75 * np.exp(-t * 38)
    fase = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(fase) * np.exp(-t * 7)
    clique = lp(RNG.normal(0, 1, n), 3500) * np.exp(-t * 180) * 0.35
    return (s + clique) * vol


def caixa(vol):
    n = int(0.3 * SR)
    t = np.arange(n) / SR
    ruido = bp(RNG.normal(0, 1, n), 1200, 6500) * np.exp(-t * 16)
    tom = np.sin(2 * np.pi * 190 * t) * np.exp(-t * 28) * 0.6
    return (ruido * 0.9 + tom) * vol


def chimbal(vol):
    n = int(0.06 * SR)
    t = np.arange(n) / SR
    return hp(RNG.normal(0, 1, n), 7500) * np.exp(-t * 70) * vol


def impacto(vol):
    n = int(3.2 * SR)
    t = np.arange(n) / SR
    f = 30 + 34 * np.exp(-t * 5)
    sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 1.9)
    estouro = lp(RNG.normal(0, 1, n), 900) * np.exp(-t * 7) * 0.9
    prato = hp(RNG.normal(0, 1, n), 5000) * np.exp(-t * 1.6) * 0.18
    return (sub * 1.2 + estouro + prato) * vol


def subida(dur, vol):
    n = int(dur * SR)
    t = np.arange(n) / SR
    rampa = (t / dur) ** 2.2
    return hp(RNG.normal(0, 1, n), 1800) * rampa * vol


def metais(notas, dur, vol):
    s = sum(serra(HZ[n] * 2, dur, 2600, dets=(-0.006, 0.0, 0.006)) for n in notas)
    s = s * env(len(s), 0.006, 4.5)
    return lp(s, 3200) * vol


def ostinato(freq, brilho, vol):
    s = serra(freq, 0.2, brilho)
    return s * env(len(s), 0.002, 22) * vol


def gera(total, inicio, viradas, final):
    """inicio: tempo do primeiro compasso; viradas: instantes das mudanças de seção;
    final: instante do acorde final. Retorna (trilha, instantes_quantizados)."""
    q = lambda x: inicio + round((x - inicio) / BEAT) * BEAT
    viradas = [q(v) for v in viradas]
    final = q(final)
    out = np.zeros(int((total + 4) * SR), dtype="float64")

    def poe(sinal, inst, ganho=1.0):
        s = int(inst * SR)
        if s < 0:
            sinal, s = sinal[-s:], 0
        e = min(len(out), s + len(sinal))
        out[s:e] += sinal[: e - s] * ganho

    def nivel(t):
        n = 1
        for v in viradas:
            if t >= v - 1e-6:
                n += 1
        return min(n, 3)

    # subida inicial até o primeiro tempo
    poe(subida(inicio, 0.25), 0.0)
    poe(impacto(0.75), inicio)

    passo = 0
    t = inicio
    while t < final - 1e-6:
        compasso = int(passo // 16) % 4
        k = passo % 16
        raiz, acorde = ACORDES[compasso]
        nv = nivel(t)
        brilho = {1: 1100, 2: 2000, 3: 3200}[nv]
        nota = HZ[acorde[PADRAO[k]]] * 2
        acento = 1.0 if k % 4 == 0 else 0.7
        poe(ostinato(nota, brilho, 0.11 * acento * (0.75 if nv == 1 else 1.0)), t)
        # baixo pulsando em colcheias
        if k % 2 == 0 and nv >= 1:
            b = serra(HZ[raiz], 0.24, 500)
            poe(lp(b * env(len(b), 0.004, 9), 600) * (0.32 if nv > 1 else 0.24), t)
        # bateria
        if k % 4 == 0:
            if nv == 3 or k in (0, 8):
                poe(bumbo(0.9 if nv > 1 else 0.6), t)
        if nv >= 2 and k in (4, 12):
            poe(caixa(0.42), t)
        if nv >= 2:
            poe(chimbal(0.10 if k % 2 else 0.16), t)
        # metais no primeiro tempo de cada compasso no nível alto
        if nv == 3 and k == 0:
            poe(metais(acorde, 0.6, 0.12), t)
        if nv == 3 and k == 10 and compasso % 2 == 1:
            poe(metais(acorde, 0.35, 0.08), t)
        passo += 1
        t = inicio + passo * S16

    # viradas: subida curta + impacto
    for v in viradas:
        poe(subida(0.9, 0.22), v - 0.9)
        poe(impacto(0.85), v)

    # acorde final longo
    poe(subida(1.0, 0.25), final - 1.0)
    poe(impacto(1.0), final)
    fim = sum(serra(HZ[n] * 2, 5.0, 2400, dets=(-0.005, 0.0, 0.005)) for n in ["D3", "F3", "A3"])
    fim += serra(HZ["D2"], 5.0, 800) * 0.8
    poe(lp(fim * env(len(fim), 0.01, 0.9), 3000) * 0.14, final)

    # ambiência curta
    ir_n = int(0.8 * SR)
    ir = RNG.normal(0, 1, ir_n) * np.exp(-np.arange(ir_n) / SR * 5.5) * 0.12
    ir[0] = 1.0
    wet = np.convolve(out, ir)[: len(out)]
    mix = 0.78 * out + 0.22 * wet
    mix = mix[: int(total * SR)]
    return (mix / (np.max(np.abs(mix)) + 1e-9)).astype("float32"), viradas, final
