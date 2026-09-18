# -*- coding: utf-8 -*-
"""
FASE 5 · Parte C (1/2) — card de depoimento com mídia + legenda.

  - css/style.css : estilos da mídia do depoimento
  - js/main.js    : renderTestimonials reescrito (mensagem + imagem/vídeo +
                    legenda + autor), mídia casada pelo NOME (home/depoimentos)

A mídia pode vir de:
  1. imagem_url / video_url do banco (URL externa — tem prioridade)
  2. pasta home/depoimentos do Drive, casada pelo nome ("ana-paula.jpg")
"""
import os

BASE = r"G:/.shortcut-targets-by-id/18wGiptBKUmAmmkKHgdfu05TU4y_roWC1/BBDPRINT - BACKUP/BBDPRINT/App BBDPRiNT/PROJETOS/Projeto SER Sagi/projeto_SER_Sagi - Hermes"

# ============================================================
# 1. CSS
# ============================================================
p_css = os.path.join(BASE, "css", "style.css")
css = open(p_css, encoding="utf-8").read()

if ".home-quote__midia" in css:
    print("  ⚠️  CSS ja tinha .home-quote__midia — pulando")
else:
    css += """

/* ============================================================
   DEPOIMENTOS COM MÍDIA — mensagem + imagem/vídeo + legenda
   (pasta home/depoimentos do Drive, casada pelo nome)
   ============================================================ */
.home-quote__midia {
  position: relative;
  margin: -1.5rem -1.5rem 0;
  border-radius: var(--radius-lg) var(--radius-lg) 0 0;
  overflow: hidden;
  background: var(--mist);
}
.home-quote__midia img,
.home-quote__midia video {
  display: block;
  width: 100%;
  aspect-ratio: 16 / 10;
  object-fit: cover;
}
.home-quote__midia--vazia { width: 100%; aspect-ratio: 16 / 10; background: linear-gradient(135deg, var(--ocean-deep), var(--ocean)); }
.home-quote__selo {
  position: absolute;
  top: 0.625rem;
  left: 0.625rem;
  z-index: 2;
  padding: 0.25rem 0.6rem;
  border-radius: 999px;
  background: rgba(8, 59, 76, 0.86);
  color: #fff;
  font-size: 0.625rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}
.home-quote__play {
  position: absolute;
  inset: 0;
  z-index: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(0deg, rgba(8, 59, 76, 0.38), rgba(8, 59, 76, 0.05));
  text-decoration: none;
}
.home-quote__play span {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 3.25rem;
  height: 3.25rem;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.94);
  color: var(--ocean);
  font-size: 1.15rem;
  box-shadow: 0 6px 16px rgba(8, 59, 76, 0.28);
}
.home-quote__legenda {
  margin: 0.75rem 0 0;
  font-size: 0.72rem;
  font-style: italic;
  line-height: 1.5;
  color: #64748b;
}
.home-quote__corpo {
  display: flex;
  flex-direction: column;
  flex: 1;
  margin-top: 1rem;
}
.home-quote__avatar--foto { object-fit: cover; }
"""
    open(p_css, "w", encoding="utf-8", newline="").write(css)
    print("  ✅ css/style.css — estilos da mídia do depoimento")

# ============================================================
# 2. JS — renderTestimonials reescrito
# ============================================================
p_js = os.path.join(BASE, "js", "main.js")
js = open(p_js, encoding="utf-8").read()

if "markupDepoimento" in js:
    print("  ⚠️  main.js ja tinha markupDepoimento — pulando")
else:
    ini = js.index("function renderTestimonials(items) {")
    fim = js.index("\nfunction renderPartners(")

    novo = '''function escaparHtml(texto) {
  return (texto || '').toString()
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

// Monta UM depoimento: mídia (foto/vídeo) + legenda + mensagem + autor.
// `midia` vem da pasta home/depoimentos, casada pelo nome.
function markupDepoimento(item, midia) {
  const m = midia || {};
  const imagem = item.imagem_url || m.imagem || '';
  const video = item.video_url || m.video || '';
  const legenda = item.legenda || m.legenda || '';
  const ehArquivoVideo = /\\.(mp4|webm|mov|m4v)(\\?|$)/i.test(video);
  const nome = escaparHtml(item.nome || '');
  const inicial = (item.nome || 'S').trim().charAt(0).toUpperCase();
  const papel = escaparHtml([item.perfil, item.local || 'Comunidade Sagi'].filter(Boolean).join(' · '));

  let midiaHtml = '';
  if (imagem || video) {
    let dentro = '';
    if (imagem) {
      dentro += '<img src="' + escaparHtml(imagem) + '" alt="' + escaparHtml(legenda || item.nome || 'Depoimento') + '" loading="lazy">';
      if (video) {
        dentro += '<a class="home-quote__play" href="' + escaparHtml(video) + '" target="_blank" rel="noopener" aria-label="Assistir ao depoimento"><span><i class="fa-solid fa-play"></i></span></a>';
      }
    } else if (ehArquivoVideo) {
      dentro += '<video src="' + escaparHtml(video) + '" controls preload="metadata" playsinline></video>';
    } else {
      dentro += '<div class="home-quote__midia--vazia"></div>'
        + '<a class="home-quote__play" href="' + escaparHtml(video) + '" target="_blank" rel="noopener" aria-label="Assistir ao depoimento"><span><i class="fa-solid fa-play"></i></span></a>';
    }
    midiaHtml = '<div class="home-quote__midia">' + dentro
      + '<span class="home-quote__selo">' + (video ? 'Vídeo' : 'Foto') + '</span></div>'
      + (legenda ? '<p class="home-quote__legenda">' + escaparHtml(legenda) + '</p>' : '');
  }

  return `
    <article class="home-card home-quote">
      ${midiaHtml}
      <div class="home-quote__corpo">
        <span class="home-quote__mark" aria-hidden="true">&ldquo;</span>
        <p class="home-card__text">${escaparHtml(item.texto)}</p>
        <footer class="home-quote__footer">
          <span class="home-quote__avatar">${escaparHtml(inicial)}</span>
          <span>
            <strong class="home-quote__name">${nome}</strong>
            <span class="home-quote__role">${papel}</span>
          </span>
        </footer>
      </div>
    </article>
  `;
}

function renderTestimonials(items, midias) {
  const container = document.querySelector('[data-render="testimonials"]');
  if (!container) return;

  const fallback = [
    { nome: 'Ana Paula', perfil: 'Mãe', titulo: 'Meu filho ganhou disciplina', texto: 'Desde que começou nas atividades do Instituto, meu filho está mais motivado, mais disciplinado e mais feliz.', local: 'Praia do Sagi' },
    { nome: 'João Miguel', perfil: 'Criança', titulo: 'Eu gosto de aprender e brincar', texto: 'Eu gosto muito do jiu-jitsu e quero participar também das aulas de informática e inglês.', local: 'Projeto infantil' },
    { nome: 'Carlos Henrique', perfil: 'Pai', titulo: 'A comunidade sente a diferença', texto: 'O Instituto trouxe oportunidade de verdade para as crianças e mais esperança para as famílias.', local: 'Baía Formosa/RN' }
  ];

  // [data-limite="3"] mostra so os 3 em destaque (home); sem limite, mostra todos
  const limite = parseInt(container.getAttribute('data-limite') || '0', 10);
  let data = (items || []).slice().sort((a, b) => (a.ordem || 0) - (b.ordem || 0));

  if (limite > 0) {
    const destaques = data.filter((i) => i.destaque);
    data = (destaques.length ? destaques : data).slice(0, limite);
  }
  const usandoFallback = !data.length;
  if (usandoFallback) data = fallback;

  container.innerHTML = data.map((item) => {
    const chave = normalizarChave(item.nome);
    const midia = (midias || {})[chave];
    return markupDepoimento(item, midia);
  }).join('');

  container.setAttribute('data-ilustrativo', usandoFallback ? 'true' : 'false');
}

'''
    js = js[:ini] + novo + js[fim + 1:]

    # loadDynamicSections: busca tambem a midia dos depoimentos
    velho = """    const [depoimentos, parceiros, galeria] = await Promise.all([
      fetchTableData('depoimentos').catch(() => ({ data: [] })),
      fetchTableData('parceiros').catch(() => ({ data: [] })),
      fetchTableData('galeria').catch(() => ({ data: [] }))
    ]);

    renderTestimonials((depoimentos.data || []).filter((item) => !item.deleted));
    renderPartners((parceiros.data || []).filter((item) => !item.deleted));
    renderGallery((galeria.data || []).filter((item) => !item.deleted));
  } catch (error) {
    renderTestimonials([]);
    renderPartners([]);
    renderGallery([]);
  }"""
    novo2 = """    const [depoimentos, parceiros, galeria, midiasDep] = await Promise.all([
      fetchTableData('depoimentos').catch(() => ({ data: [] })),
      fetchTableData('parceiros').catch(() => ({ data: [] })),
      fetchTableData('galeria').catch(() => ({ data: [] })),
      fetchMidiasDepoimentos().catch(() => ({}))
    ]);

    renderTestimonials((depoimentos.data || []).filter((item) => !item.deleted), midiasDep);
    renderPartners((parceiros.data || []).filter((item) => !item.deleted));
    renderGallery((galeria.data || []).filter((item) => !item.deleted));
  } catch (error) {
    renderTestimonials([], {});
    renderPartners([]);
    renderGallery([]);
  }"""
    if velho not in js:
        raise SystemExit("❌ nao achei loadDynamicSections")
    js = js.replace(velho, novo2, 1)

    # busca a midia da pasta home/depoimentos e monta o mapa por chave
    ancora = "async function fetchSecao(categoria, secao) {"
    helper = '''// Mídia dos depoimentos publicada da pasta home/depoimentos do Drive.
// Devolve { "ana-paula": { imagem: url, video: url, legenda: titulo } }.
// O casamento é pelo NOME do arquivo (mesma regra dos blocos da home).
async function fetchMidiasDepoimentos() {
  const itens = await fetchSecao('Home', 'depoimentos');
  const mapa = {};
  for (const i of itens) {
    const k = normalizarChave(i.titulo);
    if (!k) continue;
    if (!mapa[k]) mapa[k] = {};
    if (i.tipo === 'video' || (i.video_url && !i.imagem_url)) {
      mapa[k].video = i.video_url || i.imagem_url;
    } else {
      mapa[k].imagem = i.imagem_url || i.video_url;
    }
    if (!mapa[k].legenda && i.descricao) mapa[k].legenda = i.descricao;
  }
  return mapa;
}

'''
    if ancora not in js:
        raise SystemExit("❌ nao achei fetchSecao")
    js = js.replace(ancora, helper + ancora, 1)

    open(p_js, "w", encoding="utf-8", newline="").write(js)
    print("  ✅ js/main.js — markupDepoimento + renderTestimonials + fetchMidiasDepoimentos")
