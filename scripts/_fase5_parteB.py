# -*- coding: utf-8 -*-
"""
FASE 5 · Parte B — fotos nos blocos de itens fixos da home.

  home/pilares      (5) -> foto no TOPO do card de pilar
  home/numeros      (6) -> foto CIRCULAR acima do rótulo
  home/como-ajudar  (3) -> foto no TOPO do card

O NOME DO ARQUIVO é a chave (decisão 1-A). A chave é normalizada:
  minúscula, sem acento, com hífen.  Ex.: "Jiu-jitsu.jpg" -> "jiu-jitsu"

Sem foto publicada, a <img> fica com [hidden] e o card continua como está.
"""
import os
import re

BASE = r"G:/.shortcut-targets-by-id/18wGiptBKUmAmmkKHgdfu05TU4y_roWC1/BBDPRINT - BACKUP/BBDPRINT/App BBDPRiNT/PROJETOS/Projeto SER Sagi/projeto_SER_Sagi - Hermes"


def chave(texto):
    """Mesma normalizacao do js/main.js."""
    import unicodedata
    t = unicodedata.normalize("NFD", (texto or "").lower())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    t = re.sub(r"[^a-z0-9]+", "-", t)
    return t.strip("-")


IMG = ('<img class="{cls}" data-categoria="Home" data-secao-img="{bloco}" '
       'data-secao-chave="{chave}" alt="" hidden>')

# ---------- 1. CSS ----------
p_css = os.path.join(BASE, "css", "style.css")
css = open(p_css, encoding="utf-8").read()
if ".home-foto" in css:
    print("  ⚠️  CSS ja tinha .home-foto — pulando")
else:
    css += """

/* ============================================================
   FASE 5 · Fotos dos blocos da home
   (pastas home/pilares, home/numeros e home/como-ajudar)
   Sem foto publicada a <img> fica com [hidden] e o card
   continua exatamente como era antes.
   ============================================================ */
.home-foto {
  display: block;
  width: 100%;
  aspect-ratio: 16 / 10;
  object-fit: cover;
  border-radius: var(--radius-sm);
  margin-bottom: 1.25rem;
}
.home-foto[hidden] { display: none; }

.home-stat__foto {
  display: block;
  width: 3rem;
  height: 3rem;
  border-radius: 9999px;
  object-fit: cover;
  margin-bottom: 0.75rem;
}
.home-stat__foto[hidden] { display: none; }
"""
    open(p_css, "w", encoding="utf-8", newline="").write(css)
    print("  ✅ css/style.css — .home-foto e .home-stat__foto")

# ---------- 2. HTML ----------
p_idx = os.path.join(BASE, "index.html")
html = open(p_idx, encoding="utf-8").read()
antes = html
contagem = {}

# 2a. PILARES — insere a foto logo apos a abertura do <a class="home-card home-pillar">
def add_pilar(m):
    titulo = m.group(2)
    k = chave(titulo)
    contagem.setdefault("pilares", []).append(k)
    return m.group(0).replace(m.group(1), m.group(1) + IMG.format(cls="home-foto", bloco="pilares", chave=k), 1)

html = re.sub(
    r'(<a href="[^"]*" class="home-card home-pillar">)(.*?<h3 class="home-card__title">([^<]+)</h3>)',
    lambda m: m.group(1) + IMG.format(cls="home-foto", bloco="pilares", chave=chave(m.group(3))) + m.group(2),
    html, flags=re.DOTALL)

# 2b. NUMEROS — insere a foto circular antes do <dt>
html = re.sub(
    r'(<div class="home-stat">\s*)(<dt class="home-stat__label">([^<]+)</dt>)',
    lambda m: m.group(1) + IMG.format(cls="home-stat__foto", bloco="numeros", chave=chave(m.group(3))) + "\n            " + m.group(2),
    html)

# 2c. COMO AJUDAR — insere a foto logo apos a abertura do <article>
html = re.sub(
    r'(<article class="home-card text-center">)(.*?<h3[^>]*>([^<]+)</h3>)',
    lambda m: m.group(1) + IMG.format(cls="home-foto", bloco="como-ajudar", chave=chave(m.group(3))) + m.group(2),
    html, flags=re.DOTALL)

if html != antes:
    open(p_idx, "w", encoding="utf-8", newline="").write(html)

# conta o que entrou
for bloco in ("pilares", "numeros", "como-ajudar"):
    n = len(re.findall(r'data-secao-img="%s"' % re.escape(bloco), html))
    chaves = re.findall(r'data-secao-img="%s" data-secao-chave="([^"]+)"' % re.escape(bloco), html)
    print(f"  ✅ {bloco:12} {n} card(s) → chaves: {', '.join(chaves)}")

# ---------- 3. JS ----------
p_js = os.path.join(BASE, "js", "main.js")
js = open(p_js, encoding="utf-8").read()
if "normalizarChave" in js:
    print("  ⚠️  main.js ja tinha normalizarChave — pulando")
else:
    velho = """  // Imagens unicas (hero / imagem principal)
  const imagens = document.querySelectorAll('[data-secao-img]');
  for (const img of imagens) {
    const pagina = img.getAttribute('data-pagina');
    const secao = pagina ? `${pagina}/${img.getAttribute('data-secao-img')}` : img.getAttribute('data-secao-img');
    const categoria = img.getAttribute('data-categoria') || '';
    try {
      const itens = (await fetchSecao(categoria, secao)).filter((i) => i.imagem_url);
      if (itens.length) {
        img.src = itens[0].imagem_url;
        if (itens[0].titulo) img.alt = itens[0].titulo;
      }
    } catch (error) { /* mantem a imagem padrao do HTML */ }
  }"""
    novo = """  // Imagens unicas (hero / imagem principal)
  // Com [data-secao-chave], escolhe a foto cujo NOME DE ARQUIVO casa com a
  // chave (blocos de itens fixos da home: pilares, numeros, como-ajudar).
  const imagens = document.querySelectorAll('[data-secao-img]');
  for (const img of imagens) {
    const pagina = img.getAttribute('data-pagina');
    const secao = pagina ? `${pagina}/${img.getAttribute('data-secao-img')}` : img.getAttribute('data-secao-img');
    const categoria = img.getAttribute('data-categoria') || '';
    const chaveAlvo = img.getAttribute('data-secao-chave');
    try {
      let itens = (await fetchSecao(categoria, secao)).filter((i) => i.imagem_url);
      if (chaveAlvo) {
        itens = itens.filter((i) => normalizarChave(i.titulo) === normalizarChave(chaveAlvo));
      }
      if (itens.length) {
        img.src = itens[0].imagem_url;
        if (itens[0].titulo) img.alt = itens[0].titulo;
        img.hidden = false;
      }
    } catch (error) { /* mantem a imagem padrao do HTML */ }
  }"""
    if velho not in js:
        raise SystemExit("❌ nao achei o bloco de imagens unicas no main.js")
    js = js.replace(velho, novo, 1)

    # funcao de normalizacao (mesma regra do Python)
    ancora = "async function fetchSecao(categoria, secao) {"
    helper = """// Normaliza texto para casar nome de arquivo com chave: minusculo, sem
// acento, com hifen. "Jiu-jitsu.jpg" (titulo "Jiu Jitsu") -> "jiu-jitsu"
function normalizarChave(texto) {
  return (texto || '').toString().toLowerCase()
    .normalize('NFD').replace(/[\\u0300-\\u036f]/g, '')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '');
}

"""
    js = js.replace(ancora, helper + ancora, 1)
    open(p_js, "w", encoding="utf-8", newline="").write(js)
    print("  ✅ js/main.js — data-secao-chave + normalizarChave()")
