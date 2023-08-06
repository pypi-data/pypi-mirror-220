import asyncio
import sys
from contextlib import asynccontextmanager
from dataclasses import dataclass
from datetime import datetime as Datetime
from pathlib import Path
from typing import Any, Final

import nest_asyncio
from colorama import Fore
from typer import Typer

from beni import bcolor, bfunc, block, blog, bpath, btime
from beni.btype import Null

app = Typer()

nest_asyncio.apply()


@dataclass
class _Options:
    tasksPath: Path = Null
    lock: str = 'btask'
    package: str = 'tasks'
    logPath: Path = Null
    binPath: Path = Null
    logFilesLimit: int = 100


options: Final = _Options()
isShowSummary: bool = False


def main():
    assert options.tasksPath, '请先设置 options.mainFile'

    async def func():
        async with _task():
            try:
                files = options.tasksPath.glob('*.py')
                files = filter(lambda x: not x.name.startswith('_'), files)
                for moduleName in [x.stem for x in files]:
                    exec(f'import {options.package}.{moduleName}')
                    module = eval(f'{options.package}.{moduleName}')
                    if hasattr(module, 'app'):
                        sub: Typer = getattr(module, 'app')
                        if sub is not app:
                            sub.info.name = moduleName.replace('_', '-')
                            app.add_typer(sub, name=sub.info.name)
                app()
            except BaseException as ex:
                if type(ex) is SystemExit and ex.code in (0, 2):
                    # 0 - 正常结束
                    # 2 - Error: Missing command.
                    pass
                else:
                    raise
    asyncio.run(func())


def dev(name: str, *args: Any, **kwargs: Any):
    '例：db.reverse'
    async def func():
        async with _task():
            module, cmd = name.split('.')
            exec(f'from {options.package} import {module}')
            eval(f'{module}.{cmd}')(*args, **kwargs)
    asyncio.run(func())


@asynccontextmanager
async def _task():
    _checkVscodeVenv()
    bfunc.sysUtf8()
    if options.binPath:
        bfunc.addEnvPath(options.binPath)
    async with block.useFileLock(options.lock):
        start_time = Datetime.now()
        bfunc.initErrorFormat()
        if options.logPath:
            logFile = bpath.get(options.logPath, btime.datetimeStr('%Y%m%d_%H%M%S.log'))
            assert logFile.is_file(), f'日志文件创建失败（已存在） {logFile}'
        else:
            logFile = None
        try:
            blog.init(logFile=logFile)
            yield
        except BaseException as ex:
            bcolor.set(Fore.LIGHTRED_EX)
            blog.error(str(ex))
            blog.error('执行失败')
            raise
        finally:
            if isShowSummary:
                criticalNum = blog.getCountCritical()
                errorNum = blog.getCountError()
                warningNum = blog.getCountWarning()
                if criticalNum:
                    color = Fore.LIGHTMAGENTA_EX
                elif errorNum:
                    color = Fore.LIGHTRED_EX
                elif warningNum:
                    color = Fore.YELLOW
                else:
                    color = Fore.LIGHTGREEN_EX
                msgAry = ['', '-' * 75]
                if criticalNum:
                    msgAry.append(f'critical：{criticalNum}')
                if errorNum:
                    msgAry.append(f'error：{errorNum}')
                if warningNum:
                    msgAry.append(f'warning：{warningNum}')
                duration = str(Datetime.now() - start_time)
                if duration.startswith('0:'):
                    duration = '0' + duration
                msgAry.append(f'任务结束（{duration}）')
                bcolor.set(color)
                blog.info('\n'.join(msgAry))

            # 删除多余的日志
            try:
                if logFile:
                    logFileAry = list(logFile.parent.glob('*.log'))
                    logFileAry.remove(logFile)
                    logFileAry.sort()
                    logFileAry = logFileAry[options.logFilesLimit:]
                    await bpath.remove(*logFileAry)
            except:
                pass


def _checkVscodeVenv():
    par = '--vscode-venv'
    if par in sys.argv:
        sys.argv.remove(par)
        sys.orig_argv.remove(par)
        input('回车后继续（为了兼容vscode venv问题）...')
