# -*- coding: utf-8 -*-
"""
FASE 5 · Parte C (2/2) — página depoimentos.html + botão na home.

  Cria depoimentos.html a partir do shell de transparencia.html
  (cabeçalho, menu e rodapé idênticos; só o miolo muda).
  Na home: limite de 3 cards + botão "Ver todos os depoimentos".
"""
import os

BASE = r"G:/.shortcut-targets-by-id/18wGiptBKUmAmmkKHgdfu05TU4y_roWC1/BBDPRINT - BACKUP/BBDPRINT/App BBDPRiNT/PROJETOS/Projeto SER Sagi/projeto_SER_Sagi - Hermes"
L = lambda p: os.path.join(BASE, p)  # noqa: E731

# ============================================================
# 1. depoimentos.html (a partir do shell de transparencia.html)
# ============================================================
tpl = open(L("transparencia.html"), encoding="utf-8", newline="").read()

tpl = tpl.replace("<title>Transparência | Instituto S.E.R. Sagi</title>",
                  "<title>Depoimentos | Instituto S.E.R. Sagi</title>")
tpl = tpl.replace(
    'content="Área de transparência do Instituto S.E.R. Sagi com organização de relatórios, documentos, parceiros e indicadores institucionais."',
    'content="Histórias de famílias, crianças, voluntários e parceiros do Instituto S.E.R. Sagi — depoimentos em texto, foto e vídeo."')
tpl = tpl.replace('"name": "Transparência"', '"name": "Depoimentos"')

# --- hero com imagem + scrim ---
ini = tpl.index('<section class="page-banner text-white">')
fim = tpl.index("</section>", ini) + len("</section>")
hero = '''<section class="page-banner text-white relative overflow-hidden banner-alto">
      <!-- CAMADA 1 · IMAGEM de fundo (ilustrativa — trocar por foto real em depoimentos/hero/) -->
      <img src="https://loremflickr.com/1600/600/community,people,portrait?lock=901" alt="" aria-hidden="true" data-secao-img="hero" data-categoria="Depoimentos" class="absolute inset-0 h-full w-full object-cover">
      <!-- CAMADA 2 · SCRIM (véu diagonal, mesmo efeito do hero da home) -->
      <div class="banner-scrim absolute inset-0"></div>
      <div class="relative z-10 mx-auto max-w-7xl px-4 py-16 lg:px-8 lg:py-20">
        <p class="text-sm font-semibold uppercase tracking-[0.25em] text-sun">Depoimentos</p>
        <h1 class="mt-4 max-w-4xl text-4xl font-extrabold leading-tight sm:text-5xl">Histórias que aproximam famílias, crianças e parceiros</h1>
        <p class="mt-6 max-w-3xl text-lg text-white/85">Quem participa do Instituto conta como o esporte, a saúde e a educação mudaram a rotina da comunidade do Sagi.</p>
      </div>
    </section>'''
tpl = tpl[:ini] + hero + tpl[fim:]

# --- breadcrumb ---
ini = tpl.index('<nav class="breadcrumb')
fim = tpl.index("</nav>", ini) + len("</nav>")
tpl = tpl[:ini] + '''<nav class="breadcrumb breadcrumb--claro mx-auto max-w-7xl px-4 lg:px-8" aria-label="Você está aqui">
      <ol>
        <li><a href="./">Início</a></li>
        <li><span aria-current="page">Depoimentos</span></li>
      </ol>
    </nav>''' + tpl[fim:]

# --- miolo ---
ini = tpl.index('<section class="mx-auto max-w-7xl px-4 py-16 lg:px-8">')
fim = tpl.index("</main>")
miolo = '''<section class="mx-auto max-w-7xl px-4 py-16 lg:px-8">
      <div class="max-w-3xl">
        <p class="text-sm font-semibold uppercase tracking-[0.25em] text-ocean">Quem vive o Instituto</p>
        <h2 class="section-title text-3xl font-extrabold text-oceanDeep">Todas as histórias</h2>
        <div class="mt-4 flex items-center gap-2" data-badge-depoimentos>
          <span class="inline-flex items-center gap-1.5 rounded-full bg-sun/20 px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.15em] text-oceanDeep" title="Conteúdo demonstrativo — será substituído por conteúdo real"><i class="fa-solid fa-wand-magic-sparkles text-[10px]"></i>Conteúdo ilustrativo</span>
        </div>
        <p class="mt-4 leading-8 text-slate-600">Depoimentos reais de mães, pais, crianças, voluntários e parceiros — publicados sempre com autorização. Cada história pode vir com foto, vídeo e uma legenda.</p>
      </div>
      <div data-render="testimonials" class="mt-10 grid gap-6 md:grid-cols-2 xl:grid-cols-3"></div>
    </section>

    <section class="bg-mist/70 py-16">
      <div class="mx-auto max-w-7xl px-4 lg:px-8">
        <article class="rounded-[2rem] bg-oceanDeep p-8 text-white shadow-soft sm:p-10">
          <p class="text-sm font-semibold uppercase tracking-[0.25em] text-sun">Sua história</p>
          <h2 class="section-title text-3xl font-extrabold">Tem uma história com o Instituto?</h2>
          <p class="mt-6 max-w-2xl leading-8 text-white/85">Famílias, crianças, voluntários e parceiros podem enviar o seu depoimento. A publicação é sempre feita com autorização de imagem e de texto — especialmente no caso de crianças e adolescentes (ECA e LGPD).</p>
          <div class="mt-8 flex flex-wrap gap-4">
            <a href="contato.html" class="btn btn--primary">Enviar meu depoimento</a>
          </div>
        </article>
      </div>
    </section>
  '''
tpl = tpl[:ini] + miolo + tpl[fim:]

open(L("depoimentos.html"), "w", encoding="utf-8", newline="").write(tpl)
print("  ✅ depoimentos.html criado")

# ============================================================
# 2. HOME — limite 3 + botão + marcador do selo
# ============================================================
idx = open(L("index.html"), encoding="utf-8", newline="").read()
antes = idx

idx = idx.replace('<div data-render="testimonials" class="mt-10 grid gap-6 md:grid-cols-2 xl:grid-cols-3"></div>',
                  '<div data-render="testimonials" data-limite="3" class="mt-10 grid gap-6 md:grid-cols-2 xl:grid-cols-3"></div>')

# botão depois da grade de depoimentos
alvo = '<div data-render="testimonials" data-limite="3" class="mt-10 grid gap-6 md:grid-cols-2 xl:grid-cols-3"></div>'
botao = alvo + '''<div class="mt-10 flex justify-center"><a href="depoimentos.html" class="btn btn--primary">Ver todos os depoimentos <span aria-hidden="true">&rarr;</span></a></div>'''
if "depoimentos.html" not in idx:
    idx = idx.replace(alvo, botao, 1)

# marcador no selo "Conteúdo ilustrativo" (o JS esconde quando houver depoimento real)
velho_selo = '<div class="mt-4 flex items-center gap-2"><span class="inline-flex items-center gap-1.5 rounded-full bg-sun/20 px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.15em] text-oceanDeep" title="Conteúdo demonstrativo — será substituído por conteúdo real"><i class="fa-solid fa-wand-magic-sparkles text-[10px]"></i>Conteúdo ilustrativo</span></div><p class="mt-4 leading-8 text-slate-600">Depoimentos reais'
novo_selo = '<div class="mt-4 flex items-center gap-2" data-badge-depoimentos><span class="inline-flex items-center gap-1.5 rounded-full bg-sun/20 px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.15em] text-oceanDeep" title="Conteúdo demonstrativo — será substituído por conteúdo real"><i class="fa-solid fa-wand-magic-sparkles text-[10px]"></i>Conteúdo ilustrativo</span></div><p class="mt-4 leading-8 text-slate-600">Depoimentos reais'
n_selo = velho_selo in idx
idx = idx.replace(velho_selo, novo_selo, 1)

print(f"  ✅ index.html — limite 3: {'data-limite' in idx} | botão: {'depoimentos.html' in idx} | selo marcado: {n_selo}")
open(L("index.html"), "w", encoding="utf-8", newline="").write(idx)

# ============================================================
# 3. JS — esconde o selo ilustrativo quando houver depoimento real
# ============================================================
p_js = L("js/main.js")
js = open(p_js, encoding="utf-8", newline="").read()
if "data-badge-depoimentos" in js:
    print("  ⚠️  main.js ja tratava o selo — pulando")
else:
    velho = "  container.setAttribute('data-ilustrativo', usandoFallback ? 'true' : 'false');"
    novo = ("  container.setAttribute('data-ilustrativo', usandoFallback ? 'true' : 'false');\n"
            "  document.querySelectorAll('[data-badge-depoimentos]').forEach((el) => {\n"
            "    el.hidden = !usandoFallback;\n"
            "  });")
    if velho not in js:
        print("  ⚠️  nao achei o ponto do selo no main.js")
    else:
        js = js.replace(velho, novo, 1)
        open(p_js, "w", encoding="utf-8", newline="").write(js)
        print("  ✅ js/main.js — selo ilustrativo some quando houver depoimento real")

# ============================================================
# 4. publicar.py — categoria "depoimentos" (hero da página nova)
# ============================================================
p_pub = L("scripts/publicar.py")
pub = open(p_pub, encoding="utf-8", newline="").read()
if '"depoimentos": "Depoimentos"' in pub:
    print("  ⚠️  publicar.py ja tinha a categoria — pulando")
elif '    "home": "Home",' in pub:
    pub = pub.replace('    "home": "Home",',
                      '    "home": "Home",\n    "depoimentos": "Depoimentos",', 1)
    open(p_pub, "w", encoding="utf-8", newline="").write(pub)
    print("  ✅ publicar.py — categoria 'depoimentos'")
else:
    print("  ⚠️  nao achei a categoria home no publicar.py")
