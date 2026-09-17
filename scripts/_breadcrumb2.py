# -*- coding: utf-8 -*-
"""
Corrige o breadcrumb da pagina Saude:
  - sai de DENTRO do hero (nao polui mais)
  - vira uma faixa clara logo ABAIXO do hero
  - simplificado: Início > Nossas Ações > Saúde (com cara de link)
"""
import os
import re

BASE = r"G:/.shortcut-targets-by-id/18wGiptBKUmAmmkKHgdfu05TU4y_roWC1/BBDPRINT - BACKUP/BBDPRINT/App BBDPRiNT/PROJETOS/Projeto SER Sagi/projeto_SER_Sagi - Hermes"

# ============================================================
# 1) CSS — ajuste para o modo claro (fora do hero)
# ============================================================
p = os.path.join(BASE, "css", "style.css")
txt = open(p, encoding="utf-8", newline="").read()

DE = """/* Sobre fundo claro (uso opcional fora do hero) */
.breadcrumb--claro a { color: var(--ocean); }
.breadcrumb--claro li + li::before { color: rgba(15, 92, 115, 0.5); }
.breadcrumb--claro [aria-current="page"] { color: var(--ocean-deep); }"""

PARA = """/* Fora do hero (fundo claro) — faixa acima do conteudo */
.breadcrumb--claro { margin-bottom: 0; }
.breadcrumb--claro a { color: var(--ocean); }
.breadcrumb--claro a:hover { color: var(--ocean-deep); }
.breadcrumb--claro li + li::before { color: rgba(15, 92, 115, 0.45); }
.breadcrumb--claro [aria-current="page"] { color: var(--ocean-deep); font-weight: 600; }"""

assert DE in txt, "css: bloco .breadcrumb--claro nao encontrado"
txt = txt.replace(DE, PARA, 1)
open(p, "w", encoding="utf-8", newline="").write(txt)
print("  ✅ css: modo claro do breadcrumb ajustado")

# ============================================================
# 2) saude.html — tira do hero e poe abaixo dele
# ============================================================
p = os.path.join(BASE, "saude.html")
txt = open(p, encoding="utf-8", newline="").read()

# 2.1 remove o breadcrumb de dentro do banner
padrao = re.compile(r'\s*<nav class="breadcrumb" aria-label="Você está aqui">.*?</nav>', re.DOTALL)
txt, qtd = padrao.subn("", txt, count=1)
assert qtd == 1, "saude.html: breadcrumb dentro do hero nao encontrado"
print("  ✅ saude.html: breadcrumb removido de dentro do hero")

# 2.2 insere logo DEPOIS do banner (antes da secao de conteudo)
ANCORA = '''    </section>
    <section class="mx-auto max-w-7xl px-4 py-16 lg:px-8">
      <div class="grid gap-10 lg:grid-cols-[1.05fr_0.95fr] lg:items-start">'''

NOVO = '''    </section>

    <!-- 🧭 Caminho de navegacao (fora do hero) -->
    <nav class="breadcrumb breadcrumb--claro mx-auto max-w-7xl px-4 pt-7 lg:px-8" aria-label="Você está aqui">
      <ol>
        <li><a href="./">Início</a></li>
        <li><a href="acoes.html">Nossas Ações</a></li>
        <li><span aria-current="page">Saúde</span></li>
      </ol>
    </nav>

    <section class="mx-auto max-w-7xl px-4 py-16 lg:px-8">
      <div class="grid gap-10 lg:grid-cols-[1.05fr_0.95fr] lg:items-start">'''

assert ANCORA in txt, "saude.html: ancora depois do banner nao encontrada"
txt = txt.replace(ANCORA, NOVO, 1)
print("  ✅ saude.html: breadcrumb inserido abaixo do hero")

# 2.3 simplifica os dados estruturados (3 niveis)
DE = '''      { "@type": "ListItem", "position": 3, "name": "Saúde", "item": "https://bimbord.github.io/projeto_ser_sagi/saude.html" },
      { "@type": "ListItem", "position": 4, "name": "Consultório Odontológico", "item": "https://bimbord.github.io/projeto_ser_sagi/saude.html" }'''
PARA = '''      { "@type": "ListItem", "position": 3, "name": "Saúde", "item": "https://bimbord.github.io/projeto_ser_sagi/saude.html" }'''
assert DE in txt, "saude.html: JSON-LD nao encontrado"
txt = txt.replace(DE, PARA, 1)
print("  ✅ saude.html: dados estruturados simplificados (3 niveis)")

open(p, "w", encoding="utf-8", newline="").write(txt)
print("  ✅ saude.html salvo")
