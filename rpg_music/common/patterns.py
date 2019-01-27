class Singleton:
    __single = None

    @classmethod
    def reset_singleton(cls):
        cls.__single = None

    def _init(self, *args, **kwargs):
        pass

    def __init__(self, *args, **kwargs):
        cls = self.__class__
        if not cls.__single:
            self._init(*args, **kwargs)
            cls.__single = self

    def __new__(cls, *args, **kwargs):
        if cls.__single:
            return cls.__single
        return super().__new__(cls, *args, **kwargs)
