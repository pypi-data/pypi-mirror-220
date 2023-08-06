from .errors import Errors
from datetime import datetime
import asyncio
import pytz


class Tasks:


    def is_day(date: str, timezone: str=None):
        def decorator(fun):
            def wait():
                running=True
                while (running == True):
                    if timezone == None:
                        now=datetime.now()
                    elif timezone not in pytz.all_timezones:
                       raise Errors.TimeZoneNotFound("Cannnot find this timezone. Please make sure the time is correct!")
                    else:
                        now=datetime.now(pytz.timezone(timezone))
                    if f"{now.date}-{now.month}-{now.year}" == date:
                        running=False
                    else:
                        loop=asyncio.get_event_loop()
                        loop.run_until_complete(asyncio.sleep(1))
                return fun()
            return wait()
        return decorator()
    