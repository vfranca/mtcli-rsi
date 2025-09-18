# Uso
  
```bash
mt rsi --symbol WIN$N --period M5 --periodo 9 --bars 20
```
  
Parâmetros
  
| Parâmetro       | Descrição                            | Padrão   |
|------------|---------------------------|-------|
| `--symbol, -s`   | Ativo (ticker) a ser analisado         | `WINN`  |
| `--period, -p`   | Timeframe dos candles (`M1`, `D1`, ...) | `M5`     |
| `--periodo, -pe` | Período do RSI                         | `9`      |
| `--bars`         | Número de candles                      | `20`     |
| `--db`           | Nome do arquivo SQLite                 | `rsi.db` |
  
