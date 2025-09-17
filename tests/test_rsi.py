import pytest
import pandas as pd
from mtcli_rsi.rsi import (
    preparar_dataframe,
    calcular_rsi,
    formatar_resultado,
    calcular_rsi_completo,
)


@pytest.fixture
def dados_simulados():
    return [{"time": 1630000000 + i * 60, "close": 100 + i} for i in range(20)]


def test_preparar_dataframe(dados_simulados):
    df = preparar_dataframe(dados_simulados)
    assert isinstance(df, pd.DataFrame)
    assert "close" in df.columns
    assert df["close"].dtype == float


def test_calcular_rsi(dados_simulados):
    df = preparar_dataframe(dados_simulados)
    df = calcular_rsi(df, 14)
    assert "RSI" in df.columns
    assert not df["RSI"].isnull().all()


def test_formatar_resultado(dados_simulados):
    df = preparar_dataframe(dados_simulados)
    df = calcular_rsi(df, 14)
    df_result = formatar_resultado(df)
    assert {"RSI", "close", "time"} <= set(df_result.columns)
    assert pd.api.types.is_datetime64_any_dtype(df_result["time"])


def test_calcular_rsi_completo(dados_simulados):
    df_result = calcular_rsi_completo(dados_simulados, 14)
    assert len(df_result) > 0
    assert df_result["RSI"].between(0, 100).all()


def test_rsi_sem_variacao():
    dados = [{"time": 1630000000 + i * 60, "close": 100.0} for i in range(20)]
    df_result = calcular_rsi_completo(dados, 14)
    assert (df_result["RSI"] == 0).all() or df_result["RSI"].isnull().all()


def test_rsi_oscila_em_torno_de_50():
    closes = [100 + (-1) ** i * i for i in range(20)]  # Ex: 100, 99, 102, 99, 104...
    dados = [{"time": 1630000000 + i * 60, "close": c} for i, c in enumerate(closes)]
    df_result = calcular_rsi_completo(dados, 14)
    assert df_result["RSI"].between(30, 70).any()


def test_rsi_proximo_de_100():
    closes = [100 + i for i in range(20)]  # Sempre subindo
    dados = [{"time": 1630000000 + i * 60, "close": c} for i, c in enumerate(closes)]
    df_result = calcular_rsi_completo(dados, 14)
    assert df_result["RSI"].iloc[-1] >= 90  # Forte alta


def test_rsi_proximo_de_0():
    closes = [100 - i for i in range(20)]  # Sempre caindo
    dados = [{"time": 1630000000 + i * 60, "close": c} for i, c in enumerate(closes)]
    df_result = calcular_rsi_completo(dados, 14)
    assert df_result["RSI"].iloc[-1] <= 10  # Forte baixa
