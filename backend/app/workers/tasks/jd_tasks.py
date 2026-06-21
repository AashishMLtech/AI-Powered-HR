from app.workers.celery_app import celery_app


@celery_app.task
def jd_rewrite_task(job_id: str) -> str:
    return f"JD task placeholder for {job_id}"
