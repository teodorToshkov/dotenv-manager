from types import NoneType


class Singleton(type):
    _instances: NoneType = None

    def __call__(cls, *args, **kwargs):
        if not cls._instances:
            cls._initialize()
        instance = cls._instances.get(cls)
        if not instance:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return instance

    def _initialize(cls):
        cls._instances = {}
