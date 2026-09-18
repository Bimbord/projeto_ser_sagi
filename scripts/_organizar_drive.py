# -*- coding: utf-8 -*-
"""
Organiza a estrutura de pastas do Drive.

Decisoes (17/09):
  - Nomes TECNICOS: minusculo, sem acento, com hifen (slug da pagina)
  - GRANULARIDADE DO BIMBORD: uma pasta por COMPONENTE da pagina
    (hero, numeros, pilares, cards-modalidades, galeria...)

O script:
  1. cria a estrutura-alvo (slugs)
  2. remove as pastas antigas (APENAS se estiverem vazias - nenhuma foto se perde)
"""
import os

S = r"G:/Meu Drive/Instituto SER Sagi - PARA O SITE"

ALVO = [
    # HOME (um componente por bloco da página)
    "home/hero", "home/numeros", "home/pilares", "home/joia-da-coroa",
    "home/acervo", "home/depoimentos", "home/parceiros", "home/como-ajudar",

    # SAÚDE
    "saude/hero", "saude/imagem principal", "saude/carrossel", "saude/galeria",

    # ESPORTE (hub) + áreas
    "esporte/hero", "esporte/cards-modalidades",
    "esporte/escola-jiu-jitsu/hero",
    "esporte/volei/hero", "esporte/volei/cards-modalidades",
    "esporte/futevolei/hero",
    "esporte/estudio-musculacao/hero",
    "esporte/natacao/hero",
    "esporte/danca/hero",
    "esporte/arena-futevolei-volei/hero",

    # EDUCAÇÃO (hub) + áreas
    "educacao/hero", "educacao/cards-modalidades", "educacao/meio-ambiente",
    "educacao/ingles/hero", "educacao/espanhol/hero",
    "educacao/informatica/hero", "educacao/sustentabilidade/hero",

    # OUTRAS
    "cultura/hero", "preservacao/hero", "eventos",
]

ANTIGAS = [
    "esporte/Vôlei", "esporte/Dança", "esporte/Futevôlei", "esporte/Natação",
    "esporte/musculação", "esporte/Jiu-jitsu",
    "educacao/cards modalidades", "educacao/meio ambiente",
    "home/Depoimentos", "home/card joia da coroa", "home/como ajudar",
]


def remover_vazios(caminho):
    """Remove a pasta (e subpastas) SOMENTE se estiverem vazias."""
    if not os.path.isdir(caminho):
        return 0
    apagadas = 0
    for raiz, dirs, arqs in os.walk(caminho, topdown=False):
        for d in dirs:
            try:
                os.rmdir(os.path.join(raiz, d))
                apagadas += 1
            except OSError:
                pass
    try:
        os.rmdir(caminho)
        apagadas += 1
    except OSError:
        pass
    return apagadas


criadas = 0
for rel in ALVO:
    p = os.path.join(S, rel)
    if not os.path.isdir(p):
        os.makedirs(p, exist_ok=True)
        criadas += 1
print(f"  ✅ estrutura-alvo: {criadas} pasta(s) criada(s) de {len(ALVO)}")

removidas, mantidas = 0, []
for rel in ANTIGAS:
    p = os.path.join(S, rel)
    if not os.path.isdir(p):
        continue
    n = remover_vazios(p)
    if os.path.isdir(p):
        mantidas.append(rel)          # tinha arquivo dentro -> preservada
    else:
        removidas += 1
print(f"  ✅ pastas antigas removidas (vazias): {removidas}")
if mantidas:
    print(f"  ⚠️  preservadas (tinham arquivo): {', '.join(mantidas)}")

print("\n=== ESTRUTURA FINAL ===")
for raiz, dirs, arqs in os.walk(S):
    if "_publicados" in raiz:
        continue
    nivel = raiz.replace(S, "").count(os.sep)
    if nivel > 3:
        continue
    print("  " + "  " * nivel + "📁 " + os.path.basename(raiz) + "/")
