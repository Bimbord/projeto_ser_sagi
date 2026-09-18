# -*- coding: utf-8 -*-
"""
Menu com DROPDOWN (desktop) e ACORDEÃO (mobile).

Estrutura aprovada (9 itens, 3 agrupadores ▾):
  Início · Quem Somos · JÓIA DA COROA · Nossas Ações ▾ · Acervo ▾ ·
  Depoimentos · Como Ajudar · Institucional ▾ · Contato

- Jóia da Coroa fica no menu principal (pedido do dono)
- botões CTA do topo só aparecem a partir de xl (liberam espaço em lg)
- acessível: hover + clique + Esc + Tab; no celular é acordeão
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


ACOES = [("Ver todas as ações", "acoes.html"), ("Saúde", "saude.html"), ("Esporte", "esporte.html"),
         ("Educação", "educacao.html"), ("Cultura", "cultura.html"),
         ("Preservação Ambiental", "preservacao-ambiental.html"), ("Ações Solidárias", "acoes-solidarias.html")]
ACERVO = [("Acervo completo", "acervo.html"), ("Esporte", "acervo-esporte.html"), ("Saúde", "acervo-saude.html"),
          ("Educação", "acervo-educacao.html"), ("Cultura", "acervo-cultura.html"),
          ("Preservação", "acervo-preservacao.html"), ("Eventos", "acervo-eventos.html")]
INST = [("Lei de Incentivo", "lei-incentivo.html"), ("Transparência", "transparencia.html"),
        ("Instalações", "instalacoes.html")]

DESKTOP = f'''<nav class="hidden items-center gap-1 lg:flex xl:gap-2" aria-label="Menu principal">
        <a href="./" data-page-link class="nav-link">Início</a>
        <a href="quem-somos.html" data-page-link class="nav-link">Quem Somos</a>
        <a href="joia-da-coroa.html" data-page-link class="nav-link nav-link--destaque">Jóia da Coroa</a>
        {drop("Nossas Ações", ACOES)}
        {drop("Acervo", ACERVO)}
        <a href="depoimentos.html" data-page-link class="nav-link">Depoimentos</a>
        <a href="como-ajudar.html" data-page-link class="nav-link">Como Ajudar</a>
        {drop("Institucional", INST)}
        <a href="contato.html" data-page-link class="nav-link">Contato</a>
      </nav>'''

MOBILE = f'''<nav class="mx-auto flex max-w-7xl flex-col px-4 py-4" aria-label="Menu mobile">
        <a href="./" data-page-link class="py-2 text-sm font-medium">Início</a>
        <a href="quem-somos.html" data-page-link class="py-2 text-sm font-medium">Quem Somos</a>
        <a href="joia-da-coroa.html" data-page-link class="py-2 text-sm font-semibold text-ocean">Jóia da Coroa</a>
        {acordeao("Nossas Ações", ACOES)}
        {acordeao("Acervo", ACERVO)}
        <a href="depoimentos.html" data-page-link class="py-2 text-sm font-medium">Depoimentos</a>
        <a href="como-ajudar.html" data-page-link class="py-2 text-sm font-medium">Como Ajudar</a>
        {acordeao("Institucional", INST)}
        <a href="contato.html" data-page-link class="py-2 text-sm font-medium">Contato</a>
      </nav>'''

# ---------- HTML ----------
paginas = sorted(glob.glob(L("*.html")))
ok, sem = [], []
for p in paginas:
    nome = os.path.basename(p)
    txt = open(p, encoding="utf-8", newline="").read()
    orig = txt

    txt = re.sub(r'<nav class="hidden items-center[^"]*lg:flex"[^>]*>.*?</nav>', DESKTOP, txt, count=1, flags=re.DOTALL)
    txt = re.sub(r'<nav class="mx-auto flex max-w-7xl flex-col px-4 py-4"[^>]*>.*?</nav>', MOBILE, txt, count=1, flags=re.DOTALL)
    # os botões CTA do topo passam a aparecer só em telas largas
    txt = txt.replace('class="hidden items-center gap-3 lg:flex"', 'class="hidden items-center gap-3 xl:flex"')

    if txt != orig:
        open(p, "w", encoding="utf-8", newline="").write(txt)
        ok.append(nome)
    else:
        sem.append(nome)

print(f"  ✅ menu trocado em {len(ok)} páginas")
if sem:
    print(f"  ⚠️  sem alteração: {', '.join(sem)}")

# ---------- CSS ----------
p_css = L("css/style.css")
css = open(p_css, encoding="utf-8", newline="").read()
if ".nav-drop__menu" in css:
    print("  ⚠️  CSS já tinha o dropdown")
else:
    css += """

/* ============================================================
   MENU PRINCIPAL — links, dropdown (desktop) e acordeão (mobile)
   ============================================================ */
.nav-link {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.5rem 0.65rem;
  border: 0;
  border-radius: 0.6rem;
  background: none;
  font-size: 0.875rem;
  font-weight: 500;
  color: inherit;
  white-space: nowrap;
  cursor: pointer;
  transition: color 0.2s ease, background 0.2s ease;
}
.nav-link:hover { color: var(--ocean); background: var(--mist); }
.nav-link.active { color: var(--ocean); font-weight: 700; }
.nav-link--destaque { color: var(--ocean-deep); font-weight: 700; }

.nav-drop { position: relative; }
.nav-drop__botao .fa-chevron-down { font-size: 0.625rem; transition: transform 0.2s ease; }
.nav-drop.aberto .nav-drop__botao .fa-chevron-down { transform: rotate(180deg); }
.nav-drop__menu {
  position: absolute;
  top: calc(100% + 0.35rem);
  left: 0;
  z-index: 60;
  min-width: 15rem;
  padding: 0.4rem;
  border: var(--border-card);
  border-radius: 1rem;
  background: #fff;
  box-shadow: 0 24px 60px rgba(8, 59, 76, 0.18);
  opacity: 0;
  visibility: hidden;
  transform: translateY(-6px);
  transition: opacity 0.18s ease, transform 0.18s ease, visibility 0.18s;
}
.nav-drop.aberto .nav-drop__menu { opacity: 1; visibility: visible; transform: translateY(0); }
.nav-drop__menu a {
  display: block;
  padding: 0.5rem 0.75rem;
  border-radius: 0.6rem;
  font-size: 0.875rem;
  color: var(--slate);
  transition: background 0.18s ease, color 0.18s ease;
}
.nav-drop__menu a:hover { background: var(--mist); color: var(--ocean); }
.nav-drop__menu a.active { background: var(--mist); color: var(--ocean); font-weight: 700; }

.nav-acc { border-top: 1px solid rgba(15, 92, 115, 0.08); }
.nav-acc__botao {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  padding: 0.7rem 0;
  border: 0;
  background: none;
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--slate);
  cursor: pointer;
}
.nav-acc__botao .fa-chevron-down { font-size: 0.7rem; transition: transform 0.2s ease; }
.nav-acc.aberto .nav-acc__botao .fa-chevron-down { transform: rotate(180deg); }
.nav-acc__menu { display: none; padding: 0 0 0.5rem 0.75rem; }
.nav-acc.aberto .nav-acc__menu { display: block; }
"""
    open(p_css, "w", encoding="utf-8", newline="").write(css)
    print("  ✅ css/style.css — dropdown + acordeão")

# ---------- JS ----------
p_js = L("js/main.js")
js = open(p_js, encoding="utf-8", newline="").read()
if "setupDropdowns" in js:
    print("  ⚠️  JS já tinha os dropdowns")
else:
    novo = '''function setupDropdowns() {
  const drops = document.querySelectorAll('.nav-drop');
  if (!drops.length) return;
  const largura = () => window.matchMedia('(min-width: 1024px)').matches;
  const fechar = (d) => {
    d.classList.remove('aberto');
    const b = d.querySelector('.nav-drop__botao');
    if (b) b.setAttribute('aria-expanded', 'false');
  };
  drops.forEach((d) => {
    const b = d.querySelector('.nav-drop__botao');
    if (!b) return;
    b.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      const estava = d.classList.contains('aberto');
      drops.forEach(fechar);
      if (!estava) { d.classList.add('aberto'); b.setAttribute('aria-expanded', 'true'); }
    });
    d.addEventListener('mouseenter', () => {
      if (largura()) { d.classList.add('aberto'); b.setAttribute('aria-expanded', 'true'); }
    });
    d.addEventListener('mouseleave', () => { if (largura()) fechar(d); });
  });
  document.addEventListener('click', (e) => { if (!e.target.closest('.nav-drop')) drops.forEach(fechar); });
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') drops.forEach(fechar); });
}

function setupAcordeoes() {
  document.querySelectorAll('.nav-acc__botao').forEach((b) => {
    b.addEventListener('click', () => {
      const acc = b.closest('.nav-acc');
      const aberto = acc.classList.toggle('aberto');
      b.setAttribute('aria-expanded', aberto ? 'true' : 'false');
    });
  });
}

function setupActiveLinks() {'''
    js = js.replace("function setupActiveLinks() {", novo, 1)

    # marca o pai quando um filho estiver ativo
    velho_fim = """    if (destino === target) link.classList.add('active');
  });
}"""
    novo_fim = """    if (destino === target) link.classList.add('active');
  });
  // agrupador (dropdown/acordeão) fica destacado quando um filho está ativo
  document.querySelectorAll('.nav-drop, .nav-acc').forEach((grupo) => {
    if (grupo.querySelector('[data-page-link].active')) {
      const pai = grupo.querySelector('.nav-drop__botao, .nav-acc__botao');
      if (pai) pai.classList.add('active');
    }
  });
}"""
    if velho_fim in js:
        js = js.replace(velho_fim, novo_fim, 1)
    else:
        print("  ⚠️  não achei o fim do setupActiveLinks para marcar o pai")

    js = js.replace("  setupActiveLinks();", "  setupActiveLinks();\n  setupDropdowns();\n  setupAcordeoes();", 1)

    open(p_js, "w", encoding="utf-8", newline="").write(js)
    print("  ✅ js/main.js — setupDropdowns + setupAcordeoes + pai ativo")
