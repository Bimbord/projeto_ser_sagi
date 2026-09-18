# -*- coding: utf-8 -*-
"""
Reordena os dropdowns: "Ver todas as ações" e "Acervo completo" vão para o FIM
das respectivas listas, com um traço de separação (fica claro que fecham a lista).
"""
import glob
import os
import re

BASE = r"G:/.shortcut-targets-by-id/18wGiptBKUmAmmkKHgdfu05TU4y_roWC1/BBDPRINT - BACKUP/BBDPRINT/App BBDPRiNT/PROJETOS/Projeto SER Sagi/projeto_SER_Sagi - Hermes"
L = lambda p: os.path.join(BASE, p)  # noqa: E731

CHEV = '<i class="fa-solid fa-chevron-down" aria-hidden="true"></i>'


def link_drop(texto, href, todos=False):
    cls = ' class="nav-drop__todos"' if todos else ''
    return f'<a href="{href}" data-page-link{cls}>{texto}</a>'


def link_acc(texto, href, todos=False):
    cls = ' class="block py-2 text-sm nav-drop__todos"' if todos else ' class="block py-2 text-sm"'
    return f'<a href="{href}" data-page-link{cls}>{texto}</a>'


def drop(titulo, itens):
    """itens: lista de (texto, href, ehTodos)"""
    links = "\n            ".join(link_drop(t, h, x) for t, h, x in itens)
    return (f'''<div class="nav-drop">
          <button type="button" class="nav-link nav-drop__botao" aria-expanded="false" aria-haspopup="true">{titulo} {CHEV}</button>
          <div class="nav-drop__menu">
            {links}
          </div>
        </div>''')


def acordeao(titulo, itens):
    links = "\n            ".join(link_acc(t, h, x) for t, h, x in itens)
    return (f'''<div class="nav-acc">
          <button type="button" class="nav-acc__botao" aria-expanded="false">{titulo} {CHEV}</button>
          <div class="nav-acc__menu">
            {links}
          </div>
        </div>''')


QUEM_SOMOS = [("Quem Somos", "quem-somos.html", False), ("Depoimentos", "depoimentos.html", False)]
ACOES = [("Saúde", "saude.html", False), ("Esporte", "esporte.html", False),
         ("Educação", "educacao.html", False), ("Cultura", "cultura.html", False),
         ("Preservação Ambiental", "preservacao-ambiental.html", False),
         ("Ações Solidárias", "acoes-solidarias.html", False),
         ("Ver todas as ações", "acoes.html", True)]
ACERVO = [("Esporte", "acervo-esporte.html", False), ("Saúde", "acervo-saude.html", False),
          ("Educação", "acervo-educacao.html", False), ("Cultura", "acervo-cultura.html", False),
          ("Preservação", "acervo-preservacao.html", False), ("Eventos", "acervo-eventos.html", False),
          ("Acervo completo", "acervo.html", True)]
INST = [("Lei de Incentivo", "lei-incentivo.html", False), ("Transparência", "transparencia.html", False),
        ("Instalações", "instalacoes.html", False), ("Contato", "contato.html", False)]

DESKTOP = f'''<nav class="hidden items-center gap-1 lg:flex xl:gap-2" aria-label="Menu principal">
        <a href="./" data-page-link class="nav-link">Início</a>
        {drop("Quem Somos", QUEM_SOMOS)}
        <a href="joia-da-coroa.html" data-page-link class="nav-link nav-link--destaque">Jóia da Coroa</a>
        {drop("Nossas Ações", ACOES)}
        {drop("Acervo", ACERVO)}
        <a href="como-ajudar.html" data-page-link class="nav-link">Como Ajudar</a>
        {drop("Institucional", INST)}
      </nav>'''

MOBILE = f'''<nav class="mx-auto flex max-w-7xl flex-col px-4 py-4" aria-label="Menu mobile">
        <a href="./" data-page-link class="py-2 text-sm font-medium">Início</a>
        {acordeao("Quem Somos", QUEM_SOMOS)}
        <a href="joia-da-coroa.html" data-page-link class="py-2 text-sm font-semibold text-ocean">Jóia da Coroa</a>
        {acordeao("Nossas Ações", ACOES)}
        {acordeao("Acervo", ACERVO)}
        <a href="como-ajudar.html" data-page-link class="py-2 text-sm font-medium">Como Ajudar</a>
        {acordeao("Institucional", INST)}
      </nav>'''

# ---------- HTML ----------
ok, sem = [], []
for p in sorted(glob.glob(L("*.html"))):
    nome = os.path.basename(p)
    txt = open(p, encoding="utf-8", newline="").read()
    orig = txt
    txt = re.sub(r'<nav class="hidden items-center[^>]*aria-label="Menu principal"[^>]*>.*?</nav>', DESKTOP, txt, count=1, flags=re.DOTALL)
    txt = re.sub(r'<nav class="mx-auto flex max-w-7xl flex-col px-4 py-4"[^>]*>.*?</nav>', MOBILE, txt, count=1, flags=re.DOTALL)
    if txt != orig:
        open(p, "w", encoding="utf-8", newline="").write(txt)
        ok.append(nome)
    else:
        sem.append(nome)
print(f"  ✅ menu reordenado em {len(ok)} páginas")
if sem:
    print(f"  ⚠️  sem alteração: {', '.join(sem)}")

# ---------- CSS ----------
p_css = L("css/style.css")
css = open(p_css, encoding="utf-8", newline="").read()
if ".nav-drop__todos" in css:
    print("  ⚠️  CSS já tinha o separador")
else:
    css += """

/* Item que fecha a lista do dropdown ("Ver todas as ações" / "Acervo completo") */
.nav-drop__menu a.nav-drop__todos {
  margin-top: 0.3rem;
  padding-top: 0.6rem;
  border-top: 1px solid rgba(15, 92, 115, 0.12);
  font-weight: 700;
  color: var(--ocean-deep);
}
.nav-acc__menu a.nav-drop__todos {
  margin-top: 0.3rem;
  padding-top: 0.6rem;
  border-top: 1px solid rgba(15, 92, 115, 0.12);
  font-weight: 700;
  color: var(--ocean-deep);
}
"""
    open(p_css, "w", encoding="utf-8", newline="").write(css)
    print("  ✅ css/style.css — traço de separação no item final")

# ---------- conferência ----------
nav = re.search(r'<nav class="hidden items-center[^>]*aria-label="Menu principal"[^>]*>(.*?)</nav>',
                open(L("index.html"), encoding="utf-8").read(), re.DOTALL).group(1)
for bloco in re.split(r'(?=<div class="nav-drop")', nav):
    tit = re.search(r'nav-drop__botao[^>]*>([^<]+)', bloco)
    if not tit:
        continue
    itens = re.findall(r'<a href="[^"]+"[^>]*>([^<]+)</a>', bloco)
    print(f"\n  ▾ {tit.group(1).strip()}")
    for i, t in enumerate(itens):
        marca = "  ← ÚLTIMO ✔" if i == len(itens) - 1 else ""
        print(f"      {i+1}. {t}{marca}")
