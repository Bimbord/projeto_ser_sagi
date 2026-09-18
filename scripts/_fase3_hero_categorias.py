# -*- coding: utf-8 -*-
"""
FASE 3 — Hero com imagem nas 4 CATEGORIAS
         (esporte, educacao, cultura, preservacao)

Transforma o banner simples no padrao da Saude:
  - section com `relative overflow-hidden banner-alto` (mais alto)
  - <img> de fundo com data-secao-img="hero" + data-categoria
  - <div class="banner-scrim"> (veu diagonal)
  - conteudo com `relative z-10` (por cima)

A imagem de reserva e ilustrativa; quando houver fotos em
`PARA O SITE/<categoria>/hero/`, o JS troca automaticamente.
"""
import os

BASE = r"G:/.shortcut-targets-by-id/18wGiptBKUmAmmkKHgdfu05TU4y_roWC1/BBDPRINT - BACKUP/BBDPRINT/App BBDPRiNT/PROJETOS/Projeto SER Sagi/projeto_SER_Sagi - Hermes"

CONFIG = {
    "esporte.html": ("Esporte", "sports,kids,team", "esporte"),
    "educacao.html": ("Educação", "classroom,education,kids", "educacao"),
    "cultura.html": ("Cultura", "community,culture,people", "cultura"),
    "preservacao-ambiental.html": ("Preservação", "beach,nature,sea", "preservacao"),
}

ABRE_ANTIGO = '<section class="page-banner text-white">'
ABRE_NOVO = '<section class="page-banner text-white relative overflow-hidden banner-alto">'

CAMADAS = '''{abre}
      <!-- CAMADA 1 · IMAGEM de fundo (ilustrativa — trocar por foto real em {pasta}/hero/) -->
      <img src="https://loremflickr.com/1600/600/{tema}?lock={lock}" alt="" aria-hidden="true" data-secao-img="hero" data-categoria="{cat}" class="absolute inset-0 h-full w-full object-cover">
      <!-- CAMADA 2 · SCRIM (véu diagonal, mesmo efeito do hero da home) -->
      <div class="banner-scrim absolute inset-0"></div>'''

feitos, problemas = [], []

for i, (nome, (cat, tema, pasta)) in enumerate(CONFIG.items(), 1):
    p = os.path.join(BASE, nome)
    if not os.path.isfile(p):
        problemas.append((nome, "nao existe"))
        continue
    txt = open(p, encoding="utf-8", newline="").read()

    if "banner-scrim" in txt:
        problemas.append((nome, "ja tinha hero com imagem"))
        continue
    if ABRE_ANTIGO not in txt:
        problemas.append((nome, "banner page-banner simples nao encontrado"))
        continue

    # 1) o conteudo ganha "relative z-10" (fica por cima das camadas)
    i0 = txt.index(ABRE_ANTIGO)
    k = txt.index('<div class="', i0)
    txt = txt[:k] + '<div class="relative z-10 ' + txt[k + len('<div class="'):]

    # 2) a abertura da section recebe as 2 camadas
    i0 = txt.index(ABRE_ANTIGO)
    txt = (txt[:i0]
           + CAMADAS.format(abre=ABRE_NOVO, cat=cat, tema=tema, lock=300 + i, pasta=pasta)
           + txt[i0 + len(ABRE_ANTIGO):])

    open(p, "w", encoding="utf-8", newline="").write(txt)
    feitos.append(nome)

print(f"✅ FASE 3 — hero com imagem em {len(feitos)} páginas: {', '.join(feitos)}")
if problemas:
    print(f"\n⚠️  {len(problemas)} não alteradas:")
    for n, motivo in problemas:
        print(f"   [{n}] {motivo}")
