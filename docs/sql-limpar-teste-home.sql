-- ============================================================
-- Limpeza dos testes (17 e 18/09/2026)
-- Supabase → SQL Editor → New query → Run
-- ============================================================
-- Motivo: a anon key INSERE em algumas tabelas, mas NÃO apaga nem
-- atualiza (o RLS bloqueia e o PostgREST devolve HTTP 204/201 sem
-- erro aparente). Por isso a limpeza precisa ser feita aqui.
--
-- Descoberta do teste de 18/09 (qual tabela aceita INSERT com a anon key):
--   arquivo     -> SIM  (é assim que a publicação de mídia funciona)
--   contatos    -> SIM  (é o formulário do site — por design)
--   depoimentos -> NÃO  (RLS)
--   parceiros   -> NÃO  (RLS)
-- ============================================================

-- 1) CONFERE o que será marcado (deve listar 1 linha — o id 36)
select id, titulo, categoria, secao, deleted
  from public.arquivo
 where id = 36
    or (categoria = 'Home' and id in (30, 31, 32, 33, 34, 35))
 order by id;

-- 2) esconde o registro de teste de mídia (id 36)
update public.arquivo
   set deleted = true
 where id = 36;

-- 3) remove o registro de teste do formulário de contato
--    (a tabela contatos permite INSERT mas não SELECT, então o
--     registro existe mesmo não aparecendo na consulta)
delete from public.contatos where nome = 'ZZZ teste';

-- 4) CONFERE: deve voltar 0
select count(*) as restantes_arquivo
  from public.arquivo
 where deleted = false
   and (id = 36 or (categoria = 'Home' and id between 30 and 35));
