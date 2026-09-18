# -*- coding: utf-8 -*-
"""
Integra a página joia-da-coroa.html ao site:

  1. rodapé: link "Jóia da Coroa" na coluna Navegação (depois de Nossas Ações)
  2. home: o card "Projeto principal" (números) e o card "A Jóia da Coroa" -> nova página
  3. publicar.py: categoria "Jóia da Coroa"
  4. Drive: pastas joia-da-coroa/{hero,imagem principal,carrossel,galeria}
"""
import glob
import os
import re

BASE = r"G:/.shortcut-targets-by-id/18wGiptBKUmAmmkKHgdfu05TU4y_roWC1/BBDPRINT - BACKUP/BBDPRINT/App BBDPRiNT/PROJETOS/Projeto SER Sagi/projeto_SER_Sagi - Hermes"
S = r"G:/Meu Drive/Instituto SER Sagi - PARA O SITE"
L = lambda p: os.path.join(BASE, p)  # noqa: E731

# ---------- 1. rodapé em todas as páginas ----------
VELHO = '<li><a href="acoes.html" class="text-white/70 transition hover:text-white">Nossas Ações</a></li>'
NOVO = (VELHO + '\n            '
        '<li><a href="joia-da-coroa.html" class="text-sun transition hover:text-white">Jóia da Coroa</a></li>')

paginas = sorted(glob.glob(L("*.html")))
mudadas, sem_padrao = [], []
for p in paginas:
    nome = os.path.basename(p)
    txt = open(p, encoding="utf-8", newline="").read()
    if 'href="joia-da-coroa.html"' in txt and VELHO not in txt:
        continue
    if VELHO in txt:
        txt = txt.replace(VELHO, NOVO)
        open(p, "w", encoding="utf-8", newline="").write(txt)
        mudadas.append(nome)
    else:
        # a própria joia-da-coroa.html já tem o item? então tudo bem
        if 'joia-da-coroa.html' not in txt:
            sem_padrao.append(nome)

print(f"  ✅ rodapé atualizado em {len(mudadas)} páginas (de {len(paginas)})")
if sem_padrao:
    print(f"  ⚠️  sem o padrão do rodapé: {', '.join(sem_padrao)}")

# ---------- 2. home: links ----------
p_idx = L("index.html")
idx = open(p_idx, encoding="utf-8", newline="").read()
antes = idx

# 2a. card de número "Projeto principal" (estava apontando para acoes.html)
idx = idx.replace('<a class="home-stat" href="acoes.html">',
                  '<a class="home-stat" href="joia-da-coroa.html">', 1)

# 2b. card "A Jóia da Coroa" (título do card principal da home)
trocas_card = [
    ('<h2 class="section-title text-3xl font-extrabold text-oceanDeep">A Jóia da Coroa</h2>',
     '<h2 class="section-title text-3xl font-extrabold text-oceanDeep"><a href="joia-da-coroa.html" class="hover:text-ocean">A Jóia da Coroa</a></h2>'),
]
for velho, novo in trocas_card:
    if velho in idx:
        idx = idx.replace(velho, novo, 1)

if idx != antes:
    open(p_idx, "w", encoding="utf-8", newline="").write(idx)
    print("  ✅ index.html — card 'Projeto principal' -> joia-da-coroa.html")
    print(f"     título do card da Jóia com link: {'joia-da-coroa.html' in idx}")
else:
    print("  ⚠️  index.html não mudou (confira os âncoras)")

# ---------- 3. publicar.py ----------
p_pub = L("scripts/publicar.py")
pub = open(p_pub, encoding="utf-8", newline="").read()
if '"joia-da-coroa"' in pub:
    print("  ⚠️  publicar.py já tinha a categoria")
elif '    "depoimentos": "Depoimentos",' in pub:
    pub = pub.replace('    "depoimentos": "Depoimentos",',
                      '    "depoimentos": "Depoimentos",\n    "joia-da-coroa": "Jóia da Coroa",', 1)
    open(p_pub, "w", encoding="utf-8", newline="").write(pub)
    print("  ✅ publicar.py — categoria 'joia-da-coroa'")
else:
    print("  ⚠️  não achei o ponto no publicar.py")

# ---------- 4. pastas no Drive ----------
criadas = 0
for sub in ("hero", "imagem principal", "carrossel", "galeria"):
    d = os.path.join(S, "joia-da-coroa", sub)
    if not os.path.isdir(d):
        os.makedirs(d, exist_ok=True)
        criadas += 1
print(f"  ✅ Drive: joia-da-coroa/ com hero, imagem principal, carrossel e galeria ({criadas} criadas)")
