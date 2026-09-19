# -*- coding: utf-8 -*-
"""
TEXTOS — aplica as fichas de texto no HTML do site.

Diferente das fotos (que vão para o banco), os textos dos blocos fixos
(números, títulos de seção) ficam no próprio HTML. Aqui a ficha é lida e
o HTML é reescrito no lugar — sem tocar em código.

A ligação com o bloco é a CHAVE (data-secao-chave do card), nunca a ordem.

USO:
    python scripts/textos.py --status     # mostra o que difere (não escreve)
    python scripts/textos.py --aplicar    # aplica as fichas no HTML
"""
import os
import re
import sys

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
PASTA_MIDIA = r"G:/Meu Drive/Instituto SER Sagi - PARA O SITE"


# --------------------------------------------------------------------------
# Leitura das fichas (mesmo formato do fichas.py)
# --------------------------------------------------------------------------
def ler_ficha(caminho):
    with open(caminho, encoding="utf-8-sig") as fh:
        linhas = fh.read().splitlines()
    blocos, atual = [], {}
    for linha in linhas:
        limpa = linha.strip()
        if not limpa or limpa.startswith("#"):
            if atual:
                blocos.append(atual)
                atual = {}
            continue
        if ":" not in limpa:
            continue
        chave, _, valor = limpa.partition(":")
        atual[chave.strip().lower()] = valor.strip()
    if atual:
        blocos.append(atual)
    return blocos


def caminho_ficha(bloco_midia):
    return os.path.join(PASTA_MIDIA, bloco_midia.replace("/", os.sep), "ficha.txt")


# --------------------------------------------------------------------------
# BLOCO: numeros de impacto  (home/numeros/ficha.txt  ->  index.html)
# --------------------------------------------------------------------------
def aplicar_numeros(html, blocos, modo):
    mudancas = []
    for b in blocos:
        chave = b.get("chave")
        if not chave:
            continue
        # acha o <a class="home-stat" ...> que contém esta chave
        padrao = re.compile(
            r'(<a class="home-stat"[^>]*href=")(?P<link>[^"]*)("[^>]*>\s*'
            r'<img[^>]*data-secao-chave="' + re.escape(chave) + r'"[^>]*>\s*'
            r'<span class="home-stat__label">)(?P<rotulo>.*?)(</span>\s*'
            r'<span class="home-stat__value">)(?P<valor>.*?)(</span>\s*'
            r'<p class="home-stat__desc">)(?P<desc>.*?)(</p>)', re.S)
        m = padrao.search(html)
        if not m:
            mudancas.append((chave, "⚠️  card não encontrado no HTML", None))
            continue

        if modo == "aplicar":
            # remonta o card com os valores da ficha
            sufixo = b.get("sufixo", "")
            valor_novo = b.get("valor", "").strip()
            if sufixo:
                valor_novo = f"{valor_novo}<span>{sufixo}</span>"
            novo = (m.group(1) + b.get("link", m.group("link")) + m.group(3)
                    + b.get("rotulo", m.group("rotulo")) + m.group(5)
                    + valor_novo + m.group(7)
                    + b.get("descricao", m.group("desc")) + m.group(9))
            html = html[:m.start()] + novo + html[m.end():]

        for campo, atual in (("rotulo", m.group("rotulo")), ("valor", m.group("valor"))):
            novo_valor = b.get(campo, "").strip()
            if campo == "valor" and b.get("sufixo"):
                novo_valor = f"{novo_valor}<span>{b['sufixo']}</span>"
            if campo == "rotulo" and novo_valor == atual.strip():
                continue
            if campo == "valor" and novo_valor == atual.strip():
                continue
            mudancas.append((chave, campo, f"{atual.strip()[:22]!r} -> {novo_valor[:22]!r}"))
        if b.get("descricao", m.group("desc")).strip() != m.group("desc").strip():
            mudancas.append((chave, "descricao",
                             f"{m.group('desc').strip()[:26]!r} -> {b['descricao'][:26]!r}"))
        if b.get("link", m.group("link")) != m.group("link"):
            mudancas.append((chave, "link", f"{m.group('link')} -> {b['link']}"))
    return html, mudancas


# --------------------------------------------------------------------------
BLOQOS = {
    "home/numeros": ("index.html", aplicar_numeros),
}


def main():
    aplicar = "--aplicar" in sys.argv
    total = 0
    for bloco, (arquivo, funcao) in BLOQOS.items():
        caminho = caminho_ficha(bloco)
        if not os.path.isfile(caminho):
            print(f"⚠️  ficha não encontrada: {bloco}/ficha.txt")
            continue
        blocos = ler_ficha(caminho)
        caminho_html = os.path.join(BASE, arquivo)
        html = open(caminho_html, encoding="utf-8").read()
        html_novo, mudancas = funcao(html, blocos, "aplicar" if aplicar else "status")

        print(f"\n📋 {bloco}/ficha.txt  →  {arquivo}   ({len(blocos)} bloco(s))")
        if not mudancas:
            print("   ✅ igual à ficha — nada a mudar")
        for chave, campo, detalhe in mudancas:
            print(f"   • [{chave}] {campo}: {detalhe}")
        total += len(mudancas)

        if aplicar and html_novo != html:
            with open(caminho_html, "w", encoding="utf-8", newline="") as fh:
                fh.write(html_novo)
            print(f"   💾 {arquivo} reescrito")

    print()
    if aplicar:
        print(f"✅ {total} mudança(s) aplicada(s). Agora rode o bump + commit + push.")
    else:
        print(f"ℹ️  {total} diferença(s) entre a ficha e o HTML (use --aplicar para gravar)")


if __name__ == "__main__":
    main()
