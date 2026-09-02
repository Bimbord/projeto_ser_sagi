-- ============================================================
-- Instituto S.E.R. Sagi — Esquema do banco do site (Supabase)
-- Onde colar: Supabase → SQL Editor → New query → Run
-- Projeto: sersagi-site (conta Supabase do Bimbord — projeto separado)
-- Data: 31/08/2026
-- ============================================================

-- 1) ARQUIVO — Acervo (fotos e vídeos; imagem_url aponta pro R2)
create table public.arquivo (
  id bigint generated always as identity primary key,
  titulo text not null,
  tipo text not null default 'foto',           -- 'foto' ou 'video'
  categoria text not null,                      -- Esporte, Saúde, Educação, Cultura, Preservação, Eventos
  descricao text,
  imagem_url text,                              -- URL pública do R2
  video_url text,                               -- URL do vídeo (R2 ou YouTube)
  data_registro text,                           -- ex.: 2026-08-31
  destaque boolean not null default false,      -- true = aparece em "Destaques do mês"
  created_at timestamptz not null default now(),
  deleted boolean not null default false
);
create index arquivo_categoria_idx on public.arquivo (categoria);

-- 2) DEPOIMENTOS — depoimentos da home
create table public.depoimentos (
  id bigint generated always as identity primary key,
  nome text not null,
  perfil text,                                  -- Mãe, Pai, Criança...
  titulo text,
  texto text,
  local text,
  created_at timestamptz not null default now(),
  deleted boolean not null default false
);

-- 3) PARCEIROS — parceiros/patrocinadores da home
create table public.parceiros (
  id bigint generated always as identity primary key,
  nome text not null,
  categoria text,                               -- Empresa apoiadora, Patrocinador...
  logo_texto text,                              -- iniciais exibidas no lugar do logo
  descricao text,
  logo_url text,                                -- futuro: logo real (R2)
  created_at timestamptz not null default now(),
  deleted boolean not null default false
);

-- 4) GALERIA — galeria antiga (mantida por compatibilidade)
create table public.galeria (
  id bigint generated always as identity primary key,
  titulo text,
  categoria text,
  descricao text,
  imagem_url text,
  created_at timestamptz not null default now(),
  deleted boolean not null default false
);

-- 5) CONTATOS — formulário de contato
create table public.contatos (
  id bigint generated always as identity primary key,
  nome text,
  email text,
  telefone text,
  assunto text,
  mensagem text,
  origem_pagina text,
  aceite_privacidade boolean not null default false,
  created_at timestamptz not null default now()
);

-- 6) LEADS_APOIO — formulário "Seja parceiro / apoie"
create table public.leads_apoio (
  id bigint generated always as identity primary key,
  nome text,
  empresa text,
  email text,
  telefone text,
  perfil text,
  interesse text,
  mensagem text,
  origem_pagina text,
  aceite_privacidade boolean not null default false,
  created_at timestamptz not null default now()
);

-- 7) NEWSLETTER — cadastro de novidades
create table public.newsletter (
  id bigint generated always as identity primary key,
  nome text,
  email text not null,
  perfil text,
  aceite_comunicacao boolean not null default false,
  created_at timestamptz not null default now()
);

-- ============================================================
-- POLÍTICAS DE SEGURANÇA (RLS) — sem isso o site não consegue
-- ler/escrever com a anon key (padrão do Supabase)
-- ============================================================

-- Conteúdo público: leitura liberada p/ anônimos
alter table public.arquivo enable row level security;
create policy "arquivo_leitura" on public.arquivo for select using (true);
-- Inserção no arquivo liberada por enquanto (alimentação);
-- ⚠️ apertar quando o painel admin com login estiver pronto
create policy "arquivo_escrita" on public.arquivo for insert with check (true);

alter table public.depoimentos enable row level security;
create policy "depoimentos_leitura" on public.depoimentos for select using (true);

alter table public.parceiros enable row level security;
create policy "parceiros_leitura" on public.parceiros for select using (true);

alter table public.galeria enable row level security;
create policy "galeria_leitura" on public.galeria for select using (true);

-- Formulários: anônimos podem INSERIR (mas não ler)
alter table public.contatos enable row level security;
create policy "contatos_insert" on public.contatos for insert with check (true);

alter table public.leads_apoio enable row level security;
create policy "leads_apoio_insert" on public.leads_apoio for insert with check (true);

alter table public.newsletter enable row level security;
create policy "newsletter_insert" on public.newsletter for insert with check (true);
