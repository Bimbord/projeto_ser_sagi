# -*- coding: utf-8 -*-
"""
FASE 4b — seções de mídia nas 11 páginas de ÁREA (opção B: já visíveis).

Cada página ganha, antes do CTA:
  - Carrossel  -> pasta <categoria>/<pagina>/carrossel
  - Galeria    -> pasta <categoria>/<pagina>/galeria

Nasce vazio (aviso amigável) e é alimentado quando as fotos entrarem
nas pastas do Drive. O mecanismo (CSS + JS) é o mesmo da página Saúde.
"""
import os

BASE = r"G:/.shortcut-targets-by-id/18wGiptBKUmAmmkKHgdfu05TU4y_roWC1/BBDPRINT - BACKUP/BBDPRINT/App BBDPRiNT/PROJETOS/Projeto SER Sagi/projeto_SER_Sagi - Hermes"
L = lambda p: os.path.join(BASE, p)  # noqa: E731

# pagina -> (categoria no banco, slug da pasta no Drive, pagina do acervo)
PAGINAS = {
    "escola-jiu-jitsu.html":      ("Esporte",   "escola-jiu-jitsu",      "acervo-esporte.html"),
    "volei.html":                 ("Esporte",   "volei",                 "acervo-esporte.html"),
    "futevolei.html":             ("Esporte",   "futevolei",             "acervo-esporte.html"),
    "estudio-musculacao.html":    ("Esporte",   "estudio-musculacao",    "acervo-esporte.html"),
    "natacao.html":               ("Esporte",   "natacao",               "acervo-esporte.html"),
    "danca.html":                 ("Esporte",   "danca",                 "acervo-esporte.html"),
    "arena-futevolei-volei.html": ("Esporte",   "arena-futevolei-volei", "acervo-esporte.html"),
    "ingles.html":                ("Educação",  "ingles",                "acervo-educacao.html"),
    "espanhol.html":              ("Educação",  "espanhol",              "acervo-educacao.html"),
    "informatica.html":           ("Educação",  "informatica",           "acervo-educacao.html"),
    "sustentabilidade.html":      ("Educação",  "sustentabilidade",      "acervo-educacao.html"),
}

CTA = '<section class="bg-mist/70 py-16">'

BLOCO = '''<section class="mx-auto max-w-7xl px-4 pb-16 lg:px-8">
      <div class="flex flex-col gap-3">
        <p class="text-sm font-semibold uppercase tracking-[0.25em] text-ocean">Em ação</p>
        <h3 class="section-title text-3xl font-extrabold text-oceanDeep">Momentos das nossas atividades</h3>
        <p class="max-w-3xl text-slate-600">Registros de quem participa. Deslize para o lado para ver mais.</p>
      </div>
      <div class="mt-8" data-secao="carrossel" data-categoria="{cat}" data-pagina="{pag}"></div>
    </section>
    <section class="mx-auto max-w-7xl px-4 pb-16 lg:px-8">
      <div class="flex flex-col gap-3">
        <p class="text-sm font-semibold uppercase tracking-[0.25em] text-ocean">Galeria</p>
        <h3 class="section-title text-3xl font-extrabold text-oceanDeep">Veja como é na prática</h3>
        <p class="max-w-3xl text-slate-600">Fotos das atividades desta frente. Clique em uma imagem para ampliar. Os registros abaixo são <strong>ilustrativos</strong> até entrarem as fotos reais das atividades.</p>
      </div>
      <div class="mt-8" data-secao="galeria" data-categoria="{cat}" data-pagina="{pag}"></div>
      <a href="{acervo}" class="cta-lift mt-8 inline-flex items-center gap-2 rounded-full border border-ocean px-5 py-2.5 text-sm font-semibold text-ocean transition hover:bg-ocean hover:text-white"><i class="fa-solid fa-images text-xs"></i>Ver o acervo completo</a>
    </section>
    '''

feitos, problemas = [], []

for nome, (cat, pag, acervo) in PAGINAS.items():
    p = L(nome)
    if not os.path.isfile(p):
        problemas.append((nome, "não existe"))
        continue
    txt = open(p, encoding="utf-8", newline="").read()

    if f'data-secao="carrossel" data-categoria="{cat}" data-pagina="{pag}"' in txt:
        problemas.append((nome, "já tinha as seções"))
        continue
    if CTA not in txt:
        problemas.append((nome, "CTA (bg-mist/70) não encontrado"))
        continue

    txt = txt.replace(CTA, BLOCO.format(cat=cat, pag=pag, acervo=acervo) + CTA, 1)
    open(p, "w", encoding="utf-8", newline="").write(txt)
    feitos.append((nome, cat, pag))

print(f"✅ FASE 4b — seções inseridas em {len(feitos)} páginas:")
for nome, cat, pag in feitos:
    print(f"   • {nome:30} {cat}/{pag}/carrossel + /galeria")
if problemas:
    print(f"\n⚠️  {len(problemas)} sem alteração:")
    for n, m in problemas:
        print(f"   [{n}] {m}")

# ---------- aviso de seção vazia mais amigável ----------
p_js = L("js/main.js")
js = open(p_js, encoding="utf-8", newline="").read()
velho = 'el.innerHTML = `<p class="secao-vazio">Nenhuma imagem publicada nesta secao ainda.</p>`;'
novo = ('el.innerHTML = `<p class="secao-vazio"><i class="fa-solid fa-images" aria-hidden="true"></i> '
        'Ainda não há imagens publicadas nesta seção. Elas aparecem aqui assim que forem enviadas.</p>`;')
if velho in js:
    open(p_js, "w", encoding="utf-8", newline="").write(js.replace(velho, novo, 1))
    print("\n  ✅ js/main.js — aviso de seção vazia mais claro (e com acento correto)")
else:
    print("\n  ⚠️  aviso de seção vazia não casou (talvez já alterado)")
