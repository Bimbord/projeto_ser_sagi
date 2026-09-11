# -*- coding: utf-8 -*-
"""Extrai as seções relevantes da index.html para análise (hero + pilares)."""
import re, os

BASE = r"C:/Projetos Code/Projeto SER Sagi/projeto_SER_Sagi - Hermes"
html = open(os.path.join(BASE, "index.html"), encoding="utf-8").read()

# --- 1) HERO / topo ---
m = re.search(r'<main[^>]*>(.{0,4000})', html, re.S)
print("=" * 70)
print("TOPO DA HOME (hero) — primeiros 1800 caracteres:")
print("=" * 70)
topo = m.group(1) if m else "(nao achou)"
# limpa svg para nao poluir
topo_limpo = re.sub(r'<svg.*?</svg>', '[SVG]', topo, flags=re.S)
print(topo_limpo[:1800])

# --- 2) PILARES ---
mi = html.find('Nossos pilares')
if mi == -1:
    print("\n(secao de pilares nao encontrada)")
else:
    ini = html.rfind('<section', 0, mi)
    fim = html.find('</section>', mi)
    sec = html[ini:fim + 10]
    # separa os 5 cards
    cards = re.findall(r'<article class="home-card home-pillar">.*?</article>', sec, re.S)
    print("\n" + "=" * 70)
    print(f"PILARES — {len(cards)} cards encontrados:")
    print("=" * 70)
    for i, c in enumerate(cards, 1):
        limpo = re.sub(r'<svg.*?</svg>', '[SVG]', c, flags=re.S)
        titulo = re.search(r'home-card__title">([^<]*)<', c)
        print(f"\n--- CARD {i}: {titulo.group(1) if titulo else '?'} ---")
        print(limpo.strip()[:700])
