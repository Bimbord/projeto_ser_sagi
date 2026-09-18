# -*- coding: utf-8 -*-
"""
Levanta os TAMANHOS de imagem do site (px exibidos), a partir do próprio código.
Gera o mapa: contexto (arquivo/classe) -> altura exibida + largura estimada.
"""
import glob
import os
import re
from collections import defaultdict

BASE = r"G:/.shortcut-targets-by-id/18wGiptBKUmAmmkKHgdfu05TU4y_roWC1/BBDPRINT - BACKUP/BBDPRINT/App BBDPRiNT/PROJETOS/Projeto SER Sagi/projeto_SER_Sagi - Hermes"

# Tailwind: altura em px
H = {"h-32": 128, "h-40": 160, "h-44": 176, "h-48": 192, "h-56": 224, "h-64": 256}

# largura útil: max-w-7xl (1280) - px-4 lg:px-8 (32 de cada lado)
CONT = 1280 - 64  # 1216

grep = defaultdict(lambda: {"n": 0, "arquivos": set()})

for arq in sorted(glob.glob(os.path.join(BASE, "*.html"))):
    nome = os.path.basename(arq)
    txt = open(arq, encoding="utf-8").read()
    for m in re.finditer(r'<img[^>]*class="([^"]*)"', txt):
        cls = m.group(1)
        h = next((k for k in H if re.search(rf'\b{k}\b', cls)), None)
        if not h:
            continue
        # contexto: qual seção/grid está por perto (300 chars antes)
        antes = txt[max(0, m.start() - 400):m.start()]
        grade = ""
        for g in re.findall(r'grid-cols-\[?([^\s"\]]+)\]?|grid-cols-(\d)', antes):
            grade = g[0] or g[1]
        chave = (H[h], grade or "1")
        grep[chave]["n"] += 1
        grep[chave]["arquivos"].add(nome)

print(f"{'altura':>7} {'colunas':>8} {'largura est.':>13} {'imgs':>5}  onde")
print("-" * 78)
for (alt, col), info in sorted(grep.items(), key=lambda x: -x[1]["n"]):
    try:
        c = int(col)
    except ValueError:
        c = 2  # ex.: 1fr_1fr
    larg = CONT if c == 1 else (CONT - (c - 1) * 24) // c
    ex = sorted(info["arquivos"])[:4]
    print(f"{alt:>6}px {c:>8} {larg:>10}px {info['n']:>5}  {', '.join(ex)}{'…' if len(info['arquivos']) > 4 else ''}")

print("\n--- outros (sem altura fixa) ---")
print(f"  hero (banner): largura total × clamp(380px, 46vh, 560px)")
print(f"  home hero:     largura total × 100vh (tela cheia)")
print(f"  carrossel:     min(80vw, 384px) × 256px")
print(f"  galeria:       {(CONT - 48) // 3}px × altura natural (proporção livre)")
print(f"  lightbox:      até 1100px × 84vh")
