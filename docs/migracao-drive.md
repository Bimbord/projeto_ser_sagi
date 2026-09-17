# Migração para o Google Drive (17/09/2026)

A pasta de trabalho do site saiu do `C:` e agora é a cópia no **Google Drive**.

## 📁 Caminho da pasta de trabalho

```
G:\.shortcut-targets-by-id\18wGiptBKUmAmmkKHgdfu05TU4y_roWC1\BBDPRINT - BACKUP\BBDPRINT\App BBDPRiNT\PROJETOS\Projeto SER Sagi\projeto_SER_Sagi - Hermes
```

## 🎯 Por quê

- **Uma pasta só** — evita cópias soltas no `C:` virando bagunça
- **Editar/salvar já grava no Drive** — backup automático, sem passo extra

## 🔄 Rotina de trabalho

```bash
cd "G:\.shortcut-targets-by-id\18wGiptBKUmAmmkKHgdfu05TU4y_roWC1\BBDPRINT - BACKUP\BBDPRINT\App BBDPRiNT\PROJETOS\Projeto SER Sagi\projeto_SER_Sagi - Hermes"
# editar normalmente...
git add -A && git commit -m "descrição" && git push
```

**Não há mais passo de sincronização.** O antigo `scripts/_sync_drive.py` (que copiava `C:` → `G:`) ficou **obsoleto** — não rodar mais.

## 🛡️ Onde está a segurança

| Camada | Papel |
|---|---|
| **GitHub** | Backup **offsite** real — reclonável a qualquer momento (`github.com/Bimbord/projeto_ser_sagi`) |
| **Google Drive** | Redundância + histórico de versões dos arquivos |

> ⚠️ **Atenção:** o Google Drive sincroniza a pasta `.git` (milhares de arquivos pequenos). Eventualmente o Drive pode "segurar" um arquivo no meio de uma operação git → erro de `index.lock`.
> **Se acontecer:** espere o Drive terminar de sincronizar e repita o comando. O repositório não se perde — o GitHub tem tudo.

## ✅ Verificado em 17/09/2026

- 149 arquivos rastreados · idêntico ao GitHub (`db15d97`)
- `git status` / `git log` / `git push` funcionando na pasta do Drive
- Edição de arquivos funcionando
