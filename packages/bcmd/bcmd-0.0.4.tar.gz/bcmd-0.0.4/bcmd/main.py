import inspect
from beni import btask, bpath


def init():
    btask.init(
        key='bcmd',
    )


def run():
    # btask.main()
    print(_getRootDir())


if __name__ == '__main__':
    run()


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
