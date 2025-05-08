import pytest
import pandas as pd

from src.loan_risk_scoring_benchmark import (
    calculate_risk_score,
    process_chunk,
    risk_scoring_single_threaded,
    risk_scoring_multi_threaded
)

def test_calculate_risk_score_high():
    score = calculate_risk_score(10000, 1000, 2, 0)  # High income-to-loan, some dependents
    assert 0 <= score <= 1
    assert score > 0.5  # should be relatively high

def test_calculate_risk_score_low():
    score = calculate_risk_score(1000, 10000, 0, 1)  # Bad income-to-loan, bad credit
    assert 0 <= score <= 1
    assert score < 0.5

def test_process_chunk_counts_high_risk():
    df = pd.DataFrame([
        {"AMT_INCOME_TOTAL": 10000, "AMT_CREDIT": 1000, "CNT_CHILDREN": 2, "TARGET": 0},
        {"AMT_INCOME_TOTAL": 1000, "AMT_CREDIT": 10000, "CNT_CHILDREN": 0, "TARGET": 1}
    ])
    result = process_chunk(df)
    assert result in (0, 1, 2)  # depending on risk score threshold
    assert isinstance(result, int)

def mock_load_chunks(*args, **kwargs):
    # Simulates two chunks of data
    yield pd.DataFrame([{"AMT_INCOME_TOTAL": 10000, "AMT_CREDIT": 1000, "CNT_CHILDREN": 2, "TARGET": 0}])
    yield pd.DataFrame([{"AMT_INCOME_TOTAL": 20000, "AMT_CREDIT": 500, "CNT_CHILDREN": 1, "TARGET": 0}])

def test_single_vs_multi_threaded(monkeypatch):
    # Patch the chunk loader to use fake data
    from src import loan_risk_scoring_benchmark as mod
    monkeypatch.setattr(mod, "load_parquet_in_chunks", mock_load_chunks)

    single_result = mod.risk_scoring_single_threaded("dummy_path")
    multi_result = mod.risk_scoring_multi_threaded("dummy_path", num_threads=2)

    assert single_result == multi_result
    assert isinstance(single_result, int)
