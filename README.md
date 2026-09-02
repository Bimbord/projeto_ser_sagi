# Instituto S.E.R. Sagi — Site Institucional Multipágina

## Nome do projeto
Site institucional do **Instituto S.E.R. Sagi (Sabedoria, Esforço, Resultado)**, voltado para apresentação institucional, captação de parceiros, doações, voluntariado, transparência e apresentação estratégica via Lei de Incentivo ao Esporte.

## Objetivo do projeto
Estruturar uma presença digital profissional, acolhedora e confiável para o Instituto S.E.R. Sagi, com foco em:
- credibilidade institucional;
- captação de empresas parceiras via Lei de Incentivo ao Esporte;
- captação de doações e voluntariado;
- comunicação de impacto social;
- organização da transparência institucional;
- apresentação institucional convincente para parceiros e apoiadores.

## Funcionalidades concluídas
- Site multipágina responsivo e mobile-first.
- Navegação principal com páginas separadas.
- Identidade visual institucional com paleta inspirada em mar, natureza e acolhimento.
- Hero da home refinado com visual mais premium, melhor hierarquia visual e composição institucional mais forte.
- Microinterações visuais em cards e botões para melhorar percepção de qualidade.
- Nova seção estratégica “Por que apoiar o S.E.R. Sagi” na home.
- Página inicial com hero, números de impacto, pilares, projeto principal, depoimentos, parceiros, galeria institucional e newsletter.
- Página “Quem Somos” com história, missão, visão, valores e narrativa institucional.
- Página “Nossas Ações” com detalhamento dos pilares e do projeto principal.
- Página “Como Ajudar” com jornadas para parceria, doação, voluntariado e doação de materiais.
- Página especial “Lei de Incentivo ao Esporte” com argumentação de captação e formulário específico.
- Página “Transparência” com estrutura editorial para relatórios, governança, proteção à infância e parceiros.
- Página “Contato” com canais institucionais e formulário funcional.
- Formulário funcional de leads em “Como Ajudar”.
- Formulário funcional de leads na página “Lei de Incentivo ao Esporte”.
- Formulário funcional de contato institucional.
- Formulário funcional de newsletter.
- Estrutura dinâmica para renderização de depoimentos, parceiros e galeria via tabelas.
- Fallback visual com dados fictícios para apresentação enquanto os dados reais não forem inseridos.
- Armazenamento via RESTful Table API.
- CSS compartilhado em arquivo próprio.
- JavaScript compartilhado para menu mobile, links ativos, submissão de formulários e renderização dinâmica.
- Estrutura semântica com boas práticas de acessibilidade.

## URIs funcionais atuais
### Páginas principais
- `/index.html`
- `/quem-somos.html`
- `/acoes.html`
- `/acervo.html` (acervo de fotos e vídeos + destaques do mês na home)
- `/como-ajudar.html`
- `/lei-incentivo.html`
- `/transparencia.html`
- `/contato.html`

### Âncoras relevantes
- `/como-ajudar.html#parcerias`
- `/como-ajudar.html#doacao`
- `/lei-incentivo.html#formulario-incentivo`

## Funcionalidades ainda não implementadas
- Logo oficial e identidade visual definitiva.
- Inserção de depoimentos reais com fotos e vídeos.
- Inserção de logomarcas reais de parceiros.
- Inserção de imagens reais na galeria institucional.
- Upload/gestão real de documentos de transparência.
- Biblioteca real de arquivos para download.
- Integração com meios de pagamento.
- Dashboard visual com gráficos reais de impacto.
- CMS administrativo.
- SEO avançado por Open Graph, schema.org e social cards completos.
- Conteúdo institucional final revisado juridicamente, especialmente na comunicação fiscal da Lei de Incentivo.

## Próximos passos recomendados
1. Inserir logo oficial e fotos reais da instituição.
2. Alimentar tabelas com depoimentos reais de mães, pais, crianças e parceiros.
3. Substituir marcas fictícias por logomarcas reais de apoiadores.
4. Alimentar a galeria com imagens reais autorizadas.
5. Criar biblioteca documental real na área de transparência.
6. Adicionar vídeos institucionais e depoimentos em destaque.
7. Evoluir a área de doação para integração com gateway/pagamento externo permitido.
8. Revisar juridicamente a comunicação da Lei de Incentivo ao Esporte.

## Estrutura de navegação atual
- Início
- Quem Somos
- Nossas Ações
- Como Ajudar
- Lei de Incentivo
- Transparência
- Contato

## Tecnologias utilizadas
- HTML5
- CSS3
- JavaScript vanilla
- Tailwind CSS via CDN
- Font Awesome via CDN
- Google Fonts (Inter)
- RESTful Table API interna da plataforma

## Modelos de dados, estruturas e armazenamento
As informações do site são persistidas usando a **RESTful Table API** da plataforma.

### Tabela: `contatos`
Campos:
- `id` (text)
- `nome` (text)
- `email` (text)
- `telefone` (text)
- `assunto` (text)
- `mensagem` (rich_text)
- `origem_pagina` (text)
- `aceite_privacidade` (bool)

Uso:
- formulário da página `/contato.html`

### Tabela: `leads_apoio`
Campos:
- `id` (text)
- `nome` (text)
- `empresa` (text)
- `email` (text)
- `telefone` (text)
- `perfil` (text)
- `interesse` (text)
- `mensagem` (rich_text)
- `origem_pagina` (text)
- `aceite_privacidade` (bool)

Uso:
- formulário da página `/como-ajudar.html`
- formulário da página `/lei-incentivo.html`

### Tabela: `newsletter`
Campos:
- `id` (text)
- `nome` (text)
- `email` (text)
- `perfil` (text)
- `aceite_comunicacao` (bool)

Uso:
- formulário da home em `/index.html`

### Tabela: `depoimentos`
Campos:
- `id` (text)
- `nome` (text)
- `perfil` (text)
- `titulo` (text)
- `texto` (rich_text)
- `local` (text)
- `destaque` (bool)

Uso:
- renderização dinâmica da seção de depoimentos na home

### Tabela: `parceiros`
Campos:
- `id` (text)
- `nome` (text)
- `categoria` (text)
- `logo_texto` (text)
- `descricao` (text)
- `site_url` (text)
- `destaque` (bool)

Uso:
- renderização dinâmica das seções de parceiros na home e transparência

### Tabela: `galeria`
Campos:
- `id` (text)
- `titulo` (text)
- `categoria` (text)
- `descricao` (text)
- `imagem_url` (text)
- `destaque` (bool)

Uso:
- renderização dinâmica da galeria institucional na home

### Tabela: `arquivo`
Campos:
- `id` (text)
- `titulo` (text)
- `tipo` (text: `foto` ou `video`)
- `categoria` (text: Esporte, Saúde, Educação, Cultura, Preservação, Eventos)
- `descricao` (text)
- `imagem_url` (text) — capa/thumbnail
- `video_url` (text) — link do vídeo (YouTube não listado, etc.)
- `data_registro` (text) — data do evento
- `destaque` (bool) — marca o item para a seção "Destaques do mês" da home

Uso:
- renderização da página `/acervo.html` (com filtros por categoria)
- renderização da seção "Destaques do mês" na home (itens com `destaque = true`, máx. 3)

## Arquivos principais do projeto
- `index.html`
- `quem-somos.html`
- `acoes.html`
- `como-ajudar.html`
- `lei-incentivo.html`
- `transparencia.html`
- `contato.html`
- `css/style.css`
- `js/main.js`
- `README.md`

## URLs públicas
### Produção
Ainda não publicada.

### Endpoints de dados usados no frontend
- `POST /tables/contatos`
- `POST /tables/leads_apoio`
- `POST /tables/newsletter`
- `GET /tables/depoimentos`
- `GET /tables/parceiros`
- `GET /tables/galeria`

## Fontes de conteúdo utilizadas
- Briefing fornecido pelo usuário.
- Informações extraídas do contexto da apresentação do Instituto S.E.R. Sagi compartilhada na conversa.
- Boas práticas de UX, arquitetura de informação e design institucional para organizações do Terceiro Setor.

## Observações importantes
- A análise automática completa do PDF não pôde ser concluída pela ferramenta no ambiente atual.
- O projeto foi evoluído com base nas informações detalhadas fornecidas pelo usuário e no conteúdo parcial do documento.
- Depoimentos, parceiros e galeria já possuem estrutura dinâmica, mas atualmente contam com fallback demonstrativo caso não existam dados cadastrados.
- O conteúdo fiscal/jurídico da Lei de Incentivo deve ser revisado antes da publicação final.

## Publicação
Para publicar o website e colocá-lo no ar, utilize a **aba Publish** da plataforma.