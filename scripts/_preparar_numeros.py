# -*- coding: utf-8 -*-
"""
Prepara as imagens dos cards de NÚMEROS da home.

O card mostra a foto num círculo de 3rem (48 px) -> 400 px já sobra.
Redimensiona, converte para JPEG e guarda os originais em _originais/_antigos.
"""
import os
import shutil
from PIL import Image

BASE = r"G:\Meu Drive\Instituto SER Sagi - PARA O SITE\home\numeros"
BACKUP = os.path.join(BASE, "_originais", "_antigos")
os.makedirs(BACKUP, exist_ok=True)

LADO = 400
QUALIDADE = 84

for f in sorted(os.listdir(BASE)):
    caminho = os.path.join(BASE, f)
    if not os.path.isfile(caminho) or not f.lower().endswith((".png", ".jpg", ".jpeg")):
        continue

    peso_antes = os.path.getsize(caminho)
    im = Image.open(caminho)
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGB")
    larg, alt = im.size

    # backup do original (só se ainda não existir)
    destino_backup = os.path.join(BACKUP, f)
    if not os.path.isfile(destino_backup):
        shutil.copy2(caminho, destino_backup)

    if larg > LADO or alt > LADO:
        im.thumbnail((LADO, LADO), Image.LANCZOS)

    nome_jpg = os.path.splitext(f)[0] + ".jpg"
    destino = os.path.join(BASE, nome_jpg)
    im.save(destino, "JPEG", quality=QUALIDADE, optimize=True, progressive=True)

    # remove o PNG original depois de gravar o JPG
    if f.lower().endswith(".png") and os.path.isfile(destino):
        os.remove(caminho)

    print(f"  ✅ {f:26} {larg}x{alt} {peso_antes/1024:6.0f} KB -> "
          f"{im.size[0]}x{im.size[1]} {os.path.getsize(destino)/1024:5.0f} KB")

print()
print("na pasta, prontas para publicar:")
for f in sorted(os.listdir(BASE)):
    c = os.path.join(BASE, f)
    if os.path.isfile(c) and f.lower().endswith((".jpg", ".png")):
        print(f"   {f:26} {os.path.getsize(c)/1024:6.0f} KB")
