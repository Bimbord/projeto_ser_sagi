# Pendências — Instituto S.E.R. Sagi

> Lista viva de pendências do projeto. Atualizar conforme avançar.

## Pendências ativas (lembrar nas próximas sessões)

### 1. Banco + tabela `arquivo` no Supabase (banco do site) — ✅ FEITO (31/08)
- O site é de terceiros (ONG) — o banco dele vai no **Supabase** do Bimbord, em **projeto separado** (`sersagi-site`) — NÃO no Lite Pro (sistema da BBDPRiNT)
- ✅ Projeto criado + 7 tabelas + políticas RLS (SQL em `docs/supabase-schema.sql`)
- ✅ `js/main.js` conectado ao Supabase (URL + anon key); formulários gravam; `arquivo`/`depoimentos`/`parceiros` leem
- ✅ Primeira foto real registrada e testada (Home + Acervo renderizando do Supabase)
- ✅ **Registrador manual** (`scripts/publicar.py`): 1 comando sobe pro R2 + grava na tabela (testado, devolve id + URL)
- ⚠️ **Pendência pequena:** apagar as linhas de teste `id=2` e `id=3` ("Teste publicador...") no **Table Editor** do Supabase — apontam pra arquivos já removidos do R2 (a chave anon não pode apagar — RLS)

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

## Convenções do projeto (não esquecer)
- **Conteúdo ilustrativo/demonstrativo sempre marcado** com badge "Ilustrativo" ou "Imagem ilustrativa" (site não vai direto a fiscalizadores; conteúdo fictício é aceito a título de preenchimento da ideia, mas SEMPRE destacado)
- Pasta ativa de trabalho: `projeto_SER_Sagi - Hermes` (a `projeto_SER_Sagi` é a versão anterior, arquivada)
- Dados oficiais (números, missão/visão/objetivo, 7% PF na Lei de Incentivo) vieram do PDF "APRESENTAÇÃO INSTITUTO SER SAGI.pdf"
- **Grades/cards em HTML estático, NÃO via JS**: o Tailwind Play CDN não gera CSS para conteúdo injetado via JavaScript (cards ficam em coluna única). Seção de cards da página Acervo (`acervo.html`) é o exemplo: 6 cards estáticos + grid `md:grid-cols-2 xl:grid-cols-3`; o JS (`renderArchive`) só sobrescreve quando a tabela `arquivo` tiver dados reais.
