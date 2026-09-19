# -*- coding: utf-8 -*-
"""Prepara os selos 'ajude-0N' de home/parceiros (versão corrigida)."""
import os
import shutil
from PIL import Image

BASE = r"G:\Meu Drive\Instituto SER Sagi - PARA O SITE\home\parceiros"
BACKUP = os.path.join(BASE, "_originais", "_antigos")
os.makedirs(BACKUP, exist_ok=True)

LADO = 800
QUALIDADE = 88

for n in range(1, 5):
    nome = f"ajude-0{n}"
    png = os.path.join(BASE, nome + ".png")
    jpg = os.path.join(BASE, nome + ".jpg")

    # se a pasta ficou sem o arquivo, restaura o original do backup
    if not os.path.isfile(png) and not os.path.isfile(jpg):
        origem_backup = os.path.join(BACKUP, nome + ".png")
        if os.path.isfile(origem_backup):
            shutil.copy2(origem_backup, png)
            print(f"  ↺ {nome}.png restaurado do backup")
        else:
            print(f"  ⚠️  {nome}: não achei nem na pasta nem no backup")
            continue

    origem = png if os.path.isfile(png) else jpg
    peso_antes = os.path.getsize(origem)
    im = Image.open(origem)
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGB")
    larg, alt = im.size
    if larg > LADO:
        im = im.resize((LADO, round(alt * LADO / larg)), Image.LANCZOS)

    destino = os.path.join(BASE, nome + ".jpg")
    im.save(destino, "JPEG", quality=QUALIDADE, optimize=True, progressive=True)

    # guarda o ORIGINAL no backup (só o que veio do usuário)
    if origem.lower().endswith(".png"):
        destino_backup = os.path.join(BACKUP, nome + ".png")
        if os.path.isfile(origem) and not os.path.isfile(destino_backup):
            shutil.move(origem, destino_backup)
        elif os.path.isfile(origem):
            os.remove(origem)          # já tem backup, só remove o .png da pasta

    print(f"  ✅ {nome}  {larg}x{alt} {peso_antes/1024:5.0f} KB -> "
          f"{im.size[0]}x{im.size[1]} {os.path.getsize(destino)/1024:4.0f} KB")

print()
print("na pasta, prontas para publicar:")
for f in sorted(os.listdir(BASE)):
    c = os.path.join(BASE, f)
    if os.path.isfile(c) and f.lower().endswith((".jpg", ".png")):
        print(f"   {f:20} {os.path.getsize(c)/1024:6.0f} KB")
