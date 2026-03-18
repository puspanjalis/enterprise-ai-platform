from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split


def _make_synthetic_data(n_rows: int = 5000, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    countries = np.array(["US", "DE", "IN", "AU", "SG", "UK"])
    products = np.array(["Core", "Analytics", "Forecasting", "Support AI"])

    df = pd.DataFrame(
        {
            "customer_id": np.arange(100000, 100000 + n_rows),
            "country": rng.choice(countries, size=n_rows, p=[0.28, 0.12, 0.22, 0.08, 0.1, 0.2]),
            "product_family": rng.choice(products, size=n_rows),
            "tenure_months": rng.integers(1, 72, size=n_rows),
            "monthly_spend_usd": rng.normal(4200, 1100, size=n_rows).clip(350, 12000).round(2),
            "active_users": rng.integers(5, 500, size=n_rows),
            "weekly_sessions": rng.integers(3, 1200, size=n_rows),
            "support_tickets_90d": rng.poisson(2.2, size=n_rows),
            "feature_adoption_score": rng.normal(68, 14, size=n_rows).clip(5, 100).round(1),
        }
    )

    risk_signal = (
        0.020 * df["support_tickets_90d"]
        - 0.015 * df["tenure_months"]
        - 0.012 * (df["feature_adoption_score"] - 60)
        + 0.00008 * (3500 - df["monthly_spend_usd"])
        + rng.normal(0, 0.65, size=n_rows)
    )

    df["is_at_risk"] = (risk_signal > 0.15).astype(int)
    return df


def load_or_create_data(csv_path: Path, n_rows: int = 5000, seed: int = 42) -> pd.DataFrame:
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    if not csv_path.exists():
        _make_synthetic_data(n_rows=n_rows, seed=seed).to_csv(csv_path, index=False)
    return pd.read_csv(csv_path)


def prepare_features(df: pd.DataFrame):
    features = df.drop(columns=["customer_id", "is_at_risk"])
    target = df["is_at_risk"]
    encoded = pd.get_dummies(features, columns=["country", "product_family"], drop_first=False)
    X_train, X_test, y_train, y_test = train_test_split(
        encoded, target, test_size=0.2, random_state=42, stratify=target
    )
    return X_train, X_test, y_train, y_test, encoded.columns.tolist()
