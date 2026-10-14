"""Reels da semana 19 a 23/10. Uso: python3 reels_semana.py <a|b|c> [previa t1 t2 ...]"""
import sys
sys.path.insert(0, "/home/claude")
from reels_texto import Reels, WHITE, ORANGE, GREY

OUT = "/mnt/user-data/outputs/singular_semana_19-10"


def reels_a():  # segunda 19/10: frase com "singular", P&B
    return Reels([
        {"beats": 8, "kick": "// SEGUNDA SINGULAR", "linhas": [
            (0, "Toda empresa", 100, WHITE, "b"), (1, "tem um ponto", 100, WHITE, "b"), (2.5, "singular.", 128, ORANGE, "b")]},
        {"beats": 12, "kick": "// ONDE TUDO SE DECIDE", "linhas": [
            (0, "É ali que um", 84, WHITE, "b"), (1, "detalhe vira", 84, WHITE, "b"), (3, "multa,", 84, GREY, "b"),
            (5, "retrabalho", 84, GREY, "b"), (7, "ou resultado.", 84, ORANGE, "b")]},
    ], ["A gente encontra o seu."], calmo=True)


def reels_b():  # terça 20/10: alerta FGTS/INSS
    return Reels([
        {"beats": 8, "kick": "// ALERTA DA OPERAÇÃO", "linhas": [
            (0, "Sua guia do FGTS", 92, WHITE, "b"), (1, "não bate com", 92, WHITE, "b"), (2, "a folha?", 110, ORANGE, "b"),
            (None, None, 40, None, None), (4, "Quase sempre o erro está na folha, não na guia.", 46, GREY, "l")]},
        {"beats": 12, "kick": "// DE ONDE VEM A DIFERENÇA", "itens": [
            (0.5, "Rubrica com incidência errada"), (2.5, "13º e reflexos fora do lugar"),
            (4.5, "Dissídio na competência errada"), (6.5, "Recálculo sem retransmitir o evento"),
            (8.5, "Rescisão no começo do mês")]},
        {"beats": 10, "kick": "// ANTES DE PAGAR", "itens": [
            (0.5, "Bases do eSocial contra a folha"), (2.5, "Incidência de toda rubrica nova"),
            (4.5, "Retransmitir depois de recalcular")], "linhas": []},
        {"beats": 6, "kick": "// SALVA E COMPARTILHA", "linhas": [
            (0, "Manda para quem", 92, WHITE, "b"), (1, "fecha a folha aí.", 92, ORANGE, "b"),
            (None, None, 40, None, None), (2.5, "Checklist completo no carrossel de hoje.", 46, GREY, "l")]},
    ], ["Se a sua guia não bate,", "a gente encontra o porquê."])


def reels_c():  # quinta 22/10: 13º, Reels de experimento
    return Reels([
        {"beats": 8, "kick": "// 13º SALÁRIO", "linhas": [
            (0, "A primeira parcela", 88, WHITE, "b"), (1, "vence em", 88, WHITE, "b")],
         "numero": (2, "30/11", "e a conferência começa agora.")},
        {"beats": 16, "kick": "// CHEQUE ANTES DE CALCULAR", "itens": [
            (0.5, "Médias de variáveis do ano"), (2.5, "Afastamentos na contagem"), (4.5, "Avos dos admitidos no ano"),
            (6.5, "Adiantamento das férias"), (8.5, "Incidência das rubricas"),
            (10.5, "Provisão igual à folha")]},
        {"beats": 6, "kick": "// SALVA ESTE CHECKLIST", "linhas": [
            (0, "Manda para quem", 92, WHITE, "b"), (1, "calcula o 13º aí.", 92, ORANGE, "b")]},
    ], ["13º sem retrabalho", "começa em outubro."])


if __name__ == "__main__":
    import os
    os.makedirs(OUT, exist_ok=True)
    qual = sys.argv[1]
    r = {"a": reels_a, "b": reels_b, "c": reels_c}[qual]()
    nomes = {"a": "19-10_reels_singular.mp4", "b": "20-10_reels_alerta_fgts.mp4", "c": "22-10_reels_13o.mp4"}
    if len(sys.argv) > 2 and sys.argv[2] == "previa":
        r.render(None, previa=[float(x) for x in sys.argv[3:]])
    else:
        r.render(f"{OUT}/{nomes[qual]}")
