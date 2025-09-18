# API Interna
  
calcular_rsi_completo(rates, periodo)
  
Calcula o RSI a partir de uma lista de candles.
  
- `rates`: lista de dicionários com dados de candle
- `periodo`: inteiro com o período da média
  
Retorna: DataFrame com colunas `RSI`, `close` e `time`
  
