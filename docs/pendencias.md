# Pendências — Instituto S.E.R. Sagi

> Lista viva de pendências do projeto. Atualizar conforme avançar.

## ⚡ COMEÇAR POR AQUI (resumo rápido)

**O site está no ar e funcional.** O que falta é conteúdo real e acabamento:

| # | O que | Esforço | Depende de |
|---|---|---|---|
| 2 | **Fotos reais** nas atividades e no Acervo | médio | autorização de imagem dos responsáveis |
| 2b | Exportar o **Instagram** para popular o acervo | médio | exportação manual de dados do Instagram |
| 3 | **Domínio próprio** (institutosersagi.org.br) | baixo | compra no registro.br |
| 4 | Definir **fluxo de alimentação** (manutenção pós-entrega) | médio | decisão do Bimbord/cliente |

**Ferramenta pronta para alimentar:** `python scripts/publicar.py` (sobe pro R2 + grava no banco)
**Guia:** `docs/fluxo-importacao-midias.md`

---

## Pendências ativas (lembrar nas próximas sessões)

### 1. Banco + tabela `arquivo` no Supabase (banco do site) — ✅ FEITO (31/08)
- O site é de terceiros (ONG) — o banco dele vai no **Supabase** do Bimbord, em **projeto separado** (`sersagi-site`) — NÃO no Lite Pro (sistema da BBDPRiNT)
- ✅ Projeto criado + 7 tabelas + políticas RLS (SQL em `docs/supabase-schema.sql`)
- ✅ `js/main.js` conectado ao Supabase (URL + anon key); formulários gravam; `arquivo`/`depoimentos`/`parceiros` leem
- ✅ Primeira foto real registrada e testada (Home + Acervo renderizando do Supabase)
- ✅ **Registrador manual** (`scripts/publicar.py`): 1 comando sobe pro R2 + grava na tabela (testado, devolve id + URL)
- ✅ Linhas de teste removidas do Supabase (11/09)

### 1b. Limpeza no bucket R2 — ✅ FEITO (31/08)
- ✅ Pasta `arcevo/` (typo) corrigida → `acervo/`
- ✅ Arquivos de teste (`Regras-001.png`, `teste-upload..png`) removidos
- ✅ Ferramenta ganhou modos `--list`, `--delete`, `--delete-prefix` (`scripts/upload_r2.py`)

### 2. Fotos reais (com autorização de imagem)
- Substituir as imagens ilustrativas (badge "Imagem ilustrativa") por fotos reais das atividades
- **Obrigatório:** autorização de uso de imagem dos responsáveis (crianças/adolescentes — ECA + LGPD)
- As fotos do PDF de apresentação NÃO servem (prints de baixa qualidade e obras em andamento)

### 2b. Instagram @s.e.r_sagi — exportação adiada
- Feed bloqueado sem login (HTTP 429). Fazer **exportação de dados** (Configurações → Baixar suas informações → **JSON**) do perfil `s.e.r_sagi`
- Colocar o conteúdo (posts_*.json + media/) em `instagram-scrap/export/`, rodar `python process_export.py`
- Processador já pronto em `instagram-scrap/process_export.py` (gera inventario.md/csv + consolida fotos em extract_final/)
- **Adiado:** resolver depois, na fase de trocar TODOS os dados reais
- Varredura parcial já salva em `docs/instagram-varredura.md` (foto de perfil + bio + insights da marca)

### 3. Domínio próprio
- `institutosersagi.org.br` (ou `.com.br`) via registro.br — ~R$ 40/ano
- E-mail institucional: Zoho Mail (grátis, até 5 caixas) ou via hospedagem
- Ver detalhes em `docs/estrategia-tecnica.md`

### 4. Alimentação contínua / manutenção pós-entrega
- O cliente já sinalizou que deve ficar com **manutenção mensal** — pensar no fluxo desde já
- **Decisão pendente:** como o conteúdo entra no site?
  - **A) Registrador manual** (`scripts/publicar.py`) — já pronto, funciona hoje
  - **B) Fluxo via WhatsApp** — a ONG manda fotos, agente/script cataloga em lote
  - **C) Painel self-service** — a ONG loga e sobe sozinha (mais desenvolvimento)
  - *Recomendação: começar no A, evoluir para B e depois C conforme o volume*
- **Definir por escrito o escopo do contrato**: o que está incluso (X atualizações/mês, backups, suporte) — evita virar trabalho infinito
- Documentar tudo como **case de portfólio**: "site + gestão de conteúdo para ONG"

## 🚨 Incidente e backup (11/09/2026)

**O que aconteceu:** o **drive D:** (onde o projeto estava) **morreu** e não voltou. O trabalho foi **recuperado integralmente** do backup automático no **Google Drive**.

**Estado atual (importante):**
| Camada | Onde | Situação |
|---|---|---|
| Pasta de trabalho | `C:\Projetos Code\Projeto SER Sagi\projeto_SER_Sagi - Hermes` | ✅ ativa, é um **repositório git** ligado ao GitHub |
| Repositório (código) | `github.com/Bimbord/projeto_ser_sagi` (branch `main`) | ✅ sincronizado — **este é o backup oficial do código** |
| Site publicado | `bimbord.github.io/projeto_ser_sagi` | ✅ no ar |
| Mídias | Cloudflare R2 (`midias-ser-sagi`) | ✅ intacto |
| Banco | Supabase (`sersagi-site`) | ✅ intacto |
| Backup extra | Google Drive (`projeto_SER_Sagi - Hermes`) | ✅ cópia sincronizada |

**Rotina de trabalho (nova convenção):**
```bash
# após qualquer alteração no site:
git add -A
git commit -m "descrição da mudança"
git push                      # → atualiza GitHub + GitHub Pages

# opcional: sincronizar o backup do Drive
python scripts/_sync_drive.py
```

⚠️ **O `.git` do Google Drive veio vazio** (o Drive não sincroniza pastas internas do git). Se restaurar do Drive, rode o setup do git de novo (`git init` + `remote add` + `fetch` + `reset origin/main`).

---

## Convenções do projeto (não esquecer)

- **Conteúdo ilustrativo/demonstrativo sempre marcado** com badge "Ilustrativo" ou "Imagem ilustrativa" (site não vai direto a fiscalizadores; conteúdo fictício é aceito a título de preenchimento da ideia, mas SEMPRE destacado)
- **Pasta ativa de trabalho:** `C:\Projetos Code\Projeto SER Sagi\projeto_SER_Sagi - Hermes` (a `projeto_SER_Sagi` é a versão anterior, arquivada)
- Dados oficiais (números, missão/visão/objetivo, 7% PF na Lei de Incentivo) vieram do PDF "APRESENTAÇÃO INSTITUTO SER SAGI.pdf"
- **Grades/cards em HTML estático, NÃO via JS**: o Tailwind Play CDN não gera CSS para conteúdo injetado via JavaScript (cards ficam em coluna única). Os cards do Acervo e das Ações são estáticos; o JS (`renderArchive`) só sobrescreve quando a tabela `arquivo` tiver dados reais — e nesse caso usa a classe **`.archive-grid`** (CSS puro em `css/style.css`), NÃO utilitários Tailwind.
- **Credenciais nunca vão para o repositório**: R2 fica em `C:\Users\PRE-IMPRESSOR\R2\.r2-sagi.env` (já no `.gitignore`); a anon key do Supabase é pública por design, mas a `service_role` **nunca** deve ser exposta
