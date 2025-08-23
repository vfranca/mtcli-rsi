import click
import MetaTrader5 as mt5
import pandas as pd
import sqlite3
import logging
from datetime import datetime

# Configurar logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('rsi.log')
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

# console_handler = logging.StreamHandler()
# console_handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))

logger.addHandler(file_handler)
# logger.addHandler(console_handler)

@click.command()
@click.option('--symbol', default='WINQ25', help='Símbolo do ativo (ex: WINQ25)')
@click.option('--timeframe', default='M5', help='Timeframe (ex: M1, M5, H1, D1)')
@click.option('--period', default=9, help='Período do RSI')
@click.option('--bars', default=20, help='Número de candles para análise')
@click.option('--db', default='rsi.db', help='Arquivo SQLite (ex: dados.db)')
def rsi(symbol, timeframe, period, bars, db):
    if not mt5.initialize():
        logger.error(f"Erro ao conectar MT5: {mt5.last_error()}")
        return

    tf_map = {
        'M1': mt5.TIMEFRAME_M1,
        'M2': mt5.TIMEFRAME_M2,
        'M5': mt5.TIMEFRAME_M5,
'M15': mt5.TIMEFRAME_M15,
        'H1': mt5.TIMEFRAME_H1,
        'D1': mt5.TIMEFRAME_D1
    }

    if timeframe not in tf_map:
        logger.error("Timeframe inválido.")
        return

    rates = mt5.copy_rates_from_pos(symbol, tf_map[timeframe], 0, bars + period)
    mt5.shutdown()

    if rates is None or len(rates) == 0:
        logger.error("Erro ao obter dados.")
        return

    df = pd.DataFrame(rates)
    df['close'] = df['close'].astype(float)
    df['delta'] = df['close'].diff()
    gain = df['delta'].where(df['delta'] > 0, 0.0)
    loss = -df['delta'].where(df['delta'] < 0, 0.0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))
    df['RSI'] = df['RSI'].round(0)

    df_result = df[['RSI', 'close', 'time']].dropna()
    df_result['time'] = pd.to_datetime(df_result['time'], unit='s')
    click.echo(df_result.tail(5).to_string(index=False))

    conn = sqlite3.connect(db)
    df_result.to_sql('rsi', conn, if_exists='append', index=False)
    conn.close()

    logger.info(f'Dados RSI salvos em {db} (tabela rsi) - símbolo: {symbol}, timeframe: {timeframe}, período: {period}')

if __name__ == '__main__':
    rsi()
