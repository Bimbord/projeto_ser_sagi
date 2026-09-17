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
- **Tipo de conta do dono:** Gmail comum (Google One 5 TB) → **não tem "Drives compartilhados"** (recurso exclusivo de Workspace). A pasta fica dentro do Meu Drive do Bimbord.
- Permissão: **Editor** (escolha inicial do Bimbord, avaliando mudança para o meio-termo abaixo)
- A pasta é criada no **Meu Drive do Bimbord** (não no backup `BBDPRINT - BACKUP`), então a ONG a encontra em **Compartilhados comigo**.

#### ✅ Mitos e fatos sobre "subir de nível" (verificado 16/09)

**A ONG não consegue ver o resto do Drive do Bimbord.** O compartilhamento no Google Drive é **por item**: a permissão não sobe para a pasta pai.

- Ao abrir, ela vê `Compartilhados comigo > Instituto SER Sagi - Midias`. Clicando em "Compartilhados comigo", ela cai no **próprio Drive**, vazio de conteúdo do Bimbord.
- Links de pastas não compartilhadas retornam **"Solicitar acesso"** (chega e-mail de pedido).
- A pasta foi criada **direto na raiz do Meu Drive** (ao lado dos `.lnk` de backup) e a raiz não é compartilhável → **zero herança de permissão**.
- ⚠️ A única forma de vazar acesso para cima é criar a pasta **dentro** de uma pasta já compartilhada. Não é o caso aqui — e não deve ser feito em nenhuma reorganização futura.

#### Meio-termo recomendado (mais travado sem quebrar o fluxo)

Não existe no Google um nível "só visualizar + poder subir". Os níveis são Leitor, Comentador e Editor. A configuração mais travada que ainda permite envio:

| Item | Permissão da ONG |
|---|---|
| `Instituto SER Sagi - Midias` (raiz) | **Leitor** |
| `Imagens` | **Editor** |
| `Videos` | **Editor** |
| `Documentos` | **Editor** |

Efeito: ela não renomeia/apaga a estrutura nem o `LEIA-ME`, mas sobe mídia normalmente. Permissões se somam por item, então **dentro** das 3 subpastas ela ainda pode apagar arquivo — só não mexe na "carcaça".

#### 🚨 Limite que não tem solução no plano atual

Editor pode apagar mídia já publicada, e o Drive não versiona o que já saiu. **O backup real do que foi publicado é o R2** (Cloudflare). Não tratar o Drive como acervo definitivo.

### ⚠️ Riscos conhecidos deste desenho

1. **Editor libera apagar sem aviso.** Como não há versionamento/backup da pasta, um arquivo apagado por engano se perde. Mitigação recomendada: manter cópia do que já foi publicado no **R2** (o R2 é o arquivo oficial depois de publicado).
2. **Sem autorização de imagem, não publicar** (ECA + LGPD) — vale para toda foto de criança/adolescente. O `LEIA-ME` avisa, mas a checagem final é humana.
3. **Espaço no C: está apertado (7 GB livres).** Por isso a fase 2 lê do Drive em streaming e **não** deixa cópia local. Nada de baixar o lote para C:.

---

## ✅ Fase 2 — Script implementado e testado (16/09/2026)

**Script:** `scripts/servidor_midias.py`

### Pasta espelho (a área de trabalho do Bimbord)

```
G:\Meu Drive\
├── Instituto SER Sagi - Midias\         (COMPARTILHADA - caixa de entrada da ONG)
└── Instituto SER Sagi - PARA O SITE\    (SÓ DO BIMBORD - não compartilhada)
    ├── esporte\ saude\ educacao\ cultura\ preservacao\ eventos\
    └── _publicados\
        ├── <categoria>\                 (o que já subiu, arquivado)
        └── publicados.json              (manifesto: hash, id, URL, data)
```

**Fluxo:** a ONG sobe na caixa de entrada → o Bimbord aprova e **move** o que serve para a pasta da categoria no "PARA O SITE" (mover no Drive é instantâneo, não baixa nem sobe de novo) → roda o script.

**Por que pasta separada (não compartilhada):** a ONG não consegue publicar nada no site por acidente.

### Comandos

```bash
python scripts/servidor_midias.py --status      # o que chegou / o que já subiu
python scripts/servidor_midias.py --dry-run     # simula (não sobe nada)
python scripts/servidor_midias.py --publicar    # publica de verdade
```

Flags: `--limite-gb N` (padrão 1.0, protege o C:) · `--max-mb N` (padrão 800, protege a RAM) · `--categoria X` · `--autorizado` (registra a conferência de autorização de imagem no manifesto — **não bloqueia** por decisão do Bimbord em 16/09).

### Regras automáticas

- **Categoria** = nome da pasta (`esporte\` → "Esporte" na tabela `arquivo`)
- **Título** = nome do arquivo limpo; **data** = extraída do prefixo `AAAA-MM-DD` do nome
  - `2026-09-14-festa-das-criancas-01.jpg` → título "Festa Das Criancas 01", data 2026-09-14
- **`_info.txt`** (opcional, por pasta de categoria): `titulo_base=`, `descricao=`, `destaque=1`, `autorizado=sim`
- **Deduplicação por hash SHA-256** no manifesto → arquivo já publicado nunca sobe de novo, mesmo se renomeado
- **PDFs não entram no Acervo** (não há área de documentos no site) → usar `upload_r2.py`

### Teste real executado (16/09)

| Verificação | Resultado |
|---|---|
| Publicar 1 imagem de teste | ✅ id 7, URL no R2 |
| URL pública no R2 | ✅ HTTP 200, `image/png`, 1141 bytes |
| Linha no Supabase | ✅ título/categoria/descrição corretos |
| Arquivamento + manifesto | ✅ movido para `_publicados\esporte\`, 1 item registrado |
| Deduplicação | ✅ rodar de novo = "nada novo" |
| Limpeza do teste | ✅ R2 apagado, registro apagado, tabela `arquivo` com 0 linhas |

### ⚠️ Descobertas técnicas (importantes)

1. **A anon key do Supabase NÃO apaga nem edita** (só lê e insere). `DELETE`/`PATCH` retornam 200/204 **sem afetar linha nenhuma** (falha silenciosa — perigoso!).
   - Para apagar/editar registro: usar a **service_role** (arquivo local `C:/Users/PRE-IMPRESSOR/R2/supabase.txt` — nunca commitar/expor) ou o **Table Editor** no painel do Supabase.
2. **O arquivo é lido para a memória antes de subir** (mesmo comportamento do `publicar.py`). Com `--limite-gb 1` e `--max-mb 800` fica seguro (máquina tem 11,7 GB; ~3,6 GB livres). Vídeo grande demais é ignorado com aviso.
3. **Nada é copiado para o C:** — os bytes vão do Drive direto pro R2. Mas o Google Drive materializa o arquivo no cache dele em `%LOCALAPPDATA%\Google\DriveFS` (o C: tem só ~6 GB livres): daí o limite por rodada.

### Pendente / próximo

- [ ] Aviso automático (cron do Hermes) quando chegar mídia nova na caixa de entrada
- [ ] Avaliar bloqueio de publicação sem `--autorizado` (decisão adiada pelo Bimbord)
- [ ] Painel self-service para a ONG (opcional, fase futura)

---

## 🔒 Segurança

- Credenciais do R2 continuam em `C:/Users/PRE-IMPRESSOR/R2/.r2-sagi.env` (nunca no repositório).
- Service role do Supabase: `C:/Users/PRE-IMPRESSOR/R2/supabase.txt` — **nunca** vai para o repositório nem para mensagens.
- O bucket R2 é **público**: não subir documento com dados pessoais.

