import asyncio
from asyncio import Queue
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any
from uuid import uuid4

from app.tools.essential.logger.logger import logger
from app.tools.essential.task.types.event import Event
from app.tools.essential.task.types.task_id import TaskID
from app.tools.essential.task.types.task_state import TASK_COMPLETION_STAGES, TaskStages, TaskState


class TaskBase[TS: TaskState, R: Any]:
    def __init__(self):
        self.id = self._create_id()
        self.state: TS = self._create_state()
        self.subscribers = set[Queue[Event[TS]]]()
        self.state.bind(on_change=self.publish)

    def _create_id(self) -> TaskID:
        task_id: TaskID = uuid4()
        return task_id

    def _create_state(self) -> TS:
        raise NotImplementedError

    async def publish(self) -> None:
        event = await self._get_event()
        for queue in list(self.subscribers):
            await queue.put(event)

    @asynccontextmanager
    async def subscribe(self) -> AsyncIterator[AsyncIterator[Event[TS]]]:
        event = await self._get_event()
        queue = Queue[Event[TS]]()
        queue.put_nowait(event)
        self.subscribers.add(queue)

        async def events() -> AsyncIterator[Event[TS]]:
            while True:
                event = await queue.get()
                yield event
                if event.state.status.stage in TASK_COMPLETION_STAGES:
                    break

        try:
            yield events()
        finally:
            self.subscribers.discard(queue)

    async def _get_event(self) -> Event[TS]:
        event = Event[TS](
            task_id=self.id,
            state=self.state.model_copy(deep=True),
        )
        return event

    def run_in_background(self) -> None:
        task = asyncio.create_task(self.run())
        task.add_done_callback(self._consume_exception)

    def _consume_exception(
        self,
        task: asyncio.Task,
    ) -> None:
        if task.cancelled():
            return
        task.exception()

    async def run(self) -> R:
        try:
            self.state.status.stage = TaskStages.STARTED
            result: R = await self._run(self.state)
            self.state.result = result
            self.state.status.stage = TaskStages.SUCCESS
            return result
        except Exception:
            self.state.status.stage = TaskStages.FAILURE
            logger.exception(type(self).__name__)
            raise

    async def _run(
            self,
            state: TS,
    ) -> R:
        raise NotImplementedError
