# -*- coding: utf-8 -*-
"""
Ajuste: categoria com UMA SO area nao tem hub.

Regra: 1 area  -> a pagina da categoria E a pagina do conteudo (sem passar por hub)
       2+ areas -> a pagina da categoria e um hub com os cards

Na pratica: desfaz a divisao da Saude.
  - saude.html  volta a ser a pagina completa do consultorio odontologico
  - consultorio-odontologico.html e removido
"""
import os

BASE = r"G:/.shortcut-targets-by-id/18wGiptBKUmAmmkKHgdfu05TU4y_roWC1/BBDPRINT - BACKUP/BBDPRINT/App BBDPRiNT/PROJETOS/Projeto SER Sagi/projeto_SER_Sagi - Hermes"

# ============================================================
# 1) saude.html volta a receber o conteudo do consultorio
# ============================================================
doc = open(os.path.join(BASE, "consultorio-odontologico.html"), encoding="utf-8", newline="").read()

# breadcrumb: 4 -> 3 niveis (nao existe mais sub-pagina)
DE = '''      <ol>
        <li><a href="./">Início</a></li>
        <li><a href="acoes.html">Nossas Ações</a></li>
        <li><a href="saude.html">Saúde</a></li>
        <li><span aria-current="page">Consultório Odontológico</span></li>
      </ol>'''
PARA = '''      <ol>
        <li><a href="./">Início</a></li>
        <li><a href="acoes.html">Nossas Ações</a></li>
        <li><span aria-current="page">Saúde</span></li>
      </ol>'''
assert DE in doc, "consultorio: breadcrumb de 4 niveis nao encontrado"
doc = doc.replace(DE, PARA, 1)

# JSON-LD: 4 -> 3 niveis
DE = '''      { "@type": "ListItem", "position": 3, "name": "Saúde", "item": "https://bimbord.github.io/projeto_ser_sagi/saude.html" },
      { "@type": "ListItem", "position": 4, "name": "Consultório Odontológico", "item": "https://bimbord.github.io/projeto_ser_sagi/consultorio-odontologico.html" }'''
PARA = '''      { "@type": "ListItem", "position": 3, "name": "Saúde", "item": "https://bimbord.github.io/projeto_ser_sagi/saude.html" }'''
assert DE in doc, "consultorio: JSON-LD nao encontrado"
doc = doc.replace(DE, PARA, 1)

# "voltar" volta a apontar para Nossas Acoes
doc = doc.replace('<p class="font-bold text-oceanDeep">Voltar para Saúde</p>',
                  '<p class="font-bold text-oceanDeep">Voltar para Nossas Ações</p>', 1)
doc = doc.replace("Veja as demais áreas de saúde do Instituto.",
                  "Veja o conjunto completo de frentes de atuação do Instituto na comunidade do Sagi.", 1)
doc = doc.replace('href="saude.html" class="cta-lift mt-4 inline-flex items-center gap-2 rounded-full bg-ocean px-5 py-2.5 text-sm font-semibold text-white transition hover:brightness-95"><i class="fa-solid fa-arrow-left text-xs"></i>Voltar para Saúde',
                  'href="acoes.html" class="cta-lift mt-4 inline-flex items-center gap-2 rounded-full bg-ocean px-5 py-2.5 text-sm font-semibold text-white transition hover:brightness-95"><i class="fa-solid fa-arrow-left text-xs"></i>Ver todas as categorias', 1)

open(os.path.join(BASE, "saude.html"), "w", encoding="utf-8", newline="").write(doc)
print("  ✅ saude.html: voltou a ser a pagina completa do consultório")

# ============================================================
# 2) remove a sub-pagina
# ============================================================
p_sub = os.path.join(BASE, "consultorio-odontologico.html")
if os.path.isfile(p_sub):
    os.remove(p_sub)
    print("  ✅ consultorio-odontologico.html removido")

# ============================================================
# 3) acoes.html: card da Saude sem a lista de areas (ela E a area)
# ============================================================
p = os.path.join(BASE, "acoes.html")
txt = open(p, encoding="utf-8", newline="").read()

DE = '''
            <p class="mt-5 text-xs font-semibold uppercase tracking-[0.15em] text-slate-500">Áreas nesta categoria</p>
            <ul class="mt-3 space-y-2 text-sm leading-6">
              <li><a href="consultorio-odontologico.html" class="text-ocean underline-offset-2 transition hover:text-oceanDeep hover:underline">Consultório Odontológico</a></li>
            </ul>'''
if DE in txt:
    txt = txt.replace(DE, "", 1)
    print("  ✅ acoes.html: card da Saúde simplificado (sem lista de áreas)")

# Preservacao tambem e area unica -> ja nao tem lista, ok
open(p, "w", encoding="utf-8", newline="").write(txt)

# ============================================================
# 4) links de volta para saude.html
# ============================================================
for nome in ("instalacoes.html", "quem-somos.html"):
    p = os.path.join(BASE, nome)
    txt = open(p, encoding="utf-8", newline="").read()
    if 'href="consultorio-odontologico.html"' in txt:
        txt = txt.replace('href="consultorio-odontologico.html"', 'href="saude.html"')
        open(p, "w", encoding="utf-8", newline="").write(txt)
        print(f"  ✅ {nome}: link do consultório volta pra saude.html")

# ============================================================
# 5) main.js: tira o consultorio do destaque do menu
# ============================================================
p = os.path.join(BASE, "js", "main.js")
txt = open(p, encoding="utf-8", newline="").read()
DE = "const acoesSub = ['saude.html', 'consultorio-odontologico.html',"
PARA = "const acoesSub = ['saude.html',"
assert DE in txt, "main.js: acoesSub nao encontrado"
txt = txt.replace(DE, PARA, 1)
open(p, "w", encoding="utf-8", newline="").write(txt)
print("  ✅ js/main.js: acoesSub ajustado")
