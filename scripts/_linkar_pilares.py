# -*- coding: utf-8 -*-
"""
Linka os 5 cards de pilares da home (Saúde, Esporte, Educação, Cultura, Preservação)
para as páginas de ações correspondentes.

Mapeamento:
  Saúde        -> consultorio-odontologico.html   (1:1)
  Esporte      -> acoes.html                      (3 ações: musculação, jiu-jitsu, arena)
  Educação     -> acoes.html                      (ainda não existe página específica)
  Cultura      -> acoes-solidarias.html           (1:1)
  Preservação  -> preservacao-ambiental.html      (1:1)
"""
import re, os

BASE = r"C:/Projetos Code/Projeto SER Sagi/projeto_SER_Sagi - Hermes"
ARQ = os.path.join(BASE, "index.html")

MAPA = {
    "Saúde": "consultorio-odontologico.html",
    "Esporte": "acoes.html",
    "Educação": "acoes.html",
    "Cultura": "acoes-solidarias.html",
    "Preservação": "preservacao-ambiental.html",
}

html = open(ARQ, encoding="utf-8").read()

PADRAO = re.compile(r'<article class="home-card home-pillar">(.*?)</article>', re.S)

feitos = []


def trocar(m):
    conteudo = m.group(1)
    t = re.search(r'home-card__title">([^<]*)<', conteudo)
    if not t:
        return m.group(0)
    nome = t.group(1).strip()
    href = MAPA.get(nome)
    if not href:
        return m.group(0)
    conteudo_limpo = conteudo.rstrip()
    cta = f'<span class="home-card__cta">Saiba mais <span aria-hidden="true">&rarr;</span></span>'
    feitos.append((nome, href))
    return f'<a href="{href}" class="home-card home-pillar">{conteudo_limpo}{cta}</a>'


novo, n = PADRAO.subn(trocar, html)

open(ARQ, "w", encoding="utf-8", newline="\n").write(novo)

print(f"Cards linkados: {n}\n")
for nome, href in feitos:
    print(f"  {nome:<14} -> {href}")
