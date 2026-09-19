# -*- coding: utf-8 -*-
"""
Extrai os TEXTOS dos cards de numeros da home e escreve a ficha.

A ficha fica em:  <pasta de midia>/home/numeros/ficha.txt
Cada bloco descreve um card. A ligacao com o card e a CHAVE
(o mesmo data-secao-chave que a foto ja usa) — nada de adivinhacao.
"""
import os
import re

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
PASTA_MIDIA = r"G:/Meu Drive/Instituto SER Sagi - PARA O SITE"
html = open(os.path.join(BASE, "index.html"), encoding="utf-8").read()

# pega cada <a class="home-stat" ...> ... </a>
padrao = re.compile(
    r'<a class="home-stat"[^>]*href="(?P<link>[^"]*)"[^>]*>(?P<corpo>.*?)</a>', re.S)
chave_re = re.compile(r'data-secao-chave="([^"]+)"')
valor_re = re.compile(r'class="home-stat__value"[^>]*>(.*?)(?=<p class="home-stat__desc"|</a>)', re.S)
rotulo_re = re.compile(r'class="home-stat__label"[^>]*>(.*?)</span>', re.S)
desc_re = re.compile(r'class="home-stat__desc"[^>]*>(.*?)</p>', re.S)
limpa = lambda s: re.sub(r"\s+", " ", re.sub(r"<(?!/?span)[^>]+>", "", s)).strip()

cards = []
for m in padrao.finditer(html):
    corpo = m.group("corpo")
    ch = chave_re.search(corpo)
    va = valor_re.search(corpo)
    ro = rotulo_re.search(corpo)
    de = desc_re.search(corpo)
    if not (ch and va and ro):
        continue
    # o valor pode ter um <span>+</span> dentro (ex.: 1.149<span>+</span>)
    valor_bruto = va.group(1)
    extra = re.findall(r"<span>([^<]+)</span>", valor_bruto)
    valor_limpo = re.sub(r"<[^>]+>", "", re.sub(r"<span>[^<]*</span>", "", valor_bruto)).strip()
    cards.append({
        "chave": ch.group(1),
        "valor": valor_limpo,
        "sufixo": extra[0] if extra else "",
        "rotulo": limpa(ro.group(1)),
        "descricao": limpa(de.group(1)) if de else "",
        "link": m.group("link"),
    })

print(f"encontrei {len(cards)} card(s) de numero:\n")
for c in cards:
    print(f"  [{c['chave']:20}] {c['valor']+c['sufixo']:>8}  {c['rotulo']:22} | {c['descricao'][:42]}")

# --- escreve a ficha ---
pasta = os.path.join(PASTA_MIDIA, "home", "numeros")
os.makedirs(pasta, exist_ok=True)
linhas = [
    "# ============================================================",
    "#  FICHA DOS NUMEROS DE IMPACTO  (home)",
    "#  Instituto S.E.R. Sagi",
    "# ============================================================",
    "#",
    "#  Cada bloco = um card da faixa de numeros da home.",
    "#  Separe os blocos com UMA LINHA EM BRANCO.",
    "#",
    "#  chave ..... identifica o card (NAO MUDE - e a ligacao com a foto)",
    "#  rotulo .... texto pequeno em cima do numero (ex.: Saude)",
    "#  valor ..... o numero grande (ex.: 1.149)",
    "#  sufixo .... o que vem depois do numero (ex.: +) - pode ficar vazio",
    "#  descricao . a frase embaixo do numero",
    "#  link ...... para onde o card leva quando clicado",
    "#",
    "#  linhas com # sao comentario e sao ignoradas.",
    "# ============================================================",
    "",
]
for c in cards:
    linhas += [
        f"chave: {c['chave']}",
        f"rotulo: {c['rotulo']}",
        f"valor: {c['valor']}",
        f"sufixo: {c['sufixo']}",
        f"descricao: {c['descricao']}",
        f"link: {c['link']}",
        "",
        "",
    ]
with open(os.path.join(pasta, "ficha.txt"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(linhas))
print(f"\n✅ ficha criada: home/numeros/ficha.txt  ({len(cards)} cards)")
