from enum import StrEnum
from beni import bpath, bfile

import typer
from beni import bcolor, bfunc, btask


class _MirrorsType(StrEnum):
    pip = 'pip'
    npm = 'npm'


_mirrorsFiles = {
    _MirrorsType.pip: {
        bpath.getUser('pip/pip.ini'): [
            '[global]',
            'index-url = https://mirrors.aliyun.com/pypi/simple',
        ],
    },
    _MirrorsType.npm: {
        bpath.getUser('.bashrc'): [
            'registry=https://registry.npm.taobao.org/',
            'electron_mirror=https://npm.taobao.org/mirrors/electron/',
        ],
    },
}


@btask.app.command()
@bfunc.syncCall
async def mirrors(
    types: list[_MirrorsType] = typer.Argument(None, help="镜像的类型"),
    disabled: bool = typer.Option(False, help="是否禁用"),
):
    '设置镜像'
    if not types:
        types = [_MirrorsType.pip, _MirrorsType.npm]
    for targetType in types:
        data = _mirrorsFiles[targetType]
        for file, msgAry in data.items():
            if disabled:
                await bpath.remove(file)
                bcolor.printRed('删除文件', file)
            else:
                print()
                bcolor.printYellow(file)
                msg = '\n'.join(msgAry)
                await bfile.writeText(file, msg)
                bcolor.printMagenta(msg)
    print()
