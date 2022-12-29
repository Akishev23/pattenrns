from time import time


class Router:

    def __init__(self, routs, url=None):
        self.url = url
        self.routs = routs

    def __call__(self, cls):
        if not self.url:
            self.url = self.get_url_from_class_name(cls.__name__)
        self.routs[self.url] = cls()

    @staticmethod
    def get_url_from_class_name(cls_name):
        return '/' + ''.join('-' + sym.lower() if sym.isupper() and ind else
                             sym.lower() for ind, sym in enumerate(cls_name)) + '/'


class Debug:

    def __init__(self):
        self.method_name = None
        self.class_name = None

    def __call__(self, cls):
        self.name = cls.__name__.strip('_').upper()
        self.class_name = str(cls).split()[1].partition('.')[0].upper()

        def timeit(method):
            def timed(*args, **kwargs):
                time_started = time()
                result = method(*args, **kwargs)
                time_elapsed = time() - time_started

                print(f'DEBUG ----> Method {self.name} of the class {self.class_name} was '
                      f'executed for {time_elapsed: 2.2f} ms')
                return result

            return timed

        return timeit(cls)


if __name__ == '__main__':
    class Hello:
        @Debug()
        def __init__(self):
            self.name = None
