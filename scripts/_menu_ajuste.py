# -*- coding: utf-8 -*-
"""
Ajuste no menu (pedido do dono):
  - Contato  -> passa para dentro de INSTITUCIONAL
  - Depoimentos -> passa para dentro de QUEM SOMOS (que vira dropdown)

Menu final (7 itens de topo):
  Início · Quem Somos ▾ · Jóia da Coroa · Nossas Ações ▾ · Acervo ▾ ·
  Como Ajudar · Institucional ▾

Também corrige o JS: 'instalacoes.html' estava mapeado como sub-página de
Quem Somos, mas agora vive em Institucional — o destaque do menu quebrava.
"""
import glob
import os
import re

BASE = r"G:/.shortcut-targets-by-id/18wGiptBKUmAmmkKHgdfu05TU4y_roWC1/BBDPRINT - BACKUP/BBDPRINT/App BBDPRiNT/PROJETOS/Projeto SER Sagi/projeto_SER_Sagi - Hermes"
L = lambda p: os.path.join(BASE, p)  # noqa: E731

CHEV = '<i class="fa-solid fa-chevron-down" aria-hidden="true"></i>'


def drop(titulo, itens):
    links = "\n            ".join(f'<a href="{h}" data-page-link>{t}</a>' for t, h in itens)
    return (f'''<div class="nav-drop">
          <button type="button" class="nav-link nav-drop__botao" aria-expanded="false" aria-haspopup="true">{titulo} {CHEV}</button>
          <div class="nav-drop__menu">
            {links}
          </div>
        </div>''')


def acordeao(titulo, itens):
    links = "\n            ".join(f'<a href="{h}" data-page-link class="block py-2 text-sm">{t}</a>' for t, h in itens)
    return (f'''<div class="nav-acc">
          <button type="button" class="nav-acc__botao" aria-expanded="false">{titulo} {CHEV}</button>
          <div class="nav-acc__menu">
            {links}
          </div>
        </div>''')


QUEM_SOMOS = [("Quem Somos", "quem-somos.html"), ("Depoimentos", "depoimentos.html")]
ACOES = [("Ver todas as ações", "acoes.html"), ("Saúde", "saude.html"), ("Esporte", "esporte.html"),
         ("Educação", "educacao.html"), ("Cultura", "cultura.html"),
         ("Preservação Ambiental", "preservacao-ambiental.html"), ("Ações Solidárias", "acoes-solidarias.html")]
ACERVO = [("Acervo completo", "acervo.html"), ("Esporte", "acervo-esporte.html"), ("Saúde", "acervo-saude.html"),
          ("Educação", "acervo-educacao.html"), ("Cultura", "acervo-cultura.html"),
          ("Preservação", "acervo-preservacao.html"), ("Eventos", "acervo-eventos.html")]
INST = [("Lei de Incentivo", "lei-incentivo.html"), ("Transparência", "transparencia.html"),
        ("Instalações", "instalacoes.html"), ("Contato", "contato.html")]

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
paginas = sorted(glob.glob(L("*.html")))
ok, sem = [], []
for p in paginas:
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

print(f"  ✅ menu ajustado em {len(ok)} páginas")
if sem:
    print(f"  ⚠️  sem alteração: {', '.join(sem)}")

# ---------- JS: instalacoes agora é de Institucional ----------
p_js = L("js/main.js")
js = open(p_js, encoding="utf-8", newline="").read()
velho = "  const quemSomosSub = ['instalacoes.html'];"
novo = "  const quemSomosSub = [];   // instalacoes.html passou para o menu Institucional"
if velho in js:
    open(p_js, "w", encoding="utf-8", newline="").write(js.replace(velho, novo, 1))
    print("  ✅ js/main.js — instalacoes fora do grupo 'quem-somos'")
elif "const quemSomosSub = [];" in js:
    print("  ⚠️  JS já ajustado")
else:
    print("  ⚠️  não achei quemSomosSub no main.js")

# ---------- conferência ----------
print("\n  --- menu resultante ---")
amostra = open(L("index.html"), encoding="utf-8").read()
nav = re.search(r'<nav class="hidden items-center[^>]*>.*?</nav>', amostra, re.DOTALL).group(0)
for m in re.finditer(r'<a href="([^"]+)" data-page-link class="nav-link[^"]*">([^<]+)</a>|nav-drop__botao[^>]*>([^<]+?)\s*<i', nav):
    if m.group(1):
        print(f"     link    {m.group(2):18} -> {m.group(1)}")
    else:
        print(f"     dropdown {m.group(3)}")
