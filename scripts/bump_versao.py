# -*- coding: utf-8 -*-
"""
bump_versao.py — Cache-busting do site

Adiciona/incrementa o parametro de versao nos links de CSS e JS de TODAS as
paginas HTML. Assim o navegador e OBRIGADO a baixar a versao nova, em vez de
servir a antiga do cache (aquele problema de "nao aparece a alteracao").

USO
---
    python scripts/bump_versao.py        # incrementa a versao (+1) em todas as paginas
    python scripts/bump_versao.py 7      # define a versao como 7
    python scripts/bump_versao.py --mostrar   # so mostra a versao atual, nao altera

Sempre rode este script depois de mexer em css/style.css ou js/*.js
e faca o commit junto.
"""
import os
import re
import sys

BASE = r"G:/.shortcut-targets-by-id/18wGiptBKUmAmmkKHgdfu05TU4y_roWC1/BBDPRINT - BACKUP/BBDPRINT/App BBDPRiNT/PROJETOS/Projeto SER Sagi/projeto_SER_Sagi - Hermes"

ARQUIVOS = ("css/style.css", "js/main.js", "js/hero.js")


def versao_atual(txt, caminho):
    """Le a versao atual de um link (?v=N). Retorna int ou None."""
    m = re.search(re.escape(caminho) + r'\?v=(\d+)', txt)
    return int(m.group(1)) if m else None


def aplicar(txt, versao):
    """(Re)escreve o ?v=N nos links de CSS/JS."""
    for caminho in ARQUIVOS:
        padrao = r'(href|src)="' + re.escape(caminho) + r'(\?v=\d+)?"'
        txt = re.sub(padrao, lambda m, c=caminho: f'{m.group(1)}="{c}?v={versao}"', txt)
    return txt


def main():
    args = [a for a in sys.argv[1:]]
    somente_mostrar = "--mostrar" in args
    args = [a for a in args if a != "--mostrar"]
    versao_forcada = int(args[0]) if args else None

    paginas = sorted(f for f in os.listdir(BASE) if f.endswith(".html"))
    if not paginas:
        print("❌ Nenhuma pagina HTML encontrada.")
        sys.exit(1)

    # descobre a versao atual
    atual = 0
    for nome in paginas:
        txt = open(os.path.join(BASE, nome), encoding="utf-8", newline="").read()
        for caminho in ARQUIVOS:
            v = versao_atual(txt, caminho)
            if v and v > atual:
                atual = v

    if somente_mostrar:
        print(f"📌 Versao atual dos assets: {atual or '(nenhuma)'}")
        return

    nova = versao_forcada if versao_forcada else (atual + 1)
    alteradas = 0
    for nome in paginas:
        p = os.path.join(BASE, nome)
        txt = open(p, encoding="utf-8", newline="").read()
        novo = aplicar(txt, nova)
        if novo != txt:
            open(p, "w", encoding="utf-8", newline="").write(novo)
            alteradas += 1

    print(f"✅ Versao dos assets: {atual or 0} → {nova}")
    print(f"   {alteradas} pagina(s) atualizada(s)")


if __name__ == "__main__":
    main()
