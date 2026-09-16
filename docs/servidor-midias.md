# Servidor de Mídias — Instituto S.E.R. Sagi

> Documento vivo. Fluxo oficial de **entrada de mídias** (fotos/vídeos/documentos) da ONG até o site.
> Complementa `docs/fluxo-importacao-midias.md` (que descreve a **saída**: R2 + Supabase).

---

## 🗺️ O desenho em duas fases

```
FASE 1 (feita) — CANAL DE ENTRADA
  ONG sobe arquivos na pasta compartilhada do Google Drive do Bimbord
        ↓
  Google Drive Desktop sincroniza → aparece nesta máquina em G:\Meu Drive\...

FASE 2 (a fazer) — AUTOMAÇÃO PARA O SITE
  Bimbord seleciona e trata a mídia na pasta "espelho" das pastas do site
        ↓
  Script lê do Drive em STREAMING (sem cópia local)
        ├─ ⬆️ arquivo → Cloudflare R2 (bucket midias-ser-sagi)
        └─ 🗄️ registro → Supabase (tabela arquivo)
        ↓
  Site atualiza (Acervo / Destaques da home)
```

---

## ✅ Fase 1 — Pasta compartilhada (16/09/2026)

### Estrutura criada

```
G:\Meu Drive\Instituto SER Sagi - Midias\
├── Imagens\        fotos das atividades
├── Videos\         vídeos curtos
├── Documentos\     PDFs publicáveis
└── LEIA-ME - como enviar as midias.txt   (instruções para a ONG)
```

- Pastas por **tipo de arquivo** (decisão do Bimbord) — a ONG não precisa saber as categorias do site.
- Quem seleciona a categoria (`esporte`, `saude`, `educacao`, `cultura`, `preservacao`, `eventos`) é o **Bimbord**, na fase de tratamento.
- Nomes sem acento de propósito: evita dor de cabeça de encoding em script/Windows.

### Compartilhamento

- Conta de destino: **sersagi2025@gmail.com** (conta da ONG)
- Permissão: **Editor** (decisão do Bimbord — a ONG pode subir, mover e apagar)
- A pasta é criada no **Meu Drive do Bimbord** (não no backup `BBDPRINT - BACKUP`), então a ONG a encontra em **Compartilhados comigo**.

### ⚠️ Riscos conhecidos deste desenho

1. **Editor libera apagar sem aviso.** Como não há versionamento/backup da pasta, um arquivo apagado por engano se perde. Mitigação recomendada: manter cópia do que já foi publicado no **R2** (o R2 é o arquivo oficial depois de publicado).
2. **Sem autorização de imagem, não publicar** (ECA + LGPD) — vale para toda foto de criança/adolescente. O `LEIA-ME` avisa, mas a checagem final é humana.
3. **Espaço no C: está apertado (7 GB livres).** Por isso a fase 2 lê do Drive em streaming e **não** deixa cópia local. Nada de baixar o lote para C:.

---

## 🔜 Fase 2 — O que falta definir/implementar

- [ ] Nome e formato da **pasta espelho** das pastas do site (ex.: `03-PARA-O-SITE\<categoria>\`)
- [ ] Pasta `Publicados\` para onde vai o que já subiu
- [ ] Script `scripts/servidor_midias.py`:
  - [ ] `--status` → lista o que chegou e o que ainda não foi publicado (controle por hash)
  - [ ] `--publicar` → lê em streaming do Drive, sobe pro R2 e registra no Supabase (reusa `publicar.py`)
  - [ ] `--mover` → joga o publicado para a pasta de publicados
- [ ] Manifesto de controle (`publicados.json`) guardado **no Drive**, não no C:
- [ ] Aviso automático (cron do Hermes) quando chegar mídia nova na pasta

---

## 🔒 Segurança

- Credenciais do R2 continuam em `C:/Users/PRE-IMPRESSOR/R2/.r2-sagi.env` (nunca no repositório).
- O bucket R2 é **público**: não subir documento com dados pessoais.
