---
name: revisor
description: Use para verificar algo que vai ser entregue (código, spec, documento, resposta) com rigor — verificação adversarial com 2 revisores independentes (contexto limpo, mesmo rubric), em que ambos precisam passar. Trigger keywords: revisar, revisor, verificação adversarial, santa-method, dupla checagem, gate de qualidade, anti-alucinação.
---

# Revisor — verificação adversarial (2 revisores independentes)

Um único agente revisando o próprio trabalho carrega **os mesmos vieses** que
produziram o erro. Dois revisores independentes, **sem contexto compartilhado**,
quebram isso.

## Quando usar

- Output que **vai entregar** (código, spec, doc, resposta ao usuário).
- Risco de **alucinação** (afirmações, referências, números, APIs).
- **Não** use para rascunho interno, nem quando a verificação é determinística
  (para isso, use `verificar`).

## Fluxo

1. **Gerar** o output (normal).
2. **2 revisores independentes** — dispare **dois subagentes** (ferramenta `task`),
   com o **mesmo rubric**, e **nenhum vê o outro**.
3. **Gate:** os **dois** precisam passar. Se **um** reprovar, reprovou (o ponto
   cego do outro é justamente o que queremos pegar).
4. **Consertar** só o apontado; **re-revisar** com revisores **novos** (até **3
   rodadas**).
5. Sem convergir em 3 → **escalar para o humano** (apresentar os problemas).

## Rubric (adapte ao contexto)

Cada critério com condição **objetiva** de PASS/FAIL:

| Critério | PASS | Sinal de falha |
|----------|------|----------------|
| Fato/evidência | toda afirmação tem **origem/fonte** | números/URLs/APIs inventados |
| Sem invenção | nada que não existe no material | referência a algo inexistente |
| Completude | todo requisito da spec coberto | seções/edge cases faltando |
| Consistência | sem contradição interna | seção A diz X, B diz não-X |
| Técnico | compila/roda; lógica sã | erro de sintaxe/lógica |

## Prompt do revisor

```
Você é um revisor de qualidade INDEPENDENTE. Você NÃO viu nenhuma outra revisão.

## Especificação
{spec}

## Output sob revisão
{output}

## Rubric
{rubric}

Avalie o output contra CADA critério. Devolva JSON:
{"verdict": "PASS|FAIL", "critical_issues": ["..."], "suggestions": ["..."]}

Seja rigoroso. Seu trabalho é ACHAR PROBLEMAS, não aprovar.
```

## Métricas (opcional)

- **Taxa de 1ª passada** (% que passa na rodada 1 — alvo > 70%).
- **Concordância dos revisores** (% de issues apontadas por ambos) — baixa
  concordância = rubric precisa afinar.

## Regras

- Contexto **limpo** a cada rodada (revisores não carregam memória da rodada
  anterior → evita viés de ancoragem).
- Revisor aponta; **não** conserta. Quem conserta é o fluxo principal.
- Rode o `verificar` (determinístico) **antes** do `revisor` (semântico).
