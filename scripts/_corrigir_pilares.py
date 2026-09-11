# -*- coding: utf-8 -*-
"""Corrige o destino dos cards de pilar da home conforme a hierarquia definida."""
import re, os, sys

BASE = r"C:/Projetos Code/Projeto SER Sagi/projeto_SER_Sagi - Hermes"
ARQ = os.path.join(BASE, "index.html")

# titulo do card -> pagina de destino
MAPA = {
    "Saúde": "consultorio-odontologico.html",
    "Esporte": "esporte.html",
    "Educação": "educacao.html",
    "Cultura": "cultura.html",
    "Preservação": "preservacao-ambiental.html",
}

html = open(ARQ, encoding="utf-8").read()
antes = html

alterados = []


def corrigir(m):
    conteudo = m.group(1)
    t = re.search(r'home-card__title">([^<]*)<', conteudo)
    if not t:
        return m.group(0)
    nome = t.group(1).strip()
    href = MAPA.get(nome)
    if not href:
        return m.group(0)
    atual = re.search(r'^<a href="([^"]+)"', m.group(0))
    if atual and atual.group(1) != href:
        alterados.append((nome, atual.group(1), href))
    return f'<a href="{href}" class="home-card home-pillar">{conteudo}</a>'


novo = re.sub(r'<a href="[^"]*" class="home-card home-pillar">(.*?)</a>', corrigir, html, flags=re.S)

# valida antes de salvar
if novo.count('<a href="') != antes.count('<a href="'):
    print("❌ ABORTADO: o número de links mudou — nada foi salvo")
    sys.exit(1)

open(ARQ, "w", encoding="utf-8", newline="\n").write(novo)
print("Links dos pilares atualizados:\n")
for nome, de, para in alterados:
    print(f"  {nome:<14} {de}  ->  {para}")
if not alterados:
    print("  (já estavam corretos)")
