import asyncio
import datetime

import aioschedule

from utils.view_task import _view_tasks
from services.tasks import get_task_by_date
from loader import bot


async def scheduler():
    aioschedule.every(58).seconds.do(notify)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def notify():
    local_time = str(datetime.datetime.now())[:-9] + "00"
    tasks = get_task_by_date(local_time)
    await _view_tasks(tasks, 'notify', None,  bot)
