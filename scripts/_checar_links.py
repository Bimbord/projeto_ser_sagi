# -*- coding: utf-8 -*-
"""Checa se todos os links internos (*.html) das paginas existem de verdade."""
import os
import re

BASE = r"G:/.shortcut-targets-by-id/18wGiptBKUmAmmkKHgdfu05TU4y_roWC1/BBDPRINT - BACKUP/BBDPRINT/App BBDPRiNT/PROJETOS/Projeto SER Sagi/projeto_SER_Sagi - Hermes"

paginas = sorted(f for f in os.listdir(BASE) if f.endswith(".html"))

# conjunto com TODOS os arquivos do projeto (css, js, img, html...)
arquivos = set()
for raiz, dirs, arqs in os.walk(BASE):
    dirs[:] = [d for d in dirs if d not in (".git", "__pycache__", "instagram-scrap")]
    for a in arqs:
        arquivos.add(os.path.relpath(os.path.join(raiz, a), BASE).replace("\\", "/"))

problemas = []
total_links = 0

for nome in paginas:
    txt = open(os.path.join(BASE, nome), encoding="utf-8").read()
    for href in re.findall(r'href="([^"]+)"', txt):
        if href.startswith(("http://", "https://", "mailto:", "tel:", "#")):
            continue
        alvo = href.split("#")[0].split("?")[0]
        if not alvo or alvo in ("./", "../"):
            continue
        total_links += 1
        if alvo not in arquivos:
            problemas.append((nome, href))

print(f"Páginas: {len(paginas)} | Links internos verificados: {total_links}")
if problemas:
    print(f"\n❌ LINKS QUEBRADOS ({len(problemas)}):")
    for pag, href in problemas:
        print(f"   [{pag}] -> {href}")
else:
    print("\n✅ Nenhum link quebrado — todos apontam para páginas existentes.")

# confere tambem css/js versionados
sem_versao = [n for n in paginas
              if 'css/style.css?v=' not in open(os.path.join(BASE, n), encoding="utf-8").read()]
print(f"\nPáginas sem cache-busting (?v=): {len(sem_versao)}" + (f" -> {sem_versao}" if sem_versao else " ✅"))
