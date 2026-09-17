# -*- coding: utf-8 -*-
"""
Sincroniza a pasta de trabalho (C:) com o backup no Google Drive (G:).
Copia apenas arquivos novos/diferentes. Ignora .git e __pycache__.
"""
import os, shutil, filecmp

SRC = r"C:/Projetos Code/Projeto SER Sagi/projeto_SER_Sagi - Hermes"
DST = (r"G:/.shortcut-targets-by-id/18wGiptBKUmAmmkKHgdfu05TU4y_roWC1/BBDPRINT - BACKUP/"
       r"BBDPRINT/App BBDPRiNT/PROJETOS/Projeto SER Sagi/projeto_SER_Sagi - Hermes")

IGNORAR_DIRS = {".git", "__pycache__", "node_modules"}

if not os.path.isdir(DST):
    raise SystemExit(f"ERRO: destino nao encontrado:\n{DST}")

novos, atualizados, iguais, erros = [], [], 0, []

for raiz, dirs, arqs in os.walk(SRC):
    dirs[:] = [d for d in dirs if d not in IGNORAR_DIRS]
    rel_dir = os.path.relpath(raiz, SRC)
    dst_dir = DST if rel_dir == "." else os.path.join(DST, rel_dir)
    os.makedirs(dst_dir, exist_ok=True)
    for a in arqs:
        origem = os.path.join(raiz, a)
        destino = os.path.join(dst_dir, a)
        rel = os.path.relpath(origem, SRC)
        try:
            if not os.path.exists(destino):
                shutil.copy2(origem, destino)
                novos.append(rel)
            elif not filecmp.cmp(origem, destino, shallow=False):
                shutil.copy2(origem, destino)
                atualizados.append(rel)
            else:
                iguais += 1
        except Exception as e:
            erros.append(f"{rel}: {e}")

print(f"=== SINCRONIZACAO C: -> G: (Google Drive) ===")
print(f"  ✅ novos copiados:       {len(novos)}")
for n in sorted(novos):
    print(f"       + {n}")
print(f"  🔄 atualizados:          {len(atualizados)}")
for u in sorted(atualizados):
    print(f"       ~ {u}")
print(f"  =  ja iguais:            {iguais}")
if erros:
    print(f"  ⚠️  erros: {len(erros)}")
    for e in erros[:10]:
        print(f"       ! {e}")
print("\nBackup do Drive sincronizado.")
