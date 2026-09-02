# Hero de Vídeo — Home do Instituto S.E.R. Sagi

> Spec de implementação para o Kilo Code. Gerado pelo Hermes (assistente pessoal).
> Referência visual: hero em vídeo do Instituto Neymar Jr. (institutoneymarjr.org.br) — vídeo institucional autoplay + overlay + conteúdo por cima.
> Arquivo alvo: **`index.html`** (seção hero, linhas ~35-63)

---

## 1. OBJETIVO

Transformar o hero atual da home em um **hero de vídeo institucional**: vídeo de fundo (autoplay, mudo, loop), overlay para legibilidade e o conteúdo atual (badge, título S.E.R., texto, CTAs, métricas e card "Todos somos Sagi") por cima.

**Impacto desejado:** movimento e emoção — crianças reais em atividade no topo da home. Vitrine da causa para parceiros, doadores e fiscalizadores.

---

## 2. DESIGN SYSTEM (NÃO MUDAR — já configurado no Tailwind de cada página)

| Token | Valor | Uso |
|---|---|---|
| `ocean` | `#0f5c73` | azul principal |
| `oceanDeep` | `#083b4c` | azul profundo (overlay escuro) |
| `sand` | `#f5efe3` | fundo areia |
| `sun` | `#f4b400` | amarelo CTAs/destaques |
| `coral` | `#e77b5f` | coral acentos |
| `leaf` | `#2e7d4f` | verde natureza |
| `mist` | `#e7f4f7` | azul claro |

- Fonte: **Inter** (400-800)
- Classes preservadas: `hero-pattern`, `premium-outline`, `glow-orb`, `badge-soft`, `hero-kicker`, `cta-lift`, `premium-card`, `metric-panel`, `stat-number`, `section-title`

---

## 3. ANATOMIA DO NOVO HERO (estrutura alvo)

```
<section class="hero-pattern premium-outline relative overflow-hidden ...">
  ┌─ 🎥 VÍDEO DE FUNDO (posição absoluta, cobre 100%)
  │   <video autoplay muted loop playsinline poster="img/hero-poster.jpg">
  │     <source src="img/hero-video.mp4" type="video/mp4">
  │   </video>
  ├─ 🌑 OVERLAY (gradiente escuro p/ legibilidade)
  │   <div class="absolute inset-0 bg-gradient-to-br from-oceanDeep/85 via-ocean/70 to-leaf/60"></div>
  ├─ ✨ glow-orbs (manter os 3 existentes, com z-index acima do vídeo? NÃO — manter atrás do conteúdo)
  └─ 📄 CONTEÚDO (grid atual, z-10)
      badge "Praia do Sagi • Baía Formosa/RN" (manter)
      "Instituto" + H2 S.E.R. Sagi (manter cores das letras #e0c960)
      parágrafo de apoio (manter)
      CTAs "Conheça Nossos Projetos" + "Apresentação para Parceiros" (manter)
      métricas 120 / 1.149+ / 49 (manter)
      card premium "Todos somos Sagi" (manter — fundo branco continua legível sobre o vídeo)
</section>
```

### Regras da estrutura
1. **Vídeo**: posição `absolute inset-0`, `w-full h-full object-cover`, `z-0`
2. **Overlay**: `absolute inset-0` logo acima do vídeo, `z-[1]`
3. **Conteúdo**: manter o grid atual, garantir `z-10` nos blocos (já tem `relative z-10`)
4. **Glow-orbs**: manter, mas com `z-[1]` (acima do vídeo, abaixo do texto) — ficam bonitos por cima do vídeo
5. **Nada do conteúdo atual pode ser removido ou reescrito** — só adicionar vídeo + overlay

---

## 4. ESPECIFICAÇÃO TÉCNICA DO VÍDEO

```html
<video autoplay muted loop playsinline preload="metadata"
       poster="img/hero-poster.jpg"
       aria-hidden="true"
       class="absolute inset-0 z-0 h-full w-full object-cover"
       tabindex="-1">
  <source src="img/hero-video.mp4" type="video/mp4">
</video>
```

| Atributo | Por quê |
|---|---|
| `autoplay muted loop` | navegador só permite autoplay SEM som; loop contínuo |
| `playsinline` | **obrigatório no iOS** (sem isso o Safari abre fullscreen) |
| `poster` | imagem de capa — aparece antes do vídeo carregar e como fallback |
| `preload="metadata"` | não baixa o vídeo inteiro de cara (performance) |
| `aria-hidden="true"` + `tabindex="-1"` | acessibilidade: leitor de tela ignora; sem foco por teclado |
| `object-cover` | corta sem distorcer, cobre 100% |

### Assets esperados (placeholders até o cliente entregar)
- `img/hero-video.mp4` — vídeo institucional (ver regras de tamanho abaixo)
- `img/hero-poster.jpg` — primeiro frame/imagem de capa (pode ser uma foto real do instituto)

### Se ainda não existirem os arquivos
- Deixar o `<video>` com os caminhos acima (quando o cliente entregar, é só substituir os arquivos — ZERO mudança de código)
- **NÃO** usar vídeo externo de terceiros (pexels/coverr) em produção sem avisar o humano — placeholder externo só para teste visual rápido, marcado com comentário `<!-- PLACEHOLDER: remover -->`

---

## 5. REGRAS DE FIDELIDADE (o que NÃO fazer)

- ❌ NÃO alterar `js/main.js`, `css/style.css`, `img/logo.png` (regra do `plans/plan.md`)
- ❌ NÃO remover/reescrever badge, título S.E.R., parágrafos, CTAs, métricas ou card "Todos somos Sagi"
- ❌ NÃO mudar cores, fontes ou classes existentes do hero
- ❌ NÃO colocar som no vídeo (autoplay com som é bloqueado e quebra a UX)
- ❌ NÃO esquecer o `playsinline` (quebra no iPhone)
- ✅ Se precisar de CSS extra, usar utilitários Tailwind (já carregado via CDN). Só adicionar CSS custom no `style.css` se for estritamente necessário, SEM tocar nas regras existentes
- ✅ Vídeo institucional deve ter **no máximo 15-25s de duração e ~2-5MB** (realidade de internet da comunidade — celular 3G/4G)

---

## 6. VALIDAÇÃO (checklist antes de entregar)

- [ ] Home abre com o vídeo rodando mudo em loop (desktop e mobile)
- [ ] `playsinline` presente (testar num iPhone/Android se possível)
- [ ] Poster aparece antes do vídeo carregar
- [ ] Texto e CTAs legíveis sobre o vídeo (overlay funcionando)
- [ ] Card "Todos somos Sagi" continua legível (fundo branco)
- [ ] Página abre sem erro de JS no console
- [ ] Métricas, badge e CTAs intactos e clicáveis
- [ ] Menu mobile, links ativos e formulários continuam funcionando
- [ ] Comentar o vídeo como `<!-- HERO VÍDEO: trocar arquivos em img/ -->`

---

## 7. PENDÊNCIAS PARA O CLIENTE (avisar o humano)

- [ ] Vídeo institucional real (crianças em atividade, autorização de imagem dos responsáveis!)
- [ ] Poster (frame bonito do vídeo ou foto real)
- [ ] Definir se o vídeo fica só na home ou também nas páginas internas (recomendado: SÓ na home — performance)
