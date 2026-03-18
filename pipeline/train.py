from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score


def train_model(X_train, X_test, y_train, y_test):
    model = RandomForestClassifier(
        n_estimators=120,
        max_depth=8,
        random_state=42,
        min_samples_leaf=4,
    )
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    proba = model.predict_proba(X_test)[:, 1]
    metrics = {
        "accuracy": accuracy_score(y_test, preds),
        "precision": precision_score(y_test, preds, zero_division=0),
        "recall": recall_score(y_test, preds, zero_division=0),
        "roc_auc": roc_auc_score(y_test, proba),
    }
    return model, metrics
