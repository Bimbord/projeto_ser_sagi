# -*- coding: utf-8 -*-
"""Reverte o título/H2 do banner da saude.html para 'Consultório Odontológico'
   (a mudança para 'Saúde' fica só no link/URL da página)."""
import os

BASE = r"C:/Projetos Code/Projeto SER Sagi/projeto_SER_Sagi - Hermes"
p = os.path.join(BASE, "saude.html")

txt = open(p, encoding="utf-8", newline="").read()

TROCAS = [
    (
        "<title>Saúde | Instituto S.E.R. Sagi</title>",
        "<title>Consultório Odontológico | Instituto S.E.R. Sagi</title>",
    ),
    (
        '<h2 class="mt-4 max-w-4xl text-4xl font-extrabold leading-tight sm:text-5xl">Saúde</h2>',
        '<h2 class="mt-4 max-w-4xl text-4xl font-extrabold leading-tight sm:text-5xl">Consultório Odontológico</h2>',
    ),
    (
        '<p class="mt-6 max-w-3xl text-lg text-white/85">Cuidado com a saúde da comunidade do Sagi — começando pelo consultório odontológico, com prevenção, tratamento e acolhimento.</p>',
        '<p class="mt-6 max-w-3xl text-lg text-white/85">Cuidado com a saúde bucal da comunidade: prevenção, tratamento e autoestima.</p>',
    ),
]

for de, para in TROCAS:
    if de in txt:
        txt = txt.replace(de, para)
        print(f"  revertido: {de[:70]}...")
    else:
        print(f"  ATENÇÃO - não encontrado: {de[:70]}...")

open(p, "w", encoding="utf-8", newline="").write(txt)
print("  saude.html salvo")
