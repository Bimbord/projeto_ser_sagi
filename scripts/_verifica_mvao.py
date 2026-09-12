# -*- coding: utf-8 -*-
"""Verifica se a seção Missão/Visão/Valores/Objetivo ficou com 4 cards irmãos."""
import os, re, urllib.request

BASE = r"C:/Projetos Code/Projeto SER Sagi/projeto_SER_Sagi - Hermes"
html = open(os.path.join(BASE, "quem-somos.html"), encoding="utf-8").read()

# 1) balanço geral de tags na página inteira
print("=== 1) Balanço de tags na página inteira ===")
for tag in ("article", "div", "section", "a"):
    a = len(re.findall(rf"<{tag}[\s>]", html))
    f = len(re.findall(rf"</{tag}>", html))
    print(f"   <{tag}>: {a} abre / {f} fecha  {'OK' if a == f else '❌ DESBALANCEADO'}")

# 2) a grade dos 4 cards
print("\n=== 2) Grade Missão/Visão/Valores/Objetivo ===")
i = html.find('md:grid-cols-2 xl:grid-cols-4')
ini = html.rfind("<div", 0, i)
fim = html.find("</section>", ini)
sec = html[ini:fim]
# conta os <article> que são filhos DIRETOS (no nível do grid)
bloco = html[html.find(">", i) + 1: html.rfind("</div>", ini, fim)]
artigos = re.findall(r'<article class="rounded-3xl bg-white p-6 shadow-soft"><h3[^>]*>([^<]+)</h3>', bloco)
print(f"   cards encontrados: {len(artigos)}")
for j, a in enumerate(artigos, 1):
    print(f"     {j}. {a}")
print(f"   {'✅ 4 cards separados' if len(artigos) == 4 else '❌ ainda agrupado'}")

# 3) nenhum article aninhado?
print("\n=== 3) Existe <article> dentro de <article>? ===")
aninhado = re.search(r"<article[^>]*>(?:(?!</article>).)*<article", html, re.S)
print("   ❌ SIM — ainda há aninhamento" if aninhado else "   ✅ não há aninhamento")

# 4) a página responde?
print("\n=== 4) Página no ar ===")
try:
    with urllib.request.urlopen("http://127.0.0.1:5501/quem-somos.html", timeout=5) as r:
        print(f"   HTTP {r.status}")
except Exception as e:
    print("   ❌", e)
