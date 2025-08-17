from time import sleep
import logging

from src.tasks.celery_app import celery_instance

@celery_instance.task
def test_task():
    logging.info(f"Вызывается функция test_task")
    sleep(5)
    print("Я молодец")
    logging.info(f"Результат работы ф-ии")

@celery_instance.task
def resize_image():
    """

    :return:
    """