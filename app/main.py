"""MLOps Assignment 7 - Core Utility Application.

This module provides reusable utilities for basic machine learning operations,
data normalization, and model evaluation metrics.
"""

from typing import Any, Dict, List, Tuple
import math


def min_max_scale(values: List[float]) -> List[float]:
    """Normalize a list of numbers into the [0, 1] range using Min-Max scaling.

    Args:
        values (List[float]): A list of numerical values.

    Returns:
        List[float]: Normalized values scaled between 0 and 1.

    Raises:
        ValueError: If the input list is empty.
    """
    if not values:
        raise ValueError("Cannot scale an empty list.")

    min_val = min(values)
    max_val = max(values)

    if min_val == max_val:
        return [0.0 for _ in values]

    return [(val - min_val) / (max_val - min_val) for val in values]


def calculate_accuracy(y_true: List[int], y_pred: List[int]) -> float:
    """Calculate the accuracy score for classification predictions.

    Args:
        y_true (List[int]): Ground truth binary or multiclass labels.
        y_pred (List[int]): Predicted labels.

    Returns:
        float: Accuracy score as a float between 0.0 and 1.0.

    Raises:
        ValueError: If input lists are empty or have differing lengths.
    """
    if not y_true or not y_pred:
        raise ValueError("Input lists cannot be empty.")
    if len(y_true) != len(y_pred):
        raise ValueError("Length of y_true and y_pred must match.")

    correct = sum(1 for true, pred in zip(y_true, y_pred) if true == pred)
    return correct / len(y_true)


def calculate_metrics(y_true: List[int], y_pred: List[int]) -> Dict[str, float]:
    """Calculate precision, recall, and F1-score for binary classification.

    Assumes positive label is 1 and negative label is 0.

    Args:
        y_true (List[int]): Ground truth binary labels (0 or 1).
        y_pred (List[int]): Predicted binary labels (0 or 1).

    Returns:
        Dict[str, float]: Dictionary containing precision, recall, and f1_score.

    Raises:
        ValueError: If lists are empty or lengths do not match.
    """
    if not y_true or not y_pred:
        raise ValueError("Input lists cannot be empty.")
    if len(y_true) != len(y_pred):
        raise ValueError("Length of y_true and y_pred must match.")

    true_positives = sum(1 for t, p in zip(y_true, y_pred) if t == 1 and p == 1)
    false_positives = sum(1 for t, p in zip(y_true, y_pred) if t == 0 and p == 1)
    false_negatives = sum(1 for t, p in zip(y_true, y_pred) if t == 1 and p == 0)

    precision = (
        true_positives / (true_positives + false_positives)
        if (true_positives + false_positives) > 0
        else 0.0
    )
    recall = (
        true_positives / (true_positives + false_negatives)
        if (true_positives + false_negatives) > 0
        else 0.0
    )
    f1_score = (
        2 * (precision * recall) / (precision + recall)
        if (precision + recall) > 0
        else 0.0
    )

    return {
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1_score": round(f1_score, 4),
    }


def mean_squared_error(y_true: List[float], y_pred: List[float]) -> float:
    """Compute the Mean Squared Error (MSE) between actual and predicted values.

    Args:
        y_true (List[float]): Actual continuous target values.
        y_pred (List[float]): Predicted continuous target values.

    Returns:
        float: The calculated mean squared error.

    Raises:
        ValueError: If inputs are empty or lengths do not match.
    """
    if not y_true or not y_pred:
        raise ValueError("Input lists cannot be empty.")
    if len(y_true) != len(y_pred):
        raise ValueError("Length of y_true and y_pred must match.")

    squared_errors = [(yt - yp) ** 2 for yt, yp in zip(y_true, y_pred)]
    return sum(squared_errors) / len(squared_errors)


def train_test_split(
    data: List[Any], test_ratio: float = 0.2
) -> Tuple[List[Any], List[Any]]:
    """Deterministically split a dataset into train and test partitions.

    Args:
        data (List[Any]): Dataset elements.
        test_ratio (float): Proportion of the dataset in the test split.

    Returns:
        Tuple[List[Any], List[Any]]: (train_data, test_data)

    Raises:
        ValueError: If test_ratio is not between 0 and 1, or dataset is empty.
    """
    if not data:
        raise ValueError("Cannot split an empty dataset.")
    if not (0.0 < test_ratio < 1.0):
        raise ValueError("test_ratio must be strictly between 0 and 1.")

    split_index = math.floor(len(data) * (1.0 - test_ratio))
    return data[:split_index], data[split_index:]


def run_pipeline() -> Dict[str, Any]:
    """Execute a sample pipeline demonstrating MLOps utility functions.

    Returns:
        Dict[str, Any]: Summary results of the sample pipeline.
    """
    features = [12.0, 24.0, 36.0, 48.0, 60.0]
    scaled = min_max_scale(features)

    y_true = [1, 0, 1, 1, 0, 1, 0, 0]
    y_pred = [1, 0, 1, 0, 0, 1, 1, 0]

    acc = calculate_accuracy(y_true, y_pred)
    metrics = calculate_metrics(y_true, y_pred)
    mse = mean_squared_error([1.0, 2.0, 3.0], [1.1, 1.9, 3.2])

    return {
        "scaled_features": scaled,
        "accuracy": acc,
        "metrics": metrics,
        "mse": round(mse, 4),
    }


if __name__ == "__main__":
    print("========================================")
    print("  MLOps CI/CD Demo Application Started  ")
    print("========================================")
    results = run_pipeline()
    for key, val in results.items():
        print(f"{key}: {val}")
    print("========================================")
    print("Application executed successfully.")
