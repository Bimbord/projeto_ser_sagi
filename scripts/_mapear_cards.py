# -*- coding: utf-8 -*-
"""Mapeia os cards (link + titulo) das paginas de hub/acoes."""
import os
import re

BASE = r"G:/.shortcut-targets-by-id/18wGiptBKUmAmmkKHgdfu05TU4y_roWC1/BBDPRINT - BACKUP/BBDPRINT/App BBDPRiNT/PROJETOS/Projeto SER Sagi/projeto_SER_Sagi - Hermes"

PAGINAS = ["acoes.html", "esporte.html", "educacao.html", "instalacoes.html",
           "cultura.html", "preservacao-ambiental.html", "acoes-solidarias.html", "saude.html"]

for nome in PAGINAS:
    p = os.path.join(BASE, nome)
    if not os.path.isfile(p):
        print(f"\n=== {nome} === (nao existe)")
        continue
    txt = open(p, encoding="utf-8").read()
    # titulo da pagina
    t = re.search(r"<title>([^<]*)</title>", txt)
    print(f"\n=== {nome} ===")
    print(f"    titulo: {t.group(1) if t else '?'}")

    # cards: <a href="X" ...> ... <h3 ...>Titulo</h3>
    cards = re.findall(r'<a href="([^"]+)"[^>]*class="(?:home-card|block)[^"]*"[^>]*>.*?<h3[^>]*>([^<]+)</h3>', txt, re.DOTALL)
    if cards:
        print(f"    cards ({len(cards)}):")
        for href, titulo in cards:
            print(f"       • {titulo.strip():32} -> {href}")
    else:
        # fallback: titulos h2/h3 soltos
        hs = re.findall(r"<h[23][^>]*>([^<]{3,60})</h[23]>", txt)
        print(f"    (sem cards-padrao) titulos: {hs[:8]}")
