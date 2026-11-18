import os


def get_env(
        key: str,
        default: str | None = None,
) -> str:
    env = os.getenv(key, default)
    if env is None:
        raise KeyError(f'Environment variable {key} does not exist')
    return env
