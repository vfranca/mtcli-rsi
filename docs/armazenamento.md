Armazenamento

Os resultados do RSI são armazenados automaticamente no banco `SQLite` definido (padrão: `rsi.db`).

Tabela: `rsi`

| Coluna | Descrição           |
|--------|---------------------|
| RSI    | Valor do indicador  |
| close  | Preço de fechamento |
| time   | Timestamp            |


---

6. docs/desenvolvimento.md

markdown
Desenvolvimento

Estrutura de código

- `rsi.py`: lógica de cálculo do RSI
- `_main_.py`: comando CLI com `click`
- `tests/`: testes automatizados com `pytest`

Executar testes

bash
