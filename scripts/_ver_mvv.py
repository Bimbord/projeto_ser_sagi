# -*- coding: utf-8 -*-
"""Mostra a seção Missão/Visão/Valores/Objetivo do quem-somos.html (formatação atual)."""
import os, re

BASE = r"C:/Projetos Code/Projeto SER Sagi/projeto_SER_Sagi - Hermes"
html = open(os.path.join(BASE, "quem-somos.html"), encoding="utf-8").read()

i = html.find('grid gap-6 md:grid-cols-2 xl:grid-cols-4')
ini = html.rfind('<div', 0, i)
fim = html.find('</article>', html.find('Objetivo'))
sec = html[ini:fim + len('</article>')]

print("=== TRECHO ATUAL (formatado) ===")
# quebra em tags para ler
formatado = re.sub(r'><', '>\n<', sec)
print(formatado)
