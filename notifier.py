import asyncio
import datetime

import aioschedule

from models import User
from services.tasks import get_task_by_date
from win10toast import ToastNotifier


async def schedular(user_id: int):
    aioschedule.every(1).minutes.do(notify(user_id))
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def notify(user_id: int):
    toaster = ToastNotifier()
    while True:
        tasks = get_task_by_date(user_id, str(datetime.datetime.now().time())[:-7])
        for task in tasks:
            message = f"{task.name} is due now!"
            toaster.show_toast(title="Task Due", msg=message, duration=5)
        await asyncio.sleep(60)
