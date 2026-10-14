"""Trilha original 'intergaláctica': sintetizadores analógicos, sem órgão.
Lá menor, 120 bpm. Universo: pad cósmico com filtro respirando e brilhos com eco.
Mergulho: sequência de baixo em semicolcheias abrindo o filtro. Quintal: queda com
bateria eletrônica, acordes supersaw e melodia de sintetizador. Final: acorde enorme."""
import numpy as np
from scipy.signal import butter, sosfilt

SR = 48000
BPM = 120
BEAT = 60 / BPM
S16 = BEAT / 4
RNG = np.random.default_rng(2077)
NOTA = lambda m: 440.0 * 2 ** ((m - 69) / 12)

ACORDES = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]   # Am F C G
BAIXO = [33, 29, 36, 31]
SEQ = [0, 12, 7, 12, 0, 12, 10, 12, 0, 12, 7, 12, 3, 12, 7, 15]       # baixo sequenciado (semitons)
MELODIA = [(76, 3), (74, 1), (72, 2), (71, 2), (72, 3), (74, 1), (76, 4),
           (79, 3), (77, 1), (76, 2), (74, 2)]


def lp(x, fc, o=2):
    return sosfilt(butter(o, min(fc, SR / 2 - 100), "low", fs=SR, output="sos"), x)


def hp(x, fc, o=2):
    return sosfilt(butter(o, fc, "high", fs=SR, output="sos"), x)


def bp(x, a, b):
    return sosfilt(butter(2, [a, b], "band", fs=SR, output="sos"), x)


def sat(x, k=1.8):
    return np.tanh(k * x) / np.tanh(k)


def serra(f, n, fase0=0.0, harm=40):
    t = np.arange(n) / SR
    hs = range(1, int(min(harm, 15000 / max(f, 1))) + 1)
    return sum(np.sin(2 * np.pi * f * h * t + fase0 * h) / h for h in hs)


def filtro_movel(x, fcs, blocos=32):
    """Filtro passa-baixa variando no tempo (aproximação em blocos com sobreposição)."""
    n = len(x)
    out = np.zeros(n)
    tam = n // blocos + 1
    for k in range(blocos):
        a, b = k * tam, min(n, (k + 1) * tam)
        if a >= n:
            break
        fc = fcs[min(len(fcs) - 1, a)]
        y = lp(x, fc)
        out[a:b] = y[a:b]
    return out


def supersaw(notas, dur, vol, fc0=600, fc1=6000, ataque=0.6, solta=0.8):
    n = int(dur * SR)
    t = np.arange(n) / SR
    s = np.zeros(n)
    for m in notas:
        f = NOTA(m)
        for dt in (-0.012, -0.006, -0.002, 0.002, 0.006, 0.012):
            s += serra(f * (1 + dt), n, RNG.uniform(0, 6.28), harm=28)
    fcs = fc0 + (fc1 - fc0) * np.minimum(1, t / max(dur * 0.6, 0.01))
    s = filtro_movel(s, fcs)
    env = np.minimum(1, t / ataque) * np.clip((dur - t) / solta, 0, 1)
    return s * env * vol / (len(notas) * 6)


def pad_cosmico(notas, dur, vol):
    n = int(dur * SR)
    t = np.arange(n) / SR
    s = np.zeros(n)
    for m in notas:
        f = NOTA(m)
        for dt in (-0.008, 0.0, 0.008):
            s += serra(f * (1 + dt), n, RNG.uniform(0, 6.28), harm=20)
    lfo = 900 + 700 * (0.5 + 0.5 * np.sin(2 * np.pi * 0.18 * t))
    s = filtro_movel(s, lfo, 48)
    s += 0.3 * np.sin(2 * np.pi * NOTA(notas[0] - 12) * t)
    env = np.minimum(1, t / 1.5) * np.clip((dur - t) / 1.2, 0, 1)
    return s * env * vol / (len(notas) * 3)


def brilho(f, vol):
    n = int(0.9 * SR)
    t = np.arange(n) / SR
    s = np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * f * 2 * t) * np.exp(-t * 10)
    return s * np.minimum(1, t / 0.002) * np.exp(-t * 5) * vol


def baixo_seq(f, vol, abertura):
    n = int(S16 * 0.95 * SR)
    t = np.arange(n) / SR
    s = serra(f, n, harm=30) + 0.5 * serra(f * 1.005, n, harm=30)
    fc = 200 + abertura * 3000 * np.exp(-t * 18) + abertura * 400
    s = filtro_movel(s, fc, 6)
    return sat(s * np.minimum(1, t / 0.003) * np.exp(-t * 5) * vol, 1.5)


def lead(notas, t0, n_total, vol):
    freq = np.zeros(n_total)
    amp = np.zeros(n_total)
    t = t0
    ant = None
    for m, tempos in notas:
        dur = tempos * BEAT
        a, b = int(t * SR), min(n_total, int((t + dur) * SR))
        if b > a:
            f = NOTA(m)
            k = np.arange(b - a) / SR
            f0 = ant or f
            freq[a:b] = (f + (f0 - f) * np.exp(-k / 0.03)) * (1 + 0.004 * np.sin(2 * np.pi * 5.5 * k) * np.clip((k - 0.3) / 0.3, 0, 1))
            amp[a:b] = np.minimum(1, k / 0.02) * np.clip((dur - k) / 0.05, 0, 1)
            ant = f
        t += dur
    amp = lp(amp, 30)
    s = np.zeros(n_total)
    for dt in (-0.005, 0.0, 0.005):
        fase = 2 * np.pi * np.cumsum(freq * (1 + dt)) / SR
        s += sum(np.sin(h * fase) / h for h in range(1, 14))
    return lp(s, 4500) * amp * vol / 3


def bumbo(vol):
    n = int(0.5 * SR)
    t = np.arange(n) / SR
    f = 44 + 120 * np.exp(-t * 40)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 6) + lp(RNG.normal(0, 1, n), 6000) * np.exp(-t * 200) * 0.3
    return sat(s * vol, 2.2)


def caixa(vol):
    n = int(0.6 * SR)
    t = np.arange(n) / SR
    s = bp(RNG.normal(0, 1, n), 1200, 8000) * np.exp(-t * 9) + np.sin(2 * np.pi * 190 * t) * np.exp(-t * 30) * 0.5
    return s * vol


def chimbal(vol):
    n = int(0.06 * SR)
    t = np.arange(n) / SR
    return hp(RNG.normal(0, 1, n), 9000) * np.exp(-t * 70) * vol


def laser(vol):
    n = int(0.6 * SR)
    t = np.arange(n) / SR
    f = 3200 * np.exp(-t * 7) + 120
    s = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * np.exp(-t * 5)
    return lp(s, 7000) * vol


def boom(vol):
    n = int(4.5 * SR)
    t = np.arange(n) / SR
    f = 28 + 70 * np.exp(-t * 6)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 1.0) * 1.5
    s += lp(RNG.normal(0, 1, n), 300) * np.exp(-t * 5) * 1.2
    s += hp(RNG.normal(0, 1, n), 4000) * np.exp(-t * 1.2) * 0.12
    return sat(s * vol, 1.3)


def varredura(dur, vol, sobe=True):
    n = int(dur * SR)
    t = np.arange(n) / SR
    r = RNG.normal(0, 1, n)
    out = np.zeros(n)
    for k in range(20):
        a, b = k * n // 20, (k + 1) * n // 20
        p = k / 19 if sobe else 1 - k / 19
        out[a:b] = bp(r, 150 + 3000 * p, 600 + 9000 * p)[a:b]
    env = (t / dur) ** 2 if sobe else np.exp(-t * 2)
    return out * env * vol


def eco(x, atraso, ganho, vezes=4):
    d = int(atraso * SR)
    out = np.concatenate([x, np.zeros(d * vezes)])
    for k in range(1, vezes + 1):
        out[d * k: d * k + len(x)] += x * ganho ** k
    return out


def gera(total, inicio, viradas, final):
    q = lambda x: inicio + round((x - inicio) / BEAT) * BEAT
    viradas = [q(v) for v in viradas]
    final = q(final)
    v_zoom, v_quintal, v_sing = viradas[:3]
    N = int((total + 6) * SR)
    out = np.zeros(N)
    brilhos = np.zeros(N)

    def poe(s, inst, g=1.0, alvo=None):
        alvo = out if alvo is None else alvo
        i = int(inst * SR)
        if i < 0:
            s, i = s[-i:], 0
        e = min(N, i + len(s))
        alvo[i:e] += s[: e - i] * g

    comp = 4 * BEAT
    acorde = lambda t: int((t - inicio) // comp) % 4

    # pad cósmico do início ao quintal; supersaw a partir do quintal
    t = 0.0
    while t < v_quintal - 0.1:
        c = acorde(max(t, inicio))
        poe(pad_cosmico([m - 12 for m in ACORDES[c]] + [ACORDES[c][0]], comp + 1.2, 0.8), t)
        t += comp
    t = v_quintal
    while t < final - 1e-6:
        c = acorde(t)
        vol = 0.55 if t < v_sing else 0.7
        poe(supersaw(ACORDES[c] + [ACORDES[c][0] + 12], comp + 0.3, vol, 1500, 5000, 0.02, 0.3), t)
        t += comp
    # brilhos com eco (universo e mergulho)
    n = 0
    t = inicio
    while t < v_quintal - 1e-6:
        if n % 3 == 0 or t >= v_zoom:
            c = acorde(t)
            m = ACORDES[c][(n * 2) % 3] + 24
            poe(brilho(NOTA(m), 0.10), t, alvo=brilhos)
        n += 1
        t += BEAT / 2 if t < v_zoom else BEAT / 4
    out += eco(brilhos, BEAT * 0.75, 0.45, 5)[:N]
    # baixo sequenciado: entra no mergulho com filtro fechado e vai abrindo
    n = 0
    t = v_zoom
    while t < final - 1e-6:
        c = acorde(t)
        if t < v_quintal:
            ab = 0.1 + 0.9 * ((t - v_zoom) / (v_quintal - v_zoom)) ** 1.5
            vol = 0.35
        else:
            ab, vol = 1.0, 0.45
        poe(baixo_seq(NOTA(BAIXO[c] + 12 + SEQ[n % 16]), vol, ab), t)
        n += 1
        t = v_zoom + n * S16
    # sub grave sustentado no universo
    poe(lp(np.sin(2 * np.pi * NOTA(33) * np.arange(int(v_zoom * SR)) / SR), 200)
        * np.minimum(1, np.arange(int(v_zoom * SR)) / SR / 2.0), 0, 0.35)
    # bateria eletrônica a partir do quintal
    n = 0
    t = v_quintal
    while t < final - 1e-6:
        k = n % 16
        if k % 4 == 0:
            poe(bumbo(0.95), t)
        if k in (4, 12):
            poe(caixa(0.6), t)
        if k % 2 == 1:
            poe(chimbal(0.16), t)
        if t >= v_sing and k in (3, 7, 11, 15):
            poe(chimbal(0.1), t)
        n += 1
        t = v_quintal + n * S16
    # melodia de sintetizador: entra no quintal
    out += eco(lead(MELODIA, v_quintal, N, 0.22), BEAT * 0.75, 0.3, 3)[:N]
    out += lead([(m + 12, d) for m, d in MELODIA[:6]], v_sing, N, 0.12)
    # transições: varredura subindo, boom e laser
    poe(boom(0.6), inicio)
    for v, vol in [(v_zoom, 0.8), (v_quintal, 1.0), (v_sing, 0.9)]:
        poe(varredura(1.3, 0.3), v - 1.3)
        poe(boom(vol), v)
        poe(laser(0.25), v)
        poe(varredura(1.5, 0.15, sobe=False), v)
    poe(varredura(1.5, 0.35), final - 1.5)
    poe(boom(1.1), final)
    poe(laser(0.3), final)
    poe(supersaw([45, 57, 61, 64, 69, 73, 76], 5.0, 1.2, 4000, 2000, 0.02, 2.5), final)   # Lá maior
    poe(eco(brilho(NOTA(88), 0.3), BEAT * 0.75, 0.5, 6), final)
    # espaço: reverberação longa
    ir_n = int(3.0 * SR)
    ir = RNG.normal(0, 1, ir_n) * np.exp(-np.arange(ir_n) / SR * 1.8) * 0.035
    ir[0] = 1.0
    L = N + ir_n
    wet = np.fft.irfft(np.fft.rfft(out, L) * np.fft.rfft(ir, L))[:N]
    mix = (0.65 * out + 0.35 * lp(wet, 8000))[: int(total * SR)]
    mix = sat(mix / np.max(np.abs(mix)) * 1.25, 1.2)
    return (mix / (np.max(np.abs(mix)) + 1e-9)).astype("float32"), viradas, final
