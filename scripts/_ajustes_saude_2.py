# -*- coding: utf-8 -*-
"""
Ajustes na pagina Saude:
  1) hero mais alto
  2) remover o selo/nome "Imagem ilustrativa" do card principal
  3) carrossel com setas nas extremidades
  4) galeria: clicar amplia (lightbox) com setas de navegacao
"""
import os
import re

BASE = r"G:/.shortcut-targets-by-id/18wGiptBKUmAmmkKHgdfu05TU4y_roWC1/BBDPRINT - BACKUP/BBDPRINT/App BBDPRiNT/PROJETOS/Projeto SER Sagi/projeto_SER_Sagi - Hermes"

# ============================================================
# 1) CSS
# ============================================================
CSS_EXTRA = """
/* --- Banner mais alto (melhor para fotos) --- */
.banner-alto {
  display: flex;
  align-items: center;
  min-height: clamp(380px, 46vh, 560px);
}

/* --- Carrossel com setas nas extremidades --- */
.carrossel-wrap { position: relative; }
.carrossel-arrow {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  z-index: 5;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 3rem;
  height: 3rem;
  border-radius: 999px;
  border: 1px solid rgba(15, 92, 115, 0.25);
  background: rgba(255, 255, 255, 0.94);
  color: var(--ocean);
  cursor: pointer;
  box-shadow: var(--shadow-card);
  transition: background .25s ease, color .25s ease;
}
.carrossel-arrow:hover { background: var(--ocean); color: #fff; }
.carrossel-arrow--prev { left: -0.75rem; }
.carrossel-arrow--next { right: -0.75rem; }
@media (max-width: 639px) {
  .carrossel-arrow { width: 2.5rem; height: 2.5rem; }
  .carrossel-arrow--prev { left: 0.15rem; }
  .carrossel-arrow--next { right: 0.15rem; }
}

/* --- Galeria clicavel --- */
.secao-figura {
  display: block;
  width: 100%;
  padding: 0;
  border: 0;
  background: none;
  cursor: zoom-in;
  overflow: hidden;
  border-radius: var(--radius-md);
}
.secao-figura img { transition: transform .3s ease; }
.secao-figura:hover img { transform: scale(1.04); }

/* --- Lightbox (foto ampliada + setas) --- */
.lightbox {
  position: fixed;
  inset: 0;
  z-index: 100;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  background: rgba(4, 28, 37, 0.94);
}
.lightbox[hidden] { display: none; }
.lightbox__img {
  max-width: min(92vw, 1100px);
  max-height: 84vh;
  border-radius: var(--radius-md);
  box-shadow: 0 30px 90px rgba(0, 0, 0, 0.5);
}
.lightbox__close {
  position: absolute;
  top: 1rem;
  right: 1rem;
  width: 3rem;
  height: 3rem;
  border-radius: 999px;
  border: 1px solid rgba(255, 255, 255, 0.35);
  background: rgba(255, 255, 255, 0.12);
  color: #fff;
  font-size: 1.5rem;
  line-height: 1;
  cursor: pointer;
}
.lightbox__arrow {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 3.25rem;
  height: 3.25rem;
  border-radius: 999px;
  border: 1px solid rgba(255, 255, 255, 0.35);
  background: rgba(255, 255, 255, 0.12);
  color: #fff;
  font-size: 1.35rem;
  cursor: pointer;
}
.lightbox__arrow:hover, .lightbox__close:hover { background: rgba(255, 255, 255, 0.26); }
.lightbox__arrow--prev { left: 1rem; }
.lightbox__arrow--next { right: 1rem; }
.lightbox__contador {
  position: absolute;
  bottom: 1.25rem;
  left: 50%;
  transform: translateX(-50%);
  color: rgba(255, 255, 255, 0.85);
  font-size: 0.85rem;
}
"""

p = os.path.join(BASE, "css", "style.css")
txt = open(p, encoding="utf-8", newline="").read()
if ".banner-alto" not in txt:
    open(p, "w", encoding="utf-8", newline="").write(txt.rstrip() + "\n" + CSS_EXTRA)
    print("  ✅ css: banner-alto + setas do carrossel + lightbox")
else:
    print("  ℹ️  css: ja aplicado")

# ============================================================
# 2) JS — carrossel com setas + galeria com lightbox
# ============================================================
p = os.path.join(BASE, "js", "main.js")
txt = open(p, encoding="utf-8", newline="").read()

DE = '''function markupCarrossel(itens) {
  return `<div class="carrossel">` + itens.map((i) => `
    <figure class="carrossel__item">
      <img src="${i.imagem_url}" alt="${i.titulo || ''}" loading="lazy" />
      ${i.titulo ? `<figcaption class="carrossel__caption">${i.titulo}</figcaption>` : ''}
    </figure>`).join('') + `</div>`;
}

function markupGrade(itens) {
  return `<div class="secao-grid">` + itens.map((i) => `
    <figure><img src="${i.imagem_url}" alt="${i.titulo || ''}" loading="lazy" /></figure>`).join('') + `</div>`;
}'''

PARA = '''function markupCarrossel(itens) {
  return `
  <div class="carrossel-wrap">
    <button type="button" class="carrossel-arrow carrossel-arrow--prev" data-carrossel-prev aria-label="Imagem anterior"><i class="fa-solid fa-chevron-left"></i></button>
    <div class="carrossel">
      ${itens.map((i) => `
      <figure class="carrossel__item">
        <img src="${i.imagem_url}" alt="${i.titulo || ''}" loading="lazy" />
        ${i.titulo ? `<figcaption class="carrossel__caption">${i.titulo}</figcaption>` : ''}
      </figure>`).join('')}
    </div>
    <button type="button" class="carrossel-arrow carrossel-arrow--next" data-carrossel-next aria-label="Proxima imagem"><i class="fa-solid fa-chevron-right"></i></button>
  </div>`;
}

function ligarSetasCarrossel(el) {
  const faixa = el.querySelector('.carrossel');
  if (!faixa) return;
  const passo = () => {
    const item = faixa.querySelector('.carrossel__item');
    return item ? item.getBoundingClientRect().width + 16 : Math.round(faixa.clientWidth * 0.8);
  };
  const prev = el.querySelector('[data-carrossel-prev]');
  const next = el.querySelector('[data-carrossel-next]');
  if (prev) prev.addEventListener('click', () => faixa.scrollBy({ left: -passo(), behavior: 'smooth' }));
  if (next) next.addEventListener('click', () => faixa.scrollBy({ left: passo(), behavior: 'smooth' }));
}

function markupGrade(itens) {
  return `<div class="secao-grid">` + itens.map((i, n) => `
    <button type="button" class="secao-figura" data-lb="${n}" aria-label="Ampliar imagem">
      <img src="${i.imagem_url}" alt="${i.titulo || ''}" loading="lazy" />
    </button>`).join('') + `</div>`;
}

// ---- Lightbox da galeria (ampliar + setas) ----
let lbItens = [];
let lbIndice = 0;

function garantirLightbox() {
  let lb = document.getElementById('lightbox');
  if (lb) return lb;
  lb = document.createElement('div');
  lb.id = 'lightbox';
  lb.className = 'lightbox';
  lb.hidden = true;
  lb.setAttribute('role', 'dialog');
  lb.setAttribute('aria-modal', 'true');
  lb.innerHTML = `
    <button type="button" class="lightbox__close" data-lb-close aria-label="Fechar">&times;</button>
    <button type="button" class="lightbox__arrow lightbox__arrow--prev" data-lb-prev aria-label="Imagem anterior"><i class="fa-solid fa-chevron-left"></i></button>
    <img class="lightbox__img" alt="" />
    <button type="button" class="lightbox__arrow lightbox__arrow--next" data-lb-next aria-label="Proxima imagem"><i class="fa-solid fa-chevron-right"></i></button>
    <p class="lightbox__contador"></p>`;
  document.body.appendChild(lb);
  lb.querySelector('[data-lb-close]').addEventListener('click', fecharLightbox);
  lb.querySelector('[data-lb-prev]').addEventListener('click', () => navegarLightbox(-1));
  lb.querySelector('[data-lb-next]').addEventListener('click', () => navegarLightbox(1));
  lb.addEventListener('click', (e) => { if (e.target === lb) fecharLightbox(); });
  document.addEventListener('keydown', (e) => {
    if (lb.hidden) return;
    if (e.key === 'Escape') fecharLightbox();
    else if (e.key === 'ArrowLeft') navegarLightbox(-1);
    else if (e.key === 'ArrowRight') navegarLightbox(1);
  });
  return lb;
}

function mostrarLightbox() {
  const itens = lbItens.filter((i) => i.imagem_url);
  if (!itens.length) return;
  lbItens = itens;
  lbIndice = ((lbIndice % itens.length) + itens.length) % itens.length;
  const lb = garantirLightbox();
  const img = lb.querySelector('.lightbox__img');
  img.src = itens[lbIndice].imagem_url;
  img.alt = itens[lbIndice].titulo || '';
  const cont = lb.querySelector('.lightbox__contador');
  if (cont) cont.textContent = `${lbIndice + 1} / ${itens.length}` + (itens[lbIndice].titulo ? ` — ${itens[lbIndice].titulo}` : '');
  lb.hidden = false;
  document.body.style.overflow = 'hidden';
}

function fecharLightbox() {
  const lb = document.getElementById('lightbox');
  if (lb) lb.hidden = true;
  document.body.style.overflow = '';
}

function navegarLightbox(passo) {
  lbIndice += passo;
  mostrarLightbox();
}

function ligarGaleria(el, itens) {
  el.querySelectorAll('[data-lb]').forEach((btn) => {
    btn.addEventListener('click', () => {
      lbItens = itens;
      lbIndice = parseInt(btn.getAttribute('data-lb'), 10) || 0;
      mostrarLightbox();
    });
  });
}'''
assert DE in txt, "main.js: bloco de markup nao encontrado"
txt = txt.replace(DE, PARA, 1)

DE = """      el.innerHTML = secao.toLowerCase().includes('carrossel')
        ? markupCarrossel(itens)
        : markupGrade(itens);"""
PARA = """      if (secao.toLowerCase().includes('carrossel')) {
        el.innerHTML = markupCarrossel(itens);
        ligarSetasCarrossel(el);
      } else {
        el.innerHTML = markupGrade(itens);
        ligarGaleria(el, itens);
      }"""
assert DE in txt, "main.js: render das secoes nao encontrado"
txt = txt.replace(DE, PARA, 1)

open(p, "w", encoding="utf-8", newline="").write(txt)
print("  ✅ js/main.js: setas do carrossel + lightbox da galeria")

# ============================================================
# 3) saude.html — hero mais alto + remover selo do card principal
# ============================================================
p = os.path.join(BASE, "saude.html")
txt = open(p, encoding="utf-8", newline="").read()

DE = '<section class="page-banner text-white relative overflow-hidden">'
PARA = '<section class="page-banner text-white relative overflow-hidden banner-alto">'
assert DE in txt, "saude.html: banner nao encontrado"
txt = txt.replace(DE, PARA, 1)

# Remover o selo "Imagem ilustrativa" do CARD PRINCIPAL (primeira ocorrencia)
padrao = re.compile(
    r'\s*<span class="mt-3 inline-flex items-center gap-1\.5 rounded-full bg-sand px-2\.5 py-1 text-\[10px\][^"]*"[^>]*>'
    r'<i class="fa-solid fa-wand-magic-sparkles text-\[9px\]"></i>Imagem ilustrativa</span>')
txt, qtd = padrao.subn("", txt, count=1)
assert qtd == 1, "saude.html: selo 'Imagem ilustrativa' do card nao encontrado"
print("  ✅ saude.html: selo 'Imagem ilustrativa' removido do card principal")

txt = txt.replace(DE, PARA, 1)
open(p, "w", encoding="utf-8", newline="").write(txt)
print("  ✅ saude.html: hero com banner-alto + selo removido")
