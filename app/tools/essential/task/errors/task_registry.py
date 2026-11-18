class TaskRegistryError(Exception):
    pass


class TaskNotFoundError(TaskRegistryError):
    pass


class IsBusyError(TaskRegistryError):
    pass
