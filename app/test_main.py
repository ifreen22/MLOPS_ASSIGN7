"""Unit tests for the MLOps Assignment 7 core application."""

import pytest
from app.main import (
    calculate_accuracy,
    calculate_metrics,
    mean_squared_error,
    min_max_scale,
    run_pipeline,
    train_test_split,
)


def test_min_max_scale_valid():
    """Test min_max_scale with standard numerical inputs."""
    data = [10.0, 20.0, 30.0, 40.0, 50.0]
    scaled = min_max_scale(data)
    assert scaled[0] == pytest.approx(0.0)
    assert scaled[-1] == pytest.approx(1.0)
    assert scaled[2] == pytest.approx(0.5)


def test_min_max_scale_identical_values():
    """Test min_max_scale when all values in list are identical."""
    data = [5.0, 5.0, 5.0]
    scaled = min_max_scale(data)
    assert scaled == [0.0, 0.0, 0.0]


def test_min_max_scale_empty_raises_error():
    """Test min_max_scale raises ValueError on empty input."""
    with pytest.raises(ValueError, match="Cannot scale an empty list"):
        min_max_scale([])


def test_calculate_accuracy_perfect():
    """Test calculate_accuracy with 100% match."""
    y_true = [1, 0, 1, 1, 0]
    y_pred = [1, 0, 1, 1, 0]
    assert calculate_accuracy(y_true, y_pred) == 1.0


def test_calculate_accuracy_partial():
    """Test calculate_accuracy with known partial match."""
    y_true = [1, 1, 0, 0]
    y_pred = [1, 0, 0, 1]
    assert calculate_accuracy(y_true, y_pred) == 0.5


def test_calculate_accuracy_mismatched_length():
    """Test calculate_accuracy raises ValueError when lengths differ."""
    with pytest.raises(ValueError, match="Length of y_true and y_pred"):
        calculate_accuracy([1, 0], [1])


def test_calculate_metrics_values():
    """Test calculate_metrics outputs precision, recall, and f1_score."""
    y_true = [1, 1, 0, 0]
    y_pred = [1, 0, 0, 0]
    metrics = calculate_metrics(y_true, y_pred)
    assert metrics["precision"] == 1.0
    assert metrics["recall"] == 0.5
    assert metrics["f1_score"] == pytest.approx(0.6667, abs=1e-3)


def test_calculate_metrics_zero_division_guard():
    """Test calculate_metrics handles cases where no positives are predicted."""
    y_true = [1, 1, 1]
    y_pred = [0, 0, 0]
    metrics = calculate_metrics(y_true, y_pred)
    assert metrics["precision"] == 0.0
    assert metrics["recall"] == 0.0
    assert metrics["f1_score"] == 0.0


def test_mean_squared_error_exact():
    """Test mean_squared_error with exact predictions."""
    y_true = [2.0, 4.0, 6.0]
    y_pred = [2.0, 4.0, 6.0]
    assert mean_squared_error(y_true, y_pred) == 0.0


def test_mean_squared_error_offset():
    """Test mean_squared_error with calculated deviation."""
    y_true = [1.0, 2.0, 3.0]
    y_pred = [2.0, 3.0, 4.0]
    # Errors: (1)^2, (1)^2, (1)^2 -> avg 1.0
    assert mean_squared_error(y_true, y_pred) == pytest.approx(1.0)


def test_mean_squared_error_empty():
    """Test mean_squared_error raises ValueError on empty input."""
    with pytest.raises(ValueError, match="Input lists cannot be empty"):
        mean_squared_error([], [])


def test_train_test_split_proportions():
    """Test train_test_split splits data properly."""
    dataset = list(range(10))
    train, test = train_test_split(dataset, test_ratio=0.3)
    assert len(train) == 7
    assert len(test) == 3
    assert train + test == dataset


def test_train_test_split_invalid_ratio():
    """Test train_test_split raises ValueError on invalid ratio."""
    with pytest.raises(ValueError, match="test_ratio must be strictly between"):
        train_test_split([1, 2, 3], test_ratio=1.5)


def test_run_pipeline():
    """Test run_pipeline returns expected dictionary keys."""
    result = run_pipeline()
    assert "scaled_features" in result
    assert "accuracy" in result
    assert "metrics" in result
    assert "mse" in result
    assert 0.0 <= result["accuracy"] <= 1.0
