from app.workers.celery_app import celery_app


@celery_app.task
def screening_task(application_id: str) -> str:
    return f"Screening task placeholder for {application_id}"
