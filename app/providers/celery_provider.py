from typing import TypedDict, Literal, Generic, TypeVar, Any, Callable
import time
import asyncio
from celery.result import AsyncResult
from app.configs.celery_config import celery_client

_T = TypeVar('T', bound=Any)


class TaskResult(TypedDict, Generic[_T]):
    '''
    Task result
    '''
    status: Literal['PENDING', 'SUCCESS', 'FAILURE', 'RETRY', 'REVOKED']
    result: _T


class CeleryProvider(Generic[_T]):
    '''
    Celery provider for executing asynchronous tasks
    '''

    def __init__(self): ...

    def execute(self, task_name: str, *args, **kwargs) -> str:
        '''
        Send the task to the celery worker and return the task id
        '''
        task = celery_client.send_task(task_name, args=args, kwargs=kwargs)
        return task.id

    def get_result(self, task_id: str, wait_until_complete: bool = False) -> TaskResult[_T]:
        '''
        Get the status of the task
        '''
        task = AsyncResult(task_id, app=celery_client)
        if wait_until_complete:
            return TaskResult[_T](
                status='SUCCESS',
                result=task.get()
            )

        return TaskResult[_T](
            status=task.status,
            result=task.result
        )

    async def async_on_progress(self, task_id: str, on_progress: Callable[[], TaskResult], interval: float = 1.0) -> None:
        '''
        Listen for task progress
        '''
        task = AsyncResult(task_id, app=celery_client)
        previous_result = None

        while True:
            await asyncio.sleep(interval)

            if task.state != 'SUCCESS':
                result = task.result
                if result != previous_result:
                    on_progress(TaskResult(
                        status=task.state,
                        result=result
                    ))
                    previous_result = result

            else:
                return TaskResult(
                    status='SUCCESS',
                    result=task.result
                )

    def on_progress(self, task_id: str, on_progress: Callable[[TaskResult], Any], interval: float = 1.0) -> None:
        '''
        Listen for task progress
        '''
        task = AsyncResult(task_id, app=celery_client)
        previous_result = None

        while True:
            time.sleep(interval)

            if task.state != 'SUCCESS':
                result = task.result
                if result != previous_result:
                    on_progress(TaskResult(
                        status=task.state,
                        result=result
                    ))
                    previous_result = result

            else:
                return on_progress(TaskResult(
                    status='SUCCESS',
                    result=task.result
                ))
