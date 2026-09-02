# Plano de Execução — Hero Grande de Mídia (Vídeo / Fotos / Slides)

**Projeto:** Instituto S.E.R. Sagi — Site Institucional
**Versão:** 3.0 (evolução do hero)
**Data:** 25/08/2026
**Gerente:** Agente ORCHESTRATOR
**Origem:** [`docs/hero-midia.md`](../docs/hero-midia.md) — Spec do ARCHITECT (seção 9, tasks H1–H11)

> Este plano substitui o plano de conformidade v2.0 já concluído. O escopo atual é **único**: evoluir o hero da home para um componente de mídia adaptativa (vídeo → slides → imagem → gradiente), com visual inspirado no site de referência aprovado pelo SEO.

---

## 1. Objetivo

Transformar o hero estático de [`index.html`](../index.html:35-63) em um **hero "grande" em tela cheia** que aceite **vídeo, fotos ou slides**, degradando graciosamente entre 4 modos na ordem: **vídeo → slideshow → imagem única → gradiente atual**.

**Referência visual aprovada:** hero do Instituto Neymar Jr. — tela cheia, mídia de fundo com `object-cover`, overlay escuro para legibilidade, título grande com palavra em cor de destaque e bloco de patrocinadores no canto.

---

## 2. Regras Gerais para o CODE (OBRIGATÓRIO)

1. **Não tocar** em [`js/main.js`](../js/main.js), [`img/logo.png`](../img/logo.png) nem nas regras já existentes de [`css/style.css`](../css/style.css)
2. **Não remover ou reescrever** o conteúdo institucional do hero: badge, título S.E.R., parágrafo, CTAs, métricas e o card "Todos somos Sagi" permanecem intactos
3. **Preservar** a paleta Tailwind configurada inline e as classes `cta-lift`, `premium-card`, `metric-panel`, `stat-number`, `badge-soft`, `hero-kicker`, `glow-orb`, `hero-pattern`, `premium-outline`
4. **Não colocar som** no vídeo (autoplay com som é bloqueado)
5. **`playsinline` é obrigatório** no `<video>` (quebra no iOS sem ele)
6. CSS custom permitido **somente no final** de [`css/style.css`](../css/style.css), **sem alterar as regras existentes**
7. O novo JS deve viver em **arquivo novo** [`js/hero.js`](../js/hero.js) — **não** em `main.js`
8. Enquanto os assets reais (`img/hero-video.mp4`, `img/hero-slides/*`, `img/hero-poster.jpg`) não existirem, o componente **deve** degradar para o gradiente atual — **zero erro visual e zero erro de JS no console**
9. Placeholder externo de terceiros (pexels/coverr) só para teste visual rápido e **obrigatoriamente** marcado com `<!-- PLACEHOLDER: remover -->`; não usar em produção sem avisar o humano

---

## 3. Estrutura de Pastas Esperada

```
img/
├── hero-video.mp4       (NOVO — vídeo institucional, 15-25s, 2-5MB, 720p, mudo)
├── hero-video.webm      (NOVO — opcional, fallback Safari/iOS)
├── hero-poster.jpg      (NOVO — capa do vídeo + fallback de imagem única, ~150KB)
└── hero-slides/
    ├── slide-01.jpg     (NOVO — 1920x1080, 200-400KB)
    ├── slide-02.jpg     (NOVO)
    └── slide-03.jpg     (NOVO)
js/
├── main.js              (INTOCÁVEL)
└── hero.js              (NOVO — resolvedor + slideshow, só na home)
```

> Os arquivos de mídia reais serão entregues pelo cliente. O CODE **não** precisa criá-los — apenas referenciá-los corretamente e garantir o fallback.

---

## 4. Tasks de Implementação

### Wave 1 — Base do Componente (independente dos assets reais)

#### Task H1 — Inserir camada de mídia e overlay na seção hero

**Arquivo:** [`index.html`](../index.html:35-63)

**O que fazer:**
1. Na `<section>` do hero (linha 35), adicionar a classe `flex min-h-screen flex-col` mantendo as classes existentes (`hero-pattern premium-outline relative overflow-hidden ... text-white`)
2. Logo após a abertura da `<section>`, inserir a camada de mídia vazia:
```html
<!-- CAMADA 1 · MÍDIA (renderizada por js/hero.js) -->
<div id="hero-media" class="absolute inset-0 z-0" aria-hidden="true"></div>
```
3. Ajustar o overlay: adicionar `<div class="absolute inset-0 z-[1] bg-gradient-to-br from-oceanDeep/85 via-ocean/60 to-leaf/50"></div>` logo após `#hero-media`
4. Nos 3 `glow-orb` existentes (linhas 36-38), adicionar `z-[1]` às classes
5. Na `<div>` que contém o grid do conteúdo (linha 39), adicionar `relative z-10 flex-1 content-center` mantendo o restante (`mx-auto grid max-w-7xl gap-12 px-4 py-16 lg:grid-cols-[1.08fr_0.92fr] lg:px-8 lg:py-28`)

**Validação:** home abre idêntica ao estado atual (gradiente visível, sem mídia), sem erro de JS no console, conteúdo intacto.

---

#### Task H2 — Criar `js/hero.js` com resolvedor de 4 modos

**Arquivo:** [`js/hero.js`](../js/hero.js) (novo)

**O que fazer:**
1. Criar o arquivo com a config declarativa no topo:
```js
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
```
2. Implementar `resolveHeroMode()` que, em `mode:'auto'`, retorna a prioridade: `video` (se o arquivo de vídeo existir) → `slides` (se houver 2+ slides) → `image` (se o poster existir) → `none`
3. Implementar `renderHeroMedia(mode)` que injeta dentro de `#hero-media`:
   - **video:** `<video autoplay muted loop playsinline preload="metadata" poster="img/hero-poster.jpg" class="h-full w-full object-cover" tabindex="-1" aria-hidden="true"><source src="img/hero-video.mp4" type="video/mp4"><source src="img/hero-video.webm" type="video/webm"></video>`
   - **slides:** `<ul class="hero-slides relative h-full w-full overflow-hidden">` com `<li>` por slide (primeiro `active`), imagens com `class="h-full w-full object-cover"`
   - **image:** `<img src="img/hero-poster.jpg" alt="Instituto S.E.R. Sagi em ação" class="h-full w-full object-cover">`
   - **none:** deixar `#hero-media` vazio (gradiente atual assume)
4. Detectar existência de arquivos via `fetch` com `HEAD`/`GET` (ou usar o erro de carregamento da `<img>`/`<video>` como gatilho de fallback) — escolher a abordagem mais robusta, garantindo que `none` nunca gere 404 ruidoso
5. Executar a resolução e renderização em `DOMContentLoaded`

**Validação:** com `mode:'none'` o gradiente permanece; com `mode:'image'` e um poster de teste, a imagem aparece; console sem erros.

---

#### Task H3 — Adicionar animação de crossfade + reduced-motion no CSS

**Arquivo:** [`css/style.css`](../css/style.css)

**O que fazer:** adicionar **no final do arquivo** (sem tocar nas regras existentes):
1. Regras para `.hero-slides` (lista em `absolute inset-0`), `.hero-slide` (posicionamento absoluto, `opacity:0`, `transition: opacity 1s ease`), `.hero-slide.active` (`opacity:1`)
2. Estilo dos controles `.hero-slide-controls` (setas e dots)
3. Bloco `@media (prefers-reduced-motion: reduce)` desativando a transição/animação

**Validação:** transição suave entre slides; sem animação quando o SO solicita redução de movimento.

---

#### Task H4 — Carregar o script do hero na home

**Arquivo:** [`index.html`](../index.html:124)

**O que fazer:** adicionar `<script src="js/hero.js"></script>` imediatamente antes de `</body>`, **após** `<script src="js/main.js"></script>` (manter a ordem: main.js primeiro, hero.js depois).

**Validação:** `hero.js` carrega sem conflito com `main.js`; funcionalidades de menu/formulários continuam operando.

---

### Wave 2 — Slideshow Funcional

#### Task H5 — Troca automática de slides com pausa no hover

**Arquivo:** [`js/hero.js`](../js/hero.js)

**O que fazer:**
1. Implementar autoplay usando `setInterval` com o valor de `slideInterval`
2. Alternar a classe `active` entre os `<li>` a cada intervalo
3. Pausar o timer ao passar o mouse sobre `#hero` e retomar ao sair

**Validação:** slides alternam a cada 5s e pausam no hover.

---

#### Task H6 — Setas anterior/próximo e indicadores com reset de timer

**Arquivo:** [`js/hero.js`](../js/hero.js)

**O que fazer:**
1. Adicionar controles: botões anterior/próximo e dots indicadores dentro de `#hero-media` (ou como elemento irmão, com `aria-label` e `role="group"`)
2. Ao clicar, ir para o slide correspondente e **reiniciar** o timer de autoplay
3. Garantir navegação circular (do último volta ao primeiro)

**Validação:** navegação manual funciona em ambos os sentidos, dots refletem o slide ativo, autoplay reinicia após interação.

---

#### Task H7 — Pausar vídeo fora da viewport (IntersectionObserver)

**Arquivo:** [`js/hero.js`](../js/hero.js)

**O que fazer:** usar `IntersectionObserver` sobre `#hero` para pausar o `<video>` quando o hero sair da viewport e retomar ao voltar (apenas no modo vídeo).

**Validação:** vídeo pausa fora da tela e retoma ao voltar; sem efeito colateral nos demais modos.

---

### Wave 3 — Ajustes Visuais (referência visual aprovada)

#### Task H8 — Altura em tela cheia

**Arquivo:** [`index.html`](../index.html:35)

**O que fazer:** garantir `min-h-screen` no desktop (100vh) e altura flexível no mobile (mínimo necessário para não cortar CTAs e o card "Todos somos Sagi").

**Validação:** hero ocupa toda a primeira dobra no desktop; no mobile todos os CTAs visíveis sem rolagem forçada para cima.

---

#### Task H9 — Refinar overlay e glow-orbs

**Arquivo:** [`index.html`](../index.html)

**O que fazer:** ajustar o overlay para `from-oceanDeep/85 via-ocean/60 to-leaf/50` e calibrar os glow-orbs para legibilidade sobre fotos claras e escuras.

**Validação:** contraste AA do texto branco sobre qualquer imagem de teste.

---

#### Task H10 — Tipografia grande com destaque

**Arquivo:** [`index.html`](../index.html:43-51)

**O que fazer:** aplicar escala tipográfica maior ao título S.E.R. mantendo o dourado `#e0c960` nas letras "S.E.R." e destacando a palavra **"Resultado"** em `sun` (`#f4b400`), coerente com a referência visual.

**Validação:** título grande e legível; destaque visual presente e harmônico com a paleta.

---

#### Task H11 — Faixa inferior "Quem confia"

**Arquivo:** [`index.html`](../index.html)

**O que fazer:** adicionar, na base do hero (após o grid de conteúdo), uma faixa discreta com o rótulo "Quem confia" e logos de parceiros, reutilizando o mesmo padrão visual da seção Parceiros existente ([`index.html`](../index.html:99-119)). Não remover a seção Parceiros existente.

**Validação:** selo de parceiros visível na base do hero; seção Parceiros original intacta.

---

## 5. Ordem de Execução Recomendada

| Ordem | Task | Wave | Dependências |
|---|---|---|---|
| 1º | H1 | 1 | — |
| 2º | H2 | 1 | H1 |
| 3º | H3 | 1 | H1 |
| 4º | H4 | 1 | H2 |
| 5º | H5 | 2 | H2, H3 |
| 6º | H6 | 2 | H5 |
| 7º | H7 | 2 | H2 |
| 8º | H8 | 3 | H1 |
| 9º | H9 | 3 | H1 |
| 10º | H10 | 3 | H8 |
| 11º | H11 | 3 | H8 |

---

## 6. Critérios de Aceitação Gerais

- [ ] Home abre com o hero em tela cheia (desktop) e sem erros de JS
- [ ] Com mídia ausente, o gradiente atual permanece (fallback `none`)
- [ ] Com vídeo presente, reproduz mudo em loop com `playsinline`
- [ ] Com slides presentes, slideshow funciona com autoplay, pausa no hover, setas e dots
- [ ] Com apenas o poster, imagem única é exibida
- [ ] Overlay garante legibilidade (contraste AA)
- [ ] Conteúdo institucional (badge, título, texto, CTAs, métricas, card "Todos somos Sagi") intacto
- [ ] [`js/main.js`](../js/main.js) e [`img/logo.png`](../img/logo.png) intocados
- [ ] [`css/style.css`](../css/style.css) preservado com adições apenas no final
- [ ] Menu mobile, links ativos e formulários continuam funcionando
- [ ] `prefers-reduced-motion` respeitado

---

## 7. Handoff do ORCHESTRATOR para o CODE

1. Processar as tasks **por Wave** (1 → 2 → 3) e na ordem da seção 5
2. Cada task é atômica e validável; reportar a conclusão de cada uma
3. **Não** executar trabalho fora do escopo H1–H11
4. Ao concluir, usar `attempt_completion` com resumo objetivo do que foi implementado, arquivos alterados e resultado das validações

**Arquivos gerados nesta etapa:**
- ✅ [`docs/hero-midia.md`](../docs/hero-midia.md) — spec do ARCHITECT
- ✅ [`plans/plan.md`](../plans/plan.md) — este plano do ORCHESTRATOR

---

## 8. Tarefa Adicional — Logotipo sobreposto ao Hero (L1–L2)

**Origem:** [`docs/hero-logo.md`](../docs/hero-logo.md) — Spec do ARCHITECT (pedido do SEO)
**Escopo:** sobrepor [`img/logo2-hero.png`](../img/logo2-hero.png) à direita do hero, por cima da imagem, sem tocar no resolvedor de mídia nem no conteúdo institucional. Tarefa independente das Waves H1–H11 já concluídas.

### Snippet (copiar exatamente)

```html
<!-- CAMADA LOGO · logotipo sobreposto ao hero, à direita -->
<img src="img/logo2-hero.png" alt="" aria-hidden="true"
     class="pointer-events-none select-none absolute right-6 top-6 z-[15] h-auto w-28 drop-shadow-lg sm:w-36 lg:w-44">
```

#### Task L1 — Inserir o logotipo no hero

**Arquivo:** [`index.html`](../index.html:41-42)

**O que fazer:** inserir o `<img>` acima **após o terceiro `glow-orb`** (linha 41, `bg-coral/20`) e **antes** do comentário `<!-- CAMADA 1.1 · CONTROLES DO SLIDESHOW ... -->` (linha 42).

**Validação:** logo visível no canto superior direito sobre o gradiente; demais camadas intactas; console sem erro.

#### Task L2 — Validação responsiva e de contraste

**O que fazer:** abrir a home em desktop (≥1024px), tablet e mobile (<640px).

**Validação:** logo sem distorção (`h-auto`), sem cobrir badge/título/card "Todos somos Sagi", legível sobre os 4 modos de mídia, sem interceptar cliques nos CTAs.

### Regras específicas (acrescentam às da seção 2)

- ✅ Editar **somente** [`index.html`](../index.html:41-42)
- ❌ Não tocar em [`js/main.js`](../js/main.js), [`js/hero.js`](../js/hero.js), [`css/style.css`](../css/style.css) nem [`img/logo.png`](../img/logo.png)
- ❌ Não alterar [`img/logo2-hero.png`](../img/logo2-hero.png) (apenas referenciar)

---

## 9. Ordem de Execução — Tarefa Adicional

| Ordem | Task | Dependências |
|---|---|---|
| 1º | L1 | — |
| 2º | L2 | L1 |
