# -*- coding: utf-8 -*-
"""Diagnóstico do Live Server: porta, arquivos na pasta e estado do workspace."""
import os, socket, json

BASE = r"C:/Projetos Code/Projeto SER Sagi/projeto_SER_Sagi - Hermes"

print("=== 1) Teste de bind nas portas ===")
for porta in (5500, 5501, 5502):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(("127.0.0.1", porta))
        print(f"  porta {porta}: LIVRE (pode usar)")
    except OSError as e:
        print(f"  porta {porta}: ❌ OCUPADA/BLOQUEADA ({e})")
    finally:
        s.close()

print("\n=== 2) Volume de arquivos na pasta (watcher do Live Server) ===")
total, por_pasta = 0, {}
for raiz, dirs, arqs in os.walk(BASE):
    rel = os.path.relpath(raiz, BASE).split(os.sep)[0]
    n = len(arqs)
    total += n
    por_pasta[rel] = por_pasta.get(rel, 0) + n
for k in sorted(por_pasta, key=lambda x: -por_pasta[x])[:10]:
    print(f"  {k:<25} {por_pasta[k]:>6} arquivos")
print(f"  TOTAL: {total} arquivos")

print("\n=== 3) Workspace está confiável (trusted)? ===")
ws_dir = os.path.expandvars(r"%APPDATA%/Code/User/workspaceStorage")
achou = False
for d in os.listdir(ws_dir):
    wj = os.path.join(ws_dir, d, "workspace.json")
    if not os.path.exists(wj):
        continue
    try:
        txt = open(wj, encoding="utf-8").read()
    except Exception:
        continue
    if "projeto_SER_Sagi%20-%20Hermes" in txt and "c%3A" in txt:
        meta = os.path.join(ws_dir, d, "meta.json")
        print(f"  workspace encontrado: {d}")
        achou = True
if not achou:
    print("  (workspace do C: não localizado no storage)")

print("\n=== 4) Configurações do Live Server ===")
print("  projeto:", open(os.path.join(BASE, ".vscode", "settings.json"), encoding="utf-8").read().strip())
