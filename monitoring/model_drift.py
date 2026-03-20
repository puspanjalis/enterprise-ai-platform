def check_drift(current, baseline):
    return abs(current - baseline) > 0.1
