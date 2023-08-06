import asyncio
import inspect
import sys
from contextlib import asynccontextmanager
from datetime import datetime as Datetime
from pathlib import Path

import nest_asyncio
from colorama import Fore
from typer import Typer

from beni import bcolor, bfunc, block, blog, bpath, btime
from beni.btype import Null

app = Typer()
_LOGFILE_COUNT = 100
_TASKS = 'tasks'

nest_asyncio.apply()

_key: str = 'btask'
_logDir: Path = Null
_binDir: Path = Null


@bfunc.onceCall
def init(
    *,
    key: str = '',
    logDir: Path | str = '',
    binDir: Path | str = ''
):
    global _key, _logDir, _binDir
    if key:
        _key = key
    if logDir:
        _logDir = bpath.get(logDir)
    if binDir:
        _binDir = bpath.get(binDir)


def main():
    async def func():
        async with _task():
            try:
                tasksDir = _getRootDir() / _TASKS
                files = tasksDir.glob('*.py')
                files = filter(lambda x: not x.name.startswith('_'), files)
                for moduleName in [x.stem for x in files]:
                    exec(f'import {_TASKS}.{moduleName}')
                    module = eval(f'{_TASKS}.{moduleName}')
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


def dev(name: str):
    '例：db.reverse'
    async def func():
        async with _task():
            module, cmd = name.split('.')
            exec(f'from {_TASKS} import {module}')
            exec(f'{module}.{cmd}()')
    asyncio.run(func())


@asynccontextmanager
async def _task():
    _checkVscodeVenv()
    bfunc.sysUtf8()
    if _binDir:
        bfunc.addEnvPath(_binDir)
    async with block.useFileLock(_key):
        start_time = Datetime.now()
        bfunc.initErrorFormat()
        if _logDir:
            logFile = bpath.get(_logDir, btime.datetimeStr('%Y%m%d_%H%M%S.log'))
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
            bcolor.set(color)
            blog.info('-' * 75)
            msgAry = ['任务结束']
            if criticalNum:
                msgAry.append(f'critical({criticalNum})')
            if errorNum:
                msgAry.append(f'error({errorNum})')
            if warningNum:
                msgAry.append(f'warning({warningNum})')
            duration = str(Datetime.now() - start_time)
            if duration.startswith('0:'):
                duration = '0' + duration
            msgAry.append(f'\n用时: {duration}')
            bcolor.set(color)
            blog.info(' '.join(msgAry))

            # 删除多余的日志
            try:
                if logFile:
                    logFileAry = list(logFile.parent.glob('*.log'))
                    logFileAry.remove(logFile)
                    logFileAry.sort()
                    logFileAry = logFileAry[_LOGFILE_COUNT:]
                    await bpath.remove(*logFileAry)
            except:
                pass


def _getRootDir():
    frametype = inspect.currentframe()
    target = frametype
    while True:
        assert target and target.f_back
        target = target.f_back
        if target.f_locals.get('__name__') == '__main__':
            file = target.f_locals.get('__file__')
            if type(file) is str:
                return bpath.get(file).parent


def _checkVscodeVenv():
    par = '--vscode-venv'
    if par in sys.argv:
        sys.argv.remove(par)
        sys.orig_argv.remove(par)
        input('回车后继续（为了兼容vscode venv问题）...')
