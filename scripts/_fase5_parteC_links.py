# -*- coding: utf-8 -*-
"""
FASE 5 · Parte C (3/3) — link "Depoimentos" no menu e no rodapé de todas as páginas.

  menu desktop : depois de "Acervo"
  menu mobile  : depois de "Acervo"
  rodapé       : coluna Institucional, depois de "Transparência"
"""
import os
import re
import glob

BASE = r"G:/.shortcut-targets-by-id/18wGiptBKUmAmmkKHgdfu05TU4y_roWC1/BBDPRINT - BACKUP/BBDPRINT/App BBDPRiNT/PROJETOS/Projeto SER Sagi/projeto_SER_Sagi - Hermes"

TROCAS = [
    # menu desktop
    ('<a href="acervo.html" data-page-link class="text-sm font-medium hover:text-ocean">Acervo</a>',
     '<a href="acervo.html" data-page-link class="text-sm font-medium hover:text-ocean">Acervo</a>'
     '<a href="depoimentos.html" data-page-link class="text-sm font-medium hover:text-ocean">Depoimentos</a>',
     "menu"),
    # menu mobile
    ('<a href="acervo.html" data-page-link class="py-2 text-sm font-medium">Acervo</a>',
     '<a href="acervo.html" data-page-link class="py-2 text-sm font-medium">Acervo</a>'
     '<a href="depoimentos.html" data-page-link class="py-2 text-sm font-medium">Depoimentos</a>',
     "menu mobile"),
    # rodapé
    ('<li><a href="transparencia.html" class="text-white/70 transition hover:text-white">Transparência</a></li>',
     '<li><a href="transparencia.html" class="text-white/70 transition hover:text-white">Transparência</a></li>\n            '
     '<li><a href="depoimentos.html" class="text-white/70 transition hover:text-white">Depoimentos</a></li>',
     "rodapé"),
]

arquivos = sorted(glob.glob(os.path.join(BASE, "*.html")))
totais = {nome: 0 for _, _, nome in TROCAS}
paginas_menu, paginas_rodape, ja_tinham = [], [], []

for p in arquivos:
    nome = os.path.basename(p)
    txt = open(p, encoding="utf-8", newline="").read()
    original = txt

    for velho, novo, rotulo in TROCAS:
        if velho in txt:
            txt = txt.replace(velho, novo)
            totais[rotulo] += 1

    if txt != original:
        open(p, "w", encoding="utf-8", newline="").write(txt)
        paginas_menu.append(nome)
    else:
        ja_tinham.append(nome)

print(f"  ✅ {len(arquivos)} páginas verificadas")
print(f"     menu desktop atualizado .... {totais['menu']}")
print(f"     menu mobile atualizado ..... {totais['menu mobile']}")
print(f"     rodapé atualizado .......... {totais['rodapé']}")
if ja_tinham:
    print(f"     já estavam ok (sem padrão) . {', '.join(ja_tinham)}")

# conferência final: quantas paginas tem o link
com_link = [os.path.basename(p) for p in arquivos
            if 'href="depoimentos.html"' in open(p, encoding="utf-8").read()]
print(f"\n  📊 páginas com link para depoimentos.html: {len(com_link)} de {len(arquivos)}")
faltando = [os.path.basename(p) for p in arquivos if os.path.basename(p) not in com_link]
if faltando:
    print(f"  ⚠️  sem link: {', '.join(faltando)}")
