# Tamanhos de imagem — guia de exportação

> Levantado do próprio CSS/HTML em 18/09/2026 (`scripts/_mapa_tamanhos.py`).
> Regra geral: **envie com ~2× o tamanho exibido**, sempre em **JPG** (fotos) ou
> **PNG com fundo transparente** (só logomarcas). O site **não redimensiona** —
> exporte já no tamanho certo, senão a página fica pesada.

## Regras rápidas

| | Valor |
|---|---|
| Formato | **JPG** (fotos) · **PNG** (logo com transparência) |
| Peso | hero até **600 KB** · cards até **250 KB** · bolinhas até **80 KB** |
| Paisagem | quase tudo é cortado em **paisagem** (deitado). Retrato só nas bolinhas |
| Assunto | deixe o assunto **no centro** — o site corta as bordas (`object-cover`) |
| Galeria | mantenha a **mesma proporção** em todas as fotos (senão a grade fica irregular) |

---

## 1. Heroes (banners do topo)

| Onde | Exibido | **Enviar** | Proporção |
|---|---|---|---|
| Hero das páginas internas (todas) | largura da tela × 380–560 px | **1920 × 700** | ~2,7:1 (bem deitada) |
| Hero da home (slideshow, 2+ fotos) | largura da tela × altura da tela | **1920 × 1080** | 16:9 |

> Nas páginas internas o corte vertical varia com a tela: em monitor largo corta mais
> em cima/embaixo. **Assunto no centro** resolve.

## 2. Home

| Bloco | Pasta | Exibido | **Enviar** | Proporção |
|---|---|---|---|---|
| Jóia da Coroa | `home/joia-da-coroa` | 594 × 160 px | **1200 × 330** | ~3,6:1 |
| Pilares (5 fotos) | `home/pilares` | 176 × 110 px | **600 × 375** | 16:10 |
| Números (6 fotos) | `home/numeros` | 48 × 48 px (bolinha) | **300 × 300** | **1:1** |
| Como ajudar (3 fotos) | `home/como-ajudar` | 341 × 213 px | **800 × 500** | 16:10 |
| Depoimentos | `home/depoimentos` | 389 × 243 px | **900 × 563** | 16:10 |
| Parceiros (logos) | `home/parceiros` | ~290 px de largura | **400 × 400** | 1:1, **fundo transparente** |

## 3. Blocos de mídia (Saúde + 11 áreas)

| Bloco | Exibido | **Enviar** | Proporção |
|---|---|---|---|
| Carrossel | 384 × 256 px | **800 × 533** | 3:2 |
| Galeria (grade) | 389 px × altura livre | **800 × 600** | **4:3** (padronize) |
| Ampliação (lightbox) | até 1100 px | usa a **mesma** da galeria | — |

## 4. Cards das páginas internas

Todos cortam em paisagem, entre 2:1 e 2,3:1 — então **1000 × 500 serve para todos**:

| Card | Exibido | **Enviar** |
|---|---|---|
| Card de modalidade / área (hub, acervo, ações) | 389 px (3 col) ou 286 px (4 col) × 160–192 px | **1000 × 500** |
| Imagem principal (ex.: consultório na página Saúde) | 596 × 256 px | **1200 × 520** |
| Cards de destaque (transparência, lei de incentivo, como ajudar) | 286 × 128 px | **800 × 400** |
| Cards de instalações | 596 × 176 px | **1200 × 500** |

---

## Se der preguiça (o caminho mais rápido)

- **Hero:** 1920 × 700
- **Qualquer card de página interna:** 1000 × 500
- **Galeria/carrossel:** 800 × 600
- **Bolinha (números):** 300 × 300
- Tudo em JPG, assunto no centro.

Serve para 100% dos casos com corte automático.

> `scripts/_mapa_tamanhos.py` refaz esse levantamento se o layout mudar.
