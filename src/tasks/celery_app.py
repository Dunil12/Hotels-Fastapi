from celery import Celery
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from first_project.src.config import settings

celery_instance = Celery(
    main="tasks",
    broker=settings.REDIS_URL,
    include=["first_project.src.tasks.tasks"]
)