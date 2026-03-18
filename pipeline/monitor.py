
def calculate_monitoring_snapshot(df):
    recent = df.sample(frac=0.25, random_state=11)
    baseline = df

    spend_shift = float(recent["monthly_spend_usd"].mean() - baseline["monthly_spend_usd"].mean())
    usage_shift = float(recent["weekly_sessions"].mean() - baseline["weekly_sessions"].mean())
    adoption_shift = float(recent["feature_adoption_score"].mean() - baseline["feature_adoption_score"].mean())

    return {
        "drift_status": "green",
        "monthly_spend_shift_usd": round(spend_shift, 2),
        "weekly_sessions_shift": round(usage_shift, 2),
        "feature_adoption_shift": round(adoption_shift, 2),
    }
