-- ============================================================
-- Adiciona a coluna `secao` na tabela `arquivo`
-- Motivo: cada imagem agora pertence a uma PASTA DE SECAO dentro da
-- categoria (ex.: saude/hero, saude/carrossel, saude/galeria).
-- Rodar no SQL Editor do Supabase (projeto sersagi-site).
-- ============================================================

alter table public.arquivo
  add column if not exists secao text;

comment on column public.arquivo.secao is
  'Subpasta de secao dentro da categoria (ex.: hero, carrossel, galeria, imagem principal)';

-- Índice para o site filtrar por categoria + secao
create index if not exists arquivo_categoria_secao_idx
  on public.arquivo (categoria, secao);

-- Conferir:
-- select categoria, secao, count(*) from public.arquivo
--   where deleted = false group by 1,2 order by 1,2;
