# 🔧 Troubleshooting local — máquina do Bimbord

> Problemas de ambiente/ferramentas que já resolvemos (pra não perder tempo de novo).

---

## ⚠️ CCleaner apagando "duplicados" quebra aplicativos

**História:** o CCleaner limpou arquivos duplicados e **afetou vários aplicativos** — inclusive a extensão **Live Server** do VS Code, que passou a mostrar:
> `"Something went wrong! Please check into Developer Console or report on GitHub."` (Origem: Live Server)

**Por que acontece:** dentro de qualquer `node_modules` existem **centenas de arquivos idênticos** (ex.: `mime-db/db.json`, `lodash.js`, `esprima.js`). O removedor de duplicados apaga "as cópias" — que na verdade são **dependências de programas diferentes**.

### Diagnóstico que fizemos
```bash
# o servidor interno da extensão não carregava:
node -e "require('<EXT>/node_modules/live-server')"
# -> Cannot find module './db.json'   (mime-db/db.json apagado)
```

### Correção aplicada (11/09/2026)
Restauramos na extensão `ritwickdey.liveserver-5.7.10` (`~/.vscode/extensions/`):

| Pacote | Arquivo restaurado | Versão |
|---|---|---|
| `mime-db` | `db.json` | 1.52.0 |
| `acorn` | `dist/acorn.js` | 5.7.4 |
| `esprima` | `dist/esprima.js` | 4.0.1 |
| `lodash` | `lodash.js` | 4.17.21 |
| `rx-lite` | `rx.lite.js` | 3.1.2 |

Fonte dos arquivos: `https://cdn.jsdelivr.net/npm/<pacote>@<versao>/<arquivo>`

**Depois de restaurar:** recarregar a janela do VS Code (`Ctrl+Shift+P` → *Developer: Reload Window*) e o **Go Live** volta a funcionar.

### 🚫 Regra nova
**NÃO usar o "localizador de duplicados" do CCleaner** (nem similares) em pastas de programas/apps. Limpeza de disco pode ser feita em pastas de dados/usuário, nunca em `node_modules`, `Program Files`, `AppData/Local/Programs`, pastas de extensões.

### Como verificar a integridade da extensão (script pronto)
Os scripts de diagnóstico ficaram em `%LOCALAPPDATA%\Temp\`:
- `diag_ls.js` — testa se os módulos carregam
- `verifica_ls.js` — varre todos os pacotes + sobe o servidor de teste
- `restaura_ls.js` — baixa e restaura arquivos principais faltantes

---

## Live Server: o servidor serve a pasta aberta no VS Code

Se der erro/404, confira **qual pasta está aberta** (Arquivo → Abrir Pasta). Um workspace apontando para pasta inexistente (ex.: drive removido) causa falha.

Porta configurada neste projeto: **5501** (`.vscode/settings.json`).

---

## Alternativa sem extensão (se o Live Server falhar)
```bash
cd "C:\Projetos Code\Projeto SER Sagi\projeto_SER_Sagi - Hermes"
python -m http.server 5501
# abre http://127.0.0.1:5501/ no navegador
```
