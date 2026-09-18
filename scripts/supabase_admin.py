# -*- coding: utf-8 -*-
"""
Credenciais de ADMIN do Supabase (service_role) — leitura local.

A chave NUNCA vai para o repositório nem para o site. Ela fica em:
    C:/Users/PRE-IMPRESSOR/R2/.supabase-sagi.env
ou na variável de ambiente SUPABASE_SERVICE_ROLE_KEY.

Uso nos scripts:
    from supabase_admin import admin_disponivel, admin_headers, SUPABASE_URL
"""
import os
import re

ARQUIVOS = [
    r"C:/Users/PRE-IMPRESSOR/R2/.supabase-sagi.env",
    r"C:/Users/PRE-IMPRESSOR/R2/.r2-sagi.env",
]
INVALIDOS = ("", "COLOQUE_AQUI", "colocar_aqui", "None", "none")


def _ler_arquivo(chave):
    for caminho in ARQUIVOS:
        if not os.path.isfile(caminho):
            continue
        try:
            with open(caminho, encoding="utf-8", errors="ignore") as f:
                for linha in f:
                    linha = linha.strip()
                    if not linha or linha.startswith("#"):
                        continue
                    m = re.match(r"^(?:export\s+)?([A-Za-z0-9_]+)\s*=\s*(.*)$", linha)
                    if m and m.group(1).upper() == chave.upper():
                        return m.group(2).strip().strip('"').strip("'")
        except OSError:
            continue
    return None


def _obter(*nomes):
    for n in nomes:
        v = os.environ.get(n) or _ler_arquivo(n)
        if v and v not in INVALIDOS and not v.upper().startswith("COLOQUE"):
            return v
    return None


SUPABASE_URL = _obter("SUPABASE_URL") or "https://icrasqxbxmqbnelmkrei.supabase.co"
SERVICE_KEY = _obter("SUPABASE_SERVICE_ROLE_KEY", "SERVICE_ROLE_KEY", "SUPABASE_KEY_ADMIN")
ARQUIVO_ESPERADO = ARQUIVOS[0]

INSTRUCOES = (
    "Chave service_role não encontrada.\n"
    f"  1. Abra o arquivo: {ARQUIVO_ESPERADO}\n"
    "  2. No Supabase: Project Settings -> API -> Project API keys -> service_role (Reveal)\n"
    "  3. Cole no lugar de COLOQUE_AQUI (mesma linha, sem aspas), salve e feche\n"
    "  4. NÃO cole a chave no chat."
)


def admin_disponivel():
    return bool(SERVICE_KEY)


def admin_headers(json_body=False):
    """Cabeçalhos com a service_role. Levanta erro claro se a chave faltar."""
    if not SERVICE_KEY:
        raise RuntimeError(INSTRUCOES)
    h = {"apikey": SERVICE_KEY, "Authorization": f"Bearer {SERVICE_KEY}"}
    if json_body:
        h["Content-Type"] = "application/json"
    return h
