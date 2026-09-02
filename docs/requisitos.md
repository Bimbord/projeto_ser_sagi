# Requisitos do Sistema — Instituto S.E.R. Sagi

**Projeto:** Site Institucional — Correção de Conformidade e Evolução  
**Versão:** 2.0  
**Data:** 19/06/2026  
**Arquiteto:** Agente ARCHITECT  
**Origem:** [`briefing.md`](briefing.md) — Análise de Conformidade ASK

---

## 1. Visão Geral

Este documento define os requisitos funcionais e não funcionais derivados da análise de conformidade entre o site atual e a apresentação institucional em PDF. O objetivo é elevar a conformidade de 72% para acima de 95%, corrigindo lacunas críticas de conteúdo, inconsistências técnicas e deficiências de SEO.

---

## 2. Requisitos Funcionais (RF)

### RF01 — Navegação Uniforme (CRÍTICO)

**Descrição:** O menu de navegação principal deve conter exatamente os mesmos 7 links em todas as páginas do site.

**Detalhes:**
- Links obrigatórios: Início, Quem Somos, Nossas Ações, Como Ajudar, Lei de Incentivo, Transparência, Contato
- Aplica-se ao menu desktop, menu mobile e ao atributo `data-page-link` para highlight de página ativa
- Páginas afetadas: [`quem-somos.html`](../quem-somos.html:21), [`acoes.html`](../acoes.html:11), [`como-ajudar.html`](../como-ajudar.html:10), [`contato.html`](../contato.html:10)

**Critério de aceitação:**
- Todas as 7 páginas exibem os mesmos 7 links no menu principal
- Menu mobile também deve ter 7 links em todas as páginas

---

### RF02 — Identidade Visual Consistente (Header) (IMPORTANTE)

**Descrição:** O header de todas as páginas internas deve usar a imagem real do logotipo ([`img/logo.png`](../img/logo.png)), substituindo o placeholder de ícone Font Awesome.

**Detalhes:**
- Substituir `<div class="flex h-12 w-12..."><i class="fa-solid fa-owl">` por `<img src="img/logo.png" alt="Instituto S.E.R. Sagi" class="h-16 w-auto object-contain">`
- Páginas afetadas: [`quem-somos.html`](../quem-somos.html:19), [`acoes.html`](../acoes.html:11), [`como-ajudar.html`](../como-ajudar.html:10), [`lei-incentivo.html`](../lei-incentivo.html:10), [`transparencia.html`](../transparencia.html:10), [`contato.html`](../contato.html:10)

**Critério de aceitação:**
- Header visualmente idêntico ao da [`index.html`](../index.html:24-25) em todas as páginas

---

### RF03 — CTA "Seja Parceiro" Padronizado (IMPORTANTE)

**Descrição:** O botão "Seja Parceiro" no header deve apontar sempre para [`lei-incentivo.html`](../lei-incentivo.html), independentemente da página em que o usuário se encontra.

**Detalhes:**
- Páginas afetadas: [`quem-somos.html`](../quem-somos.html:22), [`acoes.html`](../acoes.html:11), [`como-ajudar.html`](../como-ajudar.html:10)
- Atualmente apontam para `como-ajudar.html#parcerias` — devem apontar para `lei-incentivo.html`
- [`lei-incentivo.html`](../lei-incentivo.html:10) mantém âncora `#formulario-incentivo` (CTA contextual)

**Critério de aceitação:**
- CTA "Seja Parceiro" no header de qualquer página (exceto [`lei-incentivo.html`](../lei-incentivo.html)) leva a [`lei-incentivo.html`](../lei-incentivo.html)

---

### RF04 — Rodapé Padronizado (RECOMENDÁVEL)

**Descrição:** O footer deve ser consistente em todas as páginas, com as mesmas informações de contato, endereço e redes sociais.

**Detalhes:**
- Modelo de referência: footer do [`index.html`](../index.html:123)
- Incluir: nome do instituto, endereço, telefone, e-mail, links para redes sociais, link para contato
- Páginas afetadas: [`quem-somos.html`](../quem-somos.html:43), [`acoes.html`](../acoes.html:17), [`como-ajudar.html`](../como-ajudar.html), [`lei-incentivo.html`](../lei-incentivo.html:33), [`transparencia.html`](../transparencia.html), [`contato.html`](../contato.html)

**Critério de aceitação:**
- Footer completo e padronizado em todas as páginas

---

### RF05 — Conteúdo Legal da Lei de Incentivo (CRÍTICO)

**Descrição:** A página [`lei-incentivo.html`](../lei-incentivo.html) e trechos relevantes de [`como-ajudar.html`](../como-ajudar.html) devem conter informações jurídicas completas da Lei nº 11.438/2006.

**Detalhes:**
- Número da lei: "Lei nº 11.438/2006"
- Percentual empresas: "até 2% do Imposto de Renda devido" (com menção a 3%-4% para casos específicos)
- Percentual pessoas físicas: "até 6% do Imposto de Renda devido" (conforme texto legal; verificar com contador se o PDF menciona 7% incorretamente)
- Tagline oficial do PDF: "Invista, transforme e gere valor para a sociedade e para sua Empresa"

**Critério de aceitação:**
- Número da lei visível e verificável
- Percentuais claros e juridicamente precisos
- Tagline incorporada

---

### RF06 — Dados Demográficos IBGE (IMPORTANTE)

**Descrição:** Criar seção de contexto demográfico na home ou em Quem Somos com dados populacionais do IBGE.

**Detalhes:**
- População Baía Formosa (2025): 9.115 habitantes
- Faixas etárias: ~24% crianças (0-14), ~64% jovens/adultos (15-59), ~12% idosos (60+)
- Comunidade de Sagi: 900-1.000 moradores, ~230 crianças
- Comunidade da Pituba: 400-550 moradores, ~120-150 crianças
- Contexto social descritivo (PDF linhas 192-195)

**Critério de aceitação:**
- Seção visível com dados apresentados de forma clara (cards, infográfico ou lista)
- Fonte IBGE citada

---

### RF07 — Missão e Visão Alinhadas ao PDF (IMPORTANTE)

**Descrição:** Atualizar os textos de Missão e Visão em [`quem-somos.html`](../quem-somos.html:36-37) para coincidir com a redação oficial do PDF.

**Detalhes:**

**Missão oficial (PDF):**
> "Promover o desenvolvimento humano e social de crianças, adolescentes e da comunidade do Sagi **e regiões adjacentes**, por meio do esporte, da saúde, da educação, da cultura e da preservação ambiental, **fortalecendo valores como cidadania, inclusão e bem-estar**."

**Visão oficial (PDF):**
> "Ser referência **regional** em transformação social, **reconhecido pelo impacto positivo na qualidade de vida, na valorização cultural e na proteção do meio ambiente, contribuindo para uma comunidade mais saudável, consciente e sustentável**."

**Critério de aceitação:**
- Texto de Missão idêntico ao PDF oficial
- Texto de Visão idêntico ao PDF oficial

---

### RF08 — Seção "Objetivo" (IMPORTANTE)

**Descrição:** Criar seção de Objetivo Institucional em [`quem-somos.html`](../quem-somos.html) com o texto oficial do PDF.

**Detalhes:**
> "Oferecer ações e projetos que incentivem hábitos saudáveis, a prática esportiva, o cuidado com a saúde, a valorização das origens culturais e a preservação da natureza, ampliando oportunidades e fortalecendo vínculos sociais."

**Critério de aceitação:**
- Nova seção "Objetivo" visível em Quem Somos, no grid de Missão/Visão/Valores

---

### RF09 — Comunidade da Pituba no Escopo (IMPORTANTE)

**Descrição:** Incluir referência à comunidade da Pituba como parte do público-alvo do Instituto.

**Detalhes:**
- Em [`quem-somos.html`](../quem-somos.html) e [`index.html`](../index.html), mencionar que o Instituto atende "Sagi e regiões adjacentes (incluindo Pituba)"
- Alinhar com a nova redação da Missão (RF07)

**Critério de aceitação:**
- Pituba mencionada como comunidade atendida em pelo menos 2 páginas

---

### RF10 — Origens Indígenas Explicitadas (RECOMENDÁVEL)

**Descrição:** Substituir termos genéricos como "origens locais" por "origens indígenas" onde aplicável.

**Detalhes:**
- Em [`index.html`](../index.html:66), alterar "Origens locais" para "Origens indígenas"
- Em [`quem-somos.html`](../quem-somos.html:33), reforçar "origens indígenas da comunidade"

**Critério de aceitação:**
- Referência explícita a origens indígenas em pelo menos 2 locais do site

---

### RF11 — História da Criação do Logo (RECOMENDÁVEL)

**Descrição:** Incluir a narrativa sobre a criação do logotipo em [`quem-somos.html`](../quem-somos.html).

**Detalhes:**
> "O logo foi criado por um amigo que conseguiu, em poucas horas, traduzir nossa essência em imagem."

**Critério de aceitação:**
- História incluída na seção de Identidade/Símbolo

---

### RF12 — Termo "A Arte Suave" para Jiu-Jitsu (RECOMENDÁVEL)

**Descrição:** Adicionar o termo "a arte suave" ao descrever o Jiu-Jitsu em [`acoes.html`](../acoes.html:14).

**Critério de aceitação:**
- Expressão "a arte suave" presente na descrição do Jiu-Jitsu

---

### RF13 — Detalhamento de Ações Solidárias (RECOMENDÁVEL)

**Descrição:** Especificar "comemorações de aniversário" e "momentos de convivência" nas ações solidárias.

**Detalhes:**
- Em [`acoes.html`](../acoes.html:14), expandir descrição de "Ações Solidárias"

**Critério de aceitação:**
- Menção explícita a aniversários e convivência comunitária

---

### RF14 — Metadados SEO Completos (RECOMENDÁVEL)

**Descrição:** Adicionar Open Graph, Twitter Cards e Schema.org em todas as páginas.

**Detalhes:**
- Open Graph: `og:title`, `og:description`, `og:image`, `og:url`, `og:type`
- Twitter Cards: `twitter:card`, `twitter:title`, `twitter:description`, `twitter:image`
- Schema.org: `Organization` na home, `WebPage` nas demais
- `<meta keywords>` em páginas internas
- `<meta name="theme-color">` em todas as páginas

**Critério de aceitação:**
- Todas as 7 páginas com meta tags completas
- Página validada no [Facebook Sharing Debugger](https://developers.facebook.com/tools/debug/) e [Twitter Card Validator](https://cards-dev.twitter.com/validator)

---

### RF15 — FAQ na Página de Contato (RECOMENDÁVEL)

**Descrição:** Adicionar seção de Perguntas Frequentes em [`contato.html`](../contato.html).

**Detalhes:**
- Perguntas sugeridas: Como doar? Como ser voluntário? Como funciona a Lei de Incentivo? O Instituto emite recibo? Onde fica a sede?
- Respostas curtas e diretas com links para páginas relevantes

**Critério de aceitação:**
- Seção FAQ com no mínimo 5 perguntas e respostas

---

## 3. Requisitos Não Funcionais (RNF)

### RNF01 — Consistência Visual (MANUTENIBILIDADE)

**Descrição:** O site deve manter identidade visual uniforme em todas as páginas.

**Indicadores:**
- Header idêntico (logo real) em 7/7 páginas
- Footer idêntico em 7/7 páginas
- Menu idêntico (7 links) em 7/7 páginas
- CTA "Seja Parceiro" com destino consistente

---

### RNF02 — Performance (PERFORMANCE)

**Descrição:** O site deve manter-se leve e rápido, apesar das adições de conteúdo.

**Restrições:**
- Todas as dependências externas (Tailwind, Font Awesome, Google Fonts) continuam via CDN — sem bundlers ou build step
- Nenhum framework JavaScript adicional; manter vanilla JS
- Imagens otimizadas (a logo existente já está em PNG de 248KB; considerar versão WebP futura)
- Páginas devem permanecer estáticas (HTML puro), sem SSR ou SSG adicionais

---

### RNF03 — Compatibilidade (COMPATIBILIDADE)

**Descrição:** O site deve funcionar corretamente nos navegadores modernos.

**Alvos:**
- Chrome 90+, Firefox 90+, Safari 15+, Edge 90+
- Dispositivos móveis (responsive design mantido)
- Leitores de tela (acessibilidade preservada)

---

### RNF04 — Segurança (SEGURANÇA)

**Descrição:** Manter e reforçar boas práticas de segurança existentes.

**Requisitos:**
- Formulários continuam usando a RESTful Table API (sanitização server-side)
- Campos de entrada com validação HTML5 (`required`, `type="email"`, etc.)
- Checkbox de aceite de privacidade em todos os formulários
- Senhas ou dados sensíveis não são armazenados no frontend

---

### RNF05 — Escalabilidade do Conteúdo (ESCALABILIDADE)

**Descrição:** A arquitetura deve permitir crescimento futuro sem refatoração.

**Requisitos:**
- As 6 tabelas RESTful (`contatos`, `leads_apoio`, `newsletter`, `depoimentos`, `parceiros`, `galeria`) permanecem como único backend
- Novas seções de conteúdo devem ser texto estático (HTML) ou consumir dados dinâmicos das tabelas existentes
- Estrutura de pastas não deve ser alterada (sem reorganização de assets)

---

### RNF06 — SEO e Indexabilidade (SEO)

**Descrição:** O site deve estar otimizado para mecanismos de busca e compartilhamento social.

**Indicadores:**
- 7/7 páginas com `<title>` único e descritivo
- 7/7 páginas com `<meta description>` específica
- 7/7 páginas com Open Graph e Twitter Cards
- 1/1 página (home) com Schema.org `Organization`
- Sitemap implícito pela navegação completa

---

### RNF07 — Precisão Jurídica (CONFORMIDADE)

**Descrição:** Todo conteúdo com implicações legais ou fiscais deve ser validado.

**Requisitos:**
- Percentuais da Lei de Incentivo devem ser verificados por contador antes da publicação
- O texto oficial da missão/visão/objetivo vem do PDF institucional
- Dados do IBGE devem ser citados com fonte e ano

---

## 4. Regras de Negócio (RN)

| # | Regra | Fonte | Ação |
|---|-------|-------|------|
| RN01 | O Instituto atende Sagi e regiões adjacentes (incluindo Pituba) | PDF missão + IBGE | Atualizar missão (RF07) e mencionar Pituba (RF09) |
| RN02 | Captação via Lei nº 11.438/2006 como principal mecanismo | PDF linha 160 | Inserir número da lei (RF05) |
| RN03 | Empresas: até 2% do IR devido (3-4% casos especiais) | PDF linha 162-164 | Inserir percentuais (RF05) |
| RN04 | Pessoas físicas: até 6% com restituição (verificar juridicamente) | Lei 11.438/2006 | Inserir percentual correto (RF05) |
| RN05 | Projeto "Jóia da Coroa" é o carro-chefe para captação | PDF linha 137-152 | Já conforme — manter destaque |
| RN06 | Transparência como pilar de credibilidade | PDF linha 18-19 | Já conforme — página dedicada existe |
| RN07 | Coruja como símbolo central da identidade | PDF linha 21-24 | Já conforme — reforçar com história (RF11) |
| RN08 | Valorização de origens indígenas e preservação de tartarugas | PDF linha 124-135 | Explicitar origens indígenas (RF10) |

---

## 5. Matriz de Rastreabilidade

| Requisito | Origem (Briefing) | Prioridade | Páginas Afetadas |
|-----------|-------------------|------------|------------------|
| RF01 | Recomendação #3 | 🔴 CRÍTICA | 4 páginas |
| RF02 | Recomendação #9 | 🟡 IMPORTANTE | 6 páginas |
| RF03 | Recomendação #10 | 🟡 IMPORTANTE | 3 páginas |
| RF04 | Recomendação #16 | 🟢 RECOMENDÁVEL | 6 páginas |
| RF05 | Recomendações #1, #2, #4, #15 | 🔴 CRÍTICA | 2 páginas |
| RF06 | Recomendação #5 | 🟡 IMPORTANTE | 2 páginas |
| RF07 | Recomendações #6, #7 | 🟡 IMPORTANTE | 1 página |
| RF08 | Recomendação #8 | 🟡 IMPORTANTE | 1 página |
| RF09 | Recomendação #11 | 🟡 IMPORTANTE | 2 páginas |
| RF10 | Recomendação #12 | 🟢 RECOMENDÁVEL | 2 páginas |
| RF11 | Recomendação #13 | 🟢 RECOMENDÁVEL | 1 página |
| RF12 | Recomendação #14 | 🟢 RECOMENDÁVEL | 1 página |
| RF13 | Seção 3.8 do briefing | 🟢 RECOMENDÁVEL | 1 página |
| RF14 | Recomendações #17, #18, #19 | 🟢 RECOMENDÁVEL | 7 páginas |
| RF15 | Recomendação #20 | 🟢 RECOMENDÁVEL | 1 página |

---

## 6. Handoff para ORCHESTRATOR

Este documento deve ser encaminhado ao agente **ORCHESTRATOR** para:
1. Consolidar com [`escopo.md`](escopo.md) e [`roadmap.md`](roadmap.md)
2. Criar tasks detalhadas para o agente CODE
3. Coordenar a implementação por ondas (Wave 1 → Wave 2 → Wave 3)

**Pré-requisitos para CODE:**
- Nenhuma dependência externa nova
- Sem necessidade de build tools
- Trabalhar apenas com edição de HTML, CSS e JS existentes
- Preservar a API RESTful Table intacta
