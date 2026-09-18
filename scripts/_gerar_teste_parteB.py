# -*- coding: utf-8 -*-
"""Gera 3 PNGs ineditos para o teste da FASE 5 Parte B (hash novo no scanner)."""
import os, zlib, struct

S = r"G:/Meu Drive/Instituto SER Sagi - PARA O SITE"


def png_solido(w, h, cor):
    raw = b"".join(b"\x00" + bytes(cor) * w for _ in range(h))

    def chunk(tipo, dados):
        corpo = tipo + dados
        return struct.pack(">I", len(dados)) + corpo + struct.pack(">I", zlib.crc32(corpo) & 0xFFFFFFFF)

    ihdr = struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))


TESTES = [
    ("home/pilares/saude.png",        (231, 123, 95)),    # coral
    ("home/numeros/jiu-jitsu.png",    (244, 180, 0)),     # sun
    ("home/como-ajudar/doe.png",      (46, 125, 79)),     # leaf
]

for rel, cor in TESTES:
    p = os.path.join(S, rel.replace("/", os.sep))
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "wb") as f:
        f.write(png_solido(160, 100, cor))
    print(f"  ✅ {rel}  ({os.path.getsize(p)} bytes)")
