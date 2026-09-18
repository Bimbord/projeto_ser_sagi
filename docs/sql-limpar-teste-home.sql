-- ============================================================
-- Limpeza dos testes da FASE 5 (17-18/09/2026)
-- ============================================================
-- Foram publicadas imagens de TESTE para validar:
--   PARTE A → pastas home/hero (ids 30,31) e home/joia-da-coroa (id 32)
--   PARTE B → pastas home/pilares (id 34), home/numeros (id 33)
--             e home/como-ajudar (id 35)
--
-- A anon key NAO consegue atualizar nem apagar: o RLS bloqueia e o
-- PostgREST devolve HTTP 204 mesmo assim (0 linhas afetadas) — por
-- isso este SQL roda no painel.
--
-- Supabase → SQL Editor → New query → Run.
-- ============================================================

-- 1) CONFERE o que sera marcado (deve listar 6 linhas; a PARTE A ja saiu)
select id, titulo, categoria, secao, deleted
  from public.arquivo
 where categoria = 'Home'
   and id in (30, 31, 32, 33, 34, 35)
 order by id;

-- 2) marca como excluido (o site filtra deleted = false)
update public.arquivo
   set deleted = true
 where categoria = 'Home'
   and id in (30, 31, 32, 33, 34, 35);

-- 3) CONFERE: deve voltar 0
select count(*) as restantes_ativos
  from public.arquivo
 where categoria = 'Home'
   and deleted = false;
