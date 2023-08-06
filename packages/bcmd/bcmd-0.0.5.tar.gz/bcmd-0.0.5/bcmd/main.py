from beni import btask, bpath


def init():
    btask.options.tasksPath = bpath.get(__file__, '../tasks')
    btask.options.package = 'bcmd.tasks'
    btask.options.lock = 'bcmd'


def run():
    init()
    btask.main()


if __name__ == '__main__':
    run()
