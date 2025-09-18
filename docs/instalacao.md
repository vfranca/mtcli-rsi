Instalação

bash
git clone https://github.com/seu-usuario/mtcli-rsi.git
cd mtcli-rsi
poetry install
```
> Requisitos:
> - Python 3.8+
> - MetaTrader 5 instalado
> - Conta válida e login ativo na corretora


---

4. *docs/uso.md*

markdown
Uso

bash
poetry run mtcli rsi --symbol WINN –period M5 –periodo 9 –bars 20
“`

Parâmetros

| Parâmetro       | Descrição                            | Padrão   |
|——————|—————————————-|———-|
| `–symbol, -s`   | Ativo (ticker) a ser analisado         | `WINN`  |
| `--period, -p`   | Timeframe dos candles (`M1`, `D1`, ...) | `M5`     |
| `--periodo, -pe` | Período do RSI                         | `9`      |
| `--bars`         | Número de candles                      | `20`     |
| `--db`           | Nome do arquivo SQLite                 | `rsi.db` |


---

5. docs/armazenamento.md

markdown
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
