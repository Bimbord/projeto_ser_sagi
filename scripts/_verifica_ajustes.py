# -*- coding: utf-8 -*-
"""Verifica as alterações feitas na home e no CSS."""
import os, re

BASE = r"C:/Projetos Code/Projeto SER Sagi/projeto_SER_Sagi - Hermes"
html = open(os.path.join(BASE, "index.html"), encoding="utf-8").read()
css = open(os.path.join(BASE, "css", "style.css"), encoding="utf-8").read()

print("=== 1) Título da home ===")
t = re.search(r"<title>([^<]*)</title>", html)
print("  ", t.group(1))

print("\n=== 2) Cards de pilar linkados ===")
cards = re.findall(r'<a href="([^"]+)" class="home-card home-pillar">', html)
for c in cards:
    existe = os.path.exists(os.path.join(BASE, c))
    print(f"   {'OK ' if existe else 'ERRO'} -> {c}" + ("" if existe else "  (arquivo NAO existe!)"))
print(f"   total: {len(cards)}")

print("\n=== 3) Balanço das tags <a> (o HTML ficou válido?) ===")
abre = len(re.findall(r"<a\s", html))
fecha = len(re.findall(r"</a>", html))
print(f"   <a ...> = {abre}  |  </a> = {fecha}  -> {'OK' if abre == fecha else 'DESBALANCEADO!'}")

print("\n=== 4) CSS novo ===")
for sel in ["a.home-card", ".home-card__cta", ".archive-grid"]:
    print(f"   {'OK ' if sel in css else 'FALTA'} {sel}")

print("\n=== 5) Outros cards da home continuam como <article>? ===")
print("   artigos home-card restantes:", len(re.findall(r'<article class="home-card', html)))
