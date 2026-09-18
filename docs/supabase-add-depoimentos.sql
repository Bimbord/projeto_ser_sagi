-- ============================================================
-- Depoimentos com mídia (mensagem + imagem/vídeo + legenda)
-- Rodar no Supabase → SQL Editor → New query → Run
-- ============================================================
-- A mídia normalmente vem da pasta home/depoimentos do Drive
-- (casada pelo NOME do arquivo com o campo `nome`).
-- imagem_url e video_url são OPCIONAIS: servem para apontar
-- direto para uma URL externa (ex.: vídeo no YouTube), que
-- tem prioridade sobre a mídia do Drive.
-- ============================================================

alter table public.depoimentos
  add column if not exists imagem_url text,
  add column if not exists video_url  text,
  add column if not exists legenda    text,
  add column if not exists destaque   boolean not null default false,
  add column if not exists ordem      integer not null default 0;

-- ordem: controla a sequência (menor primeiro)
-- destaque = true: aparece na home (máx. 3)

create index if not exists depoimentos_ordem_idx
  on public.depoimentos (destaque desc, ordem asc, id asc);

-- conferência
select column_name, data_type
  from information_schema.columns
 where table_schema = 'public'
   and table_name = 'depoimentos'
 order by ordinal_position;
