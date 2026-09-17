# -*- coding: utf-8 -*-
"""
Liga as SECOES do Drive (categoria + secao no Supabase) a pagina saude.html.

  1) css/style.css  -> estilos do carrossel (scroll-snap) e da grade de secao
  2) js/main.js     -> loadSecoes(): le o Supabase e preenche os blocos
  3) saude.html     -> marca hero / imagem principal / carrossel / galeria
"""
import os
import re

BASE = r"G:/.shortcut-targets-by-id/18wGiptBKUmAmmkKHgdfu05TU4y_roWC1/BBDPRINT - BACKUP/BBDPRINT/App BBDPRiNT/PROJETOS/Projeto SER Sagi/projeto_SER_Sagi - Hermes"

CSS_NOVO = """

/* ============================================================
   SECOES ALIMENTADAS PELAS PASTAS DO DRIVE (categoria + secao)
   Renderizadas por js/main.js -> loadSecoes().
   CSS puro de proposito: o Tailwind Play CDN nao gera classes
   para conteudo injetado via JavaScript.
   ============================================================ */
.carrossel {
  display: flex;
  gap: 1rem;
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  -webkit-overflow-scrolling: touch;
  padding-bottom: .75rem;
}
.carrossel__item {
  flex: 0 0 auto;
  width: min(80vw, 24rem);
  scroll-snap-align: start;
  border-radius: var(--radius-lg);
  overflow: hidden;
  background: #fff;
  border: var(--border-card);
  box-shadow: var(--shadow-card);
}
.carrossel__item img { display: block; width: 100%; height: 16rem; object-fit: cover; }
.carrossel__caption { padding: .85rem 1rem; font-size: .85rem; color: #475569; }

.secao-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 1rem; }
@media (max-width: 1023px) { .secao-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
@media (max-width: 639px)  { .secao-grid { grid-template-columns: 1fr; } }
.secao-grid img { display: block; width: 100%; height: 14rem; object-fit: cover; border-radius: var(--radius-md); }

.secao-vazio {
  padding: 1.25rem;
  border-radius: var(--radius-md);
  background: var(--mist);
  color: #475569;
  font-size: .9rem;
}
"""

JS_NOVO = """// ============================================================
// SECOES ALIMENTADAS POR PASTA DO DRIVE (categoria + secao)
// Cada subpasta de secao no Drive vira uma `secao` na tabela
// `arquivo`. O bloco marcado com [data-secao="x"] e preenchido
// com as imagens daquela secao; [data-secao-img="x"] recebe a
// primeira imagem (usado no hero e na imagem principal).
// ============================================================
async function fetchSecao(categoria, secao) {
  const url = `${SUPABASE_URL}/rest/v1/arquivo?select=id,titulo,descricao,imagem_url`
    + `&categoria=eq.${encodeURIComponent(categoria)}`
    + `&secao=eq.${encodeURIComponent(secao)}`
    + `&deleted=eq.false&order=id.asc`;
  const response = await fetch(url, {
    headers: {
      apikey: SUPABASE_ANON_KEY,
      Authorization: `Bearer ${SUPABASE_ANON_KEY}`
    }
  });
  if (!response.ok) throw new Error(`Erro ao buscar a secao ${secao}`);
  return response.json();
}

function markupCarrossel(itens) {
  return `<div class="carrossel">` + itens.map((i) => `
    <figure class="carrossel__item">
      <img src="${i.imagem_url}" alt="${i.titulo || ''}" loading="lazy" />
      ${i.titulo ? `<figcaption class="carrossel__caption">${i.titulo}</figcaption>` : ''}
    </figure>`).join('') + `</div>`;
}

function markupGrade(itens) {
  return `<div class="secao-grid">` + itens.map((i) => `
    <figure><img src="${i.imagem_url}" alt="${i.titulo || ''}" loading="lazy" /></figure>`).join('') + `</div>`;
}

async function loadSecoes() {
  // Blocos com varias imagens (carrossel / galeria)
  const blocos = document.querySelectorAll('[data-secao]');
  for (const el of blocos) {
    const secao = el.getAttribute('data-secao');
    const categoria = el.getAttribute('data-categoria') || '';
    try {
      const itens = (await fetchSecao(categoria, secao)).filter((i) => i.imagem_url);
      if (!itens.length) {
        el.innerHTML = `<p class="secao-vazio">Nenhuma imagem publicada nesta secao ainda.</p>`;
        continue;
      }
      el.innerHTML = secao.toLowerCase().includes('carrossel')
        ? markupCarrossel(itens)
        : markupGrade(itens);
    } catch (error) {
      el.innerHTML = `<p class="secao-vazio">Nao foi possivel carregar as imagens desta secao.</p>`;
    }
  }

  // Imagens unicas (hero / imagem principal)
  const imagens = document.querySelectorAll('[data-secao-img]');
  for (const img of imagens) {
    const secao = img.getAttribute('data-secao-img');
    const categoria = img.getAttribute('data-categoria') || '';
    try {
      const itens = (await fetchSecao(categoria, secao)).filter((i) => i.imagem_url);
      if (itens.length) {
        img.src = itens[0].imagem_url;
        if (itens[0].titulo) img.alt = itens[0].titulo;
      }
    } catch (error) { /* mantem a imagem padrao do HTML */ }
  }
}

"""

# ============================================================
# 1) CSS
# ============================================================
p = os.path.join(BASE, "css", "style.css")
txt = open(p, encoding="utf-8", newline="").read()
if ".carrossel {" not in txt:
    open(p, "w", encoding="utf-8", newline="").write(txt.rstrip() + "\n" + CSS_NOVO)
    print("  ✅ css/style.css: estilos do carrossel + grade de secao")
else:
    print("  ℹ️  css/style.css: ja tinha os estilos")

# ============================================================
# 2) JS
# ============================================================
p = os.path.join(BASE, "js", "main.js")
txt = open(p, encoding="utf-8", newline="").read()
ANCORA = "let archiveData = [];"
assert ANCORA in txt, "main.js: ancora 'let archiveData = [];' nao encontrada"
if "async function loadSecoes" not in txt:
    txt = txt.replace(ANCORA, JS_NOVO + ANCORA, 1)
    DE_INIT = """  setupArchiveFilters();
  loadArchive();"""
    PARA_INIT = """  setupArchiveFilters();
  loadArchive();
  loadSecoes();"""
    assert DE_INIT in txt, "main.js: init nao encontrado"
    txt = txt.replace(DE_INIT, PARA_INIT, 1)
    open(p, "w", encoding="utf-8", newline="").write(txt)
    print("  ✅ js/main.js: loadSecoes() adicionado + chamada no init")
else:
    print("  ℹ️  js/main.js: loadSecoes() ja existia")

# ============================================================
# 3) saude.html
# ============================================================
p = os.path.join(BASE, "saude.html")
txt = open(p, encoding="utf-8", newline="").read()

# 3.1 hero do banner
DE = '<img src="https://loremflickr.com/1600/600/dentist,health,care?lock=201" alt="" aria-hidden="true" class="absolute inset-0 h-full w-full object-cover">'
PARA = '<img src="https://loremflickr.com/1600/600/dentist,health,care?lock=201" alt="" aria-hidden="true" data-secao-img="hero" data-categoria="Saúde" class="absolute inset-0 h-full w-full object-cover">'
assert DE in txt, "saude.html: imagem do hero nao encontrada"
txt = txt.replace(DE, PARA, 1)

# 3.2 imagem principal do card
DE = '<img src="https://loremflickr.com/800/500/dentist,clinic,tooth?lock=101" alt="Imagem ilustrativa — Consultório Odontológico" class="h-64 w-full object-cover" loading="lazy" />'
PARA = '<img src="https://loremflickr.com/800/500/dentist,clinic,tooth?lock=101" alt="Imagem ilustrativa — Consultório Odontológico" data-secao-img="imagem principal" data-categoria="Saúde" class="h-64 w-full object-cover" loading="lazy" />'
assert DE in txt, "saude.html: imagem principal nao encontrada"
txt = txt.replace(DE, PARA, 1)

# 3.3 galeria estatica -> bloco dinamico
padrao = re.compile(r'<div class="mt-8 grid gap-6 md:grid-cols-2 xl:grid-cols-3">.*?<a href="acervo-saude\.html"', re.DOTALL)
novo = '<div class="mt-8" data-secao="galeria" data-categoria="Saúde"></div>\n      <a href="acervo-saude.html"'
txt, qtd = padrao.subn(novo, txt, count=1)
assert qtd == 1, "saude.html: bloco da galeria nao encontrado"
print("  ✅ saude.html: galeria virou bloco dinamico")

# 3.4 carrossel novo (antes da galeria)
ANCORA_GAL = '    <section class="mx-auto max-w-7xl px-4 pb-16 lg:px-8">\n      <div class="flex flex-col gap-3">\n        <p class="text-sm font-semibold uppercase tracking-[0.25em] text-ocean">Galeria</p>'
assert ANCORA_GAL in txt, "saude.html: ancora da galeria nao encontrada"
CARROSSEL = '''    <section class="mx-auto max-w-7xl px-4 pb-16 lg:px-8">
      <div class="flex flex-col gap-3">
        <p class="text-sm font-semibold uppercase tracking-[0.25em] text-ocean">Resultados</p>
        <h3 class="section-title text-3xl font-extrabold text-oceanDeep">Sorrisos que falam por si</h3>
        <p class="max-w-3xl text-slate-600">Registros de quem passou pelo nosso consultório. Deslize para o lado para ver mais.</p>
      </div>
      <div class="mt-8" data-secao="carrossel" data-categoria="Saúde"></div>
    </section>
''' + ANCORA_GAL
txt = txt.replace(ANCORA_GAL, CARROSSEL, 1)
print("  ✅ saude.html: secao do carrossel criada")

open(p, "w", encoding="utf-8", newline="").write(txt)
print("  ✅ saude.html salvo")
