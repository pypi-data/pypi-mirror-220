import time
from datetime import datetime as Datetime
from datetime import timezone
from zoneinfo import ZoneInfo

import typer
from beni import bcolor, bfunc, btask
from beni.btype import Null
from colorama import Fore


@btask.app.command('time')
@bfunc.syncCall
async def showtime(
    value1: str = typer.Argument('', help='时间戳（整形或浮点型）或日期（格式: 2021-11-23）', show_default=False, metavar='[Timestamp or Date]'),
    value2: str = typer.Argument('', help='时间（格式: 09:20:20），只有第一个参数为日期才有意义', show_default=False, metavar='[Time]')
):
    '''
    格式化时间戳\n
    beni time\n
    beni time 1632412740\n
    beni time 1632412740.1234\n
    beni time 2021-9-23\n
    beni time 2021-9-23 09:47:00\n
    '''
    timestamp: float = Null
    if not value1:
        timestamp = time.time()
    else:
        try:
            timestamp = float(value1)
        except:
            try:
                if value2:
                    timestamp = Datetime.strptime(f'{value1} {value2}', '%Y-%m-%d %H:%M:%S').timestamp()
                else:
                    timestamp = Datetime.strptime(f'{value1}', '%Y-%m-%d').timestamp()
            except:
                pass
    if timestamp is None:
        color = typer.colors.BRIGHT_RED
        typer.secho('参数无效', fg=color)
        typer.secho('\n可使用格式: ', fg=color)
        msg_ary = str(showtime.__doc__).strip().replace('\n\n', '\n').split('\n')[1:]
        msg_ary = [x.strip() for x in msg_ary]
        typer.secho('\n'.join(msg_ary), fg=color)
        raise typer.Abort()
    print()
    print(timestamp)
    print()
    localtime = time.localtime(timestamp)
    tzname = time.tzname[(time.daylight and localtime.tm_isdst) and 1 or 0]
    bcolor.printx(time.strftime('%Y-%m-%d %H:%M:%S %z', localtime), tzname, colorList=[Fore.YELLOW])
    print()
    datetime_utc = Datetime.fromtimestamp(timestamp, tz=timezone.utc)
    tzname_list = [
        'Australia/Sydney',
        'Asia/Tokyo',
        'Asia/Kolkata',
        'Africa/Cairo',
        'Europe/London',
        'America/Sao_Paulo',
        'America/New_York',
        'America/Chicago',
        'America/Los_Angeles',
    ]
    for tzname in tzname_list:
        datetime_tz = datetime_utc.astimezone(ZoneInfo(tzname))
        dstStr = ''
        dst = datetime_tz.dst()
        if dst:
            dstStr = f'(DST+{dst})'
        print(f'{datetime_tz} {tzname} {dstStr}')
    print()
