---
name: verificar
description: Use ao terminar uma feature/refatoração (ou antes de entregar) para conferir se o trabalho "está de pé" — verificação determinística em fases (build, tipos, lint, testes+cobertura, segredos, diff) com relatório PASS/FAIL. Trigger keywords: verificar, verificação, rodar testes, lint, type-check, está pronto, quality gate.
---

# Verificar — verificação determinística

Confere se o trabalho está **de pé** antes de considerar "pronto". É o passo
*determinístico* (máquina verifica); o `revisor` é o *semântico* (juízo). Rode
**este primeiro**.

## Fases

1. **Build** — o projeto compila/roda? Se falhar, **PARE** e corrija.
2. **Type-check** — ferramenta do stack (ex.: Python `mypy`; TS `tsc --noEmit`).
3. **Lint** — ferramenta do stack (ex.: Python `ruff`; JS `eslint`).
4. **Testes + cobertura** — rodar (ex.: `pytest --cov`); reportar **X/Y** e **%**.
5. **Segredos** — varredura por chaves/tokens no código (`sk-`, `api_key`,
   `.env` versionado).
6. **Diff** — `git diff --stat`; revisar o que mudou (mudança indevida? edge
   case faltando?).

## Relatório

```
VERIFICAÇÃO
Build:     PASS/FAIL
Tipos:     PASS/FAIL (N erros)
Lint:      PASS/FAIL (N avisos)
Testes:    PASS/FAIL (X/Y, Z%)
Segredos:  PASS/FAIL (N)
Diff:      N arquivos
Veredito:  PRONTO / NÃO PRONTO
A corrigir: ...
```

## Regras

- **Adapte as ferramentas ao stack** do projeto (descubra no `pyproject.toml` /
  `package.json`). Se não houver ferramenta definida, é hora de definir (Fase 6).
- **Não invente**: reporte o que **rodou** de verdade.
- É o "definition of done" técnico do *Fluxo por Feature*.
