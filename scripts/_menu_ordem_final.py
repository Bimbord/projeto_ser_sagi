# -*- coding: utf-8 -*-
"""
Ordem do menu definida pelo dono:

  Início · Quem Somos · Nossas Ações · Acervo · Jóia da Coroa ·
  Como Ajudar · Institucional · Seja Parceiro · Doe Agora

- Jóia da Coroa passa para depois do Acervo (5ª posição)
- "Seja Parceiro" e "Doe Agora" entram no menu do CELULAR (antes só existiam
  no desktop em telas largas) — fechando a mesma ordem
"""
import glob
import os
import re

BASE = r"G:/.shortcut-targets-by-id/18wGiptBKUmAmmkKHgdfu05TU4y_roWC1/BBDPRINT - BACKUP/BBDPRINT/App BBDPRiNT/PROJETOS/Projeto SER Sagi/projeto_SER_Sagi - Hermes"
L = lambda p: os.path.join(BASE, p)  # noqa: E731

CHEV = '<i class="fa-solid fa-chevron-down" aria-hidden="true"></i>'


def drop(titulo, itens):
    links = "\n            ".join(
        f'<a href="{h}" data-page-link' + (' class="nav-drop__todos"' if x else '') + f'>{t}</a>'
        for t, h, x in itens)
    return (f'''<div class="nav-drop">
          <button type="button" class="nav-link nav-drop__botao" aria-expanded="false" aria-haspopup="true">{titulo} {CHEV}</button>
          <div class="nav-drop__menu">
            {links}
          </div>
        </div>''')


def acordeao(titulo, itens):
    links = "\n            ".join(
        f'<a href="{h}" data-page-link class="block py-2 text-sm' + (' nav-drop__todos' if x else '') + f'">{t}</a>'
        for t, h, x in itens)
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

# ---------------- ORDEM NOVA ----------------
DESKTOP = f'''<nav class="hidden items-center gap-1 lg:flex xl:gap-2" aria-label="Menu principal">
        <a href="./" data-page-link class="nav-link">Início</a>
        {drop("Quem Somos", QUEM_SOMOS)}
        {drop("Nossas Ações", ACOES)}
        {drop("Acervo", ACERVO)}
        <a href="joia-da-coroa.html" data-page-link class="nav-link nav-link--destaque">Jóia da Coroa</a>
        <a href="como-ajudar.html" data-page-link class="nav-link">Como Ajudar</a>
        {drop("Institucional", INST)}
      </nav>'''

MOBILE = f'''<nav class="mx-auto flex max-w-7xl flex-col px-4 py-4" aria-label="Menu mobile">
        <a href="./" data-page-link class="py-2 text-sm font-medium">Início</a>
        {acordeao("Quem Somos", QUEM_SOMOS)}
        {acordeao("Nossas Ações", ACOES)}
        {acordeao("Acervo", ACERVO)}
        <a href="joia-da-coroa.html" data-page-link class="py-2 text-sm font-semibold text-ocean">Jóia da Coroa</a>
        <a href="como-ajudar.html" data-page-link class="py-2 text-sm font-medium">Como Ajudar</a>
        {acordeao("Institucional", INST)}
        <div class="mt-4 flex flex-col gap-2 border-t border-slate-200 pt-4">
          <a href="lei-incentivo.html" class="rounded-full border border-ocean px-4 py-2.5 text-center text-sm font-semibold text-ocean">Seja Parceiro</a>
          <a href="como-ajudar.html#doacao" class="rounded-full bg-sun px-4 py-2.5 text-center text-sm font-semibold text-oceanDeep">Doe Agora</a>
        </div>
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

# ---------- conferência da ORDEM ----------
h = open(L("index.html"), encoding="utf-8").read()
for rotulo, padrao in (("DESKTOP", r'aria-label="Menu principal"[^>]*>(.*?)</nav>'),
                       ("MOBILE", r'aria-label="Menu mobile"[^>]*>(.*?)</nav>')):
    m = re.search(padrao, h, re.DOTALL)
    nav = m.group(1)
    itens = re.findall(r'<a href="([^"]+)"[^>]*class="nav-link[^"]*"[^>]*>([^<]+)</a>'
                       r'|<a href="([^"]+)"[^>]*class="py-2[^"]*"[^>]*>([^<]+)</a>'
                       r'|<button type="button" class="nav-link nav-drop__botao"[^>]*>([^<]+)'
                       r'|<button type="button" class="nav-acc__botao"[^>]*>([^<]+)', nav)
    print(f"\n  --- {rotulo} ---")
    pos = 0
    for href1, t1, href2, t2, t3, t4 in itens:
        pos += 1
        if href1 or href2:
            print(f"     {pos}. {t1 or t2}  ({href1 or href2})")
        else:
            print(f"     {pos}. {(t3 or t4).strip()}  [dropdown]")
    for cta in re.findall(r'rounded-full[^>]*>([^<]+)</a>', nav):
        pos += 1
        print(f"     {pos}. {cta}  [botão CTA]")
