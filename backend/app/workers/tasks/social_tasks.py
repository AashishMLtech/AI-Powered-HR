from app.workers.celery_app import celery_app


@celery_app.task
def social_asset_task(job_id: str) -> str:
    return f"Social asset task placeholder for {job_id}"
