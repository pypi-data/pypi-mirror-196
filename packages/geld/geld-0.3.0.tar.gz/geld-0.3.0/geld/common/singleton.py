class SingletonMeta(type):
    """
    This metaclass is used for creating singleton objects.
    The class maintains a dictionary of instances created by the class,
    and ensures that only one instance of the class is ever created.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
