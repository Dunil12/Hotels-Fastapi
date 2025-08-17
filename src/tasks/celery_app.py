from celery import Celery
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
sys.path.append(str(Path(__file__).parent.parent.parent))
sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent))

print(sys.path) # не работает

from src.config import settings

celery_instance = Celery(
    main="tasks",
    broker=settings.REDIS_URL,
    include=["src.tasks.tasks", "src.tasks.emails.emails"],
)