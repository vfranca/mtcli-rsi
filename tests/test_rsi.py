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


@pytest.mark.skip("testes com erros a verificar")
@pytest.mark.parametrize(
    "closes, expected_range",
    [
        ([100] * 20, (45, 55)),  # Preço constante → RSI ~50
        ([i for i in range(100, 120)], (90, 100)),  # Alta contínua → RSI ~100
        ([i for i in range(120, 100, -1)], (0, 10)),  # Queda contínua → RSI ~0
    ],
)
def test_rsi_parametrizado(closes, expected_range):
    rates = [{"time": 1630000000 + i * 60, "close": c} for i, c in enumerate(closes)]
    periodo = 14
    df_result = calcular_rsi_completo(rates, periodo)
    rsi = df_result["RSI"].iloc[-1]
    assert expected_range[0] <= rsi <= expected_range[1]


def test_rsi_dados_insuficientes():
    rates = [
        {"time": 1630000000 + i * 60, "close": 100} for i in range(5)
    ]  # menos que o período 14
    periodo = 14
    df_result = calcular_rsi_completo(rates, periodo)
    # Com menos dados, o resultado deve ser vazio (dropna)
    assert df_result.empty


@pytest.mark.skip("teste com erros a verificar")
def test_rsi_com_nan():
    rates = [
        {"time": 1630000000 + i * 60, "close": (100 if i != 5 else None)}
        for i in range(20)
    ]
    periodo = 14
    df_result = calcular_rsi_completo(rates, periodo)
    # O RSI deve ser calculado ignorando o NaN, resultado não vazio
    assert not df_result.empty
    assert "RSI" in df_result.columns
    assert df_result["RSI"].notna().all()


def test_rsi_valores_aleatorios():
    import random

    random.seed(42)
    closes = [random.uniform(90, 110) for _ in range(30)]
    rates = [{"time": 1630000000 + i * 60, "close": c} for i, c in enumerate(closes)]
    periodo = 14
    df_result = calcular_rsi_completo(rates, periodo)
    assert not df_result.empty
    assert df_result["RSI"].between(0, 100).all()
