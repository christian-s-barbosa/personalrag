---
name: git-flow
description: Use ao versionar qualquer projeto (criar branch, commitar, abrir PR, fazer merge). Define a convenção GitHub Flow + Conventional Commits. Trigger keywords: git, commit, branch, PR, pull request, push, merge, versionar, gitflow.
---

# git-flow — GitHub Flow + Conventional Commits

Convenção de versionamento dos projetos. Leve (para uso solo), porém disciplinada.

## Modelo: GitHub Flow

- `main` é a versão **boa** — **sempre funcionando e sempre verde**.
- Cada tarefa nasce de uma **branch curta** → vira um **PR** → merge na `main` → apaga a branch.
- Nada de `develop`/`release`/`hotfix` (isso é GitFlow de time; aqui é cerimônia demais).

## Branches

`<tipo>/<slug-curto>`:

| Tipo | Uso |
|------|-----|
| `feat/...` | nova funcionalidade |
| `fix/...` | correção de bug |
| `docs/...` | documentação / vault |
| `chore/...` | manutenção (config, deps, tooling) |
| `refactor/...` | refatoração (sem mudar comportamento) |

## Commits — Conventional Commits

Formato: `<tipo>: <descrição curta, no imperativo>`
- Tipos: `feat`, `fix`, `docs`, `chore`, `refactor`, `test`.
- Ex.: `docs: migra personalrag pro layout novo`
- **Um commit = uma mudança coerente** (não misture coisas não relacionadas).

## Fluxo

```bash
git switch -c <tipo>/<slug>          # cria a branch
# ...trabalho...
git add <arquivos>                    # específicos (evite `git add .` às cegas)
git commit -m "<tipo>: <descrição>"
git push -u origin <tipo>/<slug>
gh pr create --fill                   # abre o PR
gh pr merge --squash --delete-branch  # junta na main e apaga a branch
```

## O que vai pro git

- **Vai:** código, docs, `AGENTS.md`, `.opencode/` (skills/agentes), `doc/vault/`.
- **Não vai:** segredos/`.env`, `node_modules/`, artefatos de build, o
  `workspace.json` do Obsidian (opcional, é estado de UI da máquina).

## Regras (para o agente)

- **Mostre o que vai commitar** antes (`git status` / `git diff`).
- **Nunca** versione segredo/token.
- **Não** faça `push` nem `merge` **sem avisar** o usuário.
- Não crie commits em lote sem autorização explícita.
- Em dúvida, **pergunte** — não empilhe mudanças na `main`.
