# -*- coding: utf-8 -*-
"""Aplica bg-oceanDeep (azul petróleo escuro) no rodapé de todas as páginas."""
import os

BASE = r"C:/Projetos Code/Projeto SER Sagi/projeto_SER_Sagi - Hermes"

total = 0
for nome in sorted(os.listdir(BASE)):
    if not nome.endswith(".html"):
        continue
    p = os.path.join(BASE, nome)
    txt = open(p, encoding="utf-8").read()
    if 'bg-leaf text-white' not in txt:
        continue
    novo = txt.replace('<footer class="bg-leaf text-white">', '<footer class="bg-oceanDeep text-white">')
    open(p, "w", encoding="utf-8", newline="\n").write(novo)
    total += 1

print(f"✅ rodapé -> bg-oceanDeep em {total} páginas")
