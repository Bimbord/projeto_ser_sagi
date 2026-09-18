# -*- coding: utf-8 -*-
"""
Liga os cards de PARCEIROS da home à pasta home/parceiros (última lacuna da Fase 5).

O texto vem da tabela `parceiros`; a LOGOMARCA vem da pasta, casada pelo NOME
(mesma regra dos depoimentos):  nome = "Grupo Atlântico" -> home/parceiros/grupo-atlantico.jpg

Sem logo publicada, o card continua mostrando as iniciais (logo_texto) — nada quebra.
"""
import os

BASE = r"G:/.shortcut-targets-by-id/18wGiptBKUmAmmkKHgdfu05TU4y_roWC1/BBDPRINT - BACKUP/BBDPRINT/App BBDPRiNT/PROJETOS/Projeto SER Sagi/projeto_SER_Sagi - Hermes"
L = lambda p: os.path.join(BASE, p)  # noqa: E731

# ---------- 1. CSS ----------
p_css = L("css/style.css")
css = open(p_css, encoding="utf-8", newline="").read()
if ".home-partner__logo img" in css:
    print("  ⚠️  CSS já tinha .home-partner__logo img — pulando")
else:
    css += """

/* ============================================================
   LOGOMARCA DE PARCEIRO (pasta home/parceiros, casada pelo nome)
   Sem logo publicada, o card mostra as iniciais (logo_texto).
   ============================================================ */
.home-partner__logo img {
  display: block;
  max-width: 100%;
  max-height: 100%;
  width: auto;
  height: auto;
  object-fit: contain;
  filter: grayscale(1);
  opacity: .75;
  transition: filter .25s ease, opacity .25s ease;
}
.home-partner:hover .home-partner__logo img { filter: grayscale(0); opacity: 1; }
"""
    open(p_css, "w", encoding="utf-8", newline="").write(css)
    print("  ✅ css/style.css — estilo da logomarca")

# ---------- 2. JS ----------
p_js = L("js/main.js")
js = open(p_js, encoding="utf-8", newline="").read()

if "renderPartners(items, midias)" in js:
    print("  ⚠️  main.js já estava alterado — pulando")
else:
    ini = js.index("function renderPartners(items) {")
    fim = js.index("\nfunction renderGallery(")

    novo = '''function renderPartners(items, midias) {
  const container = document.querySelector('[data-render="partners"]');
  if (!container) return;

  const fallback = [
    { nome: 'Grupo Atlântico', categoria: 'Empresa apoiadora', logo_texto: 'GA', descricao: 'Apoio institucional à transformação social na comunidade.' },
    { nome: 'Instituto Horizonte', categoria: 'Parceiro institucional', logo_texto: 'IH', descricao: 'Parceiro de articulação social e comunitária.' },
    { nome: 'Onda Verde', categoria: 'Patrocinador', logo_texto: 'OV', descricao: 'Patrocínio de projetos esportivos e ambientais.' },
    { nome: 'Rede Potiguar', categoria: 'Apoiador local', logo_texto: 'RP', descricao: 'Apoiador local com foco em impacto territorial.' }
  ];

  const data = (items || []).length ? items : fallback;
  container.innerHTML = data.map((item) => {
    // logo: URL do banco > pasta home/parceiros (casada pelo nome) > iniciais
    const pelaPasta = (midias || {})[normalizarChave(item.nome)];
    const logo = item.logo_url || (pelaPasta && pelaPasta.imagem) || '';
    const dentro = logo
      ? `<img src="${escaparHtml(logo)}" alt="${escaparHtml(item.nome || 'Parceiro')}" loading="lazy">`
      : escaparHtml(item.logo_texto || 'MK');
    return `
    <article class="home-card home-partner" title="${escaparHtml(item.descricao || '')}">
      <span class="home-partner__logo" aria-hidden="true">${dentro}</span>
      <span class="home-partner__name">${escaparHtml(item.nome || '')}</span>
      <span class="home-partner__cat">${escaparHtml(item.categoria || '')}</span>
    </article>
  `;
  }).join('');
}

'''
    js = js[:ini] + novo + js[fim + 1:]

    # loadDynamicSections: busca também a mídia dos parceiros
    velho = """      fetchMidiasDepoimentos().catch(() => ({}))
    ]);"""
    novo2 = """      fetchMidiasDepoimentos().catch(() => ({})),
      fetchMidiasParceiros().catch(() => ({}))
    ]);"""
    if velho in js:
        js = js.replace(velho, novo2, 1)
        js = js.replace("    const [depoimentos, parceiros, galeria, midiasDep] = await Promise.all([",
                        "    const [depoimentos, parceiros, galeria, midiasDep, midiasPar] = await Promise.all([", 1)
        js = js.replace("    renderPartners((parceiros.data || []).filter((item) => !item.deleted));",
                        "    renderPartners((parceiros.data || []).filter((item) => !item.deleted), midiasPar);", 1)
        js = js.replace("    renderPartners([]);", "    renderPartners([], {});", 1)
        print("  ✅ js/main.js — renderPartners usa a pasta + loadDynamicSections busca a mídia")
    else:
        print("  ⚠️  não casou o ponto do Promise.all — conferir")

    # função que busca a pasta home/parceiros
    ancora = "async function fetchMidiasDepoimentos() {"
    helper = '''// Logomarcas de parceiros publicadas da pasta home/parceiros do Drive.
// Mesma regra dos depoimentos: o NOME do arquivo casa com o campo `nome`.
async function fetchMidiasParceiros() {
  const itens = await fetchSecao('Home', 'parceiros');
  const mapa = {};
  for (const i of itens) {
    const k = normalizarChave(i.titulo);
    if (k && !mapa[k]) mapa[k] = { imagem: i.imagem_url || i.video_url, legenda: i.descricao || '' };
  }
  return mapa;
}

'''
    if ancora in js:
        js = js.replace(ancora, helper + ancora, 1)
    else:
        print("  ⚠️  não achei fetchMidiasDepoimentos para ancorar")

    open(p_js, "w", encoding="utf-8", newline="").write(js)
