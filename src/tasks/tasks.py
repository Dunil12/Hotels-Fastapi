from time import sleep

from first_project.src.tasks.celery_app import celery_instance
# from .celery_app import celery_instance

@celery_instance.task
def test_task():
    sleep(5)
    print("Я молодец")

@celery_instance.task
def resize_image():
    """

    :return:
    """