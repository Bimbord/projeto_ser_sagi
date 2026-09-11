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

## 📄 Estrutura atual do site (20 páginas)

| Arquivo | Página |
|---|---|
| `index.html` | Início (home) |
| `quem-somos.html` | Quem Somos |
| `acoes.html` | Nossas Ações (6 cards → páginas individuais) |
| `consultorio-odontologico.html` | Ação: Consultório Odontológico |
| `estudio-musculacao.html` | Ação: Estúdio de Musculação |
| `escola-jiu-jitsu.html` | Ação: Escola de Jiu-Jitsu |
| `arena-futevolei-volei.html` | Ação: Arena de Futevôlei e Vôlei |
| `acoes-solidarias.html` | Ação: Ações Solidárias |
| `preservacao-ambiental.html` | Ação: Preservação Ambiental |
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
