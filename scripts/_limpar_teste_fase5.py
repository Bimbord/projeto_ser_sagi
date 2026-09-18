# -*- coding: utf-8 -*-
"""Limpeza do teste da FASE 5 — tenta marcar os registros de teste como deleted."""
import sys, os, json, urllib.request, urllib.error

BASE = r"G:/.shortcut-targets-by-id/18wGiptBKUmAmmkKHgdfu05TU4y_roWC1/BBDPRINT - BACKUP/BBDPRINT/App BBDPRiNT/PROJETOS/Projeto SER Sagi/projeto_SER_Sagi - Hermes"
sys.path.insert(0, os.path.join(BASE, "scripts"))
from publicar import SUPABASE_URL, SUPABASE_ANON_KEY

IDS = [30, 31, 32]
print("Tentando marcar deleted=true (anon key) nos ids de teste:", IDS)

ok = True
for i in IDS:
    url = f"{SUPABASE_URL}/rest/v1/arquivo?id=eq.{i}"
    req = urllib.request.Request(url, method="PATCH",
                                data=json.dumps({"deleted": True}).encode())
    req.add_header("apikey", SUPABASE_ANON_KEY)
    req.add_header("Authorization", f"Bearer {SUPABASE_ANON_KEY}")
    req.add_header("Content-Type", "application/json")
    req.add_header("Prefer", "return=minimal")
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            print(f"  ✅ id {i} -> HTTP {r.status} (marcado como excluído)")
    except urllib.error.HTTPError as e:
        ok = False
        print(f"  ❌ id {i} -> HTTP {e.code} (anon nao tem permissao de update)")

if ok:
    print("\n✅ Registros de teste escondidos do site.")
else:
    print("\n⚠️  Precisa rodar o SQL no Supabase (voce tem a service_role lá).")
