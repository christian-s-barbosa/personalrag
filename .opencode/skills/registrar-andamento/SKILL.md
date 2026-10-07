---
name: registrar-andamento
description: Use when a development session ends (user says "/ends", "fim de sessão", "registrar andamento"). Records a short session log (feito · decisões · próximo) in doc/vault/historico/YYYY/mm/progresso/YYYY_mm_dd_dev.md and updates estado-atual.md. Trigger keywords: fim de sessão, registrar andamento, andamento, encerrar sessão, progresso do projeto.
---

# Registrar andamento — desenvolvimento

Ao fim de cada sessão de desenvolvimento, registre o andamento e atualize o
estado do projeto. É **leve** — é o andamento do projeto, não uma avaliação de
aprendizado.

## Passos

1. **Registro de sessão** — leia o template `andamento.md`
   (`.opencode/templates/andamento/andamento.md`) e grave:
   - **feito** · **decisões** · **próximo** · **bloqueios**.
   Em `doc/vault/historico/YYYY/mm/progresso/YYYY_mm_dd_dev.md` (crie a pasta se faltar).

2. **Atualizar `estado-atual.md`** (estado do **projeto**): o que está
   construído, em andamento, próximo e riscos.

3. **Regenerar o índice** (MOC, ligado a todas as notas):
   ```
   powershell -NoProfile -ExecutionPolicy Bypass -File "C:\Users\chris\Projetos\.opencode\scripts\gerar-index.ps1" -VaultPath "<vault do projeto>" -Titulo "<nome do projeto>"
   ```

4. **Evitar sobrescrever** — se o arquivo do dia existir, sufixe `_2`, `_3`.

5. **Confirmar** — mostre os caminhos salvos e um resumo de 1 linha.

## Regras

- Não invente: registre o que **foi feito**.
- Não é avaliação de habilidade (isso é do tipo `estudo`).
