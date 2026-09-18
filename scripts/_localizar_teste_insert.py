# -*- coding: utf-8 -*-
"""
Localiza os registros criados pelo teste de INSERT (18/09/2026) e gera o SQL
de limpeza.

O teste provou quais tabelas aceitam INSERT com a anon key:
    arquivo   -> SIM (201)   <- por isso a publicacao de midia funciona
    contatos  -> SIM (201)
    depoimentos -> NAO (401, RLS)
    parceiros   -> NAO (401, RLS)

Como o INSERT passou em `arquivo` e `contatos`, ficaram 2 registros de lixo
que só saem com SQL (a anon key não apaga).
"""
import sys
import os
import json
import urllib.parse
import urllib.request

BASE = r"G:/.shortcut-targets-by-id/18wGiptBKUmAmmkKHgdfu05TU4y_roWC1/BBDPRINT - BACKUP/BBDPRINT/App BBDPRiNT/PROJETOS/Projeto SER Sagi/projeto_SER_Sagi - Hermes"
sys.path.insert(0, os.path.join(BASE, "scripts"))
from publicar import SUPABASE_URL, SUPABASE_ANON_KEY  # noqa: E402

H = {"apikey": SUPABASE_ANON_KEY, "Authorization": f"Bearer {SUPABASE_ANON_KEY}"}


def buscar(tabela, coluna, valor, extra=""):
    v = urllib.parse.quote(valor)
    url = f"{SUPABASE_URL}/rest/v1/{tabela}?select=id,{coluna}{extra}&{coluna}=eq.{v}"
    req = urllib.request.Request(url)
    for k, val in H.items():
        req.add_header(k, val)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


print("=== registros de teste encontrados ===")
ids_arquivo = [r["id"] for r in buscar("arquivo", "titulo", "ZZZ teste")]
ids_contatos = [r["id"] for r in buscar("contatos", "nome", "ZZZ teste")]
print(f"  arquivo  : {ids_arquivo}")
print(f"  contatos : {ids_contatos}")

# os depoimentos/parceiros foram bloqueados -> nada foi criado
dep = buscar("depoimentos", "nome", "ZZZ Teste Hermes")
par = buscar("parceiros", "nome", "ZZZ Teste Hermes")
print(f"  depoimentos (bloqueado, deve ser vazio): {[r['id'] for r in dep]}")
print(f"  parceiros   (bloqueado, deve ser vazio): {[r['id'] for r in par]}")

sql = ["-- Limpeza dos registros criados no teste de INSERT (18/09/2026)",
       "-- (a anon key insere, mas não apaga — precisa rodar no painel)"]
if ids_arquivo:
    sql.append(f"update public.arquivo  set deleted = true where id in ({', '.join(map(str, ids_arquivo))});")
if ids_contatos:
    sql.append(f"delete from public.contatos where id in ({', '.join(map(str, ids_contatos))});")

print("\n=== SQL DE LIMPEZA ===")
print("\n".join(sql))
