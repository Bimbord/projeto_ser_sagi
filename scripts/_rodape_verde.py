# -*- coding: utf-8 -*-
"""Troca o fundo do rodapé de bg-slate-950 (quase preto) para bg-leaf (verde do hero)."""
import os

BASE = r"C:/Projetos Code/Projeto SER Sagi/projeto_SER_Sagi - Hermes"

total = 0
for nome in sorted(os.listdir(BASE)):
    if not nome.endswith(".html"):
        continue
    p = os.path.join(BASE, nome)
    txt = open(p, encoding="utf-8").read()
    if 'bg-slate-950 text-white' not in txt:
        continue
    novo = txt.replace('<footer class="bg-slate-950 text-white">', '<footer class="bg-leaf text-white">')
    open(p, "w", encoding="utf-8", newline="\n").write(novo)
    total += 1

print(f"✅ fundo do rodapé trocado para verde (bg-leaf) em {total} páginas")
