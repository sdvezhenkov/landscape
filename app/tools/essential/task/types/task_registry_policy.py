from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class TaskRegistryLimits:
    active: int = 10
    storage: int = 30

    def __post_init__(
        self,
    ) -> None:
        if self.active > self.storage:
            raise ValueError('Active task limit must not exceed storage limit')

@dataclass(frozen=True, slots=True)
class TaskRegistryPolicy:
    limit: TaskRegistryLimits = field(default_factory=TaskRegistryLimits)
