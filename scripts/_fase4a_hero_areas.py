# -*- coding: utf-8 -*-
"""
FASE 4a — Hero com imagem nas 11 paginas de AREA.

Cada pagina ganha:
  - banner mais alto + imagem de fundo + scrim
  - <img> com data-secao-img="hero", data-categoria e data-pagina
    (o data-pagina e o nome da pasta no Drive: esporte/volei/hero/)

A imagem de reserva e ilustrativa; troca sozinha quando houver foto
em  PARA O SITE/<categoria>/<pagina>/hero/
"""
import os

BASE = r"G:/.shortcut-targets-by-id/18wGiptBKUmAmmkKHgdfu05TU4y_roWC1/BBDPRINT - BACKUP/BBDPRINT/App BBDPRiNT/PROJETOS/Projeto SER Sagi/projeto_SER_Sagi - Hermes"

# pagina -> (categoria no banco, pasta no Drive, tema da imagem de reserva)
CONFIG = {
    # ---- Áreas de ESPORTE ----
    "escola-jiu-jitsu.html":      ("Esporte", "escola-jiu-jitsu",      "jiu-jitsu,martial-arts,kids"),
    "volei.html":                 ("Esporte", "volei",                "volleyball,beach,sport"),
    "futevolei.html":             ("Esporte", "futevolei",            "beach,football,volleyball"),
    "estudio-musculacao.html":    ("Esporte", "estudio-musculacao",   "gym,weights,fitness"),
    "natacao.html":               ("Esporte", "natacao",              "swimming,pool,kids"),
    "danca.html":                 ("Esporte", "danca",                "dance,kids,class"),
    "arena-futevolei-volei.html": ("Esporte", "arena-futevolei-volei", "sports,court,beach"),
    # ---- Áreas de EDUCAÇÃO ----
    "ingles.html":                ("Educação", "ingles",              "english,class,students"),
    "espanhol.html":              ("Educação", "espanhol",            "spanish,class,students"),
    "informatica.html":           ("Educação", "informatica",         "computer,class,kids"),
    "sustentabilidade.html":      ("Educação", "sustentabilidade",    "environment,kids,plants"),
}

ABRE_ANTIGO = '<section class="page-banner text-white">'
ABRE_NOVO = '<section class="page-banner text-white relative overflow-hidden banner-alto">'

CAMADAS = '''{abre}
      <!-- CAMADA 1 · IMAGEM de fundo (ilustrativa — trocar por foto real em {cat_pasta}/{pasta}/hero/) -->
      <img src="https://loremflickr.com/1600/600/{tema}?lock={lock}" alt="" aria-hidden="true" data-secao-img="hero" data-categoria="{cat}" data-pagina="{pasta}" class="absolute inset-0 h-full w-full object-cover">
      <!-- CAMADA 2 · SCRIM (véu diagonal, mesmo efeito do hero da home) -->
      <div class="banner-scrim absolute inset-0"></div>'''

feitos, problemas = [], []

for i, (nome, (cat, pasta, tema)) in enumerate(CONFIG.items(), 1):
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

    # 1) conteudo por cima
    i0 = txt.index(ABRE_ANTIGO)
    k = txt.index('<div class="', i0)
    txt = txt[:k] + '<div class="relative z-10 ' + txt[k + len('<div class="'):]

    # 2) camadas de imagem + scrim
    i0 = txt.index(ABRE_ANTIGO)
    pasta_cat = {"Esporte": "esporte", "Educação": "educacao", "Cultura": "cultura",
                 "Preservação": "preservacao", "Saúde": "saude"}[cat]
    txt = (txt[:i0]
           + CAMADAS.format(abre=ABRE_NOVO, cat=cat, pasta=pasta, tema=tema,
                            lock=400 + i, cat_pasta=pasta_cat)
           + txt[i0 + len(ABRE_ANTIGO):])

    open(p, "w", encoding="utf-8", newline="").write(txt)
    feitos.append(nome)

print(f"✅ FASE 4a — hero com imagem em {len(feitos)} páginas de área:")
for n in feitos:
    print(f"   • {n:30} -> pasta {CONFIG[n][1]}/hero/")
if problemas:
    print(f"\n⚠️  {len(problemas)} não alteradas:")
    for n, motivo in problemas:
        print(f"   [{n}] {motivo}")
