# -*- coding: utf-8 -*-
"""
DEMONSTRAÇÃO — liga os 6 cards de "Resultados que geram confiança" a home/numeros.

1. lê as CHAVES direto do index.html (não inventa)
2. gera 1 imagem de teste por chave (cores distintas, para dar pra ver)
3. publica
4. confirma o casamento

Depois é só rodar scripts/_limpar_demo_numeros.py para remover tudo.
"""
import os
import re
import struct
import sys
import zlib

BASE = r"G:/.shortcut-targets-by-id/18wGiptBKUmAmmkKHgdfu05TU4y_roWC1/BBDPRINT - BACKUP/BBDPRINT/App BBDPRiNT/PROJETOS/Projeto SER Sagi/projeto_SER_Sagi - Hermes"
S = r"G:/Meu Drive/Instituto SER Sagi - PARA O SITE/home/numeros"

# ---- 1. chaves do HTML ----
html = open(os.path.join(BASE, "index.html"), encoding="utf-8").read()
chaves = re.findall(r'data-secao-img="numeros" data-secao-chave="([^"]+)"', html)
print(f"chaves encontradas no HTML ({len(chaves)}): {', '.join(chaves)}")

# ---- 2. imagens de teste (cores distintas) ----
CORES = {
    "projeto-principal": (15, 92, 115),    # ocean
    "saude": (231, 123, 95),               # coral
    "consultorio": (244, 180, 0),          # sun
    "esporte": (46, 125, 79),              # leaf
    "jiu-jitsu": (8, 59, 76),              # oceanDeep
    "musculacao": (148, 163, 184),         # slate
}


def png(w, h, cor):
    raw = b"".join(b"\x00" + bytes(cor) * w for _ in range(h))

    def chunk(t, d):
        c = t + d
        return struct.pack(">I", len(d)) + c + struct.pack(">I", zlib.crc32(c) & 0xFFFFFFFF)

    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))


os.makedirs(S, exist_ok=True)
for k in chaves:
    p = os.path.join(S, f"{k}.png")
    with open(p, "wb") as f:
        f.write(png(300, 300, CORES.get(k, (200, 200, 200))))
print(f"  ✅ {len(chaves)} imagens de teste criadas em home/numeros/")
print("   (publique com: python scripts/servidor_midias.py --publicar --autorizado)")
