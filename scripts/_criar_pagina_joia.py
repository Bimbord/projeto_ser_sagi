# -*- coding: utf-8 -*-
"""
Cria joia-da-coroa.html — a página do projeto principal.

Conteúdo 100% do PDF oficial "APRESENTAÇÃO INSTITUTO SER SAGI.pdf"
(páginas 4, 7, 10, 13, 16, 23, 24, 26).

Shell (cabeçalho + menu + rodapé) vem de transparencia.html, igual foi feito
na depoimentos.html.
"""
import os

BASE = r"G:/.shortcut-targets-by-id/18wGiptBKUmAmmkKHgdfu05TU4y_roWC1/BBDPRINT - BACKUP/BBDPRINT/App BBDPRiNT/PROJETOS/Projeto SER Sagi/projeto_SER_Sagi - Hermes"
L = lambda p: os.path.join(BASE, p)  # noqa: E731

tpl = open(L("transparencia.html"), encoding="utf-8", newline="").read()

# ---------- head ----------
tpl = tpl.replace("<title>Transparência | Instituto S.E.R. Sagi</title>",
                  "<title>Jóia da Coroa | Instituto S.E.R. Sagi</title>")
tpl = tpl.replace(
    'content="Área de transparência do Instituto S.E.R. Sagi com organização de relatórios, documentos, parceiros e indicadores institucionais."',
    'content="Jóia da Coroa: o projeto principal do Instituto S.E.R. Sagi — esporte, educação e saúde para 120 crianças de 5 a 13 anos da comunidade do Sagi."')
tpl = tpl.replace('"name": "Transparência"', '"name": "Jóia da Coroa"')

# ---------- hero ----------
ini = tpl.index('<section class="page-banner')
fim = tpl.index("</section>", ini) + len("</section>")
tpl = tpl[:ini] + '''<section class="page-banner text-white relative overflow-hidden banner-alto">
      <!-- CAMADA 1 · IMAGEM de fundo (ilustrativa — trocar por foto real em joia-da-coroa/hero/) -->
      <img src="https://loremflickr.com/1600/600/children,community,brazil?lock=950" alt="" aria-hidden="true" data-secao-img="hero" data-categoria="Jóia da Coroa" class="absolute inset-0 h-full w-full object-cover">
      <!-- CAMADA 2 · SCRIM (véu diagonal, mesmo efeito do hero da home) -->
      <div class="banner-scrim absolute inset-0"></div>
      <div class="relative z-10 mx-auto max-w-7xl px-4 py-16 lg:px-8 lg:py-20">
        <p class="text-sm font-semibold uppercase tracking-[0.25em] text-sun">Projeto principal &bull; Em captação</p>
        <h1 class="mt-4 max-w-4xl text-4xl font-extrabold leading-tight sm:text-5xl lg:text-6xl">Jóia da Coroa</h1>
        <p class="mt-6 max-w-3xl text-lg text-white/90">O coração do Instituto S.E.R. Sagi: esporte, educação e saúde no mesmo lugar, para 120 crianças de 5 a 13 anos da comunidade do Sagi.</p>
      </div>
    </section>''' + tpl[fim:]

# ---------- breadcrumb ----------
ini = tpl.index('<nav class="breadcrumb')
fim = tpl.index("</nav>", ini) + len("</nav>")
tpl = tpl[:ini] + '''<nav class="breadcrumb breadcrumb--claro mx-auto max-w-7xl px-4 lg:px-8" aria-label="Você está aqui">
      <ol>
        <li><a href="./">Início</a></li>
        <li><a href="acoes.html">Nossas Ações</a></li>
        <li><span aria-current="page">Jóia da Coroa</span></li>
      </ol>
    </nav>''' + tpl[fim:]

# ---------- conteúdo ----------
ini = tpl.index('<section class="mx-auto max-w-7xl px-4 py-16 lg:px-8">')
fim = tpl.index("</main>")


def card_modalidade(titulo, desc, href, cat, pag, tema, lock):
    pag_attr = f' data-pagina="{pag}"' if pag else ""
    return f'''<a href="{href}" class="home-card overflow-hidden p-0">
        <div class="relative">
          <img src="https://loremflickr.com/800/500/{tema}?lock={lock}" alt="Imagem ilustrativa — {titulo}" data-secao-img="hero" data-categoria="{cat}"{pag_attr} class="h-40 w-full object-cover" hidden>
        </div>
        <div class="p-6">
          <h3 class="text-lg font-bold text-oceanDeep">{titulo}</h3>
          <p class="mt-2 text-sm leading-7 text-slate-600">{desc}</p>
          <span class="mt-4 inline-flex items-center gap-2 text-sm font-semibold text-ocean">Ver a página <span aria-hidden="true">&rarr;</span></span>
        </div>
      </a>'''


conteudo = f'''<section class="mx-auto max-w-7xl px-4 py-16 lg:px-8">
      <div class="grid gap-10 lg:grid-cols-[1.1fr_0.9fr] lg:items-center">
        <div>
          <p class="text-sm font-semibold uppercase tracking-[0.25em] text-ocean">O que é</p>
          <h2 class="section-title mt-3 text-3xl font-extrabold text-oceanDeep">Um lugar onde tudo acontece junto</h2>
          <p class="mt-6 leading-8 text-slate-600">A Jóia da Coroa reúne, no mesmo espaço, o que a comunidade do Sagi mais precisa: esporte que disciplina, educação que abre portas e saúde que cuida. É a frente que dá sentido às outras — e a que mais precisa de apoio para crescer.</p>
          <blockquote class="mt-8 rounded-2xl border-l-4 border-sun bg-sand/60 p-6">
            <p class="leading-8 text-slate-700">&ldquo;O Instituto S.E.R. Sagi é a <strong>Jóia da Coroa</strong> das ações sociais da ONG S.E.R. SAGI, pois além do Consultório Odontológico, Estúdio de Musculação, Arena de Futevôlei/Vôlei e Escola de Jiu-Jitsu para adultos e crianças da comunidade, pretende oferecer para <strong>120 crianças na faixa etária de 5 a 13 anos</strong>, as atividades esportivas e educacionais do projeto.&rdquo;</p>
            <footer class="mt-4 text-xs font-semibold uppercase tracking-[0.2em] text-ocean">Apresentação oficial do Instituto</footer>
          </blockquote>
        </div>
        <div class="overflow-hidden rounded-[2rem] bg-white p-4 shadow-soft">
          <img src="https://loremflickr.com/800/600/children,kids,learning?lock=951" alt="Imagem ilustrativa do projeto Jóia da Coroa" data-secao-img="imagem principal" data-categoria="Jóia da Coroa" class="h-80 w-full rounded-[1.5rem] object-cover" loading="lazy">
          <div class="mt-3 flex items-center gap-2 px-2 pb-1">
            <span class="inline-flex items-center gap-1.5 rounded-full bg-sand px-2.5 py-1 text-[10px] font-semibold uppercase tracking-[0.15em] text-slate-500"><i class="fa-solid fa-wand-magic-sparkles text-[9px]"></i>Imagem ilustrativa</span>
          </div>
        </div>
      </div>
    </section>

    <section class="bg-mist/70 py-16">
      <div class="mx-auto max-w-7xl px-4 lg:px-8">
        <div class="max-w-3xl">
          <p class="text-sm font-semibold uppercase tracking-[0.25em] text-ocean">O projeto em números</p>
          <h2 class="section-title text-3xl font-extrabold text-oceanDeep">A dimensão da Jóia da Coroa</h2>
        </div>
        <div class="mt-10 grid gap-6 md:grid-cols-2 xl:grid-cols-4">
          <article class="rounded-3xl bg-white p-6 text-center shadow-soft"><p class="text-4xl font-extrabold text-oceanDeep">120</p><p class="mt-2 text-sm font-semibold uppercase tracking-[0.15em] text-ocean">crianças</p><p class="mt-2 text-sm text-slate-600">atendidas pelo projeto</p></article>
          <article class="rounded-3xl bg-white p-6 text-center shadow-soft"><p class="text-4xl font-extrabold text-oceanDeep">5 a 13</p><p class="mt-2 text-sm font-semibold uppercase tracking-[0.15em] text-ocean">anos</p><p class="mt-2 text-sm text-slate-600">faixa etária atendida</p></article>
          <article class="rounded-3xl bg-white p-6 text-center shadow-soft"><p class="text-4xl font-extrabold text-oceanDeep">5</p><p class="mt-2 text-sm font-semibold uppercase tracking-[0.15em] text-ocean">modalidades esportivas</p><p class="mt-2 text-sm text-slate-600">jiu-jitsu, futevôlei, vôlei, natação e dança</p></article>
          <article class="rounded-3xl bg-white p-6 text-center shadow-soft"><p class="text-4xl font-extrabold text-oceanDeep">4</p><p class="mt-2 text-sm font-semibold uppercase tracking-[0.15em] text-ocean">frentes educacionais</p><p class="mt-2 text-sm text-slate-600">inglês, espanhol, informática e sustentabilidade</p></article>
        </div>
      </div>
    </section>

    <section class="mx-auto max-w-7xl px-4 py-16 lg:px-8">
      <div class="max-w-3xl">
        <p class="text-sm font-semibold uppercase tracking-[0.25em] text-ocean">Atividades esportivas</p>
        <h2 class="section-title text-3xl font-extrabold text-oceanDeep">Esporte que forma</h2>
        <p class="mt-6 leading-8 text-slate-600">Disciplina, convivência, saúde e autoestima — o esporte é a porta de entrada de muitas crianças no Instituto.</p>
      </div>
      <div class="mt-10 grid gap-6 md:grid-cols-2 xl:grid-cols-3">
        {card_modalidade("Jiu-jitsu", "A arte suave: espírito de equipe, disciplina, respeito e inclusão social.", "escola-jiu-jitsu.html", "Esporte", "escola-jiu-jitsu", "jiu-jitsu,martial-arts,kids", 1011)}
        {card_modalidade("Futevôlei", "Esporte de areia que nasceu na praia — técnica, parceria e alegria.", "futevolei.html", "Esporte", "futevolei", "beach,football,volleyball", 1012)}
        {card_modalidade("Vôlei", "Trabalho em equipe e coordenação, na quadra e na areia.", "volei.html", "Esporte", "volei", "volleyball,beach,sport", 1013)}
        {card_modalidade("Natação", "Segurança na água e condicionamento, essenciais numa vila de praia.", "natacao.html", "Esporte", "natacao", "swimming,pool,kids", 1014)}
        {card_modalidade("Dança", "Expressão corporal, cultura e autoestima para crianças e adolescentes.", "danca.html", "Esporte", "danca", "dance,kids,class", 1015)}
        {card_modalidade("Arena de Futevôlei e Vôlei", "O espaço que fica vivo o ano inteiro: esporte, eventos e convivência comunitária.", "arena-futevolei-volei.html", "Esporte", "arena-futevolei-volei", "sports,court,beach", 1016)}
      </div>
    </section>

    <section class="bg-mist/70 py-16">
      <div class="mx-auto max-w-7xl px-4 lg:px-8">
        <div class="max-w-3xl">
          <p class="text-sm font-semibold uppercase tracking-[0.25em] text-ocean">Atividades educacionais</p>
          <h2 class="section-title text-3xl font-extrabold text-oceanDeep">Educação que abre portas</h2>
          <p class="mt-6 leading-8 text-slate-600">Idiomas, tecnologia e consciência ambiental — conteúdo que amplia o repertório e as oportunidades das crianças do Sagi.</p>
        </div>
        <div class="mt-10 grid gap-6 md:grid-cols-2 xl:grid-cols-4">
          {card_modalidade("Inglês", "O idioma que conecta o mundo e amplia oportunidades.", "ingles.html", "Educação", "ingles", "english,class,students", 1017)}
          {card_modalidade("Espanhol", "A língua dos nossos vizinhos — comunicação e cultura.", "espanhol.html", "Educação", "espanhol", "spanish,class,students", 1018)}
          {card_modalidade("Informática", "Inclusão digital: ferramentas que abrem caminhos no estudo e no trabalho.", "informatica.html", "Educação", "informatica", "computer,class,kids", 1019)}
          {card_modalidade("Sustentabilidade", "Educação socioambiental: cuidar do mar, da praia e do futuro.", "sustentabilidade.html", "Educação", "sustentabilidade", "environment,kids,plants", 1020)}
        </div>
      </div>
    </section>

    <section class="mx-auto max-w-7xl px-4 py-16 lg:px-8">
      <div class="max-w-3xl">
        <p class="text-sm font-semibold uppercase tracking-[0.25em] text-ocean">Onde acontece</p>
        <h2 class="section-title text-3xl font-extrabold text-oceanDeep">A estrutura que já está de pé</h2>
        <p class="mt-6 leading-8 text-slate-600">A Jóia da Coroa se apoia em espaços que já funcionam e atendem a comunidade o ano inteiro.</p>
      </div>
      <div class="mt-10 grid gap-6 md:grid-cols-2 xl:grid-cols-4">
        <a href="saude.html" class="rounded-3xl bg-white p-6 shadow-soft transition hover:shadow-lg"><p class="text-xs font-semibold uppercase tracking-[0.15em] text-ocean">Saúde</p><h3 class="mt-2 text-lg font-bold text-oceanDeep">Consultório Odontológico</h3><p class="mt-3 text-sm leading-7 text-slate-600"><strong class="text-oceanDeep">194 pacientes</strong> e <strong class="text-oceanDeep">1.149 procedimentos</strong> — de limpeza a próteses.</p></a>
        <a href="estudio-musculacao.html" class="rounded-3xl bg-white p-6 shadow-soft transition hover:shadow-lg"><p class="text-xs font-semibold uppercase tracking-[0.15em] text-ocean">Esporte</p><h3 class="mt-2 text-lg font-bold text-oceanDeep">Estúdio de Musculação</h3><p class="mt-3 text-sm leading-7 text-slate-600"><strong class="text-oceanDeep">118 inscritos</strong> — 89 moradores e 29 residentes.</p></a>
        <a href="arena-futevolei-volei.html" class="rounded-3xl bg-white p-6 shadow-soft transition hover:shadow-lg"><p class="text-xs font-semibold uppercase tracking-[0.15em] text-ocean">Esporte</p><h3 class="mt-2 text-lg font-bold text-oceanDeep">Arena de Futevôlei/Vôlei</h3><p class="mt-3 text-sm leading-7 text-slate-600">Esporte, festas e eventos — um ponto de encontro da comunidade.</p></a>
        <a href="escola-jiu-jitsu.html" class="rounded-3xl bg-white p-6 shadow-soft transition hover:shadow-lg"><p class="text-xs font-semibold uppercase tracking-[0.15em] text-ocean">Esporte</p><h3 class="mt-2 text-lg font-bold text-oceanDeep">Escola de Jiu-Jitsu</h3><p class="mt-3 text-sm leading-7 text-slate-600"><strong class="text-oceanDeep">49 alunos</strong> — disciplina, respeito e autoestima.</p></a>
      </div>
    </section>

    <section class="mx-auto max-w-7xl px-4 pb-16 lg:px-8">
      <div class="flex flex-col gap-3">
        <p class="text-sm font-semibold uppercase tracking-[0.25em] text-ocean">Resultados</p>
        <h3 class="section-title text-3xl font-extrabold text-oceanDeep">Momentos da Jóia da Coroa</h3>
        <p class="max-w-3xl text-slate-600">Registros das atividades do projeto. Deslize para o lado para ver mais.</p>
      </div>
      <div class="mt-8" data-secao="carrossel" data-categoria="Jóia da Coroa"></div>
    </section>
    <section class="mx-auto max-w-7xl px-4 pb-16 lg:px-8">
      <div class="flex flex-col gap-3">
        <p class="text-sm font-semibold uppercase tracking-[0.25em] text-ocean">Galeria</p>
        <h3 class="section-title text-3xl font-extrabold text-oceanDeep">O projeto em imagens</h3>
        <p class="max-w-3xl text-slate-600">Fotos das atividades com as crianças. Clique em uma imagem para ampliar. Os registros abaixo são <strong>ilustrativos</strong> até entrarem as fotos reais.</p>
      </div>
      <div class="mt-8" data-secao="galeria" data-categoria="Jóia da Coroa"></div>
      <a href="acervo.html" class="cta-lift mt-8 inline-flex items-center gap-2 rounded-full border border-ocean px-5 py-2.5 text-sm font-semibold text-ocean transition hover:bg-ocean hover:text-white"><i class="fa-solid fa-images text-xs"></i>Ver o acervo completo</a>
    </section>

    <section class="bg-mist/70 py-16">
      <div class="mx-auto max-w-7xl px-4 lg:px-8">
        <div class="rounded-[2rem] bg-oceanDeep p-8 text-white shadow-soft sm:p-10">
          <p class="text-sm font-semibold uppercase tracking-[0.25em] text-sun">Em captação</p>
          <h2 class="section-title text-3xl font-extrabold">Ajude a Jóia da Coroa a crescer</h2>
          <p class="mt-6 max-w-3xl leading-8 text-white/85">Empresas podem destinar até <strong>2% do imposto devido</strong> (podendo chegar a 3% ou 4% em casos específicos) e pessoas físicas podem aportar até <strong>7% com restituição integral</strong>, pela Lei de Incentivo ao Esporte (Lei nº 11.438/2006). Também é possível apoiar como voluntário, doador ou parceiro.</p>
          <div class="mt-8 flex flex-wrap gap-4">
            <a href="lei-incentivo.html" class="cta-lift rounded-full bg-sun px-6 py-3 font-semibold text-oceanDeep">Apoiar via Lei de Incentivo</a>
            <a href="como-ajudar.html" class="cta-lift rounded-full border border-white/40 px-6 py-3 font-semibold text-white">Ver outras formas de ajudar</a>
          </div>
        </div>
      </div>
    </section>
  '''
tpl = tpl[:ini] + conteudo + tpl[fim:]

open(L("joia-da-coroa.html"), "w", encoding="utf-8", newline="").write(tpl)
print("  ✅ joia-da-coroa.html criado")
sc = tpl.count('data-secao="carrossel"')
sg = tpl.count('data-secao="galeria"')
print("     linhas: " + str(tpl.count(chr(10)) + 1))
print("     seções com mídia: carrossel=" + str(sc) + " galeria=" + str(sg))
print("     links internos: " + str(tpl.count(".html")))
print("     marcador card_modalidade sobrando: " + str(tpl.count("card_modalidade")))
