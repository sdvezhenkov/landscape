def inverse[T1, T2](
        dict_: dict[T1, T2],
) -> dict[T2, T1]:
    inversed: dict[T2, T1] = {v: k for k, v in dict_.items()}
    return inversed
