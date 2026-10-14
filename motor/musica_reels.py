"""Trilha curta para Reels, na mesma família sonora da trilha intergaláctica aprovada.
Bateria desde o primeiro tempo (gancho), varredura e impacto em cada troca de tela,
acorde final grande no cartão da Singular."""
import numpy as np
from musica_galactica import (SR, BEAT, S16, RNG, NOTA, ACORDES, BAIXO, SEQ, MELODIA, lp, sat, supersaw,
                              pad_cosmico, brilho, baixo_seq, lead, bumbo, caixa, chimbal, laser, boom,
                              varredura, eco)


def gera(total, inicio, trocas, final, calmo=False):
    N = int((total + 6) * SR)
    out = np.zeros(N)

    def poe(s, inst, g=1.0):
        i = int(inst * SR)
        if i < 0:
            s, i = s[-i:], 0
        e = min(N, i + len(s))
        out[i:e] += s[: e - i] * g

    comp = 4 * BEAT
    acorde = lambda t: int((t - inicio) // comp) % 4
    t = inicio
    while t < final - 1e-6:
        c = acorde(t)
        if calmo:
            poe(pad_cosmico([m - 12 for m in ACORDES[c]] + [ACORDES[c][0]], comp + 1.0, 0.9), t)
        else:
            poe(supersaw(ACORDES[c] + [ACORDES[c][0] + 12], comp + 0.3, 0.6, 1500, 5000, 0.02, 0.3), t)
        t += comp
    n = 0
    t = inicio
    while t < final - 1e-6:
        c = acorde(t)
        poe(baixo_seq(NOTA(BAIXO[c] + 12 + SEQ[n % 16]), 0.32 if calmo else 0.45, 0.5 if calmo else 1.0), t)
        n += 1
        t = inicio + n * S16
    n = 0
    t = inicio
    while t < final - 1e-6:
        k = n % 16
        if calmo:
            if k in (0, 8):
                poe(bumbo(0.8), t)
            if k % 4 == 2:
                poe(chimbal(0.1), t)
        else:
            if k % 4 == 0:
                poe(bumbo(0.95), t)
            if k in (4, 12):
                poe(caixa(0.6), t)
            if k % 2 == 1:
                poe(chimbal(0.16), t)
        n += 1
        t = inicio + n * S16
    if trocas:
        out[:] += eco(lead(MELODIA, trocas[0], N, 0.16 if calmo else 0.2), BEAT * 0.75, 0.3, 3)[:N]
    poe(boom(0.7), inicio)
    poe(laser(0.2), inicio)
    for v in trocas:
        poe(varredura(1.0, 0.25), v - 1.0)
        poe(boom(0.75), v)
        poe(varredura(1.2, 0.12, sobe=False), v)
    poe(varredura(1.5, 0.35), final - 1.5)
    poe(boom(1.1), final)
    poe(laser(0.3), final)
    poe(supersaw([45, 57, 61, 64, 69, 73, 76], 5.0, 1.2, 4000, 2000, 0.02, 2.5), final)
    poe(eco(brilho(NOTA(88), 0.3), BEAT * 0.75, 0.5, 6), final)
    ir_n = int(3.0 * SR)
    ir = RNG.normal(0, 1, ir_n) * np.exp(-np.arange(ir_n) / SR * 1.8) * 0.035
    ir[0] = 1.0
    L = N + ir_n
    wet = np.fft.irfft(np.fft.rfft(out, L) * np.fft.rfft(ir, L))[:N]
    mix = (0.65 * out + 0.35 * lp(wet, 8000))[: int(total * SR)]
    mix = sat(mix / np.max(np.abs(mix)) * 1.25, 1.2)
    f = int(0.8 * SR)
    mix[-f:] *= np.linspace(1, 0, f)
    return (mix / (np.max(np.abs(mix)) + 1e-9)).astype("float32")
