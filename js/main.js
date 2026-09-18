function setupMobileMenu() {
  const menuToggle = document.getElementById('menu-toggle');
  const mobileMenu = document.getElementById('mobile-menu');
  if (!menuToggle || !mobileMenu) return;

  menuToggle.addEventListener('click', () => {
    const expanded = menuToggle.getAttribute('aria-expanded') === 'true';
    menuToggle.setAttribute('aria-expanded', String(!expanded));
    mobileMenu.classList.toggle('hidden');
  });

  mobileMenu.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => {
      mobileMenu.classList.add('hidden');
      menuToggle.setAttribute('aria-expanded', 'false');
    });
  });
}

function setupActiveLinks() {
  const current = window.location.pathname.split('/').pop() || 'index.html';
  // Sub-páginas de "Nossas Ações" (pages individuais de cada ação)
  const acoesSub = ['saude.html', 'estudio-musculacao.html', 'escola-jiu-jitsu.html', 'arena-futevolei-volei.html', 'acoes-solidarias.html', 'preservacao-ambiental.html', 'esporte.html', 'educacao.html', 'cultura.html', 'volei.html', 'futevolei.html', 'natacao.html', 'danca.html', 'ingles.html', 'espanhol.html', 'informatica.html', 'sustentabilidade.html'];
  // Sub-páginas de "Acervo" (páginas por categoria)
  const acervoSub = ['acervo-esporte.html', 'acervo-saude.html', 'acervo-educacao.html', 'acervo-cultura.html', 'acervo-preservacao.html', 'acervo-eventos.html'];
  // Sub-páginas de "Quem Somos" (instalações)
  const quemSomosSub = ['instalacoes.html'];
  let target = current;
  if (acoesSub.includes(current)) target = 'acoes.html';
  else if (acervoSub.includes(current)) target = 'acervo.html';
  else if (quemSomosSub.includes(current)) target = 'quem-somos.html';
  document.querySelectorAll('[data-page-link]').forEach((link) => {
    const href = link.getAttribute('href');
    // o link do Início aponta para a raiz ("./") para a URL não mostrar "index.html"
    const destino = href === './' ? 'index.html' : href;
    if (destino === target) link.classList.add('active');
  });
}

// ============================================================
// Conexão com o Supabase (banco do site — projeto sersagi-site)
// A anon key é pública de propósito (padrão Supabase — vai no
// código do cliente); a proteção dos dados é feita pelas
// políticas RLS criadas no SQL Editor.
// ============================================================
const SUPABASE_URL = 'https://icrasqxbxmqbnelmkrei.supabase.co';
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImljcmFzcXhieG1xYm5lbG1rcmVpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODgyMDYzOTUsImV4cCI6MjEwMzc4MjM5NX0.u7cWsqTRWIvJJ-jsU7BbcOw1cVI-Su8eJBL_pBaQb_g';

async function fetchTableData(tableName, options = {}) {
  const { limit = 50, sort = 'created_at' } = options;
  const url = `${SUPABASE_URL}/rest/v1/${tableName}?select=*&order=${sort}.desc&limit=${limit}`;
  const response = await fetch(url, {
    headers: {
      apikey: SUPABASE_ANON_KEY,
      Authorization: `Bearer ${SUPABASE_ANON_KEY}`
    }
  });
  if (!response.ok) throw new Error(`Erro ao buscar ${tableName}`);
  const data = await response.json();
  return { data };
}

async function submitToTable(tableName, payload) {
  const response = await fetch(`${SUPABASE_URL}/rest/v1/${tableName}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      apikey: SUPABASE_ANON_KEY,
      Authorization: `Bearer ${SUPABASE_ANON_KEY}`
    },
    body: JSON.stringify(payload)
  });

  if (!response.ok) {
    throw new Error(`Erro ao enviar formulário para ${tableName}`);
  }

  return response.json();
}

function setFeedback(element, message, type) {
  if (!element) return;
  element.classList.remove('hidden', 'success', 'error');
  element.classList.add(type);
  element.textContent = message;
}

function getFormData(form) {
  const formData = new FormData(form);
  return Object.fromEntries(formData.entries());
}

function normalizeCheckbox(value) {
  return value === 'on' || value === true || value === 'true';
}

function setupLeadForms() {
  document.querySelectorAll('[data-form-type="lead"]').forEach((form) => {
    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      const feedback = form.querySelector('.form-feedback');
      const button = form.querySelector('button[type="submit"]');
      const data = getFormData(form);

      const payload = {
        nome: data.nome || '',
        empresa: data.empresa || '',
        email: data.email || '',
        telefone: data.telefone || '',
        perfil: data.perfil || 'Pessoa física',
        interesse: data.interesse || 'Outro',
        mensagem: data.mensagem || '',
        origem_pagina: data.origem_pagina || window.location.pathname,
        aceite_privacidade: normalizeCheckbox(data.aceite_privacidade)
      };

      if (!payload.nome || !payload.email || !payload.mensagem || !payload.aceite_privacidade) {
        setFeedback(feedback, 'Preencha os campos obrigatórios e aceite a política de privacidade.', 'error');
        return;
      }

      try {
        if (button) button.disabled = true;
        await submitToTable('leads_apoio', payload);
        form.reset();
        setFeedback(feedback, 'Interesse enviado com sucesso. Nossa equipe entrará em contato em breve.', 'success');
      } catch (error) {
        setFeedback(feedback, 'Não foi possível enviar agora. Tente novamente em instantes.', 'error');
      } finally {
        if (button) button.disabled = false;
      }
    });
  });
}

function setupContactForms() {
  document.querySelectorAll('[data-form-type="contact"]').forEach((form) => {
    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      const feedback = form.querySelector('.form-feedback');
      const button = form.querySelector('button[type="submit"]');
      const data = getFormData(form);

      const payload = {
        nome: data.nome || '',
        email: data.email || '',
        telefone: data.telefone || '',
        assunto: data.assunto || 'Contato institucional',
        mensagem: data.mensagem || '',
        origem_pagina: data.origem_pagina || window.location.pathname,
        aceite_privacidade: normalizeCheckbox(data.aceite_privacidade)
      };

      if (!payload.nome || !payload.email || !payload.mensagem || !payload.aceite_privacidade) {
        setFeedback(feedback, 'Preencha nome, e-mail, mensagem e aceite a política de privacidade.', 'error');
        return;
      }

      try {
        if (button) button.disabled = true;
        await submitToTable('contatos', payload);
        form.reset();
        setFeedback(feedback, 'Mensagem enviada com sucesso. Obrigado pelo contato!', 'success');
      } catch (error) {
        setFeedback(feedback, 'Não foi possível enviar sua mensagem agora. Tente novamente.', 'error');
      } finally {
        if (button) button.disabled = false;
      }
    });
  });
}

function setupNewsletterForms() {
  document.querySelectorAll('[data-form-type="newsletter"]').forEach((form) => {
    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      const feedback = form.querySelector('.form-feedback');
      const button = form.querySelector('button[type="submit"]');
      const data = getFormData(form);

      const payload = {
        nome: data.nome || '',
        email: data.email || '',
        perfil: data.perfil || 'Apoiador',
        aceite_comunicacao: normalizeCheckbox(data.aceite_comunicacao)
      };

      if (!payload.email || !payload.aceite_comunicacao) {
        setFeedback(feedback, 'Informe um e-mail válido e autorize o recebimento de comunicações.', 'error');
        return;
      }

      try {
        if (button) button.disabled = true;
        await submitToTable('newsletter', payload);
        form.reset();
        setFeedback(feedback, 'Cadastro realizado com sucesso na newsletter.', 'success');
      } catch (error) {
        setFeedback(feedback, 'Não foi possível concluir o cadastro agora.', 'error');
      } finally {
        if (button) button.disabled = false;
      }
    });
  });
}

function escaparHtml(texto) {
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
  const ehArquivoVideo = /\.(mp4|webm|mov|m4v)(\?|$)/i.test(video);
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
  document.querySelectorAll('[data-badge-depoimentos]').forEach((el) => {
    el.hidden = !usandoFallback;
  });
}

function renderPartners(items, midias) {
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

function renderGallery(items) {
  const container = document.querySelector('[data-render="gallery"]');
  if (!container) return;

  const fallback = [
    { titulo: 'Aula de jiu-jitsu', categoria: 'Esporte', descricao: 'Espaço reservado para foto real das atividades esportivas.', imagem_url: '' },
    { titulo: 'Atendimento odontológico', categoria: 'Saúde', descricao: 'Espaço reservado para registro do consultório e atendimentos.', imagem_url: '' },
    { titulo: 'Atividades educativas', categoria: 'Educação', descricao: 'Espaço reservado para informática, idiomas e sustentabilidade.', imagem_url: '' },
    { titulo: 'Comunidade e convivência', categoria: 'Comunidade', descricao: 'Espaço reservado para ações solidárias e encontros comunitários.', imagem_url: '' },
    { titulo: 'Preservação ambiental', categoria: 'Ambiental', descricao: 'Espaço reservado para tartarugas, praia e educação ambiental.', imagem_url: '' },
    { titulo: 'Eventos institucionais', categoria: 'Evento', descricao: 'Espaço reservado para campanhas, celebrações e datas especiais.', imagem_url: '' }
  ];

  const data = items.length ? items : fallback;
  container.innerHTML = data.map((item) => {
    const imageMarkup = item.imagem_url
      ? `<img src="${item.imagem_url}" alt="${item.titulo || 'Imagem da galeria'}" class="h-56 w-full rounded-3xl object-cover" />`
      : `<div class="flex h-56 w-full items-center justify-center rounded-3xl bg-gradient-to-br from-mist to-sand text-center text-sm font-semibold text-oceanDeep">Imagem institucional<br/>em breve</div>`;

    return `
      <article class="overflow-hidden rounded-3xl bg-white p-4 shadow-soft">
        ${imageMarkup}
        <div class="p-2 pt-4">
          <p class="text-xs font-semibold uppercase tracking-[0.2em] text-ocean">${item.categoria || ''}</p>
          <h3 class="mt-2 text-lg font-bold text-oceanDeep">${item.titulo || ''}</h3>
          <p class="mt-2 text-sm leading-7 text-slate-600">${item.descricao || ''}</p>
        </div>
      </article>
    `;
  }).join('');
}

async function loadDynamicSections() {
  try {
    const [depoimentos, parceiros, galeria, midiasDep, midiasPar] = await Promise.all([
      fetchTableData('depoimentos').catch(() => ({ data: [] })),
      fetchTableData('parceiros').catch(() => ({ data: [] })),
      fetchTableData('galeria').catch(() => ({ data: [] })),
      fetchMidiasDepoimentos().catch(() => ({})),
      fetchMidiasParceiros().catch(() => ({}))
    ]);

    renderTestimonials((depoimentos.data || []).filter((item) => !item.deleted), midiasDep);
    renderPartners((parceiros.data || []).filter((item) => !item.deleted), midiasPar);
    renderGallery((galeria.data || []).filter((item) => !item.deleted));
  } catch (error) {
    renderTestimonials([], {});
    renderPartners([], {});
    renderGallery([]);
  }
}

function archiveItemMarkup(item) {
  const tipo = item.tipo === 'video' ? 'video' : 'foto';
  const imagem = item.imagem_url
    ? `<img src="${item.imagem_url}" alt="${item.titulo || 'Registro do Instituto'}" class="h-56 w-full object-cover" loading="lazy" />`
    : `<div class="flex h-56 w-full items-center justify-center bg-gradient-to-br from-mist to-sand"><i class="fa-solid fa-image text-4xl text-ocean/40"></i></div>`;
  const play = tipo === 'video' && item.video_url
    ? `<a href="${item.video_url}" target="_blank" rel="noopener" class="absolute inset-0 flex items-center justify-center" aria-label="Assistir vídeo: ${item.titulo || ''}"><span class="flex h-14 w-14 items-center justify-center rounded-full bg-white/90 text-ocean shadow-soft"><i class="fa-solid fa-play text-xl"></i></span></a>`
    : '';
  const data = item.data_registro ? `<p class="mt-1 text-xs text-slate-400">${item.data_registro}</p>` : '';
  return `
    <article class="overflow-hidden rounded-3xl bg-white p-4 shadow-soft">
      <div class="relative overflow-hidden rounded-2xl">${imagem}${play}</div>
      <div class="p-2 pt-4">
        <div class="flex items-center justify-between gap-2">
          <p class="text-xs font-semibold uppercase tracking-[0.2em] text-ocean">${item.categoria || 'Instituto'}</p>
          ${tipo === 'video' ? '<p class="text-xs font-semibold text-slate-400"><i class="fa-solid fa-video mr-1"></i>Vídeo</p>' : ''}
        </div>
        <h3 class="mt-2 text-lg font-bold text-oceanDeep">${item.titulo || ''}</h3>
        <p class="mt-2 text-sm leading-7 text-slate-600">${item.descricao || ''}</p>
        ${data}
      </div>
    </article>`;
}

function renderArchive(items) {
  const container = document.querySelector('[data-render="archive"]');
  if (!container) return;
  const secao = document.getElementById('archive-registros');
  if (!items.length) {
    // Sem registros reais: a seção de fotos publicadas fica oculta.
    // Os cards de categoria continuam estáticos em data-render="archive-categorias".
    if (secao) secao.classList.add('hidden');
    return;
  }
  if (secao) secao.classList.remove('hidden');
  container.innerHTML = `<div class="archive-grid">` + items.map(archiveItemMarkup).join('') + `</div>`;
}

function renderHighlights(items) {
  const container = document.querySelector('[data-render="highlights"]');
  if (!container) return;
  const destaques = items.filter((i) => i.destaque).slice(0, 3);
  if (!destaques.length) {
    const ilustra = [
      { url: 'https://loremflickr.com/800/500/kids,sport,playing?lock=711', cat: 'Esporte', titulo: 'Aula de jiu-jitsu', desc: 'Imagem ilustrativa de uma atividade esportiva do Instituto.' },
      { url: 'https://loremflickr.com/800/500/beach,volleyball,fun?lock=712', cat: 'Comunidade', titulo: 'Arena em atividade', desc: 'Imagem ilustrativa de um dia de esporte e lazer na arena.' },
      { url: 'https://loremflickr.com/800/500/children,party,celebration?lock=713', cat: 'Eventos', titulo: 'Comemoração comunitária', desc: 'Imagem ilustrativa de um evento comemorativo do Instituto.' }
    ];
    container.innerHTML = ilustra.map((i) => `
    <a href="acervo.html" class="home-card block">
      <div class="relative overflow-hidden rounded-2xl"><img src="${i.url}" alt="${i.titulo}" class="h-48 w-full object-cover" loading="lazy" /></div>
      <div class="p-2 pt-4">
        <div class="flex items-center justify-between gap-2">
          <p class="text-xs font-semibold uppercase tracking-[0.2em] text-ocean">${i.cat}</p>
          <span class="inline-flex items-center gap-1 rounded-full bg-sand px-2 py-0.5 text-[9px] font-semibold uppercase tracking-wide text-slate-500"><i class="fa-solid fa-wand-magic-sparkles text-[8px]"></i>Ilustrativo</span>
        </div>
        <h3 class="mt-2 text-lg font-bold text-oceanDeep">${i.titulo}</h3>
        <p class="mt-2 text-sm leading-7 text-slate-600">${i.desc}</p>
      </div>
    </a>`).join('');
    return;
  }
  container.innerHTML = destaques.map((item) => `
    <a href="acervo.html" class="home-card block">
      <div class="relative overflow-hidden rounded-2xl">${item.imagem_url
        ? `<img src="${item.imagem_url}" alt="${item.titulo || ''}" class="h-48 w-full object-cover" loading="lazy" />`
        : `<div class="flex h-48 w-full items-center justify-center bg-gradient-to-br from-mist to-sand"><i class="fa-solid fa-camera text-3xl text-ocean/40"></i></div>`}</div>
      <div class="p-2 pt-4">
        <p class="text-xs font-semibold uppercase tracking-[0.2em] text-ocean">${item.categoria || 'Instituto'}</p>
        <h3 class="mt-2 text-lg font-bold text-oceanDeep">${item.titulo || ''}</h3>
        <p class="mt-2 text-sm leading-7 text-slate-600">${item.descricao || ''}</p>
      </div>
    </a>
  `).join('');
}

// ============================================================
// SECOES ALIMENTADAS POR PASTA DO DRIVE (categoria + secao)
// Cada subpasta de secao no Drive vira uma `secao` na tabela
// `arquivo`. O bloco marcado com [data-secao="x"] e preenchido
// (com [data-pagina] opcional, a secao vira "pagina/secao")
// com as imagens daquela secao; [data-secao-img="x"] recebe a
// primeira imagem (usado no hero e na imagem principal).
// ============================================================
// Normaliza texto para casar nome de arquivo com chave: minusculo, sem
// acento, com hifen. "Jiu-jitsu.jpg" (titulo "Jiu Jitsu") -> "jiu-jitsu"
function normalizarChave(texto) {
  return (texto || '').toString().toLowerCase()
    .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '');
}

// Mídia dos depoimentos publicada da pasta home/depoimentos do Drive.
// Devolve { "ana-paula": { imagem: url, video: url, legenda: titulo } }.
// O casamento é pelo NOME do arquivo (mesma regra dos blocos da home).
// Logomarcas de parceiros publicadas da pasta home/parceiros do Drive.
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
}

async function loadSecoes() {
  // Blocos com varias imagens (carrossel / galeria)
  const blocos = document.querySelectorAll('[data-secao]');
  for (const el of blocos) {
    // data-pagina opcional: secao da PAGINA DA AREA (ex.: volei/carrossel)
    const pagina = el.getAttribute('data-pagina');
    const secao = pagina ? `${pagina}/${el.getAttribute('data-secao')}` : el.getAttribute('data-secao');
    const categoria = el.getAttribute('data-categoria') || '';
    try {
      const itens = (await fetchSecao(categoria, secao)).filter((i) => i.imagem_url);
      if (!itens.length) {
        el.innerHTML = `<p class="secao-vazio"><i class="fa-solid fa-images" aria-hidden="true"></i> Ainda não há imagens publicadas nesta seção. Elas aparecem aqui assim que forem enviadas.</p>`;
        continue;
      }
      if (secao.toLowerCase().includes('carrossel')) {
        el.innerHTML = markupCarrossel(itens);
        ligarSetasCarrossel(el);
      } else {
        el.innerHTML = markupGrade(itens);
        ligarGaleria(el, itens);
      }
    } catch (error) {
      el.innerHTML = `<p class="secao-vazio">Nao foi possivel carregar as imagens desta secao.</p>`;
    }
  }

  // Imagens unicas (hero / imagem principal)
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
  }
}

let archiveData = [];

async function loadArchive() {
  try {
    const resp = await fetchTableData('arquivo');
    archiveData = (resp.data || []).filter((item) => !item.deleted);
  } catch (error) {
    archiveData = [];
  }
  renderArchive(archiveData);
  renderHighlights(archiveData);
}

function setupArchiveFilters() {
  const container = document.querySelector('[data-render="archive"]');
  const botoes = document.querySelectorAll('.archive-filter');
  if (!container || !botoes.length) return;
  botoes.forEach((btn) => {
    btn.addEventListener('click', () => {
      botoes.forEach((b) => {
        b.classList.remove('bg-ocean', 'text-white');
        b.classList.add('border-slate-300', 'bg-white', 'text-slate-600');
      });
      btn.classList.add('bg-ocean', 'text-white');
      btn.classList.remove('border-slate-300', 'bg-white', 'text-slate-600');
      const filtro = btn.getAttribute('data-filter');
      const itens = filtro === 'todos' ? archiveData : archiveData.filter((i) => (i.categoria || '').toLowerCase() === filtro.toLowerCase());
      renderArchive(itens);
    });
  });
}

document.addEventListener('DOMContentLoaded', () => {
  setupMobileMenu();
  setupActiveLinks();
  setupLeadForms();
  setupContactForms();
  setupNewsletterForms();
  loadDynamicSections();
  setupArchiveFilters();
  loadArchive();
  loadSecoes();
});
