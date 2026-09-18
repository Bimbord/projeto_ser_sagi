-- ============================================================
-- Limpeza do teste da FASE 5 (17/09/2026)
-- ============================================================
-- Foram publicadas 3 imagens de TESTE (logos) para validar a
-- ligação das pastas home/hero e home/joia-da-coroa.
-- A anon key NAO consegue atualizar (o RLS bloqueia e o PostgREST
-- devolve 204 mesmo assim) — por isso este SQL.
--
-- Rode no Supabase: SQL Editor → New query → Run.
-- ============================================================

-- 1) confere o que sera apagado (deve listar 3 linhas)
select id, titulo, categoria, secao, imagem_url
  from public.arquivo
 where id in (30, 31, 32)
   and categoria = 'Home';

-- 2) marca como excluido (o site filtra deleted = false)
update public.arquivo
   set deleted = true
 where id in (30, 31, 32)
   and categoria = 'Home'
   and secao in ('hero', 'joia-da-coroa');

-- 3) conferencia: deve voltar 0 linha
select count(*) as restantes
  from public.arquivo
 where categoria = 'Home'
   and deleted = false;
