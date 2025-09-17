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
