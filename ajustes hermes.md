# Ajustes Hermes — registro de alterações

> **Para que serve:** registrar tudo que o **Hermes** alterou no site, para o Bimbord saber o que já foi feito e **evitar conflito** com edições feitas no Kilo Code (não acabarmos com duas versões diferentes do mesmo arquivo).
>
> **Como usar:** antes de pedir uma alteração no Kilo Code, confira aqui se aquele arquivo já foi mexido. Se for mexer no mesmo arquivo, atualize este registro também.

---

## ⚠️ Convenções importantes (ler antes de gerar código)

1. **Cards/grades NÃO podem ser renderizados por JavaScript.**
   O Tailwind Play CDN **não gera CSS** para conteúdo injetado via JS — os cards ficam em **coluna única**.
   → Cards e galerias devem ser **HTML estático**.
   → Quando o JS precisar montar uma grade (ex.: dados reais do Supabase no Acervo), use a classe **`.archive-grid`** (CSS puro em `css/style.css`), **não** utilitários Tailwind como `md:grid-cols-2`.

2. **Conteúdo ilustrativo sempre marcado** com badge "Imagem ilustrativa" / "Ilustrativo".
   (O site é vitrine para captar parceiros; o fictício é aceito, mas sempre sinalizado.)

3. **Credenciais nunca vão para o repositório.**
   R2 → `C:\Users\PRE-IMPRESSOR\R2\.r2-sagi.env` (já no `.gitignore`).
   A anon key do Supabase é pública por design (fica no `main.js`); a **service_role nunca** deve aparecer.

4. **Depois de qualquer alteração:**
   ```bash
   git add -A && git commit -m "descrição" && git push
   python scripts/_sync_drive.py    # sincroniza o backup do Google Drive
   ```

---

## 📄 Estrutura atual do site (28 páginas)

### 🌳 Hierarquia de navegação
```
Home (index.html)
├── Saúde        → consultorio-odontologico.html
├── Esporte      → esporte.html  (HUB)
│      ├── Jiu-Jitsu   → escola-jiu-jitsu.html
│      ├── Vôlei       → volei.html      ─┐ link cruzado
│      ├── Futevôlei   → futevolei.html  ─┘ para a Arena
│      ├── Musculação  → estudio-musculacao.html
│      ├── Natação     → natacao.html
│      └── Dança       → danca.html
├── Educação     → educacao.html
├── Cultura      → cultura.html
└── Preservação  → preservacao-ambiental.html

Quem Somos (quem-somos.html)
└── Seção "Nossas instalações" → instalacoes.html (HUB)
       ├── Arena de Futevôlei e Vôlei → arena-futevolei-volei.html
       ├── Consultório Odontológico   → consultorio-odontologico.html
       ├── Estúdio de Musculação      → estudio-musculacao.html
       └── Tatame (Jiu-Jitsu)         → escola-jiu-jitsu.html
```

### 📋 Lista de arquivos

| Arquivo | Página |
|---|---|
| `index.html` | Início (home) |
| `quem-somos.html` | Quem Somos (inclui a seção "Nossas instalações") |
| `instalacoes.html` | **HUB Instalações** (4 espaços) |
| `acoes.html` | Nossas Ações (6 cards → páginas individuais) |
| `esporte.html` | **HUB Esporte** (6 modalidades) |
| `consultorio-odontologico.html` | Ação: Consultório Odontológico |
| `estudio-musculacao.html` | Esporte: Musculação |
| `escola-jiu-jitsu.html` | Esporte: Jiu-Jitsu |
| `volei.html` | Esporte: Vôlei |
| `futevolei.html` | Esporte: Futevôlei |
| `natacao.html` | Esporte: Natação |
| `danca.html` | Esporte: Dança |
| `arena-futevolei-volei.html` | Ação: Arena de Futevôlei e Vôlei |
| `educacao.html` | Educação |
| `cultura.html` | Cultura |
| `acoes-solidarias.html` | Ação: Ações Solidárias |
| `preservacao-ambiental.html` | Preservação |
| `acervo.html` | Acervo (6 cards de categoria) |
| `acervo-esporte.html` | Acervo: Esporte |
| `acervo-saude.html` | Acervo: Saúde |
| `acervo-educacao.html` | Acervo: Educação |
| `acervo-cultura.html` | Acervo: Cultura |
| `acervo-preservacao.html` | Acervo: Preservação |
| `acervo-eventos.html` | Acervo: Eventos |
| `como-ajudar.html` | Como Ajudar |
| `lei-incentivo.html` | Lei de Incentivo |
| `transparencia.html` | Transparência |
| `contato.html` | Contato |

**Infraestrutura:** HTML + Tailwind CDN + JS vanilla (`js/main.js`, `js/hero.js`) + `css/style.css`.
**Dados dinâmicos:** Supabase (tabelas `arquivo`, `depoimentos`, `parceiros`, `galeria`, `contatos`, `leads_apoio`, `newsletter`).
**Mídias:** Cloudflare R2 (`midias-ser-sagi`).

---

## 📋 Histórico de ajustes

### 12/09/2026 (sessão 6) — Rodapé unificado e profissional (todas as páginas)

**Pedido:** criar o rodapé das páginas (baseado em referências de outros sites), usando **nossos dados** e **nossa estrutura de páginas**.

**Resultado:** rodapé novo aplicado nas **28 páginas**, com 4 colunas + barra de copyright:

| Coluna | Conteúdo |
|---|---|
| **Marca** | Nome + tagline "Sabedoria · Esforço · Resultado" + descrição + ícones de **Instagram** e **WhatsApp** + formulário de **newsletter** |
| **Navegação** | Início, Quem Somos, Nossas Ações, Esporte, Acervo, Como Ajudar |
| **Institucional** | Lei de Incentivo, Transparência, Instalações, Contato |
| **Contato** | 📍 Praia do Sagi, Baía Formosa/RN · 📸 @s.e.r_sagi · ✉️ sersagi2025@gmail.com · 📞 (84) 98655-3747 |

**Dados usados (oficiais):**
- Endereço: Praia do Sagi, Baía Formosa/RN
- Instagram: `@s.e.r_sagi` · WhatsApp: (84) 98655-3747 (link `wa.me/5584986553747`)
- E-mail: `sersagi2025@gmail.com`

**Detalhes técnicos:**
- O rodapé usa **texto** (não o logo em imagem) — o logo é escuro e não ficaria legível no fundo escuro do rodapé.
- O formulário de newsletter reusa o `data-form-type="newsletter"` → grava na tabela `newsletter` do Supabase (funciona em qualquer página).
- O link "Início" usa `href="./"` (consistente com a sessão 3).

**Arquivos:** `_rodape.py` (gerador) aplicado em todos os `*.html` (28 arquivos).

**Verificação:** 28/28 páginas com copyright e newsletter · tags balanceadas · páginas HTTP 200.

> 🟢 **Ajuste posterior (mesmo dia):** o fundo do rodapé era `bg-slate-950` (quase preto). A pedido, trocado para **`bg-leaf`** (o verde `#2e7d4f` do degradê do hero) — texto branco e detalhes mantidos.

---

### 11/09/2026 (sessão 5) — Correção: Valores e Objetivo apareciam como um card só

**Problema:** na página **Quem Somos**, os cards **"Valores"** e **"Objetivo"** apareciam grudados.
**Causa (bug de HTML):** o `<article>` de "Valores" **nunca foi fechado** — o de "Objetivo" ficou **aninhado dentro** dele. Resultado: a grade (`xl:grid-cols-4`) tinha apenas **3 filhos** em vez de 4.

**Solução:** bloco reescrito com **4 `<article>` irmãos**:
`Missão` · `Visão` · `Valores` · `Objetivo`

**Arquivo:** `quem-somos.html`

**Verificação:** balanceamento de tags OK (`article` 7/7 · `div` 31/31 · `section` 5/5 · `a` 25/25) · 4 cards confirmados · nenhum aninhamento · página HTTP 200.

> 💡 **Lição para o Kilo Code / futuras edições:** ao usar grades (`grid`), cada card precisa dos seus **próprios `<article>`…`</article>`** fechados. Um fechamento faltando faz dois cards virarem um (e o grid perde uma coluna).

---

### 11/09/2026 (sessão 4) — Instalações (hub + seção no Quem Somos + links cruzados)

**Decisão de arquitetura:** a "Arena de Futevôlei e Vôlei" não deveria virar sub-card de uma modalidade só (duplicaria texto). Optou-se por **Opção A + link cruzado**:
- Hub próprio de **Instalações** (mostra a estrutura para parceiros/Lei de Incentivo)
- **Link cruzado** das modalidades para onde acontecem (sem duplicar conteúdo)

**Criado:** `instalacoes.html` — hub com 4 cards (apontam para páginas que **já existiam**):
`arena-futevolei-volei.html` · `consultorio-odontologico.html` · `estudio-musculacao.html` · `escola-jiu-jitsu.html`

**Seção nova no `quem-somos.html`:** "Nossas instalações" (entre "Todos somos Sagi" e "Fundadores") — 4 cards compactos (só ícone + texto, sem imagem para não duplicar o visual) + botão para `instalacoes.html`.

**Link cruzado adicionado em:** `volei.html` e `futevolei.html` → caixa **"Onde acontece: Arena de Futevôlei e Vôlei"** com link para a página da arena.

**`js/main.js`:** nova lista `quemSomosSub = ['instalacoes.html']` — o menu destaca **"Quem Somos"** quando se está na página de Instalações (e a lógica virou `else if` para não haver conflito entre listas).

**Verificação:** 28/28 páginas HTTP 200 · 4 cards do hub OK · seção presente · links cruzados OK · **zero links quebrados**.

> 📌 **Onde fica o acesso:** a Instalações **não** está no menu principal (para não inchar). O caminho é **Quem Somos → seção "Nossas instalações"** e o link cruzado nas modalidades.

---

### 11/09/2026 (sessão 3) — URL do Início sem "index.html"

**Problema:** ao clicar em "Início" no menu, a barra de endereços mostrava `.../index.html`.

**Solução:** todos os links do menu/logo que apontavam para `index.html` passaram a apontar para a **raiz da pasta** (`./`). O servidor entrega o `index.html` automaticamente, e a URL fica limpa:
- Antes: `http://127.0.0.1:5501/index.html` ❌
- Agora: `http://127.0.0.1:5501/` ✅ *(e no site publicado: `bimbord.github.io/projeto_ser_sagi/`)*

**Escopo:** **83 links ajustados em 27 páginas** (logo + menu desktop + menu mobile + botões "voltar para o Início").

**Arquivos alterados:**
- Todos os `*.html` (27 arquivos) — `href="index.html"` → `href="./"`
- `js/main.js` — `setupActiveLinks()` agora entende o `./` como "index.html" (senão o menu não destacaria "Início" na home)

> ⚠️ **Atenção para quem editar:** se criar páginas novas, o link do Início deve ser `href="./"` (não `index.html`), e o link precisa continuar tendo o atributo `data-page-link` para o destaque do menu funcionar.

---

### 11/09/2026 (sessão 2) — Hierarquia de navegação: pilar → página → sub-página

**Pedido:** os cards da home precisam levar para páginas próprias, com sub-cards quando houver submodalidades.

**Criadas 7 páginas novas:**

| Página nova | O que é |
|---|---|
| `esporte.html` | **Hub Esporte** — banner + 6 cards de modalidade |
| `volei.html` | Modalidade: Vôlei |
| `futevolei.html` | Modalidade: Futevôlei |
| `natacao.html` | Modalidade: Natação |
| `danca.html` | Modalidade: Dança |
| `educacao.html` | Página de Educação (idiomas, informática, sustentabilidade) |
| `cultura.html` | Página de Cultura (origens indígenas, convivência, ações solidárias) |

**Cards da home (pilares) — destinos atualizados:**

| Card | Antes | Agora |
|---|---|---|
| Saúde | `consultorio-odontologico.html` | *(sem mudança)* |
| Esporte | `acoes.html` | **`esporte.html`** |
| Educação | `acoes.html` | **`educacao.html`** |
| Cultura | `acoes-solidarias.html` | **`cultura.html`** |
| Preservação | `preservacao-ambiental.html` | *(sem mudança)* |

**Hub Esporte — 6 cards de modalidade** (todos com página própria):
`escola-jiu-jitsu.html` · `volei.html` · `futevolei.html` · `estudio-musculacao.html` · `natacao.html` · `danca.html`

**Arquivos alterados:** `index.html` (destinos), `js/main.js` (lista `acoesSub` ampliada para o menu destacar "Nossas Ações" nas novas páginas).

**Verificação:** 27/27 páginas HTTP 200 · 5 pilares OK · 6 modalidades OK · **zero links quebrados**.

> 💡 **Observação:** a página antiga `arena-futevolei-volei.html` continua existindo (fala da arena como espaço).
> Ela **não** está no hub Esporte — se quiser aproveitá-la ou retirá-la, é só falar.

---

### 11/09/2026 — Sessão: correções, recuperação e navegação

#### 1. Grade do Acervo com dados reais (correção de bug)
- **Problema:** quando a tabela `arquivo` tinha fotos reais, os cards apareciam em **coluna única**.
- **Causa:** o Tailwind Play CDN não gera CSS para conteúdo injetado via JS.
- **Solução:** classe `.archive-grid` (CSS puro, responsiva 3/2/1 colunas).
- **Arquivos:** `css/style.css` (nova classe), `js/main.js` (`renderArchive` usa `.archive-grid`).

#### 2. Página do Consultório Odontológico — seção de galeria
- Adicionada a seção **"O consultório em imagens"** com **6 imagens ilustrativas** (todas com badge) + botão para o acervo de Saúde.
- **Arquivo:** `consultorio-odontologico.html`
- ⏳ **Pendente:** trocar as ilustrativas por fotos reais.

#### 3. Home — cards dos pilares agora são links
Os 5 cards da seção **"Nossos pilares"** deixaram de ser estáticos e passaram a levar para as ações:

| Card (home) | Vai para |
|---|---|
| Saúde | `consultorio-odontologico.html` |
| Esporte | `acoes.html` *(tem 3 ações: musculação, jiu-jitsu, arena)* |
| Educação | `acoes.html` *(ainda não existe página específica de educação)* |
| Cultura | `acoes-solidarias.html` |
| Preservação | `preservacao-ambiental.html` |

- Cada card ganhou o texto **"Saiba mais →"** e efeito de hover.
- **Arquivos:** `index.html` (5 cards viraram `<a>`), `css/style.css` (`a.home-card`, `.home-card__cta`).
- 💡 **Ajustável:** se quiser outro destino para algum pilar, é só dizer.

#### 4. Home — título padronizado
- **Antes:** `Instituto S.E.R. Sagi | Transformação social em Praia do Sagi`
- **Depois:** `Início | Instituto S.E.R. Sagi — Transformação social em Praia do Sagi`
- **Motivo:** todas as outras páginas seguem o padrão `Nome da Página | Instituto S.E.R. Sagi`.
- **Arquivo:** `index.html`

#### 5. Ferramentas criadas (pasta `scripts/`)
| Script | Para que serve |
|---|---|
| `upload_r2.py` | Subir arquivo pro R2 / listar / apagar (`--list`, `--delete`, `--delete-prefix`) |
| `publicar.py` | **Subir + registrar no banco em 1 comando** (modo único e modo lote de pasta) |
| `_check_site.py` | Verifica páginas, logos, links e conexão do site |
| `_comparar_github.py` | Compara a pasta local com o repositório do GitHub (hash por arquivo) |
| `_sync_drive.py` | Sincroniza a pasta de trabalho com o backup no Google Drive |

#### 6. Documentação criada/atualizada (pasta `docs/`)
| Arquivo | Conteúdo |
|---|---|
| `pendencias.md` | Lista viva + resumo rápido no topo + item de manutenção pós-entrega |
| `troubleshooting-local.md` | CCleaner quebrou o Live Server (arquivos restaurados) + alternativa sem extensão |
| `infraestrutura-midias.md` | R2 + Supabase + ferramentas + segurança |
| `fluxo-importacao-midias.md` | Tutorial de como publicar fotos/vídeos |
| `supabase-schema.sql` | SQL das 7 tabelas e políticas RLS |

---

## 🧭 Estado dos dados

- **Bucket R2:** `midias-ser-sagi` — atualmente **só com as pastas vazias** (`fotos/`, `videos/`, `acervo/`, `docs/`). Nenhuma mídia real publicada ainda.
- **Supabase (tabela `arquivo`):** **vazia** (linhas de teste removidas). O Acervo exibe os 6 cards ilustrativos estáticos.
- **Consequência:** enquanto não houver fotos reais, o site mostra o conteúdo ilustrativo com badges — que é o comportamento esperado nesta fase.

---

## 🚦 O que falta (visão rápida)

1. **Fotos reais** (com autorização de imagem dos responsáveis) → usar `python scripts/publicar.py`
2. **Exportar o Instagram** `@s.e.r_sagi` para popular o acervo
3. **Domínio próprio** (`institutosersagi.org.br`) + e-mail institucional
4. **Definir o fluxo de alimentação** (WhatsApp / Drive compartilhado / painel)
5. **Galeria nas outras 5 páginas de ações** (só o Consultório tem hoje)

*(Detalhes e dependências em `docs/pendencias.md`.)*

---

## 🟢 Sessão 7 — rodapé + hub de Educação (14/09/2026)

### Rodapé (finalizado)
- **Cor de fundo:** `bg-slate-950` → testado `bg-leaf` (não aprovado) → **`bg-oceanDeep`** (azul-petróleo escuro, igual às CTAs). Aplicado nas 28 páginas.
- **Contato clicável:** endereço → Google Maps · e-mail → Gmail (`mail.google.com/mail/?view=cm`) · telefone → `tel:+5584986553747`.
- **Descrição encurtada** para "Transformação social em Praia do Sagi".
- **Redes:** Instagram · Facebook (`facebook.com` provisório) · YouTube (`youtube.com` provisório) · WhatsApp. ⏳ *Aguardando URLs definitivas de Facebook/YouTube do cliente.*
- **Crédito:** "Desenvolvido por: lthomassilver@gmail.com" (mailto). Removida a frase "Uma causa em prol da infância e da comunidade do Sagi."

### Educação (hub novo)
- `educacao.html` reescrita como **hub** (estilo do Esporte) com **4 cards**: Inglês, Espanhol, Informática, Sustentabilidade e Meio Ambiente.
- **4 sub-páginas criadas:** `ingles.html`, `espanhol.html`, `informatica.html`, `sustentabilidade.html` (cada uma com banner + descrição + "O que oferecemos" + CTA).
- `js/main.js`: as 4 novas páginas adicionadas a `acoesSub` (destaque no menu "Nossas Ações").
- Cards em **HTML estático** (convenção — Tailwind CDN não gera grade via JS).

---

## 🟢 Sessão 8 — Servidor de Mídias + ajuste na home (16/09/2026)

### Ajuste de texto (home)
- Botões do hero em `index.html`: "Conheça Nossos Projetos" → **"Conheça Nossas Ações"** · "Apoie" → **"Apoie Esse Projeto"**

### Servidor de Mídias (resolve o item 4 das pendências — fluxo de alimentação)
- **Fase 1:** pasta compartilhada **`Instituto SER Sagi - Midias`** no Google Drive do Bimbord (`Imagens\` / `Videos\` / `Documentos\` + LEIA-ME para a ONG), compartilhada com a ONG como **Editor**.
- **Fase 2:** pasta espelho **`Instituto SER Sagi - PARA O SITE`** (uma subpasta por categoria do site; **não** compartilhada) + script **`scripts/servidor_midias.py`** com `--status`, `--dry-run` e `--publicar`.
- Categoria vem do nome da pasta, título e data vêm do nome do arquivo, controle de duplicidade por hash, manifesto guardado no Drive.
- Teste real ponta a ponta: publicou, apareceu no R2 e no Supabase, deduplicou — e o teste foi **limpo** (tabela `arquivo` de volta a 0 linhas).
- Documentação: **`docs/servidor-midias.md`** (novo).

### Fotos reais publicadas no Acervo (3 primeiras)
- Publicadas pelo novo pipeline: **fachada do Instituto** (Esporte), **consultório odontológico** (Saúde), **placa da Aldeia Sagi Jacu** (Preservação) — ids **8, 9, 10**.
- Origem: `img/arquivo/` (imagens extraídas do PDF de apresentação). **Otimizadas antes de subir**: a fachada saiu de **6,10 MB para 0,22 MB** (JPEG, 1600px).
- Títulos e descrições foram refinados direto no banco (a anon key não edita — usada a `service_role` local).

### ⚠️ Correção estrutural no Acervo (bug pego no teste)
- **Problema:** ao entrar o primeiro registro real, o `renderArchive` substituía **todo** o conteúdo do container — e os **6 cards de categoria** (links para `acervo-*.html`) desapareciam da página. Confirmado no DOM: zero links.
- **Correção:** os cards de categoria agora vivem em `data-render="archive-categorias"` (o JS não toca) e a grade de registros reais ganhou seção própria (`#archive-registros` + `data-render="archive"`), oculta quando não há fotos. Os filtros foram para junto dos registros.
- **Regra para futuras edições:** nunca colocar conteúdo estático dentro de um `data-render="..."` que o JS reescreve.
- Verificado no browser: 6 links de categoria no DOM · 3 fotos reais carregando · filtro "Saúde" reduz para 1 card · `renderArchive([])` esconde a seção.

### Pendente nesta frente
- Triagem das outras ~62 imagens de `img/arquivo/` (lote misto: foto boa + print de obra/baixa qualidade) antes de qualquer publicação.
- **Não usar** fotos com pessoa identificável (ex.: o paciente na cadeira odontológica).


### ⚠️ Para lembrar (não repetir o erro)
- A **anon key do Supabase não apaga nem edita** — `DELETE`/`PATCH` devolvem 200/204 **sem efeito**. Só **service_role** (local) ou **Table Editor** resolvem.

### Arquivos mexidos nesta sessão (para não conflitar com o Kilo Code)
`index.html` · `scripts/_check_site.py` · `scripts/servidor_midias.py` (novo) · `docs/servidor-midias.md` (novo) · `docs/infraestrutura-midias.md` · `docs/pendencias.md`

