# -*- coding: utf-8 -*-
"""Mapeia os TEXTOS editaveis da home (o que pode virar ficha)."""
import re
import os

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
caminho = os.path.join(BASE, "index.html")
html = open(caminho, encoding="utf-8").read()

print("=" * 78)
print("BLOCOS DE TEXTO DA HOME")
print("=" * 78)

# 1) titulos de secao (h2) com o paragrafo seguinte
print("\n--- TITULOS/SUBTITULOS DE SECAO (h2 + paragrafo) ---")
for m in re.finditer(r'<h2[^>]*>(.*?)</h2>\s*(?:<p[^>]*>(.*?)</p>)?', html, re.S):
    titulo = re.sub(r"<[^>]+>", "", m.group(1)).strip()
    sub = re.sub(r"<[^>]+>", "", m.group(2) or "").strip()
    if titulo:
        print(f"  H2: {titulo[:66]}")
        if sub:
            print(f"      {sub[:70]}")

# 2) cards de numeros
print("\n--- CARDS DE NUMEROS ---")
for m in re.finditer(r'<a class="home-stat[^"]*"[^>]*data-secao-chave="([^"]+)"[^>]*>(.*?)</a>', html, re.S):
    corpo = m.group(2)
    val = re.search(r'home-stat__value[^>]*>(.*?)<', corpo, re.S)
    lab = re.search(r'home-stat__label[^>]*>(.*?)<', corpo, re.S)
    des = re.search(r'home-stat__desc[^>]*>(.*?)<', corpo, re.S)
    limpa = lambda x: re.sub(r"<[^>]+>", "", x.group(1)).strip() if x else ""
    print(f"  [{m.group(1):20}] {limpa(val):>5}  {limpa(lab):22} | {limpa(des)[:40]}")

# 3) pilares
print("\n--- PILARES ---")
for m in re.finditer(r'home-pillar__title[^>]*>(.*?)</', html, re.S):
    print("  ", re.sub(r"<[^>]+>", "", m.group(1)).strip()[:60])
for m in re.finditer(r'home-pillar__text[^>]*>(.*?)</', html, re.S):
    print("     ", re.sub(r"<[^>]+>", "", m.group(1)).strip()[:66])

# 4) como ajudar
print("\n--- COMO AJUDAR (cards) ---")
for m in re.finditer(r'home-help__title[^>]*>(.*?)</', html, re.S):
    print("  ", re.sub(r"<[^>]+>", "", m.group(1)).strip()[:60])
for m in re.finditer(r'home-help__text[^>]*>(.*?)</', html, re.S):
    print("     ", re.sub(r"<[^>]+>", "", m.group(1)).strip()[:66])

# 5) hero
print("\n--- HERO (chamada principal) ---")
for m in re.finditer(r'<h1[^>]*>(.*?)</h1>', html, re.S):
    print("  H1:", re.sub(r"<[^>]+>", " ", m.group(1)).strip()[:70])

print()
print("totais:",
      "numeros =", len(re.findall(r'home-stat__value', html)),
      "| pilares =", len(re.findall(r'home-pillar__title', html)),
      "| como ajudar =", len(re.findall(r'home-help__title', html)))
