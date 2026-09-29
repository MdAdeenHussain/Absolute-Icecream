import os

from celery import Celery


def create_celery():
    """Create the Celery application."""

    redis_url = os.getenv(
        "CELERY_BROKER_URL",
        "redis://localhost:6379/1",
    )

    celery = Celery(
        "absolute_icecream",
        broker=redis_url,
        backend=os.getenv(
            "CELERY_RESULT_BACKEND",
            redis_url,
        ),
    )

    return celery


celery = create_celery()