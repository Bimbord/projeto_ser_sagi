# -*- coding: utf-8 -*-
"""
Troca os links do menu/logo de 'index.html' por './' (raiz da pasta).
Assim a barra de endereços não mostra 'index.html' — o servidor entrega
o index.html automaticamente.
"""
import os, sys

BASE = r"C:/Projetos Code/Projeto SER Sagi/projeto_SER_Sagi - Hermes"

total_arq, total_sub = 0, 0
for nome in sorted(os.listdir(BASE)):
    if not nome.endswith(".html"):
        continue
    p = os.path.join(BASE, nome)
    txt = open(p, encoding="utf-8").read()
    if 'href="index.html"' not in txt:
        continue
    n = txt.count('href="index.html"')
    novo = txt.replace('href="index.html"', 'href="./"')
    # validação: tem que ter trocado exatamente o mesmo número
    if novo.count('href="./"') < n:
        print(f"  ❌ ABORTADO em {nome}: contagem inesperada")
        sys.exit(1)
    open(p, "w", encoding="utf-8", newline="\n").write(novo)
    total_arq += 1
    total_sub += n

print(f"✅ {total_sub} links ajustados em {total_arq} páginas")
print("   de: href=\"index.html\"   ->   para: href=\"./\"")
