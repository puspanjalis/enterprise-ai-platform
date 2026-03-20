from datetime import datetime

def pipeline_health(status: str, records_processed: int) -> dict:
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "status": status,
        "records_processed": records_processed
    }

if __name__ == "__main__":
    print(pipeline_health("healthy", 120000))
