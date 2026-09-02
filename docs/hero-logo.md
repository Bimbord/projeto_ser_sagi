# Spec — Logotipo sobreposto ao Hero (posição direita)

**Projeto:** Instituto S.E.R. Sagi — Site Institucional
**Versão:** 1.0 (adição pontual ao hero)
**Data:** 25/08/2026
**Arquiteto:** Agente ARCHITECT
**Solicitante:** Bimbord (SEO chefe)
**Origem:** pedido direto do SEO + contexto de [`docs/hero-midia.md`](hero-midia.md)

> Escopo único e isolado: sobrepor um logotipo PNG **à direita**, por cima da imagem do hero, **sem** alterar o resolvedor de mídia nem o conteúdo institucional.

---

## 1. Objetivo

Adicionar o logotipo [`img/logo2-hero.png`](../img/logo2-hero.png) como camada decorativa sobre o hero da home, posicionado **no canto superior direito**, visível sobre qualquer um dos 4 modos de mídia (vídeo → slides → imagem → gradiente) e sobre o overlay escuro.

---

## 2. Decisão de Arquitetura

| Item | Decisão | Justificativa |
|---|---|---|
| Arquivo | [`img/logo2-hero.png`](../img/logo2-hero.png) | Confirmado pelo SEO; nome indica logo criado para o hero; arquivo hoje sem referência em nenhuma página |
| Posição | **canto superior direito** (`top-right`) | "posicionado à direita" + não colide com badge/título (esquerda) nem com o card "Todos somos Sagi" (centrado verticalmente) |
| Camada | elemento `<img>` absoluto dentro da `<section>` do hero | o hero já é `relative`; nenhuma outra camada é tocada |
| Empilhamento | `z-[15]` | acima da mídia (`z-0`), do overlay e glow-orbs (`z-[1]`) e do conteúdo (`z-10`), por ser um elemento decorativo de sobreposição |
| Interação | `pointer-events-none` | não bloqueia CTAs, métricas nem links do hero |
| Acessibilidade | `alt=""` + `aria-hidden="true"` | logo decorativo (o nome já está no título e no header); não duplica anúncio para leitores de tela |
| Responsividade | largura `w-28` → `sm:w-36` → `lg:w-44` | escala o logo nos breakpoints sem distorcer (`h-auto`) |
| Legibilidade | `drop-shadow-lg` | sombra sutil garante contraste sobre fotos/vídeos claros |

### Camadas do hero após a mudança

```
<section class="... relative ...">            ← âncora (já é relative)
  #hero-media ................ z-0   (mídia)
  overlay .................... z-[1] (gradiente)
  glow-orb ×3 ................ z-[1]
  🆕 <img logo2-hero.png> .... z-[15] ← LOGO (novo, canto superior direito)
  #hero-controls ............. z-20  (setas/dots do slideshow, pointer-events-none)
  grid de conteúdo ........... z-10  (badge, título, CTAs, métricas, card)
</section>
```

---

## 3. Referência de Marcação (snippet pronto)

```html
<!-- CAMADA LOGO · logotipo sobreposto ao hero, à direita -->
<img src="img/logo2-hero.png" alt="" aria-hidden="true"
     class="pointer-events-none select-none absolute right-6 top-6 z-[15] h-auto w-28 drop-shadow-lg sm:w-36 lg:w-44">
```

> Classes 100% Tailwind (CDN já carregado em [`index.html`](../index.html:14)). **Nenhuma** regra CSS custom é necessária — [`css/style.css`](../css/style.css) permanece intocado.

---

## 4. Ponto Exato de Inserção

**Arquivo:** [`index.html`](../index.html:35-68)

Inserir o `<img>` **após o terceiro `glow-orb`** (linha 41, `bg-coral/20`) e **antes do comentário** `<!-- CAMADA 1.1 · CONTROLES DO SLIDESHOW ... -->` (linha 42), mantendo a ordem:

1. [`#hero-media`](../index.html:37)
2. overlay (`z-[1]`) — linha 38
3. `glow-orb` branco — linha 39
4. `glow-orb` sun — linha 40
5. `glow-orb` coral — linha 41
6. **🆕 `<img>` do logo — inserir aqui**
7. [`#hero-controls`](../index.html:43)
8. grid de conteúdo (`z-10`) — linha 44

---

## 5. Regras de Fidelidade (para o CODE)

### NÃO fazer

- ❌ NÃO tocar em [`js/main.js`](../js/main.js), [`js/hero.js`](../js/hero.js), [`img/logo.png`](../img/logo.png) nem nas regras existentes de [`css/style.css`](../css/style.css)
- ❌ NÃO remover/reescrever badge, título S.E.R., parágrafo, CTAs, métricas ou card "Todos somos Sagi"
- ❌ NÃO mover nem alterar `#hero-media`, o overlay, os glow-orbs ou `#hero-controls`
- ❌ NÃO usar `alt` descritivo no logo (seria duplicado para leitores de tela) nem deixar o elemento capturando clique
- ❌ NÃO alterar [`img/logo2-hero.png`](../img/logo2-hero.png) (apenas referenciá-lo)

### PODE fazer

- ✅ Editar **somente** [`index.html`](../index.html:35-68) — única alteração é a inserção do `<img>` descrito na seção 3
- ✅ Ajustar as larguras responsivas (`w-28`/`sm:w-36`/`lg:w-44`) se o logo precisar de escala diferente
- ✅ Trocar `right-6 top-6` por `right-4 top-4`/`right-8 top-8` se o SEO preferir outro afastamento (mantendo sempre o canto superior direito)

---

## 6. Tasks para o CODE

### Task L1 — Inserir o logotipo no hero

| Campo | Detalhe |
|---|---|
| Arquivo | [`index.html`](../index.html:41-42) |
| Ação | Inserir o `<img src="img/logo2-hero.png" ...>` da seção 3 no ponto exato da seção 4 |
| Validação | Logo visível no canto superior direito sobre o gradiente; nenhuma alteração nas demais camadas; console sem erro |

### Task L2 — Validação responsiva e de contraste

| Campo | Detalhe |
|---|---|
| Ação | Abrir a home em desktop (≥1024px), tablet e mobile (<640px) |
| Validação | Logo mantém proporção (`h-auto`), não cobre badge/título nem o card "Todos somos Sagi"; legível sobre gradiente e, se houver mídia, sobre vídeo/slides/imagem; não intercepta cliques nos CTAs |

---

## 7. Critérios de Aceitação

- [ ] Logo [`img/logo2-hero.png`](../img/logo2-hero.png) aparece por cima da imagem do hero, alinhado à direita (canto superior direito)
- [ ] Visível nos 4 modos de mídia (vídeo, slides, imagem, gradiente) e sobre o overlay
- [ ] Não bloqueia interação (CTAs, métricas, links) — `pointer-events-none` ativo
- [ ] Não duplica informação para leitores de tela (`alt=""` + `aria-hidden="true"`)
- [ ] Responsivo em desktop, tablet e mobile, sem distorção
- [ ] [`js/main.js`](../js/main.js), [`js/hero.js`](../js/hero.js), [`css/style.css`](../css/style.css) e [`img/logo.png`](../img/logo.png) intocados
- [ ] Única alteração de código restrita a [`index.html`](../index.html:35-68)

---

## 8. Handoff para ORCHESTRATOR

Este documento entrega ao ORCHESTRATOR:

1. **Decisão fechada** — arquivo, posição, z-index, interação e acessibilidade do logo (seção 2)
2. **Snippet pronto** para o CODE copiar (seção 3)
3. **Ponto exato de inserção** no [`index.html`](../index.html:41-42) (seção 4)
4. **Regras de fidelidade** claras (seção 5)
5. **Tasks atômicas com validação** (seção 6) e **critérios de aceitação** (seção 7)

**Próximo passo do ORCHESTRATOR:**
- Registrar as tasks L1–L2 em [`plans/plan.md`](../plans/plan.md) como uma nova etapa independente (não depende das Waves H1–H11 já concluídas)
- Coordenar o CODE para executar a inserção e validar nos 4 modos de mídia

---

## 9. Notas e Pendências

- [`img/logo2-hero.png`](../img/logo2-hero.png) **não** está na lista de arquivos protegidos (apenas [`img/logo.png`](../img/logo.png) é intocável por regra de [`plans/plan.md`](../plans/plan.md:23)) — a referência é permitida
- Caso o SEO prefira o logo **centralizado na lateral direita** (em vez do canto), substituir `top-6` por `top-1/2 -translate-y-1/2` no snippet da seção 3
- Nenhum asset novo é necessário; o arquivo já existe em [`img/logo2-hero.png`](../img/logo2-hero.png)
