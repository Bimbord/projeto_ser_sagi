/**
 * js/hero.js — Resolvedor + renderização do hero de mídia (somente na home)
 *
 * Modos de degradação graciosa (prioridade em 'auto'):
 *   video → slides → image → none (gradiente atual assume)
 *
 * Regras:
 * - Sem som (autoplay com som é bloqueado)
 * - playsinline obrigatório no <video> (quebra no iOS sem ele)
 * - 'none' mantém #hero-media vazio, sem 404 ruidoso
 */
(function () {
  'use strict';

  const HERO_CONFIG = {
    mode: 'auto',            // 'auto' | 'video' | 'slides' | 'image' | 'none'
    video: 'img/hero-video.mp4',
    poster: 'img/hero-poster.jpg',
    slides: [
      'img/hero-slides/slide-01.jpg',
      'img/hero-slides/slide-02.jpg',
      'img/hero-slides/slide-03.jpg'
    ],
    slideInterval: 5000
  };

  // Estado do slideshow (Wave 2)
  let activeMode = null;
  const slideshow = {
    timer: null,
    index: 0
  };

  /**
   * Verifica a existência de uma imagem via evento onload/onerror (silencioso no console).
   */
  function probeImage(url) {
    return new Promise(function (resolve) {
      let settled = false;
      const done = function (ok) {
        if (settled) return;
        settled = true;
        resolve(ok);
      };

      const img = new Image();
      img.onload = function () { done(true); };
      img.onerror = function () { done(false); };
      img.src = url;

      window.setTimeout(function () { done(false); }, 4000);
    });
  }

  /**
   * Verifica a existência de um vídeo via evento de carregamento de metadados.
   */
  function probeVideo(url) {
    return new Promise(function (resolve) {
      let settled = false;
      const done = function (ok) {
        if (settled) return;
        settled = true;
        video.removeAttribute('src');
        video.load();
        resolve(ok);
      };

      const video = document.createElement('video');
      video.muted = true;
      video.preload = 'metadata';
      video.onloadedmetadata = function () { done(true); };
      video.oncanplay = function () { done(true); };
      video.onerror = function () { done(false); };
      video.src = url;

      window.setTimeout(function () { done(false); }, 4000);
    });
  }

  /**
   * Verifica se há ao menos 2 slides existentes.
   */
  async function probeSlides() {
    const list = (HERO_CONFIG.slides || []).filter(Boolean);
    if (list.length < 2) return false;

    const results = await Promise.all(list.map(probeImage));
    return results.filter(Boolean).length >= 2;
  }

  /**
   * Verifica se o usuário prefere movimento reduzido (acessibilidade).
   */
  function prefersReducedMotion() {
    return !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
  }

  /**
   * Resolve o modo efetivo do hero.
   * Prioridade (mode 'auto'): video → slides → image → none.
   */
  async function resolveHeroMode() {
    if (HERO_CONFIG.mode !== 'auto') return HERO_CONFIG.mode;

    if (await probeVideo(HERO_CONFIG.video)) return 'video';
    if (await probeSlides()) return 'slides';
    if (await probeImage(HERO_CONFIG.poster)) return 'image';

    return 'none';
  }

  function renderVideo() {
    return '<video autoplay muted loop playsinline preload="metadata" poster="' + HERO_CONFIG.poster + '" class="h-full w-full object-cover" tabindex="-1" aria-hidden="true">' +
      '<source src="' + HERO_CONFIG.video + '" type="video/mp4">' +
      '<source src="img/hero-video.webm" type="video/webm">' +
      '</video>';
  }

  function renderSlides() {
    const items = HERO_CONFIG.slides.map(function (src, index) {
      const active = index === 0 ? ' active' : '';
      const loading = index === 0 ? 'eager' : 'lazy';
      return '<li class="hero-slide' + active + '">' +
        '<img src="' + src + '" alt="" loading="' + loading + '" class="h-full w-full object-cover">' +
        '</li>';
    }).join('');

    return '<ul class="hero-slides relative h-full w-full overflow-hidden">' + items + '</ul>';
  }

  function renderImage() {
    const ajuste = HERO_CONFIG.posterCover ? 'object-cover' : 'object-contain object-top';
    return '<img src="' + HERO_CONFIG.poster + '" alt="Instituto S.E.R. Sagi em ação" class="h-full w-full ' + ajuste + '">';
  }

  function buildSlideControls() {
    const count = (HERO_CONFIG.slides || []).length;
    let dots = '';

    for (let i = 0; i < count; i++) {
      const active = i === 0 ? ' active' : '';
      dots += '<button type="button" class="hero-slide-dot' + active + '" data-slide="' + i + '" aria-label="Ir para o slide ' + (i + 1) + '"></button>';
    }

    return '<div class="hero-slide-controls" role="group" aria-label="Controles do slideshow">' +
      '<button type="button" class="hero-slide-arrow hero-slide-arrow--prev" data-slide-prev aria-label="Slide anterior"><i class="fa-solid fa-chevron-left"></i></button>' +
      '<button type="button" class="hero-slide-arrow hero-slide-arrow--next" data-slide-next aria-label="Próximo slide"><i class="fa-solid fa-chevron-right"></i></button>' +
      '<div class="hero-slide-dots">' + dots + '</div>' +
      '</div>';
  }

  /**
   * Injeta a mídia correspondente ao modo dentro de #hero-media.
   * 'none' mantém o contêiner vazio para o gradiente atual assumir.
   */
  function renderHeroMedia(mode) {
    const host = document.getElementById('hero-media');
    const controlsHost = document.getElementById('hero-controls');
    if (!host) return;

    activeMode = mode;
    host.innerHTML = '';
    if (controlsHost) controlsHost.innerHTML = '';

    if (mode === 'video') {
      host.innerHTML = renderVideo();
    } else if (mode === 'slides') {
      host.innerHTML = renderSlides();
      if (controlsHost) controlsHost.innerHTML = buildSlideControls();
    } else if (mode === 'image') {
      host.innerHTML = renderImage();
    }
  }

  function getHeroSection() {
    return document.getElementById('hero') || document.querySelector('section.hero-pattern');
  }

  function getSlides() {
    return Array.prototype.slice.call(document.querySelectorAll('#hero-media .hero-slide'));
  }

  function goToSlide(index) {
    const slides = getSlides();
    const count = slides.length;
    if (!count) return;

    const next = ((index % count) + count) % count;
    slides.forEach(function (slide, i) {
      slide.classList.toggle('active', i === next);
    });
    slideshow.index = next;
    updateSlideControls();
  }

  function nextSlide() {
    goToSlide(slideshow.index + 1);
  }

  function startSlideshow() {
    stopSlideshow();
    slideshow.timer = window.setInterval(nextSlide, HERO_CONFIG.slideInterval);
  }

  function stopSlideshow() {
    if (slideshow.timer) {
      window.clearInterval(slideshow.timer);
      slideshow.timer = null;
    }
  }

  function bindHeroHover() {
    const hero = getHeroSection();
    if (!hero) return;

    hero.addEventListener('mouseenter', function () {
      if (activeMode === 'slides') stopSlideshow();
    });
    hero.addEventListener('mouseleave', function () {
      if (activeMode === 'slides') startSlideshow();
    });
  }

  function updateSlideControls() {
    const dots = document.querySelectorAll('#hero-controls .hero-slide-dot');
    Array.prototype.forEach.call(dots, function (dot, i) {
      dot.classList.toggle('active', i === slideshow.index);
    });
  }

  function restartSlideshow() {
    if (activeMode === 'slides' && !prefersReducedMotion()) startSlideshow();
  }

  function bindSlideControls() {
    const host = document.getElementById('hero-controls');
    if (!host) return;

    const prev = host.querySelector('[data-slide-prev]');
    const next = host.querySelector('[data-slide-next]');
    const dots = host.querySelectorAll('.hero-slide-dot');

    if (prev) {
      prev.addEventListener('click', function () {
        goToSlide(slideshow.index - 1);
        restartSlideshow();
      });
    }

    if (next) {
      next.addEventListener('click', function () {
        goToSlide(slideshow.index + 1);
        restartSlideshow();
      });
    }

    Array.prototype.forEach.call(dots, function (dot) {
      dot.addEventListener('click', function () {
        goToSlide(parseInt(dot.getAttribute('data-slide'), 10));
        restartSlideshow();
      });
    });
  }

  function bindVideoVisibility() {
    if (activeMode !== 'video' || !('IntersectionObserver' in window)) return;

    const hero = getHeroSection();
    const video = document.querySelector('#hero-media video');
    if (!hero || !video) return;

    const observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          video.play().catch(function () { /* autoplay pode ser bloqueado — ignorado */ });
        } else {
          video.pause();
        }
      });
    }, { threshold: 0.1 });

    observer.observe(hero);
  }

  // ============================================================
  // FASE 5 — as fotos do hero vem da pasta `home/hero` do Drive
  // (publicadas no Supabase). Sem foto publicada, mantem os
  // arquivos locais de img/hero-slides/.
  // ============================================================
  const SUPABASE_URL = 'https://icrasqxbxmqbnelmkrei.supabase.co';
  const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImljcmFzcXhieG1xYm5lbG1rcmVpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODgyMDYzOTUsImV4cCI6MjEwMzc4MjM5NX0.u7cWsqTRWIvJJ-jsU7BbcOw1cVI-Su8eJBL_pBaQb_g';
  const HERO_CATEGORIA = 'Home';
  const HERO_SECAO = 'hero';

  function buscarSlidesDoDrive() {
    const url = SUPABASE_URL + '/rest/v1/arquivo?select=titulo,imagem_url'
      + '&categoria=eq.' + encodeURIComponent(HERO_CATEGORIA)
      + '&secao=eq.' + encodeURIComponent(HERO_SECAO)
      + '&deleted=eq.false&order=id.asc';

    return fetch(url, {
      headers: { apikey: SUPABASE_ANON_KEY, Authorization: 'Bearer ' + SUPABASE_ANON_KEY }
    })
      .then(function (r) { return r.ok ? r.json() : []; })
      .then(function (itens) {
        const urls = (itens || []).map(function (i) { return i.imagem_url; }).filter(Boolean);
        if (!urls.length) return;              // nada publicado -> locais
        if (urls.length >= 2) {
          HERO_CONFIG.slides = urls;           // 2+ -> slideshow
        } else {
          HERO_CONFIG.poster = urls[0];        // 1 -> imagem unica
          HERO_CONFIG.posterCover = true;
        }
      })
      .catch(function () { /* mantem os arquivos locais */ });
  }

  function init() {
    const host = document.getElementById('hero-media');
    if (!host) return;

    // Busca as fotos do Drive antes de decidir o modo do hero
    buscarSlidesDoDrive().then(resolveHeroMode).then(function (mode) {
      if (mode === 'video' && prefersReducedMotion()) {
        mode = 'image';
      }

      renderHeroMedia(mode);

      if (mode === 'slides') {
        goToSlide(0);
        if (!prefersReducedMotion()) {
          startSlideshow();
          bindHeroHover();
        }
        bindSlideControls();
      }

      if (mode === 'video') {
        bindVideoVisibility();
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
