import time
from celery import Task


def echo(task: Task, input_data: str):
    """ Create embedding for input data """
    for i in range(10):
        time.sleep(1)

        progress = (i+1) * 10

        task.update_state(state='PROGRESS',
                          meta={'progress': progress})

    return f"ECHO: {input_data}"
